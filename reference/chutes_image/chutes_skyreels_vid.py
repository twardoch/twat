#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["aiohttp", "requests", "pydantic", "fire", "tenacity", "loguru", "python-dotenv", "asyncio", "python-slugify", "pathvalidate", "pillow"]
# ///
# this_file: chutes_skyreels_vid.py

"""
Chutes AI SkyReels Video Generation Client

Comprehensive Python client for SkyReels-V2-14B video generation APIs.
Supports text-to-video and image-to-video generation with both library interface and CLI.
"""

import os
import json
import base64
import time
import re
from pathlib import Path
from typing import Literal, Any
from io import BytesIO
from enum import Enum

import aiohttp
import requests
import fire
from pydantic import BaseModel, Field, validator
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
SKYREELS_BASE_URL = "https://kikakkz-skyreels-v2-14b-540p.chutes.ai"
SKYREELS_T2V_URL = f"{SKYREELS_BASE_URL}/text2video"
SKYREELS_I2V_URL = f"{SKYREELS_BASE_URL}/image2video"
DEFAULT_TIMEOUT = 7200  # 120 minutes for video generation
MAX_RETRIES = 3


# Resolution options for SkyReels
class SkyreelsResolution(str, Enum):
    """Available resolutions for SkyReels video generation."""

    HD_720P = "720P"
    SD_540P = "540P"


class SkyreelsVideoRequest(BaseModel):
    """Request model for SkyReels video generation"""

    model_config = {"populate_by_name": True, "use_enum_values": True}

    # Core parameters
    prompt: str = Field(
        ..., min_length=1, description="Text prompt for video generation"
    )
    negative_prompt: str = Field(
        "色调艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，静止，整体发灰，最差质量，低质量，JPEG压缩残留，丑陋的，残缺的，多余的手指，画得不好的手部，画得不好的脸部，畸形的，毁容的，形态畸形的肢体，手指融合，静止不动的画面，杂乱的背景，三条腿，背景人很多，倒着走",
        description="Negative prompt (what to avoid)",
    )

    # Video parameters
    resolution: SkyreelsResolution = Field(
        SkyreelsResolution.SD_540P, description="Video resolution"
    )
    fps: int = Field(24, ge=16, le=60, description="Frames per second")
    num_frames: int = Field(
        97, ge=97, le=10000, description="Number of frames to generate"
    )
    base_num_frames: int = Field(
        97, ge=97, le=10000, description="Base number of frames"
    )

    # Generation control
    guidance_scale: float = Field(
        6.0, ge=1.0, le=7.5, description="Guidance scale for generation"
    )
    inference_steps: int = Field(
        30, ge=10, le=50, description="Number of inference steps"
    )
    seed: int | None = Field(
        42, ge=0, le=4294967295, description="Random seed for generation"
    )

    # Advanced parameters
    shift: float = Field(8.0, ge=1.0, le=10.0, description="Shift parameter")
    ar_step: int = Field(0, ge=0, le=5, description="AR step parameter")
    overlap_history: int = Field(17, le=10000, description="Overlap history")
    addnoise_condition: int = Field(20, ge=0, le=50, description="Add noise condition")
    causal_block_size: int = Field(1, ge=0, le=50, description="Causal block size")

    # Image inputs (for image-to-video)
    img_b64_first: str | None = Field(
        None, description="Base64 encoded first frame image"
    )
    img_b64_last: str | None = Field(
        None, description="Base64 encoded last frame image"
    )


class SkyreelsVideoResponse(BaseModel):
    """Response model for SkyReels video generation"""

    success: bool = Field(default=True)
    model_used: str = Field(..., description="Model that was used")
    video_url: str | None = Field(None, description="Generated video URL")
    video_data: bytes | None = Field(None, description="Binary video data")
    error_message: str | None = Field(None, description="Error message if failed")
    generation_time: float | None = Field(
        None, description="Time taken to generate in seconds"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )


class SkyreelsError(Exception):
    """Custom exception for SkyReels API errors"""


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


# Resolution mapping for SkyReels
SKYREELS_RESOLUTION_DIMENSIONS = {
    "720P": "1280*720",  # HD resolution
    "540P": "960*544",  # Standard resolution (approximate 540p)
}


def resize_image_to_resolution(
    image: Image.Image, target_resolution: str
) -> Image.Image:
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
        raise ValueError(
            f"Invalid hex color format: {color_hex}. Expected format: #rrggbb or rrggbb"
        )

    # Parse target resolution
    try:
        target_width, target_height = map(int, target_resolution.split("*"))
    except ValueError:
        raise ValueError(
            f"Invalid resolution format: {target_resolution}. Expected format: width*height"
        )

    # Convert hex to RGB
    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        rgb_color = (r, g, b)
    except ValueError:
        raise ValueError(f"Invalid hex color values in: {color_hex}")

    logger.debug(
        f"Creating {target_width}x{target_height} solid color image with RGB{rgb_color}"
    )

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


def encode_image_to_base64(
    image_path: str | Path | BytesIO, target_resolution: str | None = None
) -> str:
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
                raise ValueError(
                    "target_resolution is required when using hex color strings"
                )
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
                raise ValueError(
                    "image_path must be a file path, BytesIO object, or hex color string"
                )

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
        raise ValueError(f"Failed to encode image to base64: {str(e)}") from e


def detect_video_format(video_data: bytes) -> str:
    """
    Detect video format from binary data.

    Args:
        video_data: Binary video data

    Returns:
        Video format extension (e.g., 'mp4', 'avi')
    """
    # Check for common video file signatures
    if video_data.startswith(b"\x00\x00\x00\x14ftypmp4") or video_data.startswith(
        b"\x00\x00\x00\x18ftypmp4"
    ):
        return "mp4"
    elif video_data.startswith(b"RIFF") and b"AVI " in video_data[:12]:
        return "avi"
    elif video_data.startswith(b"\x1aE\xdf\xa3"):
        return "webm"
    else:
        # Default to mp4 for unknown formats
        return "mp4"


class SkyreelsClient:
    """
    SkyReels API client for text-to-video and image-to-video generation.

    Supports both sync and async operations with comprehensive error handling.
    """

    def __init__(self, api_key: str | None = None, timeout: int = DEFAULT_TIMEOUT):
        """
        Initialize SkyReels client.

        Args:
            api_key: Chutes API key. If None, uses CHUTES_API_KEY environment variable
            timeout: Request timeout in seconds
        """
        self.api_key = api_key or DEFAULT_API_KEY
        if not self.api_key:
            raise ValueError(
                "API key required. Set CHUTES_API_KEY environment variable or pass api_key parameter"
            )

        self.timeout = timeout
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        logger.info(f"SkyreelsClient initialized with timeout={timeout}s")

    @retry(
        stop=stop_after_attempt(MAX_RETRIES),
        wait=wait_exponential(multiplier=2, min=5, max=30),
        retry=retry_if_exception_type(
            (
                requests.ConnectionError,
                requests.Timeout,
                requests.HTTPError,
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
            Response binary data (video content)

        Raises:
            SkyreelsError: On API errors
        """
        try:
            logger.debug(f"Making sync request to {url}")
            logger.debug(f"Request headers: {self.headers}")
            logger.debug(f"Request payload keys: {list(data.keys())}")

            response = requests.post(
                url, headers=self.headers, json=data, timeout=self.timeout
            )

            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response headers: {dict(response.headers)}")

            response.raise_for_status()

            # SkyReels returns binary video data directly
            content_type = response.headers.get("content-type", "").lower()
            logger.debug(f"Response content type: {content_type}")

            if "video/" in content_type or "application/octet-stream" in content_type:
                logger.debug(
                    f"Received video response (size: {len(response.content)} bytes)"
                )
                return response.content
            else:
                # Unexpected content type
                logger.warning(f"Unexpected content type: {content_type}")
                # Try to parse as JSON error response
                try:
                    error_data = response.json()
                    error_msg = error_data.get("error", "Unknown error from API")
                    raise SkyreelsError(f"API error: {error_msg}")
                except json.JSONDecodeError:
                    raise SkyreelsError(
                        f"Unexpected response format. Content type: {content_type}"
                    )

        except requests.exceptions.RequestException as e:
            error_msg = f"Request failed: {str(e)}"
            logger.error(error_msg)
            logger.error(f"Request URL: {url}")
            logger.error(f"Request timeout: {self.timeout}s")
            raise SkyreelsError(error_msg) from e
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            raise SkyreelsError(error_msg) from e

    async def _make_request_async(self, url: str, data: dict[str, Any]) -> bytes:
        """
        Make HTTP request asynchronously.

        Args:
            url: API endpoint URL
            data: Request payload

        Returns:
            Response binary data (video content)

        Raises:
            SkyreelsError: On API errors
        """
        try:
            logger.debug(f"Making async request to {url}")
            logger.debug(f"Request headers: {self.headers}")
            logger.debug(f"Request payload keys: {list(data.keys())}")

            timeout = aiohttp.ClientTimeout(total=self.timeout)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(
                    url, headers=self.headers, json=data
                ) as response:
                    logger.debug(f"Response status: {response.status}")
                    logger.debug(f"Response headers: {dict(response.headers)}")

                    response.raise_for_status()

                    # SkyReels returns binary video data directly
                    content_type = response.headers.get("content-type", "").lower()
                    logger.debug(f"Response content type: {content_type}")

                    video_data = await response.read()
                    logger.debug(
                        f"Received video response (size: {len(video_data)} bytes)"
                    )
                    return video_data

        except aiohttp.ClientError as e:
            error_msg = f"Async request failed: {str(e)}"
            logger.error(error_msg)
            logger.error(f"Request URL: {url}")
            logger.error(f"Request timeout: {self.timeout}s")
            raise SkyreelsError(error_msg) from e
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            raise SkyreelsError(error_msg) from e

    def text_to_video_sync(
        self,
        prompt: str,
        negative_prompt: str | None = None,
        resolution: SkyreelsResolution = SkyreelsResolution.SD_540P,
        fps: int = 24,
        num_frames: int = 97,
        guidance_scale: float = 6.0,
        inference_steps: int = 30,
        seed: int | None = None,
        **kwargs,
    ) -> SkyreelsVideoResponse:
        """
        Generate video from text prompt synchronously.

        Args:
            prompt: Text description of desired video
            negative_prompt: What to avoid in the video
            resolution: Video resolution (720P or 540P)
            fps: Frames per second (16-60)
            num_frames: Number of frames (97-10000)
            guidance_scale: How closely to follow the prompt (1-7.5)
            inference_steps: Number of denoising steps (10-50)
            seed: Random seed for reproducible results
            **kwargs: Additional parameters

        Returns:
            SkyreelsVideoResponse with generated video information
        """
        request_data = SkyreelsVideoRequest(
            prompt=prompt,
            negative_prompt=negative_prompt
            or SkyreelsVideoRequest.model_fields["negative_prompt"].default,
            resolution=resolution,
            fps=fps,
            num_frames=num_frames,
            base_num_frames=kwargs.get("base_num_frames", num_frames),
            guidance_scale=guidance_scale,
            inference_steps=inference_steps,
            seed=seed,
            shift=kwargs.get("shift", 8.0),
            ar_step=kwargs.get("ar_step", 0),
            overlap_history=kwargs.get("overlap_history", 17),
            addnoise_condition=kwargs.get("addnoise_condition", 20),
            causal_block_size=kwargs.get("causal_block_size", 1),
        )

        logger.info(
            f"Generating SkyReels text-to-video",
            extra={
                "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
                "resolution": resolution,
                "fps": fps,
                "num_frames": num_frames,
                "guidance_scale": guidance_scale,
                "steps": inference_steps,
            },
        )

        try:
            start_time = time.time()
            video_data = self._make_request_sync(
                SKYREELS_T2V_URL, request_data.model_dump(by_alias=True)
            )
            generation_time = time.time() - start_time

            return SkyreelsVideoResponse(
                model_used="skyreels-v2-14b-540p",
                video_data=video_data,
                generation_time=generation_time,
                metadata={"request_params": request_data.model_dump(by_alias=True)},
            )
        except Exception as e:
            error_msg = f"SkyReels text-to-video generation failed: {str(e)}"
            logger.error(error_msg)
            return SkyreelsVideoResponse(
                success=False,
                model_used="skyreels-v2-14b-540p",
                error_message=error_msg,
            )

    def image_to_video_sync(
        self,
        prompt: str,
        first_frame: str | Path | BytesIO | None = None,
        last_frame: str | Path | BytesIO | None = None,
        negative_prompt: str | None = None,
        resolution: SkyreelsResolution = SkyreelsResolution.SD_540P,
        fps: int = 24,
        num_frames: int = 97,
        guidance_scale: float = 6.0,
        inference_steps: int = 30,
        seed: int | None = None,
        **kwargs,
    ) -> SkyreelsVideoResponse:
        """
        Generate video from text prompt and image inputs synchronously.

        Args:
            prompt: Text description of desired video
            first_frame: First frame image (path, BytesIO, or None)
            last_frame: Last frame image (path, BytesIO, or None)
            negative_prompt: What to avoid in the video
            resolution: Video resolution (720P or 540P)
            fps: Frames per second (16-60)
            num_frames: Number of frames (97-10000)
            guidance_scale: How closely to follow the prompt (1-7.5)
            inference_steps: Number of denoising steps (10-50)
            seed: Random seed for reproducible results
            **kwargs: Additional parameters

        Returns:
            SkyreelsVideoResponse with generated video information
        """
        # Convert images to base64 with proper resizing
        img_b64_first = None
        img_b64_last = None

        # Get target resolution dimensions
        resolution_dimensions = SKYREELS_RESOLUTION_DIMENSIONS.get(
            resolution.value, None
        )

        try:
            if first_frame is not None:
                img_b64_first = encode_image_to_base64(
                    first_frame, resolution_dimensions
                )
                logger.debug(
                    f"Encoded and resized first frame image to {resolution_dimensions or 'original size'}"
                )

            if last_frame is not None:
                img_b64_last = encode_image_to_base64(last_frame, resolution_dimensions)
                logger.debug(
                    f"Encoded and resized last frame image to {resolution_dimensions or 'original size'}"
                )
        except Exception as e:
            logger.error(f"Failed to process input images: {str(e)}")
            return SkyreelsVideoResponse(
                success=False,
                model_used="skyreels-v2-14b-540p",
                error_message=f"Image processing failed: {str(e)}",
            )

        request_data = SkyreelsVideoRequest(
            prompt=prompt,
            negative_prompt=negative_prompt
            or SkyreelsVideoRequest.model_fields["negative_prompt"].default,
            resolution=resolution,
            fps=fps,
            num_frames=num_frames,
            base_num_frames=kwargs.get("base_num_frames", num_frames),
            guidance_scale=guidance_scale,
            inference_steps=inference_steps,
            seed=seed,
            shift=kwargs.get("shift", 8.0),
            ar_step=kwargs.get("ar_step", 0),
            overlap_history=kwargs.get("overlap_history", 17),
            addnoise_condition=kwargs.get("addnoise_condition", 20),
            causal_block_size=kwargs.get("causal_block_size", 1),
            img_b64_first=img_b64_first,
            img_b64_last=img_b64_last,
        )

        logger.info(
            f"Generating SkyReels image-to-video",
            extra={
                "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
                "resolution": resolution,
                "fps": fps,
                "num_frames": num_frames,
                "guidance_scale": guidance_scale,
                "steps": inference_steps,
                "has_first_frame": first_frame is not None,
                "has_last_frame": last_frame is not None,
            },
        )

        try:
            start_time = time.time()
            video_data = self._make_request_sync(
                SKYREELS_I2V_URL, request_data.model_dump(by_alias=True)
            )
            generation_time = time.time() - start_time

            return SkyreelsVideoResponse(
                model_used="skyreels-v2-14b-540p",
                video_data=video_data,
                generation_time=generation_time,
                metadata={"request_params": request_data.model_dump(by_alias=True)},
            )
        except Exception as e:
            error_msg = f"SkyReels image-to-video generation failed: {str(e)}"
            logger.error(error_msg)
            return SkyreelsVideoResponse(
                success=False,
                model_used="skyreels-v2-14b-540p",
                error_message=error_msg,
            )

    # Keep backward compatibility aliases
    def generate_text_to_video(self, *args, **kwargs) -> SkyreelsVideoResponse:
        """Generate text-to-video (backward compatibility alias)."""
        return self.text_to_video_sync(*args, **kwargs)

    def generate_image_to_video(self, *args, **kwargs) -> SkyreelsVideoResponse:
        """Generate image-to-video (backward compatibility alias)."""
        return self.image_to_video_sync(*args, **kwargs)

    async def text_to_video_async(
        self,
        prompt: str,
        negative_prompt: str | None = None,
        resolution: SkyreelsResolution = SkyreelsResolution.SD_540P,
        fps: int = 24,
        num_frames: int = 97,
        guidance_scale: float = 6.0,
        inference_steps: int = 30,
        seed: int | None = None,
        **kwargs,
    ) -> SkyreelsVideoResponse:
        """
        Generate video from text prompt asynchronously.

        Args:
            prompt: Text description of desired video
            negative_prompt: What to avoid in the video
            resolution: Video resolution (720P or 540P)
            fps: Frames per second (16-60)
            num_frames: Number of frames (97-10000)
            guidance_scale: How closely to follow the prompt (1-7.5)
            inference_steps: Number of denoising steps (10-50)
            seed: Random seed for reproducible results
            **kwargs: Additional parameters

        Returns:
            SkyreelsVideoResponse with generated video information
        """
        request_data = SkyreelsVideoRequest(
            prompt=prompt,
            negative_prompt=negative_prompt
            or SkyreelsVideoRequest.model_fields["negative_prompt"].default,
            resolution=resolution,
            fps=fps,
            num_frames=num_frames,
            base_num_frames=kwargs.get("base_num_frames", num_frames),
            guidance_scale=guidance_scale,
            inference_steps=inference_steps,
            seed=seed,
            shift=kwargs.get("shift", 8.0),
            ar_step=kwargs.get("ar_step", 0),
            overlap_history=kwargs.get("overlap_history", 17),
            addnoise_condition=kwargs.get("addnoise_condition", 20),
            causal_block_size=kwargs.get("causal_block_size", 1),
        )

        logger.info(
            f"Generating SkyReels text-to-video async",
            extra={
                "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
                "resolution": resolution,
                "fps": fps,
                "num_frames": num_frames,
                "guidance_scale": guidance_scale,
                "steps": inference_steps,
            },
        )

        try:
            start_time = time.time()
            video_data = await self._make_request_async(
                SKYREELS_T2V_URL, request_data.model_dump(by_alias=True)
            )
            generation_time = time.time() - start_time

            return SkyreelsVideoResponse(
                model_used="skyreels-v2-14b-540p",
                video_data=video_data,
                generation_time=generation_time,
                metadata={"request_params": request_data.model_dump(by_alias=True)},
            )
        except Exception as e:
            error_msg = f"SkyReels async text-to-video generation failed: {str(e)}"
            logger.error(error_msg)
            return SkyreelsVideoResponse(
                success=False,
                model_used="skyreels-v2-14b-540p",
                error_message=error_msg,
            )

    async def image_to_video_async(
        self,
        prompt: str,
        first_frame: str | Path | BytesIO | None = None,
        last_frame: str | Path | BytesIO | None = None,
        negative_prompt: str | None = None,
        resolution: SkyreelsResolution = SkyreelsResolution.SD_540P,
        fps: int = 24,
        num_frames: int = 97,
        guidance_scale: float = 6.0,
        inference_steps: int = 30,
        seed: int | None = None,
        **kwargs,
    ) -> SkyreelsVideoResponse:
        """
        Generate video from text prompt and image inputs asynchronously.

        Args:
            prompt: Text description of desired video
            first_frame: First frame image (path, BytesIO, or None)
            last_frame: Last frame image (path, BytesIO, or None)
            negative_prompt: What to avoid in the video
            resolution: Video resolution (720P or 540P)
            fps: Frames per second (16-60)
            num_frames: Number of frames (97-10000)
            guidance_scale: How closely to follow the prompt (1-7.5)
            inference_steps: Number of denoising steps (10-50)
            seed: Random seed for reproducible results
            **kwargs: Additional parameters

        Returns:
            SkyreelsVideoResponse with generated video information
        """
        # Convert images to base64 with proper resizing
        img_b64_first = None
        img_b64_last = None

        # Get target resolution dimensions
        resolution_dimensions = SKYREELS_RESOLUTION_DIMENSIONS.get(
            resolution.value, None
        )

        try:
            if first_frame is not None:
                img_b64_first = encode_image_to_base64(
                    first_frame, resolution_dimensions
                )
                logger.debug(
                    f"Encoded and resized first frame image to {resolution_dimensions or 'original size'}"
                )

            if last_frame is not None:
                img_b64_last = encode_image_to_base64(last_frame, resolution_dimensions)
                logger.debug(
                    f"Encoded and resized last frame image to {resolution_dimensions or 'original size'}"
                )
        except Exception as e:
            logger.error(f"Failed to process input images: {str(e)}")
            return SkyreelsVideoResponse(
                success=False,
                model_used="skyreels-v2-14b-540p",
                error_message=f"Image processing failed: {str(e)}",
            )

        request_data = SkyreelsVideoRequest(
            prompt=prompt,
            negative_prompt=negative_prompt
            or SkyreelsVideoRequest.model_fields["negative_prompt"].default,
            resolution=resolution,
            fps=fps,
            num_frames=num_frames,
            base_num_frames=kwargs.get("base_num_frames", num_frames),
            guidance_scale=guidance_scale,
            inference_steps=inference_steps,
            seed=seed,
            shift=kwargs.get("shift", 8.0),
            ar_step=kwargs.get("ar_step", 0),
            overlap_history=kwargs.get("overlap_history", 17),
            addnoise_condition=kwargs.get("addnoise_condition", 20),
            causal_block_size=kwargs.get("causal_block_size", 1),
            img_b64_first=img_b64_first,
            img_b64_last=img_b64_last,
        )

        logger.info(
            f"Generating SkyReels image-to-video async",
            extra={
                "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
                "resolution": resolution,
                "fps": fps,
                "num_frames": num_frames,
                "guidance_scale": guidance_scale,
                "steps": inference_steps,
                "has_first_frame": first_frame is not None,
                "has_last_frame": last_frame is not None,
            },
        )

        try:
            start_time = time.time()
            video_data = await self._make_request_async(
                SKYREELS_I2V_URL, request_data.model_dump(by_alias=True)
            )
            generation_time = time.time() - start_time

            return SkyreelsVideoResponse(
                model_used="skyreels-v2-14b-540p",
                video_data=video_data,
                generation_time=generation_time,
                metadata={"request_params": request_data.model_dump(by_alias=True)},
            )
        except Exception as e:
            error_msg = f"SkyReels async image-to-video generation failed: {str(e)}"
            logger.error(error_msg)
            return SkyreelsVideoResponse(
                success=False,
                model_used="skyreels-v2-14b-540p",
                error_message=error_msg,
            )


class SkyreelsCLI:
    """Command-line interface for SkyReels video generation client."""

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

        self.client = SkyreelsClient(api_key=api_key)

    def video(
        self,
        prompt: str,
        output: str | None = None,
        first_frame: str | None = None,
        last_frame: str | None = None,
        negative_prompt: str | None = None,
        resolution: str = "540P",
        fps: int = 24,
        num_frames: int = 97,
        guidance_scale: float = 6.0,
        inference_steps: int = 30,
        seed: int | None = None,
        verbose: bool = False,
        # Advanced parameters
        shift: float = 8.0,
        ar_step: int = 0,
        overlap_history: int = 17,
        addnoise_condition: int = 20,
        causal_block_size: int = 1,
    ):
        """
        Generate video from text prompt and optional image inputs.

        Args:
            prompt: Text description of desired video
            output: Output file path (optional, defaults to generated name)
            first_frame: Path to first frame image OR hex color (e.g., "#ff0000") (optional, for image-to-video)
            last_frame: Path to last frame image OR hex color (e.g., "#0000ff") (optional, for image-to-video)
            negative_prompt: What to avoid in the video (optional)
            resolution: Video resolution - "720P" or "540P" (default: "540P")
            fps: Frames per second (16-60, default: 24)
            num_frames: Number of frames (97-10000, default: 97)
            guidance_scale: How closely to follow the prompt (1-7.5, default: 6.0)
            inference_steps: Number of denoising steps (10-50, default: 30)
            seed: Random seed for reproducible results (optional)
            verbose: Enable verbose debug logging
            shift: Shift parameter (1-10, default: 8.0)
            ar_step: AR step parameter (0-5, default: 0)
            overlap_history: Overlap history (max 10000, default: 17)
            addnoise_condition: Add noise condition (0-50, default: 20)
            causal_block_size: Causal block size (0-50, default: 1)

        Examples:
            # Using image files
            python chutes_skyreels_vid.py video "sunset transition" --first_frame start.jpg --last_frame end.jpg

            # Using hex colors
            python chutes_skyreels_vid.py video "fade from red to blue" --first_frame "#ff0000" --last_frame "#0000ff"

            # Mixed: image to color
            python chutes_skyreels_vid.py video "photo fades to black" --first_frame photo.jpg --last_frame "#000000"
        """
        if verbose:
            logger.remove()
            logger.add(lambda msg: print(msg, end=""), colorize=True, level="DEBUG")

        # Validate resolution
        try:
            resolution_enum = SkyreelsResolution(resolution)
        except ValueError:
            print(f"❌ Invalid resolution '{resolution}'. Valid options: 720P, 540P")
            return

        # Validate frame inputs if provided
        def validate_frame_input(frame_input: str, frame_name: str) -> bool:
            if frame_input is None:
                return True

            if is_color_hex_string(frame_input):
                # Validate hex color format
                try:
                    # This will raise ValueError if invalid
                    create_color_image(
                        frame_input, "1*1"
                    )  # Just test format validation
                    print(f"✅ {frame_name} frame: Using hex color {frame_input}")
                    return True
                except ValueError as e:
                    print(f"❌ Error: Invalid hex color for {frame_name} frame: {e}")
                    return False
            elif Path(frame_input).exists():
                print(f"✅ {frame_name} frame: Using image file {frame_input}")
                return True
            else:
                print(
                    f"❌ Error: {frame_name} frame not found and not a valid hex color: {frame_input}"
                )
                print(
                    f"💡 Use either an existing image file path or hex color format like '#ff0000'"
                )
                return False

        if not validate_frame_input(first_frame, "First"):
            return
        if not validate_frame_input(last_frame, "Last"):
            return

        # Determine if this is text-to-video or image-to-video
        is_image_to_video = first_frame is not None or last_frame is not None

        if is_image_to_video:
            # Image-to-video generation
            response = self.client.image_to_video_sync(
                prompt=prompt,
                first_frame=first_frame,
                last_frame=last_frame,
                negative_prompt=negative_prompt,
                resolution=resolution_enum,
                fps=fps,
                num_frames=num_frames,
                guidance_scale=guidance_scale,
                inference_steps=inference_steps,
                seed=seed,
                shift=shift,
                ar_step=ar_step,
                overlap_history=overlap_history,
                addnoise_condition=addnoise_condition,
                causal_block_size=causal_block_size,
            )
        else:
            # Text-to-video generation
            response = self.client.text_to_video_sync(
                prompt=prompt,
                negative_prompt=negative_prompt,
                resolution=resolution_enum,
                fps=fps,
                num_frames=num_frames,
                guidance_scale=guidance_scale,
                inference_steps=inference_steps,
                seed=seed,
                shift=shift,
                ar_step=ar_step,
                overlap_history=overlap_history,
                addnoise_condition=addnoise_condition,
                causal_block_size=causal_block_size,
            )

        if response.success:
            print(f"✅ Video generation successful!")
            if response.generation_time:
                print(f"⏱️  Generation time: {response.generation_time:.2f}s")

            if output and response.video_data:
                # Save video to file
                output_path = Path(output)
                output_path.parent.mkdir(parents=True, exist_ok=True)

                with open(output_path, "wb") as f:
                    f.write(response.video_data)
                print(f"💾 Video saved to: {output_path}")
            elif response.video_data:
                # Auto-generate filename
                prompt_slug_name = prompt_slug(prompt)
                video_format = detect_video_format(response.video_data)
                filename = f"{prompt_slug_name}_{resolution}_{fps}fps_{num_frames}f.{video_format}"

                with open(filename, "wb") as f:
                    f.write(response.video_data)
                print(f"💾 Video saved to: {filename}")
            elif response.video_url:
                print(f"📎 Video URL: {response.video_url}")
        else:
            print(f"❌ Video generation failed: {response.error_message}")

    def info(self):
        """Show information about SkyReels video generation capabilities."""
        print("SkyReels Video Generation Info:")
        print(f"Model: skyreels-v2-14b-540p")
        print(f"API Base URL: {SKYREELS_BASE_URL}")
        print()
        print("Frame Input Options:")
        print("  • Image Files: Any standard image format (JPEG, PNG, etc.)")
        print(
            "  • Hex Colors: Solid color frames using hex format (e.g., '#ff0000', '#0000ff')"
        )
        print("  • Mixed: Combine image files with hex colors")
        print()
        print("Examples:")
        print("  # Image to image")
        print(
            "  python chutes_skyreels_vid.py video 'transition' --first_frame start.jpg --last_frame end.jpg"
        )
        print()
        print("  # Color to color")
        print(
            "  python chutes_skyreels_vid.py video 'red to blue fade' --first_frame '#ff0000' --last_frame '#0000ff'"
        )
        print()
        print("  # Image to color")
        print(
            "  python chutes_skyreels_vid.py video 'fade to black' --first_frame photo.jpg --last_frame '#000000'"
        )
        print()
        print("Available Resolutions:")
        print("  • 720P (1280x720) - HD quality")
        print("  • 540P (960x544) - Standard quality")
        print()
        print("Parameter Ranges:")
        print("  • FPS: 16-60 (recommended: 24)")
        print("  • Num Frames: 97-10000 (recommended: 97-200)")
        print("  • Guidance Scale: 1.0-7.5 (recommended: 6.0)")
        print("  • Inference Steps: 10-50 (recommended: 30)")
        print("  • Shift: 1.0-10.0 (recommended: 8.0)")
        print("  • AR Step: 0-5 (recommended: 0)")
        print()
        print("Modes:")
        print("  • Text-to-Video: Generate video from text prompt only")
        print("  • Image-to-Video: Generate video from text + first/last frame images")

    def test(self, verbose: bool = False):
        """Test SkyReels API connectivity and basic functionality."""
        if verbose:
            logger.remove()
            logger.add(lambda msg: print(msg, end=""), colorize=True, level="DEBUG")

        print("🧪 Testing SkyReels API connectivity...")

        # Test with minimal parameters
        test_prompt = "A peaceful sunset over calm ocean waves"

        try:
            response = self.client.text_to_video_sync(
                prompt=test_prompt,
                num_frames=97,  # Minimum frames for faster test
                inference_steps=10,  # Minimum steps for faster test
            )

            if response.success:
                print("✅ API connectivity test successful!")
                if response.generation_time:
                    print(f"⏱️  Test generation time: {response.generation_time:.2f}s")
                if response.video_data:
                    print(f"📊 Generated video size: {len(response.video_data)} bytes")
                print("🎉 SkyReels client is working correctly!")
            else:
                print(f"❌ API test failed: {response.error_message}")
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
            print("💡 Check your API key and network connection")


def main():
    """Main CLI entry point."""
    fire.Fire(SkyreelsCLI)


if __name__ == "__main__":
    main()
