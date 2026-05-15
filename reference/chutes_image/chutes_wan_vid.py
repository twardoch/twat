#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["aiohttp", "requests", "pydantic", "fire", "tenacity", "loguru", "python-dotenv", "asyncio", "python-slugify", "pathvalidate", "pillow"]
# ///
# this_file: chutes_wan_vid.py

"""
Chutes AI WAN Video Generation Client

Comprehensive Python client for WAN 2.1 FLF2V (First Last Frame to Video) generation API.
Supports image-to-video generation with mandatory first and last frame inputs.
"""

import os
import json
import base64
import time
import tempfile
import re
from pathlib import Path
from typing import Literal, Any
from io import BytesIO
from enum import Enum

import aiohttp
import requests
import fire
from pydantic import BaseModel, Field, field_validator
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
    after_log,
)
from loguru import logger
from dotenv import load_dotenv
from slugify import slugify
from pathvalidate import sanitize_filename
from PIL import Image

# Load environment variables
load_dotenv()

# Constants
DEFAULT_API_KEY = os.getenv("CHUTES_API_KEY")
WAN_BASE_URL = "https://kikakkz-wan2-1-14b-flf2v.chutes.ai"
WAN_FLF2V_URL = f"{WAN_BASE_URL}/flf2video"
DEFAULT_TIMEOUT = 7200  # 120 minutes for complex multi-GPU processing
MAX_RETRIES = 3


# Resolution options for WAN
class WanResolution(str, Enum):
    """Available resolutions for WAN video generation."""

    LANDSCAPE_HD = "1280*720"  # 16:9 landscape HD
    PORTRAIT_HD = "720*1280"  # 9:16 portrait HD
    LANDSCAPE_WIDE = "832*480"  # Widescreen landscape
    PORTRAIT_TALL = "480*832"  # Tall portrait
    SQUARE = "1024*1024"  # Square format


# User-friendly resolution mapping
RESOLUTION_NAMES = {
    "landscape_hd": WanResolution.LANDSCAPE_HD,
    "portrait_hd": WanResolution.PORTRAIT_HD,
    "landscape_wide": WanResolution.LANDSCAPE_WIDE,
    "portrait_tall": WanResolution.PORTRAIT_TALL,
    "square": WanResolution.SQUARE,
    # Allow direct format input
    "1280*720": WanResolution.LANDSCAPE_HD,
    "720*1280": WanResolution.PORTRAIT_HD,
    "832*480": WanResolution.LANDSCAPE_WIDE,
    "480*832": WanResolution.PORTRAIT_TALL,
    "1024*1024": WanResolution.SQUARE,
}


class WanVideoRequest(BaseModel):
    """Request model for WAN FLF2V (First Last Frame to Video) generation"""

    model_config = {"populate_by_name": True, "use_enum_values": True}

    # Required parameters
    prompt: str = Field(..., min_length=1, description="Text prompt for video generation")
    first_image_b64: str = Field(..., min_length=1, description="Base64 encoded first frame image (required)")
    last_image_b64: str = Field(..., min_length=1, description="Base64 encoded last frame image (required)")

    # Optional parameters with defaults
    negative_prompt: str = Field(
        "Vibrant colors, overexposed, static, blurry details, subtitles, style, artwork, painting, picture, still, overall grayish, worst quality, low quality, JPEG compression artifacts, ugly, incomplete, extra fingers, poorly drawn hands, poorly drawn face, deformed, disfigured, malformed limbs, fused fingers, motionless image, cluttered background, three legs, many people in the background, walking backwards, slow motion",
        description="Negative prompt (what to avoid)",
    )

    # Video parameters
    resolution: WanResolution = Field(WanResolution.LANDSCAPE_WIDE, description="Video resolution")
    fps: int = Field(16, ge=16, le=60, description="Frames per second")
    frames: int = Field(81, ge=81, le=241, description="Number of frames to generate (must be 4n+1)")

    # Generation control
    guidance_scale: float = Field(5.0, ge=1.0, le=7.5, description="Guidance scale for generation")
    steps: int = Field(25, ge=20, le=50, description="Number of sampling steps")
    seed: int | None = Field(42, ge=0, le=4294967295, description="Random seed for generation")

    # Advanced parameters
    sample_shift: float | None = Field(None, ge=1.0, le=7.0, description="Sample shift parameter (default: 3.0)")
    single_frame: bool = Field(False, description="Output single frame instead of video")

    @field_validator("frames")
    @classmethod
    def validate_frames(cls, v):
        """Ensure frames follows the constraint: frames % 4 == 1"""
        if v % 4 != 1:
            # Auto-correct to nearest valid value
            corrected = v - (v % 4) + 1
            logger.warning(f"Frame count {v} adjusted to {corrected} (must be 4n+1)")
            return corrected
        return v


class WanVideoResponse(BaseModel):
    """Response model for WAN video generation"""

    success: bool = Field(default=True)
    model_used: str = Field(..., description="Model that was used")
    video_url: str | None = Field(None, description="Generated video URL")
    video_data: bytes | None = Field(None, description="Binary video data")
    image_data: bytes | None = Field(None, description="Binary image data (if single_frame=True)")
    error_message: str | None = Field(None, description="Error message if failed")
    generation_time: float | None = Field(None, description="Time taken to generate in seconds")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class WanError(Exception):
    """Custom exception for WAN API errors"""


def safe_filename(text: str, max_length: int = 80, separator: str = "_") -> str:
    """
    Convert string to a safe, slugified filename.

    Args:
        text: Input string
        max_length: Maximum filename length
        separator: Character to use as separator (default: '_')

    Returns:
        Safe filename string
    """
    # Handle file extensions
    if "." in text and not text.startswith("."):
        name, ext = text.rsplit(".", 1)
        # Slugify the name part
        safe_name = slugify(name, separator=separator)
        # Ensure the extension is safe
        safe_ext = ext.lower()
        filename = f"{safe_name}.{safe_ext}" if safe_ext else safe_name
    else:
        filename = slugify(text, separator=separator)

    # Ensure it's a valid filename across platforms
    filename = sanitize_filename(filename)

    # Trim to max length, preserving extension if possible
    if len(filename) > max_length:
        if "." in filename:
            name, ext = filename.rsplit(".", 1)
            available_length = max_length - len(ext) - 1
            filename = f"{name[:available_length]}.{ext}"
        else:
            filename = filename[:max_length]

    # Remove leading/trailing separators and dots
    filename = filename.strip(f"{separator}.")

    # Ensure we don't have an empty filename
    return filename or "untitled"


def prompt_slug(prompt: str, max_words: int = 6) -> str:
    """
    Create a slug from the first few words of a prompt.

    Args:
        prompt: The text prompt
        max_words: Maximum number of words to use

    Returns:
        Slugified version of the prompt
    """
    words = prompt.strip().split()[:max_words]
    return safe_filename(" ".join(words))


def resize_image_to_resolution(image: Image.Image, target_resolution: str) -> Image.Image:
    """
    Resize image to match target resolution by scaling to longer dimension and cropping centrally.

    Args:
        image: PIL Image object
        target_resolution: Resolution string in format "width*height" (e.g., "1280*720")

    Returns:
        Resized PIL Image object
    """
    # Parse target resolution
    target_width, target_height = map(int, target_resolution.split("*"))

    # Get current image dimensions
    current_width, current_height = image.size

    # Calculate aspect ratios
    target_aspect = target_width / target_height
    current_aspect = current_width / current_height

    # Determine scaling factor based on longer dimension
    if current_aspect > target_aspect:
        # Image is wider than target - scale based on height (longer relative dimension)
        scale_factor = target_height / current_height
    else:
        # Image is taller than target - scale based on width (longer relative dimension)
        scale_factor = target_width / current_width

    # Scale the image
    new_width = int(current_width * scale_factor)
    new_height = int(current_height * scale_factor)
    scaled_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Calculate crop coordinates for center cropping
    if new_width > target_width:
        # Crop width centrally
        left = (new_width - target_width) // 2
        right = left + target_width
        top = 0
        bottom = target_height
    else:
        # Crop height centrally
        left = 0
        right = target_width
        top = (new_height - target_height) // 2
        bottom = top + target_height

    # Crop the image
    cropped_image = scaled_image.crop((left, top, right, bottom))

    return cropped_image


def create_color_image(color_hex: str, target_resolution: str) -> BytesIO:
    """
    Create a solid color image in temp folder and return as BytesIO.

    Args:
        color_hex: Hex color string (e.g., "#ff0000" or "ff0000")
        target_resolution: Resolution string in format "width*height" (e.g., "1280*720")

    Returns:
        BytesIO object containing the generated image

    Raises:
        ValueError: If color format is invalid
    """
    # Clean and validate hex color
    hex_color = color_hex.strip().lstrip("#")
    if not re.match(r"^[0-9a-fA-F]{6}$", hex_color):
        raise ValueError(f"Invalid hex color format: {color_hex}. Expected format: #rrggbb or rrggbb")

    # Parse target resolution
    try:
        target_width, target_height = map(int, target_resolution.split("*"))
    except ValueError:
        raise ValueError(f"Invalid resolution format: {target_resolution}. Expected format: width*height")

    # Convert hex to RGB
    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        rgb_color = (r, g, b)
    except ValueError:
        raise ValueError(f"Invalid hex color values in: {color_hex}")

    logger.debug(f"Creating {target_width}x{target_height} solid color image with RGB{rgb_color}")

    # Create the image
    image = Image.new("RGB", (target_width, target_height), rgb_color)

    # Save to BytesIO buffer
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=95)
    buffer.seek(0)

    return buffer


def is_color_hex_string(image_path: str | Path | BytesIO) -> bool:
    """
    Check if the image_path is a hex color string (starts with #).

    Args:
        image_path: Input that might be a color hex string

    Returns:
        True if it's a hex color string, False otherwise
    """
    if isinstance(image_path, str):
        return image_path.strip().startswith("#")
    return False


def encode_image_to_base64(image_path: str | Path | BytesIO, target_resolution: str | None = None) -> str:
    """
    Convert image to base64 string, optionally resizing to target resolution.
    Supports both regular images and hex color strings (e.g., "#ff0000").

    Args:
        image_path: Path to image file, BytesIO object, or hex color string (e.g., "#ff0000")
        target_resolution: Optional resolution string in format "width*height" (e.g., "1280*720")

    Returns:
        Base64 encoded image string

    Raises:
        ValueError: If image cannot be processed
    """
    try:
        # Check if this is a hex color string
        if is_color_hex_string(image_path):
            if not target_resolution:
                raise ValueError("target_resolution is required when using hex color strings")
            # Create solid color image
            color_buffer = create_color_image(str(image_path), target_resolution)
            image = Image.open(color_buffer)
            logger.debug(f"Created solid color image from hex: {image_path}")
        else:
            # Load regular image
            if isinstance(image_path, (str, Path)):
                image = Image.open(image_path)
            elif isinstance(image_path, BytesIO):
                image = Image.open(image_path)
            else:
                raise ValueError("image_path must be a file path, BytesIO object, or hex color string")

            # Resize if target resolution is specified
            if target_resolution:
                image = resize_image_to_resolution(image, target_resolution)

        # Convert to RGB if necessary (removes alpha channel)
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Save to BytesIO buffer
        buffer = BytesIO()
        image.save(buffer, format="JPEG", quality=95)
        image_bytes = buffer.getvalue()

        return base64.b64encode(image_bytes).decode("utf-8")
    except Exception as e:
        raise ValueError(f"Failed to encode image to base64: {e!s}") from e


def detect_content_format(content_data: bytes) -> str:
    """
    Detect content format from binary data.

    Args:
        content_data: Binary content data

    Returns:
        Content format extension (e.g., 'mp4', 'png')
    """
    # Check for video formats first
    if content_data.startswith(b"\x00\x00\x00\x14ftypmp4") or content_data.startswith(b"\x00\x00\x00\x18ftypmp4"):
        return "mp4"
    elif content_data.startswith(b"RIFF") and b"AVI " in content_data[:12]:
        return "avi"
    elif content_data.startswith(b"\x1aE\xdf\xa3"):
        return "webm"
    # Check for image formats
    elif content_data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    elif content_data.startswith(b"\xff\xd8\xff"):
        return "jpg"
    elif content_data.startswith(b"GIF87a") or content_data.startswith(b"GIF89a"):
        return "gif"
    else:
        # Default to mp4 for unknown binary content
        return "mp4"


def resolve_resolution(resolution_input: str) -> WanResolution:
    """
    Resolve user-friendly resolution name to WAN format.

    Args:
        resolution_input: User input (friendly name or direct format)

    Returns:
        WanResolution enum value

    Raises:
        ValueError: If resolution is not recognized
    """
    resolution_lower = resolution_input.lower()
    if resolution_lower in RESOLUTION_NAMES:
        return RESOLUTION_NAMES[resolution_lower]
    elif resolution_input in WanResolution:
        return WanResolution(resolution_input)
    else:
        valid_options = list(RESOLUTION_NAMES.keys())
        raise ValueError(f"Invalid resolution '{resolution_input}'. Valid options: {valid_options}")


class WanClient:
    """
    WAN API client for FLF2V (First Last Frame to Video) generation.

    Supports both sync and async operations with comprehensive error handling.
    Requires both first and last frame images for all video generation.
    """

    def __init__(self, api_key: str | None = None, timeout: int = DEFAULT_TIMEOUT):
        """
        Initialize WAN client.

        Args:
            api_key: Chutes API key. If None, uses CHUTES_API_KEY environment variable
            timeout: Request timeout in seconds
        """
        self.api_key = api_key or DEFAULT_API_KEY
        if not self.api_key:
            raise ValueError("API key required. Set CHUTES_API_KEY environment variable or pass api_key parameter")

        self.timeout = timeout
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        logger.info(f"WanClient initialized with timeout={timeout}s")

    @retry(
        stop=stop_after_attempt(10),  # More attempts for instance availability
        wait=wait_exponential(multiplier=2, min=15, max=120),  # Longer delays for instance startup
        retry=retry_if_exception_type(
            (
                requests.ConnectionError,
                requests.Timeout,
                requests.RequestException,
            )
        ),
        before_sleep=before_sleep_log(logger, "WARNING"),
        after=after_log(logger, "INFO"),
        reraise=True,
    )
    def _make_request_sync(self, url: str, data: dict[str, Any]) -> bytes:
        """
        Make HTTP request with retry logic (sync version).

        Args:
            url: API endpoint URL
            data: Request payload

        Returns:
            Response binary data (video/image content)

        Raises:
            WanError: On API errors
        """
        try:
            logger.debug(f"Making sync request to {url}")
            logger.debug(f"Request headers: {self.headers}")
            logger.debug(f"Request payload keys: {list(data.keys())}")

            response = requests.post(url, headers=self.headers, json=data, timeout=self.timeout)

            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response headers: {dict(response.headers)}")

            # Special handling for 503 "No instances available" error before general error handling
            if response.status_code == 503:
                try:
                    error_data = response.json()
                    if "No instances available" in error_data.get("detail", ""):
                        logger.debug(f"Error response body: {response.text}")
                        logger.warning("No compute instances available, retrying...")
                        # Convert to RequestException to trigger retry logic
                        raise requests.RequestException(f"503 No instances available: {error_data.get('detail')}")
                except json.JSONDecodeError:
                    # If we can't parse JSON, fall through to standard error handling
                    pass

            if response.status_code >= 400:
                # Log response body for error diagnostics
                try:
                    error_body = response.text
                    logger.debug(f"Error response body: {error_body}")
                except:
                    logger.debug("Could not read error response body")

            response.raise_for_status()

            # WAN returns binary video/image data directly
            content_type = response.headers.get("content-type", "").lower()
            logger.debug(f"Response content type: {content_type}")

            if "video/" in content_type or "image/" in content_type or "application/octet-stream" in content_type:
                logger.debug(f"Received binary response (size: {len(response.content)} bytes)")
                return response.content
            else:
                # Unexpected content type
                logger.warning(f"Unexpected content type: {content_type}")
                # Try to parse as JSON error response
                try:
                    error_data = response.json()
                    error_msg = error_data.get("error", "Unknown error from API")
                    raise WanError(f"API error: {error_msg}")
                except json.JSONDecodeError:
                    raise WanError(f"Unexpected response format. Content type: {content_type}")

        except requests.exceptions.RequestException as e:
            # Check if this is our retry RequestException - if so, re-raise it as-is
            if "503 No instances available" in str(e):
                # This is our retry exception, re-raise it to trigger retry logic
                raise e

            error_msg = f"Request failed: {e!s}"
            logger.error(error_msg)
            logger.error(f"Request URL: {url}")
            logger.error(f"Request timeout: {self.timeout}s")
            raise WanError(error_msg) from e
        except Exception as e:
            error_msg = f"Unexpected error: {e!s}"
            logger.error(error_msg)
            raise WanError(error_msg) from e

    async def _make_request_async(self, url: str, data: dict[str, Any]) -> bytes:
        """
        Make HTTP request asynchronously.

        Args:
            url: API endpoint URL
            data: Request payload

        Returns:
            Response binary data (video/image content)

        Raises:
            WanError: On API errors
        """
        try:
            logger.debug(f"Making async request to {url}")
            logger.debug(f"Request headers: {self.headers}")
            logger.debug(f"Request payload keys: {list(data.keys())}")

            timeout = aiohttp.ClientTimeout(total=self.timeout)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, headers=self.headers, json=data) as response:
                    logger.debug(f"Response status: {response.status}")
                    logger.debug(f"Response headers: {dict(response.headers)}")

                    response.raise_for_status()

                    # WAN returns binary video/image data directly
                    content_type = response.headers.get("content-type", "").lower()
                    logger.debug(f"Response content type: {content_type}")

                    content_data = await response.read()
                    logger.debug(f"Received binary response (size: {len(content_data)} bytes)")
                    return content_data

        except aiohttp.ClientError as e:
            error_msg = f"Async request failed: {e!s}"
            logger.error(error_msg)
            logger.error(f"Request URL: {url}")
            logger.error(f"Request timeout: {self.timeout}s")
            raise WanError(error_msg) from e
        except Exception as e:
            error_msg = f"Unexpected error: {e!s}"
            logger.error(error_msg)
            raise WanError(error_msg) from e

    def image_to_video_sync(
        self,
        prompt: str,
        first_frame: str | Path | BytesIO,
        last_frame: str | Path | BytesIO,
        negative_prompt: str | None = None,
        resolution: str | WanResolution = WanResolution.LANDSCAPE_WIDE,
        fps: int = 16,
        frames: int = 81,
        guidance_scale: float = 5.0,
        steps: int = 25,
        seed: int | None = None,
        sample_shift: float | None = None,
        single_frame: bool = False,
    ) -> WanVideoResponse:
        """
        Generate video from text prompt and required first/last frame images synchronously.

        Args:
            prompt: Text description of desired video
            first_frame: First frame image (path or BytesIO, required)
            last_frame: Last frame image (path or BytesIO, required)
            negative_prompt: What to avoid in the video
            resolution: Video resolution (WanResolution enum or string)
            fps: Frames per second (16-60)
            frames: Number of frames (81-241, must be 4n+1)
            guidance_scale: How closely to follow the prompt (1-7.5)
            steps: Number of sampling steps (20-50)
            seed: Random seed for reproducible results
            sample_shift: Sample shift parameter (1-7, default: 3.0)
            single_frame: Output single frame instead of video

        Returns:
            WanVideoResponse with generated video/image information
        """
        # Validate required inputs
        if first_frame is None or last_frame is None:
            raise ValueError("Both first_frame and last_frame are required for WAN video generation")

        # Resolve resolution if string
        if isinstance(resolution, str):
            try:
                resolution = resolve_resolution(resolution)
            except ValueError as e:
                logger.error(str(e))
                return WanVideoResponse(
                    success=False,
                    model_used="wan-2.1-flf2v",
                    error_message=str(e),
                )

        # Convert images to base64 with proper resizing
        try:
            resolution_str = resolution.value if isinstance(resolution, WanResolution) else resolution
            first_image_b64 = encode_image_to_base64(first_frame, resolution_str)
            last_image_b64 = encode_image_to_base64(last_frame, resolution_str)
            logger.debug(f"Encoded and resized first and last frame images to {resolution_str}")
        except Exception as e:
            logger.error(f"Failed to process input images: {e!s}")
            return WanVideoResponse(
                success=False,
                model_used="wan-2.1-flf2v",
                error_message=f"Image processing failed: {e!s}",
            )

        request_data = WanVideoRequest(
            prompt=prompt,
            first_image_b64=first_image_b64,
            last_image_b64=last_image_b64,
            negative_prompt=negative_prompt or WanVideoRequest.model_fields["negative_prompt"].default,
            resolution=resolution,
            fps=fps,
            frames=frames,
            guidance_scale=guidance_scale,
            steps=steps,
            seed=seed,
            sample_shift=sample_shift,
            single_frame=single_frame,
        )

        logger.info(
            "Generating WAN image-to-video",
            extra={
                "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
                "resolution": resolution,
                "fps": fps,
                "frames": frames,
                "guidance_scale": guidance_scale,
                "steps": steps,
                "single_frame": single_frame,
            },
        )

        try:
            start_time = time.time()
            content_data = self._make_request_sync(WAN_FLF2V_URL, request_data.model_dump(by_alias=True))
            generation_time = time.time() - start_time

            # Determine if we got video or image data
            if single_frame:
                return WanVideoResponse(
                    model_used="wan-2.1-flf2v",
                    image_data=content_data,
                    generation_time=generation_time,
                    metadata={"request_params": request_data.model_dump(by_alias=True)},
                )
            else:
                return WanVideoResponse(
                    model_used="wan-2.1-flf2v",
                    video_data=content_data,
                    generation_time=generation_time,
                    metadata={"request_params": request_data.model_dump(by_alias=True)},
                )
        except Exception as e:
            error_msg = f"WAN image-to-video generation failed: {e!s}"
            logger.error(error_msg)
            return WanVideoResponse(success=False, model_used="wan-2.1-flf2v", error_message=error_msg)

    # Keep backward compatibility alias
    def generate_image_to_video(self, *args, **kwargs) -> WanVideoResponse:
        """Generate image-to-video (backward compatibility alias)."""
        return self.image_to_video_sync(*args, **kwargs)

    async def image_to_video_async(
        self,
        prompt: str,
        first_frame: str | Path | BytesIO,
        last_frame: str | Path | BytesIO,
        negative_prompt: str | None = None,
        resolution: str | WanResolution = WanResolution.LANDSCAPE_WIDE,
        fps: int = 16,
        frames: int = 81,
        guidance_scale: float = 5.0,
        steps: int = 25,
        seed: int | None = None,
        sample_shift: float | None = None,
        single_frame: bool = False,
    ) -> WanVideoResponse:
        """
        Generate video from text prompt and required first/last frame images asynchronously.

        Args:
            prompt: Text description of desired video
            first_frame: First frame image (path or BytesIO, required)
            last_frame: Last frame image (path or BytesIO, required)
            negative_prompt: What to avoid in the video
            resolution: Video resolution (WanResolution enum or string)
            fps: Frames per second (16-60)
            frames: Number of frames (81-241, must be 4n+1)
            guidance_scale: How closely to follow the prompt (1-7.5)
            steps: Number of sampling steps (20-50)
            seed: Random seed for reproducible results
            sample_shift: Sample shift parameter (1-7, default: 3.0)
            single_frame: Output single frame instead of video

        Returns:
            WanVideoResponse with generated video/image information
        """
        # Validate required inputs
        if first_frame is None or last_frame is None:
            raise ValueError("Both first_frame and last_frame are required for WAN video generation")

        # Resolve resolution if string
        if isinstance(resolution, str):
            try:
                resolution = resolve_resolution(resolution)
            except ValueError as e:
                logger.error(str(e))
                return WanVideoResponse(
                    success=False,
                    model_used="wan-2.1-flf2v",
                    error_message=str(e),
                )

        # Convert images to base64 with proper resizing
        try:
            resolution_str = resolution.value if isinstance(resolution, WanResolution) else resolution
            first_image_b64 = encode_image_to_base64(first_frame, resolution_str)
            last_image_b64 = encode_image_to_base64(last_frame, resolution_str)
            logger.debug(f"Encoded and resized first and last frame images to {resolution_str}")
        except Exception as e:
            logger.error(f"Failed to process input images: {e!s}")
            return WanVideoResponse(
                success=False,
                model_used="wan-2.1-flf2v",
                error_message=f"Image processing failed: {e!s}",
            )

        request_data = WanVideoRequest(
            prompt=prompt,
            first_image_b64=first_image_b64,
            last_image_b64=last_image_b64,
            negative_prompt=negative_prompt or WanVideoRequest.model_fields["negative_prompt"].default,
            resolution=resolution,
            fps=fps,
            frames=frames,
            guidance_scale=guidance_scale,
            steps=steps,
            seed=seed,
            sample_shift=sample_shift,
            single_frame=single_frame,
        )

        logger.info(
            "Generating WAN image-to-video async",
            extra={
                "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
                "resolution": resolution,
                "fps": fps,
                "frames": frames,
                "guidance_scale": guidance_scale,
                "steps": steps,
                "single_frame": single_frame,
            },
        )

        try:
            start_time = time.time()
            content_data = await self._make_request_async(WAN_FLF2V_URL, request_data.model_dump(by_alias=True))
            generation_time = time.time() - start_time

            # Determine if we got video or image data
            if single_frame:
                return WanVideoResponse(
                    model_used="wan-2.1-flf2v",
                    image_data=content_data,
                    generation_time=generation_time,
                    metadata={"request_params": request_data.model_dump(by_alias=True)},
                )
            else:
                return WanVideoResponse(
                    model_used="wan-2.1-flf2v",
                    video_data=content_data,
                    generation_time=generation_time,
                    metadata={"request_params": request_data.model_dump(by_alias=True)},
                )
        except Exception as e:
            error_msg = f"WAN async image-to-video generation failed: {e!s}"
            logger.error(error_msg)
            return WanVideoResponse(success=False, model_used="wan-2.1-flf2v", error_message=error_msg)


class WanCLI:
    """Command-line interface for WAN video generation client."""

    def __init__(self, api_key: str | None = None, verbose: bool = False):
        """
        Initialize CLI.

        Args:
            api_key: Chutes API key
            verbose: Enable verbose logging
        """
        if verbose:
            logger.remove()
            logger.add(lambda msg: print(msg, end=""), colorize=True, level="DEBUG")

        self.client = WanClient(api_key=api_key)

    def video(
        self,
        first_frame: str | Path,
        last_frame: str | Path,
        prompt: str,
        output: str | Path | None = None,
        negative_prompt: str | None = None,
        resolution: str = "landscape_wide",
        fps: int = 16,
        frames: int = 81,
        guidance_scale: float = 5.0,
        steps: int = 25,
        seed: int | None = None,
        sample_shift: float | None = None,
        single_frame: bool = False,
        verbose: bool = False,
    ) -> None:
        """
        Generate video from text prompt and required first/last frame images.

        Args:
            prompt: Text description of desired video
            first_frame: Path to first frame image OR hex color (e.g., "#ff0000") (required)
            last_frame: Path to last frame image OR hex color (e.g., "#0000ff") (required)
            output: Output file path (optional, defaults to generated name)
            negative_prompt: What to avoid in the video (optional)
            resolution: Video resolution (default: "landscape_wide")
                       Options: landscape_hd, portrait_hd, landscape_wide, portrait_tall, square
                       Or direct: 1280*720, 720*1280, 832*480, 480*832, 1024*1024
            fps: Frames per second (16-60, default: 16)
            frames: Number of frames (81-241, default: 81, must be 4n+1)
            guidance_scale: How closely to follow the prompt (1-7.5, default: 5.0)
            steps: Number of sampling steps (20-50, default: 25)
            seed: Random seed for reproducible results (optional)
            sample_shift: Sample shift parameter (1-7, default: 3.0)
            single_frame: Output single frame instead of video
            verbose: Enable verbose debug logging

        Examples:
            # Using image files
            python chutes_wan_vid.py video "sunset transition" --first_frame start.jpg --last_frame end.jpg

            # Using hex colors
            python chutes_wan_vid.py video "fade from red to blue" --first_frame "#ff0000" --last_frame "#0000ff"

            # Mixed: image to color
            python chutes_wan_vid.py video "photo fades to black" --first_frame photo.jpg --last_frame "#000000"
        """
        if verbose:
            logger.remove()
            logger.add(lambda msg: print(msg, end=""), colorize=True, level="DEBUG")

        # Validate required image inputs
        if not first_frame or not last_frame:
            print("❌ Error: Both --first_frame and --last_frame are required for WAN video generation")
            print(
                "💡 Usage: python chutes_wan_vid.py video 'prompt text' --first_frame image1.jpg --last_frame image2.jpg"
            )
            return

        # Check if inputs are valid (either existing files or hex color strings)
        def validate_frame_input(frame_input: str, frame_name: str) -> bool:
            if is_color_hex_string(frame_input):
                # Validate hex color format
                try:
                    # This will raise ValueError if invalid
                    create_color_image(frame_input, "1*1")  # Just test format validation
                    print(f"✅ {frame_name} frame: Using hex color {frame_input}")
                    return True
                except ValueError as e:
                    print(f"❌ Error: Invalid hex color for {frame_name} frame: {e}")
                    return False
            elif Path(frame_input).exists():
                print(f"✅ {frame_name} frame: Using image file {frame_input}")
                return True
            else:
                print(f"❌ Error: {frame_name} frame not found and not a valid hex color: {frame_input}")
                print("💡 Use either an existing image file path or hex color format like '#ff0000'")
                return False

        if not validate_frame_input(str(first_frame), "First"):
            return
        if not validate_frame_input(str(last_frame), "Last"):
            return

        # Generate video
        response = self.client.image_to_video_sync(
            prompt=prompt,
            first_frame=first_frame,
            last_frame=last_frame,
            negative_prompt=negative_prompt,
            resolution=resolution,
            fps=fps,
            frames=frames,
            guidance_scale=guidance_scale,
            steps=steps,
            seed=seed,
            sample_shift=sample_shift,
            single_frame=single_frame,
        )

        if response.success:
            output_type = "image" if single_frame else "video"
            print(f"✅ {output_type.title()} generation successful!")
            if response.generation_time:
                print(f"⏱️  Generation time: {response.generation_time:.2f}s")

            # Determine output data and format
            content_data = response.image_data if single_frame else response.video_data

            if output and content_data:
                # Save to specified file
                output_path = Path(output)
                output_path.parent.mkdir(parents=True, exist_ok=True)

                with open(output_path, "wb") as f:
                    f.write(content_data)
                print(f"💾 {output_type.title()} saved to: {output_path}")
            elif content_data:
                # Auto-generate filename
                prompt_slug_name = prompt_slug(prompt)
                content_format = detect_content_format(content_data)
                if single_frame:
                    filename = f"{prompt_slug_name}_{resolution}.{content_format}"
                else:
                    filename = f"{prompt_slug_name}_{resolution}_{fps}fps_{frames}f.{content_format}"

                with open(filename, "wb") as f:
                    f.write(content_data)
                print(f"💾 {output_type.title()} saved to: {filename}")
            elif response.video_url:
                print(f"📎 {output_type.title()} URL: {response.video_url}")
        else:
            print(f"❌ Video generation failed: {response.error_message}")

    def info(self):
        """Show information about WAN video generation capabilities."""
        print("WAN FLF2V (First Last Frame to Video) Info:")
        print("Model: wan-2.1-flf2v")
        print(f"API Base URL: {WAN_BASE_URL}")
        print()
        print("🔴 IMPORTANT: Both first and last frame images are REQUIRED")
        print()
        print("Frame Input Options:")
        print("  • Image Files: Any standard image format (JPEG, PNG, etc.)")
        print("  • Hex Colors: Solid color frames using hex format (e.g., '#ff0000', '#0000ff')")
        print("  • Mixed: Combine image files with hex colors")
        print()
        print("Examples:")
        print("  # Image to image")
        print("  python chutes_wan_vid.py video 'transition' --first_frame start.jpg --last_frame end.jpg")
        print()
        print("  # Color to color")
        print("  python chutes_wan_vid.py video 'red to blue fade' --first_frame '#ff0000' --last_frame '#0000ff'")
        print()
        print("  # Image to color")
        print("  python chutes_wan_vid.py video 'fade to black' --first_frame photo.jpg --last_frame '#000000'")
        print()
        print("Available Resolutions:")
        print("  • landscape_hd (1280*720) - 16:9 landscape HD")
        print("  • portrait_hd (720*1280) - 9:16 portrait HD")
        print("  • landscape_wide (832*480) - Widescreen landscape")
        print("  • portrait_tall (480*832) - Tall portrait")
        print("  • square (1024*1024) - Square format")
        print()
        print("Parameter Ranges:")
        print("  • FPS: 16-60 (recommended: 16)")
        print("  • Frames: 81-241 (must be 4n+1, recommended: 81)")
        print("  • Guidance Scale: 1.0-7.5 (recommended: 5.0)")
        print("  • Steps: 20-50 (recommended: 25)")
        print("  • Sample Shift: 1.0-7.0 (default: 3.0)")
        print()
        print("Modes:")
        print("  • Video Generation: Generate video between first and last frames")
        print("  • Single Frame: Generate single interpolated frame (--single_frame)")
        print()
        print("GPU Requirements: 8x H100/H800/H200 GPUs")

    def resolutions(self):
        """List available resolution options with details."""
        print("Available WAN Resolution Options:")
        print()
        resolutions = [
            ("landscape_hd", "1280*720", "16:9 landscape HD", "Standard widescreen"),
            ("portrait_hd", "720*1280", "9:16 portrait HD", "Mobile/social media"),
            ("landscape_wide", "832*480", "~17:10 landscape", "Ultra-widescreen"),
            ("portrait_tall", "480*832", "~9:16 portrait", "Tall portrait"),
            ("square", "1024*1024", "1:1 square", "Square format"),
        ]

        for friendly_name, format_name, aspect, description in resolutions:
            print(f"  • {friendly_name:<15} → {format_name:<10} ({aspect:<15}) - {description}")
        print()
        print("Usage:")
        print("  --resolution landscape_hd    (friendly name)")
        print("  --resolution 1280*720       (direct format)")

    def test(self, verbose: bool = False):
        """Test WAN API connectivity and basic functionality."""
        if verbose:
            logger.remove()
            logger.add(lambda msg: print(msg, end=""), colorize=True, level="DEBUG")

        print("🧪 Testing WAN API connectivity...")
        print("⚠️  Note: Test requires two sample images for first and last frames")

        # For testing, we need to create minimal sample images
        try:
            from PIL import Image
            import io

            # Create simple test images
            test_image1 = Image.new("RGB", (100, 100), color="red")
            test_image2 = Image.new("RGB", (100, 100), color="blue")

            # Convert to BytesIO
            img1_buffer = io.BytesIO()
            img2_buffer = io.BytesIO()
            test_image1.save(img1_buffer, format="PNG")
            test_image2.save(img2_buffer, format="PNG")
            img1_buffer.seek(0)
            img2_buffer.seek(0)

            test_prompt = "A smooth transition from red to blue"

            response = self.client.image_to_video_sync(
                prompt=test_prompt,
                first_frame=img1_buffer,
                last_frame=img2_buffer,
                frames=81,  # Minimum frames for faster test
                steps=20,  # Minimum steps for faster test
                single_frame=True,  # Single frame for faster test
            )

            if response.success:
                print("✅ API connectivity test successful!")
                if response.generation_time:
                    print(f"⏱️  Test generation time: {response.generation_time:.2f}s")
                if response.image_data:
                    print(f"📊 Generated content size: {len(response.image_data)} bytes")
                print("🎉 WAN client is working correctly!")
            else:
                print(f"❌ API test failed: {response.error_message}")
        except Exception as e:
            print(f"❌ Test failed with exception: {e!s}")
            print("💡 Check your API key and network connection")


def main():
    """Main CLI entry point."""
    fire.Fire(WanCLI)


if __name__ == "__main__":
    main()
