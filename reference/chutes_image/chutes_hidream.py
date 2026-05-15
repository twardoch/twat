#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["aiohttp", "requests", "pydantic", "fire", "tenacity", "loguru", "python-dotenv", "asyncio", "python-slugify", "pathvalidate", "pillow"]
# ///
# this_file: chutes_hidream.py

"""
Chutes AI HiDream API Client

Efficient Python client for HiDream text-to-image and image-editing APIs.
Provides both library interface and CLI using Fire.
"""

import os
import json
import re
import base64
import time
from pathlib import Path
from typing import Literal, Any
from io import BytesIO

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
HIDREAM_GENERATE_URL = "https://chutes-hidream.chutes.ai/generate"
HIDREAM_EDIT_URL = "https://chutes-hidream-edit.chutes.ai/generate"
DEFAULT_TIMEOUT = 120
MAX_RETRIES = 3

# Resolution options for HiDream
HIDREAM_RESOLUTIONS = Literal[
    "1024x1024", "768x1360", "1360x768", "880x1168", "1168x880", "1248x832", "832x1248"
]


class ModelInfo(BaseModel):
    """Information about an available HiDream model"""

    name: str = Field(..., description="Model identifier")
    display_name: str = Field(..., description="Human-readable model name")
    description: str | None = Field("", description="Model description")
    category: str | None = Field("hidream", description="Model category")
    supports_editing: bool = Field(
        True, description="Whether model supports image editing"
    )
    default_resolution: str = Field("1024x1024", description="Default res")
    default_steps: int = Field(50, description="Default inference steps")
    max_steps: int = Field(75, description="Maximum inference steps")
    min_steps: int = Field(5, description="Minimum inference steps")


# HiDream model registry
HIDREAM_MODEL_REGISTRY = {
    "hidream-v1": ModelInfo(
        name="hidream-v1",
        display_name="HiDream v1",
        description="High-quality text-to-image generation with HiDream",
        category="hidream",
        supports_editing=True,
        default_resolution="1024x1024",
        default_steps=50,
        max_steps=75,
        min_steps=5,
    ),
    "hidream-edit": ModelInfo(
        name="hidream-edit",
        display_name="HiDream Edit",
        description="HiDream image editing and enhancement",
        category="hidream-edit",
        supports_editing=True,
        default_resolution="1024x1024",
        default_steps=28,
        max_steps=75,
        min_steps=5,
    ),
}


class HidreamGenerateRequest(BaseModel):
    """Request model for HiDream text-to-image generation"""
    
    model_config = {"populate_by_name": True, "use_enum_values": True}

    seed: int | None = Field(
        None, ge=0, le=100000000, description="Random seed for generation"
    )
    prompt: str = Field(
        ..., min_length=1, description="Text prompt for image generation"
    )
    resolution: HIDREAM_RESOLUTIONS = Field("1024x1024", description="Image res")
    guidance_scale: float | None = Field(
        5, ge=0, le=10, description="Guidance scale for generation"
    )
    inference_steps: int | None = Field(
        50, ge=5, le=75, description="Number of inference steps", alias="num_inference_steps"
    )


class HidreamEditRequest(BaseModel):
    """Request model for HiDream image editing"""
    
    model_config = {"populate_by_name": True, "use_enum_values": True}

    seed: int | None = Field(
        None, ge=0, le=100000000, description="Random seed for generation"
    )
    prompt: str = Field(..., min_length=1, description="Text prompt for image editing")
    image_b64: str = Field(..., min_length=1, description="Base64 encoded input image")
    guidance_scale: float | None = Field(
        5, ge=0, le=10, description="Guidance scale for generation"
    )
    negative_prompt: str | None = Field("low res, blur", description="Negative prompt")
    inference_steps: int | None = Field(
        28, ge=5, le=75, description="Number of inference steps", alias="num_inference_steps"
    )
    image_guidance_scale: float | None = Field(
        4, ge=0, le=10, description="Image guidance scale"
    )


class HidreamResponse(BaseModel):
    """Response model for HiDream API calls"""

    success: bool = Field(default=True)
    model_used: str = Field(..., description="Model that was used")
    image_url: str | None = Field(None, description="Generated image URL")
    image_data: str | None = Field(None, description="Base64 encoded image data")
    error_message: str | None = Field(None, description="Error message if failed")
    generation_time: float | None = Field(
        None, description="Time taken to generate in seconds"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )


class HidreamError(Exception):
    """Custom exception for HiDream API errors"""


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
        safe_ext = re.sub(r"[^\w]", "", ext)
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


def parse_aspect_ratio_hidream(ar: str) -> str:
    """
    Parse an aspect ratio string and return closest HiDream predefined resolution.

    Args:
        ar: Aspect ratio string in format 'WIDTH:HEIGHT' (e.g., '16:9', '1:1', '4:3')

    Returns:
        Closest HiDream resolution string (e.g., '1024x1024')

    Raises:
        ValueError: If aspect ratio format is invalid
    """
    if not ar or not isinstance(ar, str):
        raise ValueError("Aspect ratio must be a non-empty string")
    
    ar = ar.strip()
    if ':' not in ar:
        raise ValueError("Aspect ratio must be in format 'WIDTH:HEIGHT' (e.g., '16:9', '1:1')")
    
    try:
        ratio_width_str, ratio_height_str = ar.split(':', 1)
        ratio_width = float(ratio_width_str.strip())
        ratio_height = float(ratio_height_str.strip())
    except ValueError as e:
        raise ValueError(f"Invalid aspect ratio format '{ar}': width and height must be numbers") from e
    
    if ratio_width <= 0 or ratio_height <= 0:
        raise ValueError(f"Aspect ratio values must be positive: {ratio_width}:{ratio_height}")
    
    # Calculate target aspect ratio
    target_aspect = ratio_width / ratio_height
    
    # Available HiDream resolutions with their aspect ratios
    # NOTE: HiDream API format is HEIGHTxWIDTH, not WIDTHxHEIGHT
    # So "768x1360" means height=768, width=1360 → actual image is 1360×768 (landscape)
    resolutions = [
        ("1024x1024", 1.0),          # Square (1024×1024)
        ("1360x768", 768/1360),      # Portrait (768×1360) 
        ("768x1360", 1360/768),      # Landscape (1360×768)
        ("1168x880", 880/1168),      # Portrait (880×1168)
        ("880x1168", 1168/880),      # Landscape (1168×880)
        ("832x1248", 1248/832),      # Landscape (1248×832)
        ("1248x832", 832/1248),      # Portrait (832×1248)
    ]
    
    # Find the resolution with closest aspect ratio
    best_resolution = "1024x1024"  # Default fallback
    best_diff = float('inf')
    
    for resolution, aspect in resolutions:
        diff = abs(aspect - target_aspect)
        if diff < best_diff:
            best_diff = diff
            best_resolution = resolution
    
    return best_resolution


def detect_image_format(image_data: bytes) -> str:
    """
    Detect image format from binary data.

    Args:
        image_data: Binary image data

    Returns:
        Image format extension (e.g., 'png', 'jpg')
    """
    try:
        with BytesIO(image_data) as img_buffer:
            img = Image.open(img_buffer)
            format_lower = img.format.lower() if img.format else "png"
            # Map common formats
            format_map = {"jpeg": "jpg", "webp": "webp", "png": "png", "gif": "gif"}
            return format_map.get(format_lower, "png")
    except Exception:
        return "png"


class HidreamClient:
    """
    HiDream API client for text-to-image generation and image editing.

    Supports both sync and async operations with comprehensive error handling.
    """

    def __init__(self, api_key: str | None = None, timeout: int = DEFAULT_TIMEOUT):
        """
        Initialize HiDream client.

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

        logger.info(f"HidreamClient initialized with timeout={timeout}s")

    @property
    def available_models(self) -> list[str]:
        """Get list of available model names."""
        return list(HIDREAM_MODEL_REGISTRY.keys())

    def get_model_info(self, model_name: str) -> ModelInfo | None:
        """
        Get information about a specific model.

        Args:
            model_name: Name of the model

        Returns:
            ModelInfo object or None if model not found
        """
        return HIDREAM_MODEL_REGISTRY.get(model_name)

    def list_models(self, category: str | None = None) -> list[ModelInfo]:
        """
        List available models, optionally filtered by category.

        Args:
            category: Filter by model category

        Returns:
            List of ModelInfo objects
        """
        models = list(HIDREAM_MODEL_REGISTRY.values())
        if category:
            models = [m for m in models if m.category == category]
        return models

    @retry(
        stop=stop_after_attempt(MAX_RETRIES),
        wait=wait_exponential(multiplier=1, min=2, max=8),
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
    def _make_request_sync(self, url: str, data: dict[str, Any]) -> dict[str, Any]:
        """
        Make HTTP request with retry logic (sync version).

        Args:
            url: API endpoint URL
            data: Request payload

        Returns:
            Response JSON data

        Raises:
            HidreamError: On API errors
        """
        try:
            logger.debug(f"Making sync request to {url}")
            logger.debug(f"Request headers: {self.headers}")
            logger.debug(f"Request payload: {data}")

            response = requests.post(
                url, headers=self.headers, json=data, timeout=self.timeout
            )

            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response headers: {dict(response.headers)}")


            response.raise_for_status()

            # Check if response is binary image data or JSON
            content_type = response.headers.get("content-type", "").lower()
            logger.debug(f"Response content type: {content_type}")

            if content_type.startswith("image/"):
                # Direct image response - convert to base64 and return structured response
                logger.debug("Received direct image response")
                image_b64 = base64.b64encode(response.content).decode("utf-8")
                result = {
                    "success": True,
                    "image_data": image_b64,
                    "image_url": None,
                    "content_type": content_type,
                }
                logger.debug(
                    f"Created structured response from image data (size: {len(response.content)} bytes)"
                )
                return result
            else:
                # JSON response
                if not raw_content.strip():
                    raise ValueError("Empty response body")

                try:
                    result = response.json()
                    logger.debug(f"Parsed JSON response: {result}")
                    return result
                except json.JSONDecodeError as json_err:
                    logger.error(f"JSON decode error: {json_err}")
                    logger.error(f"Response content type: {content_type}")
                    logger.error(f"Full response content: {raw_content}")
                    raise ValueError(
                        f"Invalid JSON response: {json_err}. Content: {raw_content[:200]}..."
                    )

        except requests.exceptions.RequestException as e:
            error_msg = f"Request failed: {str(e)}"
            logger.error(error_msg)
            logger.error(f"Request URL: {url}")
            logger.error(f"Request timeout: {self.timeout}s")
            raise HidreamError(error_msg) from e
        except ValueError as e:
            error_msg = f"Response parsing failed: {str(e)}"
            logger.error(error_msg)
            raise HidreamError(error_msg) from e

    async def _make_request_async(
        self, url: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Make HTTP request asynchronously.

        Args:
            url: API endpoint URL
            data: Request payload

        Returns:
            Response JSON data

        Raises:
            HidreamError: On API errors
        """
        try:
            logger.debug(f"Making async request to {url}")
            logger.debug(f"Request headers: {self.headers}")
            logger.debug(f"Request payload: {data}")

            timeout = aiohttp.ClientTimeout(total=self.timeout)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(
                    url, headers=self.headers, json=data
                ) as response:
                    logger.debug(f"Response status: {response.status}")
                    logger.debug(f"Response headers: {dict(response.headers)}")

                    # Log raw response content for debugging
                    raw_content = await response.text()
                    logger.debug(
                        f"Raw response content: {raw_content[:500]}{'...' if len(raw_content) > 500 else ''}"
                    )

                    response.raise_for_status()

                    # Check if response is binary image data or JSON
                    content_type = response.headers.get("content-type", "").lower()
                    logger.debug(f"Response content type: {content_type}")

                    if content_type.startswith("image/"):
                        # Direct image response - convert to base64 and return structured response
                        logger.debug("Received direct image response")
                        image_bytes = await response.read()
                        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
                        result = {
                            "success": True,
                            "image_data": image_b64,
                            "image_url": None,
                            "content_type": content_type,
                        }
                        logger.debug(
                            f"Created structured response from image data (size: {len(image_bytes)} bytes)"
                        )
                        return result
                    else:
                        # JSON response
                        if not raw_content.strip():
                            raise ValueError("Empty response body")

                        try:
                            result = await response.json()
                            logger.debug(f"Parsed JSON response: {result}")
                            return result
                        except json.JSONDecodeError as json_err:
                            logger.error(f"JSON decode error: {json_err}")
                            logger.error(f"Response content type: {content_type}")
                            logger.error(f"Full response content: {raw_content}")
                            raise ValueError(
                                f"Invalid JSON response: {json_err}. Content: {raw_content[:200]}..."
                            )

        except aiohttp.ClientError as e:
            error_msg = f"Async request failed: {str(e)}"
            logger.error(error_msg)
            logger.error(f"Request URL: {url}")
            logger.error(f"Request timeout: {self.timeout}s")
            raise HidreamError(error_msg) from e
        except ValueError as e:
            error_msg = f"Response parsing failed: {str(e)}"
            logger.error(error_msg)
            raise HidreamError(error_msg) from e

    def generate_sync(
        self,
        prompt: str,
        seed: int | None = None,
        res: str = "1024x1024",
        guidance_scale: float = 5.0,
        inference_steps: int = 50,
    ) -> HidreamResponse:
        """
        Generate image from text prompt synchronously.

        Args:
            prompt: Text description of desired image
            seed: Random seed for reproducible results
            res: Image res (default: "1024x1024")
            guidance_scale: How closely to follow the prompt (0-10, default: 5)
            inference_steps: Number of denoising steps (5-75, default: 50)

        Returns:
            HidreamResponse with generated image information
        """
        request_data = HidreamGenerateRequest(
            seed=seed,
            prompt=prompt,
            resolution=res,
            guidance_scale=guidance_scale,
            inference_steps=inference_steps,
        )

        logger.info(
            f"Generating HiDream image",
            extra={
                "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
                "res": res,
                "guidance_scale": guidance_scale,
                "steps": inference_steps,
            },
        )

        try:
            start_time = time.time()
            response_data = self._make_request_sync(
                HIDREAM_GENERATE_URL, request_data.model_dump(by_alias=True)
            )
            generation_time = time.time() - start_time

            return HidreamResponse(
                model_used="hidream-v1",
                generation_time=generation_time,
                metadata={"request_params": request_data.model_dump(by_alias=True)},
                **response_data,
            )
        except Exception as e:
            error_msg = f"HiDream generation failed: {str(e)}"
            logger.error(error_msg)
            return HidreamResponse(
                success=False, model_used="hidream-v1", error_message=error_msg
            )

    # Keep generate for backward compatibility
    def generate(self, *args, **kwargs) -> HidreamResponse:
        """Generate image (backward compatibility alias for generate_sync)."""
        return self.generate_sync(*args, **kwargs)

    async def generate_async(
        self,
        prompt: str,
        seed: int | None = None,
        res: str = "1024x1024",
        guidance_scale: float = 5.0,
        inference_steps: int = 50,
    ) -> HidreamResponse:
        """
        Generate image from text prompt asynchronously.

        Args:
            prompt: Text description of desired image
            seed: Random seed for reproducible results
            res: Image res (default: "1024x1024")
            guidance_scale: How closely to follow the prompt (0-10, default: 5)
            inference_steps: Number of denoising steps (5-75, default: 50)

        Returns:
            HidreamResponse with generated image information
        """
        request_data = HidreamGenerateRequest(
            seed=seed,
            prompt=prompt,
            resolution=res,
            guidance_scale=guidance_scale,
            inference_steps=inference_steps,
        )

        logger.info(
            f"Generating HiDream image async",
            extra={
                "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
                "res": res,
                "guidance_scale": guidance_scale,
                "steps": inference_steps,
            },
        )

        try:
            start_time = time.time()
            response_data = await self._make_request_async(
                HIDREAM_GENERATE_URL, request_data.model_dump(by_alias=True)
            )
            generation_time = time.time() - start_time

            return HidreamResponse(
                model_used="hidream-v1",
                generation_time=generation_time,
                metadata={"request_params": request_data.model_dump(by_alias=True)},
                **response_data,
            )
        except Exception as e:
            error_msg = f"HiDream async generation failed: {str(e)}"
            logger.error(error_msg)
            return HidreamResponse(
                success=False, model_used="hidream-v1", error_message=error_msg
            )

    def edit_sync(
        self,
        prompt: str,
        image_path: str | Path | BytesIO,
        seed: int | None = None,
        guidance_scale: float = 5.0,
        negative_prompt: str = "low res, blur",
        inference_steps: int = 28,
        image_guidance_scale: float = 4.0,
    ) -> HidreamResponse:
        """
        Edit existing image using text prompt synchronously.

        Args:
            prompt: Text description of desired changes
            image_path: Path to input image or BytesIO object
            seed: Random seed for reproducible results
            guidance_scale: How closely to follow the prompt (0-10, default: 5)
            negative_prompt: What to avoid in the image
            inference_steps: Number of denoising steps (5-75, default: 28)
            image_guidance_scale: How much to preserve original image (0-10, default: 4)

        Returns:
            HidreamResponse with edited image information
        """
        # Convert image to base64
        try:
            if isinstance(image_path, (str, Path)):
                with open(image_path, "rb") as f:
                    image_bytes = f.read()
            elif isinstance(image_path, BytesIO):
                image_bytes = image_path.getvalue()
            else:
                raise ValueError("image_path must be a file path or BytesIO object")

            image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        except Exception as e:
            logger.error(f"Failed to process input image: {str(e)}")
            return HidreamResponse(
                success=False,
                model_used="hidream-edit",
                error_message=f"Image processing failed: {str(e)}",
            )

        request_data = HidreamEditRequest(
            seed=seed,
            prompt=prompt,
            image_b64=image_b64,
            guidance_scale=guidance_scale,
            negative_prompt=negative_prompt,
            inference_steps=inference_steps,
            image_guidance_scale=image_guidance_scale,
        )

        logger.info(
            f"Editing HiDream image",
            extra={
                "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
                "guidance_scale": guidance_scale,
                "image_guidance_scale": image_guidance_scale,
                "steps": inference_steps,
            },
        )

        try:
            start_time = time.time()
            response_data = self._make_request_sync(
                HIDREAM_EDIT_URL, request_data.model_dump(by_alias=True)
            )
            generation_time = time.time() - start_time

            return HidreamResponse(
                model_used="hidream-edit",
                generation_time=generation_time,
                metadata={"request_params": request_data.model_dump(by_alias=True)},
                **response_data,
            )
        except Exception as e:
            error_msg = f"HiDream edit failed: {str(e)}"
            logger.error(error_msg)
            return HidreamResponse(
                success=False, model_used="hidream-edit", error_message=error_msg
            )

    # Keep edit for backward compatibility
    def edit(self, *args, **kwargs) -> HidreamResponse:
        """Edit image (backward compatibility alias for edit_sync)."""
        return self.edit_sync(*args, **kwargs)

    async def edit_async(
        self,
        prompt: str,
        image_path: str | Path | BytesIO,
        seed: int | None = None,
        guidance_scale: float = 5.0,
        negative_prompt: str = "low res, blur",
        inference_steps: int = 28,
        image_guidance_scale: float = 4.0,
    ) -> HidreamResponse:
        """
        Edit existing image using text prompt asynchronously.

        Args:
            prompt: Text description of desired changes
            image_path: Path to input image or BytesIO object
            seed: Random seed for reproducible results
            guidance_scale: How closely to follow the prompt (0-10, default: 5)
            negative_prompt: What to avoid in the image
            inference_steps: Number of denoising steps (5-75, default: 28)
            image_guidance_scale: How much to preserve original image (0-10, default: 4)

        Returns:
            HidreamResponse with edited image information
        """
        # Convert image to base64
        try:
            if isinstance(image_path, (str, Path)):
                with open(image_path, "rb") as f:
                    image_bytes = f.read()
            elif isinstance(image_path, BytesIO):
                image_bytes = image_path.getvalue()
            else:
                raise ValueError("image_path must be a file path or BytesIO object")

            image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        except Exception as e:
            logger.error(f"Failed to process input image: {str(e)}")
            return HidreamResponse(
                success=False,
                model_used="hidream-edit",
                error_message=f"Image processing failed: {str(e)}",
            )

        request_data = HidreamEditRequest(
            seed=seed,
            prompt=prompt,
            image_b64=image_b64,
            guidance_scale=guidance_scale,
            negative_prompt=negative_prompt,
            inference_steps=inference_steps,
            image_guidance_scale=image_guidance_scale,
        )

        logger.info(
            f"Editing HiDream image async",
            extra={
                "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
                "guidance_scale": guidance_scale,
                "image_guidance_scale": image_guidance_scale,
                "steps": inference_steps,
            },
        )

        try:
            start_time = time.time()
            response_data = await self._make_request_async(
                HIDREAM_EDIT_URL, request_data.model_dump(by_alias=True)
            )
            generation_time = time.time() - start_time

            return HidreamResponse(
                model_used="hidream-edit",
                generation_time=generation_time,
                metadata={"request_params": request_data.model_dump(by_alias=True)},
                **response_data,
            )
        except Exception as e:
            error_msg = f"HiDream async edit failed: {str(e)}"
            logger.error(error_msg)
            return HidreamResponse(
                success=False, model_used="hidream-edit", error_message=error_msg
            )

    def _generate_with_retries(self, **kwargs) -> HidreamResponse:
        """Wrapper that handles final failure after retries are exhausted."""
        try:
            return self.generate_sync(**kwargs)
        except Exception as e:
            # Final failure after all retries exhausted
            prompt = kwargs.get("prompt", "")

            error_context = {
                "model": "hidream-v1",
                "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
                "parameters": {
                    "res": kwargs.get("res", "1024x1024"),
                    "guidance_scale": kwargs.get("guidance_scale", 5.0),
                    "inference_steps": kwargs.get("inference_steps", 50),
                    "seed": kwargs.get("seed"),
                },
                "attempts": MAX_RETRIES,
                "api_url": HIDREAM_GENERATE_URL,
            }

            error_msg = (
                f"HiDream generation failed after {MAX_RETRIES} attempts: {str(e)}"
            )
            logger.error(
                error_msg,
                extra={
                    "error_context": error_context,
                    "error_type": type(e).__name__,
                    "final_failure": True,
                },
            )

            return HidreamResponse(
                success=False,
                model_used="hidream-v1",
                error_message=error_msg,
                metadata={
                    "error_context": error_context,
                    "retry_attempts": MAX_RETRIES,
                },
            )

    def _edit_with_retries(self, **kwargs) -> HidreamResponse:
        """Wrapper that handles final failure after retries are exhausted."""
        try:
            return self.edit_sync(**kwargs)
        except Exception as e:
            # Final failure after all retries exhausted
            prompt = kwargs.get("prompt", "")

            error_context = {
                "model": "hidream-edit",
                "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
                "parameters": {
                    "guidance_scale": kwargs.get("guidance_scale", 5.0),
                    "inference_steps": kwargs.get("inference_steps", 28),
                    "image_guidance_scale": kwargs.get("image_guidance_scale", 4.0),
                    "seed": kwargs.get("seed"),
                },
                "attempts": MAX_RETRIES,
                "api_url": HIDREAM_EDIT_URL,
            }

            error_msg = f"HiDream edit failed after {MAX_RETRIES} attempts: {str(e)}"
            logger.error(
                error_msg,
                extra={
                    "error_context": error_context,
                    "error_type": type(e).__name__,
                    "final_failure": True,
                },
            )

            return HidreamResponse(
                success=False,
                model_used="hidream-edit",
                error_message=error_msg,
                metadata={
                    "error_context": error_context,
                    "retry_attempts": MAX_RETRIES,
                },
            )


class HidreamCLI:
    """Command-line interface for HiDream API client."""

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

        self.client = HidreamClient(api_key=api_key)

    def image(
        self,
        prompt: str,
        output: str | None = None,
        seed: int | None = None,
        res: str = "1024x1024",
        guidance_scale: float = 5.0,
        inference_steps: int = 50,
        verbose: bool = False,
        ar: str | None = None,
    ):
        """
        Generate image from text prompt.

        Args:
            prompt: Text description of desired image
            output: Output file path (optional)
            seed: Random seed for reproducible results
            res: Image resolution (default: "1024x1024")
            guidance_scale: How closely to follow the prompt (0-10, default: 5)
            inference_steps: Number of denoising steps (5-75, default: 50)
            verbose: Enable verbose debug logging
            ar: Aspect ratio in format 'WIDTH:HEIGHT' (e.g., '16:9', '1:1'). Finds closest HiDream resolution. Overrides res if specified.
        """
        if verbose:
            logger.remove()
            logger.add(lambda msg: print(msg, end=""), colorize=True, level="DEBUG")
        
        # Handle aspect ratio parameter - overrides res if specified
        if ar is not None:
            try:
                res = parse_aspect_ratio_hidream(ar)
                # Extract actual dimensions from HiDream API format (HEIGHTxWIDTH)
                height, width = res.split('x')
                logger.info(f"Aspect ratio parameter '{ar}' mapped to HiDream resolution {res} → generates {width}×{height} image")
            except ValueError as e:
                print(f"❌ Invalid aspect ratio format '{ar}': {e}")
                return
        
        response = self.client.generate(
            prompt=prompt,
            seed=seed,
            res=res,
            guidance_scale=guidance_scale,
            inference_steps=inference_steps,
        )

        if response.success:
            print(f"✅ Generation successful!")
            if response.image_url:
                print(f"📎 Image URL: {response.image_url}")
            
            # Save image if we have image data
            if response.image_data:
                import base64
                
                try:
                    image_bytes = base64.b64decode(response.image_data)
                    image_format = detect_image_format(image_bytes)
                    
                    # Determine final output path
                    if output:
                        final_output_path = Path(output)
                    else:
                        # Auto-generate filename from prompt
                        prompt_slug_name = prompt_slug(prompt)
                        filename = f"{prompt_slug_name}.{image_format}"
                        final_output_path = Path.cwd() / filename
                    
                    # Ensure directory exists
                    final_output_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Save image
                    with open(final_output_path, "wb") as f:
                        f.write(image_bytes)
                    print(f"💾 Image saved to: {final_output_path}")
                    
                except Exception as e:
                    print(f"⚠️  Failed to save image: {e}")
        else:
            print(f"❌ Generation failed: {response.error_message}")

    def edit(
        self,
        image: str,
        prompt: str,
        output: str | None = None,
        seed: int | None = None,
        guidance_scale: float = 5.0,
        negative_prompt: str = "low res, blur",
        inference_steps: int = 28,
        image_guidance_scale: float = 4.0,
        verbose: bool = False,
    ):
        """
        Edit existing image using text prompt.

        Args:
            image: Path to input image
            prompt: Text description of desired changes
            output: Output file path (optional)
            seed: Random seed for reproducible results
            guidance_scale: How closely to follow the prompt (0-10, default: 5)
            negative_prompt: What to avoid in the image
            inference_steps: Number of denoising steps (5-75, default: 28)
            image_guidance_scale: How much to preserve original image (0-10, default: 4)
            verbose: Enable verbose debug logging
        """
        if verbose:
            logger.remove()
            logger.add(lambda msg: print(msg, end=""), colorize=True, level="DEBUG")
        response = self.client.edit(
            prompt=prompt,
            image_path=image,
            seed=seed,
            guidance_scale=guidance_scale,
            negative_prompt=negative_prompt,
            inference_steps=inference_steps,
            image_guidance_scale=image_guidance_scale,
        )

        if response.success:
            print(f"✅ Edit successful!")
            if response.image_url:
                print(f"📎 Image URL: {response.image_url}")
            
            # Save image if we have image data
            if response.image_data:
                import base64
                
                try:
                    image_bytes = base64.b64decode(response.image_data)
                    image_format = detect_image_format(image_bytes)
                    
                    # Determine final output path
                    if output:
                        final_output_path = Path(output)
                    else:
                        # Auto-generate filename from prompt
                        prompt_slug_name = prompt_slug(prompt)
                        filename = f"{prompt_slug_name}_edited.{image_format}"
                        final_output_path = Path.cwd() / filename
                    
                    # Ensure directory exists
                    final_output_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Save image
                    with open(final_output_path, "wb") as f:
                        f.write(image_bytes)
                    print(f"💾 Image saved to: {final_output_path}")
                    
                except Exception as e:
                    print(f"⚠️  Failed to save image: {e}")
        else:
            print(f"❌ Edit failed: {response.error_message}")

    def resolutions(self):
        """List available resolutions."""
        print("Available HiDream resolutions:")
        resolutions = [
            "1024x1024",
            "768x1360",
            "1360x768",
            "880x1168",
            "1168x880",
            "1248x832",
            "832x1248",
        ]
        for res in resolutions:
            # Add aspect ratio info
            width, height = map(int, res.split("x"))
            aspect = width / height
            if aspect == 1.0:
                aspect_desc = "(square)"
            elif aspect > 1.0:
                aspect_desc = "(landscape)"
            else:
                aspect_desc = "(portrait)"
            print(f"  • {res} {aspect_desc}")

    def list(self, category: str | None = None):
        """
        List available HiDream models.

        Args:
            category: Filter by category (optional)
        """
        models = self.client.list_models(category=category)

        if category:
            print(f"HiDream models in category '{category}':")
        else:
            print("Available HiDream models:")

        # Group by category
        by_category = {}
        for model in models:
            if model.category not in by_category:
                by_category[model.category] = []
            by_category[model.category].append(model)

        for cat, cat_models in sorted(by_category.items()):
            print(f"\n📁 {cat.title()}:")
            for model in sorted(cat_models, key=lambda x: x.display_name):
                desc = f" - {model.description}" if model.description else ""
                edit_support = " (editing supported)" if model.supports_editing else ""
                print(f"  • {model.name} ({model.display_name}){desc}{edit_support}")

    def categories(self):
        """List available HiDream model categories."""
        categories = {model.category for model in HIDREAM_MODEL_REGISTRY.values()}
        print("Available HiDream categories:")
        for category in sorted(categories):
            count = len(
                [m for m in HIDREAM_MODEL_REGISTRY.values() if m.category == category]
            )
            print(f"  • {category} ({count} models)")

    def info(self, model: str):
        """
        Show information about a specific HiDream model.

        Args:
            model: Model name
        """
        model_info = self.client.get_model_info(model)
        if model_info:
            print(f"Model: {model_info.name}")
            print(f"Display Name: {model_info.display_name}")
            print(f"Category: {model_info.category}")
            if model_info.description:
                print(f"Description: {model_info.description}")
            print(f"Supports Editing: {model_info.supports_editing}")
            print(f"Default Resolution: {model_info.default_resolution}")
            print(f"Default Steps: {model_info.default_steps}")
            print(f"Step Range: {model_info.min_steps}-{model_info.max_steps}")
        else:
            print(f"❌ Model '{model}' not found")
            print("\n💡 Use 'list' command to see available models")


def main():
    """Main CLI entry point."""
    fire.Fire(HidreamCLI)


if __name__ == "__main__":
    main()
