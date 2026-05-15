#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["aiohttp", "requests", "pydantic", "fire", "tenacity", "loguru", "python-dotenv", "asyncio", "python-slugify", "pathvalidate", "pillow"]
# ///
# this_file: chutes_image.py

"""
Chutes AI General Image Generation Client

Unified Python client for multiple image generation models via Chutes AI.
Supports both sync and async operations with comprehensive model registry.
"""

import os
import json
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any
from collections.abc import AsyncIterator

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
import io

# Load environment variables
load_dotenv()

# Constants
DEFAULT_API_KEY = os.getenv("CHUTES_API_KEY")
CHUTES_IMAGE_URL = "https://image.chutes.ai/generate"
DEFAULT_TIMEOUT = 120
MAX_RETRIES = 3
MAX_CONCURRENT_MODELS = 8


class ImageGenerationRequest(BaseModel):
    """Request model for general image generation"""

    model: str = Field(..., min_length=1, description="Model identifier")
    prompt: str = Field(
        ..., min_length=1, description="Text prompt for image generation"
    )
    negative_prompt: str | None = Field("", description="Negative prompt")
    guidance_scale: float | None = Field(
        7.5, ge=1, le=20, description="Guidance scale for generation"
    )
    width: int | None = Field(1024, ge=128, le=2048, description="Image width")
    height: int | None = Field(1024, ge=128, le=2048, description="Image height")
    inference_steps: int | None = Field(
        30, ge=1, le=100, description="Number of inference steps"
    )
    seed: int | None = Field(
        None, ge=0, le=4294967295, description="Random seed for generation"
    )


class ImageGenerationResponse(BaseModel):
    """Response model for image generation"""

    success: bool = Field(default=True)
    model_used: str = Field(..., description="Model that was used")
    image_url: str | None = Field(None, description="Generated image URL")
    image_data: str | None = Field(None, description="Base64 encoded image data")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Generation metadata"
    )
    error_message: str | None = Field(None, description="Error message if failed")
    generation_time: float | None = Field(
        None, description="Time taken to generate in seconds"
    )


class ModelInfo(BaseModel):
    """Information about an available model"""

    name: str = Field(..., description="Model identifier")
    display_name: str = Field(..., description="Human-readable model name")
    description: str | None = Field("", description="Model description")
    category: str | None = Field("general", description="Model category")
    supports_negative_prompt: bool = Field(
        True, description="Whether model supports negative prompts"
    )
    max_width: int = Field(2048, description="Maximum image width")
    max_height: int = Field(2048, description="Maximum image height")
    default_steps: int = Field(25, description="Default inference steps")


class ImageGenerationError(Exception):
    """Custom exception for image generation errors"""


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


def parse_resolution(res: str) -> tuple[int, int]:
    """
    Parse a resolution string like '1920x1080' into width and height.

    Args:
        res: Resolution string in format 'WIDTHxHEIGHT' (e.g., '1920x1080', '512x512')

    Returns:
        Tuple of (width, height) as integers

    Raises:
        ValueError: If resolution format is invalid or values are out of range
    """
    if not res or not isinstance(res, str):
        raise ValueError("Resolution must be a non-empty string")
    
    # Support both 'x' and 'X' as separators
    res = res.strip().lower()
    if 'x' not in res:
        raise ValueError("Resolution must be in format 'WIDTHxHEIGHT' (e.g., '1920x1080')")
    
    try:
        width_str, height_str = res.split('x', 1)
        width = int(width_str.strip())
        height = int(height_str.strip())
    except ValueError as e:
        raise ValueError(f"Invalid resolution format '{res}': width and height must be integers") from e
    
    # Validate range (same as ImageGenerationRequest model)
    if not (128 <= width <= 2048):
        raise ValueError(f"Width {width} out of range (128-2048)")
    if not (128 <= height <= 2048):
        raise ValueError(f"Height {height} out of range (128-2048)")
    
    return width, height


def parse_aspect_ratio(ar: str, max_width: int = 2048, max_height: int = 2048) -> tuple[int, int]:
    """
    Parse an aspect ratio string like '16:9' and return largest possible resolution.

    Args:
        ar: Aspect ratio string in format 'WIDTH:HEIGHT' (e.g., '16:9', '1:1', '4:3')
        max_width: Maximum allowed width (default: 2048)
        max_height: Maximum allowed height (default: 2048)

    Returns:
        Tuple of (width, height) as integers for the largest possible resolution

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
    
    # Calculate aspect ratio
    aspect = ratio_width / ratio_height
    
    # Find largest possible resolution that fits within constraints
    if aspect >= 1.0:
        # Landscape or square - width is limiting factor
        width = min(max_width, 2048)
        height = int(width / aspect)
        
        # Ensure height doesn't exceed limits
        if height > max_height or height > 2048:
            height = min(max_height, 2048)
            width = int(height * aspect)
    else:
        # Portrait - height is limiting factor
        height = min(max_height, 2048)
        width = int(height * aspect)
        
        # Ensure width doesn't exceed limits
        if width > max_width or width > 2048:
            width = min(max_width, 2048)
            height = int(width / aspect)
    
    # Ensure minimum sizes
    width = max(128, width)
    height = max(128, height)
    
    # Round to multiples of 8 for better model compatibility
    width = (width // 8) * 8
    height = (height // 8) * 8
    
    return width, height


def detect_image_format(image_data: bytes) -> str:
    """
    Detect image format from binary data.

    Args:
        image_data: Binary image data

    Returns:
        Image format extension (e.g., 'png', 'jpg')
    """
    try:
        with io.BytesIO(image_data) as img_buffer:
            img = Image.open(img_buffer)
            format_lower = img.format.lower() if img.format else "png"
            # Map common formats
            format_map = {"jpeg": "jpg", "webp": "webp", "png": "png", "gif": "gif"}
            return format_map.get(format_lower, "png")
    except Exception:
        return "png"


# Comprehensive model registry based on analysis
MODEL_REGISTRY = {
    # Character Models
    "diagonalge/Booba": ModelInfo(
        name="diagonalge/Booba",
        display_name="Booba",
        description="Specialized character generation model",
        category="character",
        supports_negative_prompt=True,
        max_width=2048,
        max_height=2048,
        default_steps=30,
    ),
    
    # General Models
    "FLUX.1-dev": ModelInfo(
        name="FLUX.1-dev",
        display_name="FLUX.1 Dev",
        description="High-quality text-to-image generation model",
        category="general",
        supports_negative_prompt=True,
        max_width=2048,
        max_height=2048,
        default_steps=50,
    ),
    "Qwen/Qwen-Image": ModelInfo(
        name="Qwen/Qwen-Image",
        display_name="Qwen Image",
        description="Advanced Qwen image generation model",
        category="general",
        supports_negative_prompt=True,
        max_width=2048,
        max_height=2048,
        default_steps=50,
    ),
    "qwen-image": ModelInfo(
        name="qwen-image",
        display_name="Qwen Image (Simple)",
        description="Simplified Qwen image generation",
        category="general",
        supports_negative_prompt=True,
        max_width=2048,
        max_height=2048,
        default_steps=50,
    ),
    "playground-v2.5": ModelInfo(
        name="playground-v2.5",
        display_name="Playground v2.5",
        description="Versatile playground model",
        category="general",
        supports_negative_prompt=True,
        max_width=2048,
        max_height=2048,
        default_steps=50,
    ),
    "Shitao/OmniGen-v1": ModelInfo(
        name="Shitao/OmniGen-v1",
        display_name="OmniGen v1",
        description="Omnipotent generation model",
        category="general",
        supports_negative_prompt=True,
        max_width=2048,
        max_height=2048,
        default_steps=50,
    ),
    
    # Anime Models
    "Animij": ModelInfo(
        name="Animij",
        display_name="Animij",
        description="Anime-style image generation",
        category="anime",
        supports_negative_prompt=True,
        max_width=2048,
        max_height=2048,
        default_steps=50,
    ),
    "HassakuXL": ModelInfo(
        name="HassakuXL",
        display_name="Hassaku XL",
        description="High-quality anime generation",
        category="anime",
        supports_negative_prompt=True,
        max_width=2048,
        max_height=2048,
        default_steps=50,
    ),
    "Illustrious-XL": ModelInfo(
        name="Illustrious-XL",
        display_name="Illustrious XL",
        description="High-resolution anime illustration",
        category="anime",
        supports_negative_prompt=True,
        max_width=2048,
        max_height=2048,
        default_steps=50,
    ),
    "Ilustrij": ModelInfo(
        name="Ilustrij",
        display_name="Ilustrij",
        description="Illustration-focused anime model",
        category="anime",
        supports_negative_prompt=True,
        max_width=2048,
        max_height=2048,
        default_steps=50,
    ),
    
    # Realistic Models
    "JuggernautXL": ModelInfo(
        name="JuggernautXL",
        display_name="Juggernaut XL",
        description="High-resolution realistic image generation",
        category="realistic",
        supports_negative_prompt=True,
        max_width=2048,
        max_height=2048,
        default_steps=50,
    ),
    
    # Artistic Models
    "chroma": ModelInfo(
        name="chroma",
        display_name="Chroma",
        description="Chromatic artistic generation",
        category="artistic",
        supports_negative_prompt=True,
        max_width=2048,
        max_height=2048,
        default_steps=50,
    ),
    "diagonalge/ConstShaper": ModelInfo(
        name="diagonalge/ConstShaper",
        display_name="ConstShaper",
        description="Constraint-based artistic shaping",
        category="artistic",
        supports_negative_prompt=True,
        max_width=2048,
        max_height=2048,
        default_steps=50,
    ),
    "iLustMix": ModelInfo(
        name="iLustMix",
        display_name="iLustMix",
        description="Mixed artistic style generation",
        category="artistic",
        supports_negative_prompt=True,
        max_width=2048,
        max_height=2048,
        default_steps=50,
    ),
    "Lykon/dreamshaper-xl-1-0": ModelInfo(
        name="Lykon/dreamshaper-xl-1-0",
        display_name="DreamShaper XL",
        description="Versatile XL model for various styles",
        category="artistic",
        supports_negative_prompt=True,
        max_width=2048,
        max_height=2048,
        default_steps=50,
    ),
    
    # Cartoon Models
    "nova-cartoon-xl": ModelInfo(
        name="nova-cartoon-xl",
        display_name="Nova Cartoon XL",
        description="Cartoon-style generation",
        category="cartoon",
        supports_negative_prompt=True,
        max_width=2048,
        max_height=2048,
        default_steps=50,
    ),
    
    # Furry Models
    "NovaFurryXL": ModelInfo(
        name="NovaFurryXL",
        display_name="Nova Furry XL",
        description="Furry character generation",
        category="furry",
        supports_negative_prompt=True,
        max_width=2048,
        max_height=2048,
        default_steps=50,
    ),
    
    # Specialized Models
    "orphic-lora": ModelInfo(
        name="orphic-lora",
        display_name="Orphic LoRA",
        description="LoRA-based specialized model",
        category="specialized",
        supports_negative_prompt=True,
        max_width=2048,
        max_height=2048,
        default_steps=50,
    ),
    "ostris/Flex.1-alpha": ModelInfo(
        name="ostris/Flex.1-alpha",
        display_name="Flex.1 Alpha",
        description="Flexible experimental model",
        category="specialized",
        supports_negative_prompt=True,
        max_width=2048,
        max_height=2048,
        default_steps=50,
    ),
    "neta-lumina": ModelInfo(
        name="neta-lumina",
        display_name="Neta Lumina",
        description="Luminous specialized generation",
        category="specialized",
        supports_negative_prompt=True,
        max_width=2048,
        max_height=2048,
        default_steps=50,
    ),
}


class ChutesImageClient:
    """
    Unified client for Chutes AI image generation.

    Supports multiple models with both sync and async operations.
    """

    def __init__(self, api_key: str | None = None, timeout: int = DEFAULT_TIMEOUT):
        """
        Initialize Chutes Image client.

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

        logger.info(f"ChutesImageClient initialized with timeout={timeout}s")

    @property
    def available_models(self) -> list[str]:
        """Get list of available model names."""
        return list(MODEL_REGISTRY.keys())

    def get_model_info(self, model_name: str) -> ModelInfo | None:
        """
        Get information about a specific model.

        Args:
            model_name: Name of the model

        Returns:
            ModelInfo object or None if model not found
        """
        return MODEL_REGISTRY.get(model_name)

    def list_models(self, category: str | None = None) -> list[ModelInfo]:
        """
        List available models, optionally filtered by category.

        Args:
            category: Filter by model category

        Returns:
            List of ModelInfo objects
        """
        models = list(MODEL_REGISTRY.values())
        if category:
            models = [m for m in models if m.category == category]
        return models

    def _parse_streaming_response(self, response_text: str) -> list[str]:
        """Parse Server-Sent Events response."""
        chunks = []
        for line in response_text.split("\n"):
            line = line.strip()
            if line.startswith("data: "):
                data = line[6:]
                if data == "[DONE]":
                    break
                if data:
                    chunks.append(data)
        return chunks

    @retry(
        stop=stop_after_attempt(MAX_RETRIES),
        wait=wait_exponential(multiplier=2, min=5, max=30),  # Longer delays for server issues
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
    def generate_sync(
        self,
        model: str,
        prompt: str,
        negative_prompt: str = "",
        guidance_scale: float = 7.5,
        width: int = 1024,
        height: int = 1024,
        inference_steps: int = 30,
        seed: int | None = None,
    ) -> ImageGenerationResponse:
        """
        Generate image synchronously.

        Args:
            model: Model identifier
            prompt: Text prompt for image generation
            negative_prompt: Negative prompt (optional)
            guidance_scale: How closely to follow the prompt (1-20, default: 7.5)
            width: Image width (128-2048, default: 1024)
            height: Image height (128-2048, default: 1024)
            inference_steps: Number of inference steps (1-100, default: 30)
            seed: Random seed for reproducible results

        Returns:
            ImageGenerationResponse with generation results
        """
        if model not in MODEL_REGISTRY:
            logger.warning(f"Model {model} not in registry, using anyway")

        request_data = ImageGenerationRequest(
            model=model,
            prompt=prompt,
            negative_prompt=negative_prompt,
            guidance_scale=guidance_scale,
            width=width,
            height=height,
            inference_steps=inference_steps,
            seed=seed,
        )

        logger.info(
            f"Generating image with {model}",
            extra={
                "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
                "resolution": f"{width}x{height}",
                "guidance_scale": guidance_scale,
            },
        )

        try:
            import time

            start_time = time.time()

            # Convert inference_steps to num_inference_steps for API call
            api_data = request_data.model_dump()
            if "inference_steps" in api_data:
                api_data["num_inference_steps"] = api_data.pop("inference_steps")

            response = requests.post(
                CHUTES_IMAGE_URL,
                headers=self.headers,
                json=api_data,
                timeout=self.timeout,
                stream=True,
            )
            response.raise_for_status()

            # Check content type to determine if we're getting text or binary data
            content_type = response.headers.get("content-type", "").lower()

            if "image/" in content_type:
                # Direct image response - collect as bytes and encode as base64
                import base64

                image_bytes = b""
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        image_bytes += chunk

                image_data = base64.b64encode(image_bytes).decode("utf-8")

                return ImageGenerationResponse(
                    success=True,
                    model_used=model,
                    image_data=image_data,
                    generation_time=time.time() - start_time,
                    metadata={
                        "content_type": content_type,
                        "request_params": request_data.model_dump(),
                    },
                )
            else:
                # Text/streaming response
                response_text = ""
                for chunk in response.iter_content(decode_unicode=True):
                    if chunk:
                        # Ensure chunk is string, not bytes
                        if isinstance(chunk, bytes):
                            try:
                                chunk = chunk.decode("utf-8")
                            except UnicodeDecodeError:
                                # If we can't decode, it might be binary data
                                logger.warning(
                                    "Received binary data in text response, treating as base64"
                                )
                                import base64

                                return ImageGenerationResponse(
                                    success=True,
                                    model_used=model,
                                    image_data=base64.b64encode(chunk).decode("utf-8"),
                                    generation_time=time.time() - start_time,
                                    metadata={
                                        "request_params": request_data.model_dump()
                                    },
                                )
                        response_text += chunk

                generation_time = time.time() - start_time

                # Parse streaming response
                chunks = self._parse_streaming_response(response_text)

                # Try to parse the last chunk as JSON or treat as image URL
                image_url = None
                image_data = None

                if chunks:
                    last_chunk = chunks[-1].strip()
                    try:
                        # Try to parse as JSON first
                        result = json.loads(last_chunk)
                        if isinstance(result, dict):
                            image_url = result.get("url")
                            image_data = result.get("image")
                        else:
                            image_url = last_chunk
                    except json.JSONDecodeError:
                        # Treat as direct URL or base64
                        if last_chunk.startswith("http"):
                            image_url = last_chunk
                        else:
                            image_data = last_chunk

                return ImageGenerationResponse(
                    success=True,
                    model_used=model,
                    image_url=image_url,
                    image_data=image_data,
                    generation_time=generation_time,
                    metadata={
                        "chunks_received": len(chunks),
                        "request_params": request_data.model_dump(),
                    },
                )

        except Exception as e:
            # Create detailed error context
            error_context = {
                "model": model,
                "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
                "parameters": {
                    "resolution": f"{width}x{height}",
                    "guidance_scale": guidance_scale,
                    "inference_steps": inference_steps,
                    "seed": seed,
                    "negative_prompt": negative_prompt[:50] + "..."
                    if negative_prompt and len(negative_prompt) > 50
                    else negative_prompt,
                },
                "api_url": CHUTES_IMAGE_URL,
                "timeout": self.timeout,
            }

            error_msg = f"Generation failed with {model}: {str(e)}"
            
            # Log different error types differently
            if isinstance(e, requests.exceptions.HTTPError):
                status_code = getattr(e.response, 'status_code', None)
                if status_code in [503, 500, 502, 504]:
                    logger.warning(f"Server error ({status_code}) for {model}, will retry with longer delay")
                elif status_code == 429:
                    logger.warning(f"Rate limited for {model}, will retry")
                else:
                    logger.error(error_msg, extra={"error_context": error_context, "error_type": type(e).__name__})
            elif isinstance(e, requests.exceptions.Timeout):
                logger.warning(f"Timeout for {model} ({self.timeout}s), consider using fewer concurrent models")
            else:
                logger.error(error_msg, extra={"error_context": error_context, "error_type": type(e).__name__})

            # Re-raise for tenacity to handle retries properly
            raise

    def _generate_with_retries(self, **kwargs) -> ImageGenerationResponse:
        """Wrapper that handles final failure after retries are exhausted."""
        try:
            return self.generate_sync(**kwargs)
        except Exception as e:
            # Final failure after all retries exhausted
            model = kwargs.get("model", "unknown")
            prompt = kwargs.get("prompt", "")

            error_context = {
                "model": model,
                "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
                "parameters": {
                    "resolution": f"{kwargs.get('width', 1024)}x{kwargs.get('height', 1024)}",
                    "guidance_scale": kwargs.get("guidance_scale", 7.5),
                    "inference_steps": kwargs.get("inference_steps", 30),
                    "seed": kwargs.get("seed"),
                    "negative_prompt": kwargs.get("negative_prompt", "")[:50] + "..."
                    if kwargs.get("negative_prompt", "")
                    and len(kwargs.get("negative_prompt", "")) > 50
                    else kwargs.get("negative_prompt", ""),
                },
                "attempts": MAX_RETRIES,
                "api_url": CHUTES_IMAGE_URL,
            }

            # Determine error type for better messaging
            error_type = "Unknown error"
            if isinstance(e, requests.exceptions.HTTPError):
                status_code = getattr(e.response, 'status_code', None)
                if status_code in [503, 500, 502, 504]:
                    error_type = f"Server error ({status_code}) - model may be temporarily unavailable"
                elif status_code == 429:
                    error_type = "Rate limited - too many requests"
                elif status_code == 404:
                    error_type = "Model not found or unavailable"
                else:
                    error_type = f"HTTP error ({status_code})"
            elif isinstance(e, requests.exceptions.Timeout):
                error_type = f"Timeout after {kwargs.get('timeout', DEFAULT_TIMEOUT)}s - model may be overloaded"
            elif isinstance(e, requests.exceptions.ConnectionError):
                error_type = "Connection error - network or API issue"

            error_msg = f"Generation failed after {MAX_RETRIES} attempts with {model}: {error_type}"
            logger.error(
                error_msg,
                extra={
                    "error_context": error_context,
                    "error_type": type(e).__name__,
                    "final_failure": True,
                },
            )

            return ImageGenerationResponse(
                success=False,
                model_used=model,
                error_message=error_msg,
                metadata={
                    "error_context": error_context,
                    "retry_attempts": MAX_RETRIES,
                    "error_type": error_type,
                },
            )

    async def generate_async(
        self,
        model: str,
        prompt: str,
        negative_prompt: str = "",
        guidance_scale: float = 7.5,
        width: int = 1024,
        height: int = 1024,
        inference_steps: int = 30,
        seed: int | None = None,
    ) -> ImageGenerationResponse:
        """
        Generate image asynchronously.

        Args:
            model: Model identifier
            prompt: Text prompt for image generation
            negative_prompt: Negative prompt (optional)
            guidance_scale: How closely to follow the prompt (1-20, default: 7.5)
            width: Image width (128-2048, default: 1024)
            height: Image height (128-2048, default: 1024)
            inference_steps: Number of inference steps (1-100, default: 30)
            seed: Random seed for reproducible results

        Returns:
            ImageGenerationResponse with generation results
        """
        if model not in MODEL_REGISTRY:
            logger.warning(f"Model {model} not in registry, using anyway")

        request_data = ImageGenerationRequest(
            model=model,
            prompt=prompt,
            negative_prompt=negative_prompt,
            guidance_scale=guidance_scale,
            width=width,
            height=height,
            inference_steps=inference_steps,
            seed=seed,
        )

        logger.info(
            f"Generating image async with {model}",
            extra={
                "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
                "resolution": f"{width}x{height}",
                "guidance_scale": guidance_scale,
            },
        )

        try:
            import time

            start_time = time.time()

            # Convert inference_steps to num_inference_steps for API call
            api_data = request_data.model_dump()
            if "inference_steps" in api_data:
                api_data["num_inference_steps"] = api_data.pop("inference_steps")

            timeout = aiohttp.ClientTimeout(total=self.timeout)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(
                    CHUTES_IMAGE_URL, headers=self.headers, json=api_data
                ) as response:
                    response.raise_for_status()

                    # Collect streaming response
                    response_text = ""
                    async for chunk in response.content:
                        if chunk:
                            # Ensure proper decoding
                            if isinstance(chunk, bytes):
                                chunk_str = chunk.decode("utf-8")
                            else:
                                chunk_str = str(chunk)
                            response_text += chunk_str

            generation_time = time.time() - start_time

            # Parse streaming response
            chunks = self._parse_streaming_response(response_text)

            # Try to parse the last chunk as JSON or treat as image URL
            image_url = None
            image_data = None

            if chunks:
                last_chunk = chunks[-1].strip()
                try:
                    # Try to parse as JSON first
                    result = json.loads(last_chunk)
                    if isinstance(result, dict):
                        image_url = result.get("url")
                        image_data = result.get("image")
                    else:
                        image_url = last_chunk
                except json.JSONDecodeError:
                    # Treat as direct URL or base64
                    if last_chunk.startswith("http"):
                        image_url = last_chunk
                    else:
                        image_data = last_chunk

            return ImageGenerationResponse(
                success=True,
                model_used=model,
                image_url=image_url,
                image_data=image_data,
                generation_time=generation_time,
                metadata={
                    "chunks_received": len(chunks),
                    "request_params": request_data.model_dump(),
                },
            )

        except Exception as e:
            error_msg = f"Async generation failed: {str(e)}"
            logger.error(error_msg)
            return ImageGenerationResponse(
                success=False, model_used=model, error_message=error_msg
            )

    async def generate_stream(
        self,
        model: str,
        prompt: str,
        negative_prompt: str = "",
        guidance_scale: float = 7.5,
        width: int = 1024,
        height: int = 1024,
        inference_steps: int = 30,
        seed: int | None = None,
    ) -> AsyncIterator[str]:
        """
        Generate image with streaming updates.

        Args:
            model: Model identifier
            prompt: Text prompt for image generation
            negative_prompt: Negative prompt (optional)
            guidance_scale: How closely to follow the prompt (1-20, default: 7.5)
            width: Image width (128-2048, default: 1024)
            height: Image height (128-2048, default: 1024)
            inference_steps: Number of inference steps (1-100, default: 30)
            seed: Random seed for reproducible results

        Yields:
            Stream chunks as they arrive
        """
        request_data = ImageGenerationRequest(
            model=model,
            prompt=prompt,
            negative_prompt=negative_prompt,
            guidance_scale=guidance_scale,
            width=width,
            height=height,
            inference_steps=inference_steps,
            seed=seed,
        )

        logger.info(f"Starting streaming generation with {model}")

        # Convert inference_steps to num_inference_steps for API call
        api_data = request_data.model_dump()
        if "inference_steps" in api_data:
            api_data["num_inference_steps"] = api_data.pop("inference_steps")

        timeout = aiohttp.ClientTimeout(total=self.timeout)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                CHUTES_IMAGE_URL, headers=self.headers, json=api_data
            ) as response:
                response.raise_for_status()

                buffer = ""
                async for chunk in response.content:
                    if chunk:
                        # Ensure proper decoding
                        if isinstance(chunk, bytes):
                            chunk_str = chunk.decode("utf-8")
                        else:
                            chunk_str = str(chunk)
                        buffer += chunk_str
                        lines = buffer.split("\n")
                        buffer = lines[-1]  # Keep incomplete line

                        for line in lines[:-1]:
                            line = line.strip()
                            if line.startswith("data: "):
                                data = line[6:]
                                if data == "[DONE]":
                                    return
                                if data:
                                    yield data


class ChutesImageCLI:
    """Command-line interface for Chutes Image client."""

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

        self.client = ChutesImageClient(api_key=api_key)

    def image(
        self,
        prompt: str,
        model: str | list[str] = "FLUX.1-dev",
        output: str | None = None,
        negative_prompt: str = "worst quality, low quality, low res, blurry, jpeg artifacts, grainy, watermark, logo, signature, username, extra digits, cropped, out of frame, body out of frame, poorly drawn hands, extra fingers, missing fingers, fused fingers, mutated hands, poorly drawn face, cloned face, disfigured, mutation, malformed limbs, bad anatomy, bad proportions, extra limbs, missing arms, missing legs, long neck, duplicate, ugly, blur, visual noise, boring background, branding, cgi, unreal engine",
        guidance_scale: float = 7.5,
        width: int = 1024,
        height: int = 1024,
        inference_steps: int = 30,
        seed: int | None = None,
        res: str | None = None,
        ar: str | None = None,
    ):
        """
        Generate image from text prompt.

        Args:
            prompt: Text description of desired image
            model: Model to use (default: FLUX.1-dev) or comma-separated list
            output: Output file path or directory (optional)
            negative_prompt: What to avoid in the image
            guidance_scale: How closely to follow the prompt (1-20, default: 7.5)
            width: Image width (128-2048, default: 1024)
            height: Image height (128-2048, default: 1024)
            inference_steps: Number of inference steps (1-100, default: 30)
            seed: Random seed for reproducible results
            res: Resolution in format 'WIDTHxHEIGHT' (e.g., '1920x1080'). Overrides width and height if specified.
            ar: Aspect ratio in format 'WIDTH:HEIGHT' (e.g., '16:9', '1:1'). Calculates largest possible resolution. Overrides width, height, and res if specified.
        """
        # Handle aspect ratio parameter - highest priority, overrides res, width and height
        if ar is not None:
            try:
                width, height = parse_aspect_ratio(ar)
                logger.info(f"Aspect ratio parameter '{ar}' calculated to {width}x{height} (largest possible)")
            except ValueError as e:
                print(f"❌ Invalid aspect ratio format '{ar}': {e}")
                return
        # Handle resolution parameter - overrides width and height if specified (but not ar)
        elif res is not None:
            try:
                width, height = parse_resolution(res)
                logger.info(f"Resolution parameter '{res}' parsed to {width}x{height}")
            except ValueError as e:
                print(f"❌ Invalid resolution format '{res}': {e}")
                return
        
        # Parse models - support both string (comma-separated) and list
        if isinstance(model, str):
            if model.strip() == "*":
                # Use all available models when * is specified
                models = self.client.available_models
                logger.info(f"Using all {len(models)} available models for generation")
            else:
                models = [m.strip() for m in model.split(",") if m.strip()]
        elif hasattr(model, "__iter__") and not isinstance(model, str):
            models = list(model)
        else:
            models = [str(model)]
            
        # Validate models exist in registry
        valid_models = []
        for model_name in models:
            if model_name in self.client.available_models:
                valid_models.append(model_name)
            else:
                print(f"⚠️  Model '{model_name}' not found in registry, skipping")
        
        if not valid_models:
            print("❌ No valid models found")
            return
            
        original_count = len(models)
        models = valid_models
        if len(models) != original_count:
            print(f"ℹ️  Using {len(models)} valid models from {original_count} requested")

        # Generate prompt slug for filename
        prompt_slug_name = prompt_slug(prompt)

        # Prepare output directory and paths
        output_dir = Path.cwd()
        output_paths = []

        if output:
            output_path = Path(output)
            if output_path.is_dir() or (
                not output_path.suffix and not output_path.exists()
            ):
                # Output is a directory
                output_dir = output_path
                output_dir.mkdir(parents=True, exist_ok=True)
                output_paths = [None] * len(models)  # Will be generated per model
            else:
                # Output is a file path
                output_dir = output_path.parent
                if len(models) == 1:
                    # Single model - use exact path
                    output_paths = [output_path]
                else:
                    # Multiple models - insert model slug before extension
                    stem = output_path.stem
                    suffix = output_path.suffix or ".png"
                    output_paths = [
                        output_dir / f"{stem}--{safe_filename(model_name)}{suffix}"
                        for model_name in models
                    ]
        else:
            # No output specified - use current directory with generated names
            output_paths = [None] * len(models)  # Will be generated per model

        # Generate images in parallel
        def generate_single(
            model_name: str, output_path: Path | None
        ) -> tuple[str, ImageGenerationResponse, Path | None]:
            response = self.client._generate_with_retries(
                model=model_name,
                prompt=prompt,
                negative_prompt=negative_prompt,
                guidance_scale=guidance_scale,
                width=width,
                height=height,
                inference_steps=inference_steps,
                seed=seed,
            )
            return model_name, response, output_path

        # Use ThreadPoolExecutor for parallel generation (limited to prevent API overload)
        max_workers = min(len(models), MAX_CONCURRENT_MODELS) if len(models) > 5 else min(len(models), 4)
        logger.info(f"Starting parallel generation with {max_workers} workers for {len(models)} models")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(generate_single, model_name, output_path)
                for model_name, output_path in zip(models, output_paths)
            ]

            results = [future.result() for future in futures]

        # Process results
        successful_count = 0
        total_time = 0.0

        for model_name, response, specified_output_path in results:
            if response.success:
                successful_count += 1
                if response.generation_time:
                    total_time += response.generation_time

                print(f"✅ Generation successful with {response.model_used}!")
                if response.generation_time:
                    print(f"⏱️  Generation time: {response.generation_time:.2f}s")
                if response.image_url:
                    print(f"📎 Image URL: {response.image_url}")

                # Save image if we have image data
                if response.image_data:
                    import base64

                    try:
                        image_bytes = base64.b64decode(response.image_data)
                        image_format = detect_image_format(image_bytes)

                        # Determine final output path
                        if specified_output_path:
                            final_output_path = specified_output_path
                        else:
                            # Generate filename
                            model_slug_name = safe_filename(model_name)
                            if len(models) == 1:
                                filename = f"{prompt_slug_name}.{image_format}"
                            else:
                                filename = f"{prompt_slug_name}--{model_slug_name}.{image_format}"
                            final_output_path = output_dir / filename

                        # Ensure directory exists
                        final_output_path.parent.mkdir(parents=True, exist_ok=True)

                        # Save image
                        with open(final_output_path, "wb") as f:
                            f.write(image_bytes)
                        print(f"💾 Image saved to: {final_output_path}")

                    except Exception as e:
                        print(f"⚠️  Failed to save image from {model_name}: {e}")

            else:
                # Show detailed error information
                print(
                    f"❌ Generation failed with {model_name}: {response.error_message}"
                )
                if response.metadata:
                    if "error_context" in response.metadata:
                        error_context = response.metadata["error_context"]
                        if "parameters" in error_context:
                            params = error_context["parameters"]
                            print(
                                f"   ℹ️  Parameters: {params['resolution']}, guidance: {params['guidance_scale']}, steps: {params['inference_steps']}"
                            )
                    if "retry_attempts" in response.metadata:
                        print(
                            f"   🔄 Failed after {response.metadata['retry_attempts']} retry attempts"
                        )
                    if "error_type" in response.metadata:
                        print(f"   ⚠️  Error type: {response.metadata['error_type']}")

        # Summary
        if len(models) > 1:
            print(
                f"\n📊 Summary: {successful_count}/{len(models)} generations successful"
            )
            if successful_count > 0:
                if total_time > 0:
                    print(f"⏱️  Total generation time: {total_time:.2f}s")
                    print(
                        f"⏱️  Average generation time: {total_time / successful_count:.2f}s"
                    )
            else:
                print("❌ No successful generations")
                print("💡 Suggestions:")
                print("   • Check API key is valid (CHUTES_API_KEY)")
                print("   • Try fewer models simultaneously (avoid using '*')")
                print("   • Some models may be temporarily unavailable")
                print("   • Increase timeout if using complex models")

    def list(self, category: str | None = None):
        """
        List available models.

        Args:
            category: Filter by category (optional)
        """
        models = self.client.list_models(category=category)

        if category:
            print(f"Models in category '{category}':")
        else:
            print("Available models:")

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
                print(f"  • {model.name} ({model.display_name}){desc}")

    def categories(self):
        """List available model categories."""
        categories = {model.category for model in MODEL_REGISTRY.values()}
        print("Available categories:")
        for category in sorted(categories):
            count = len([m for m in MODEL_REGISTRY.values() if m.category == category])
            print(f"  • {category} ({count} models)")

    def info(self, model: str):
        """
        Show information about a specific model.

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
            print(f"Supports Negative Prompt: {model_info.supports_negative_prompt}")
            print(f"Max Resolution: {model_info.max_width}x{model_info.max_height}")
            print(f"Default Steps: {model_info.default_steps}")
        else:
            print(f"❌ Model '{model}' not found")
            print("\n💡 Use 'models' command to see available models")


def main():
    """Main CLI entry point."""
    fire.Fire(ChutesImageCLI)


if __name__ == "__main__":
    main()
