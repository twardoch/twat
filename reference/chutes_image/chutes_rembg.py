#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["aiohttp", "requests", "pydantic", "fire", "tenacity", "loguru", "python-dotenv", "pillow"]
# ///
# this_file: chutes_rembg.py

"""
Chutes AI Background Removal Client

Python client for background removal using the Chutes AI RemBG service.
Supports stdin/stdout operations, file input/output, and comprehensive error handling.
"""

import os
import sys
import json
import base64
import time
from pathlib import Path
from typing import Any
from io import BytesIO

import aiohttp
import requests
import fire
from pydantic import BaseModel, Field
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
from PIL import Image

# Load environment variables
load_dotenv()

# Constants
DEFAULT_API_KEY = os.getenv("CHUTES_API_KEY") or os.getenv("CHUTES_API_TOKEN")
REMBG_URL = "https://desudesuka-rembg.chutes.ai/remove"
DEFAULT_TIMEOUT = 120
MAX_RETRIES = 3


class RemoveRequest(BaseModel):
    """Request model for background removal"""

    image_b64: str = Field(
        ..., min_length=1, description="Base64 encoded image to remove background from"
    )


class RemoveResponse(BaseModel):
    """Response model for background removal"""

    success: bool = Field(default=True)
    image_data: str | None = Field(
        None, description="Base64 encoded image with background removed"
    )
    error_message: str | None = Field(None, description="Error message if failed")
    processing_time: float | None = Field(
        None, description="Time taken to process in seconds"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )


class RemBGError(Exception):
    """Custom exception for RemBG API errors"""


def image_to_base64(image_data: bytes) -> str:
    """
    Convert binary image data to base64 string.

    Args:
        image_data: Binary image data

    Returns:
        Base64 encoded string
    """
    return base64.b64encode(image_data).decode("utf-8")


def base64_to_image(b64_string: str) -> bytes:
    """
    Convert base64 string to binary image data.

    Args:
        b64_string: Base64 encoded image string

    Returns:
        Binary image data
    """
    # Handle data URL format
    if b64_string.startswith("data:"):
        b64_string = b64_string.split(",", 1)[1]

    return base64.b64decode(b64_string)


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


def ensure_png_format(image_data: bytes) -> bytes:
    """
    Convert image to PNG format if it's not already.

    Args:
        image_data: Binary image data

    Returns:
        PNG format image data
    """
    try:
        with BytesIO(image_data) as input_buffer:
            img = Image.open(input_buffer)
            # Convert to RGBA to preserve transparency
            if img.mode != "RGBA":
                img = img.convert("RGBA")

            with BytesIO() as output_buffer:
                img.save(output_buffer, format="PNG", optimize=True)
                return output_buffer.getvalue()
    except Exception as e:
        logger.warning(f"Failed to convert to PNG: {e}, returning original data")
        return image_data


class RemBGClient:
    """
    RemBG API client for background removal.

    Supports both sync and async operations with comprehensive error handling.
    """

    def __init__(self, api_key: str | None = None, timeout: int = DEFAULT_TIMEOUT):
        """
        Initialize RemBG client.

        Args:
            api_key: Chutes API key. If None, uses CHUTES_API_KEY or CHUTES_API_TOKEN environment variable
            timeout: Request timeout in seconds
        """
        self.api_key = api_key or DEFAULT_API_KEY
        if not self.api_key:
            raise ValueError(
                "API key required. Set CHUTES_API_KEY or CHUTES_API_TOKEN environment variable or pass api_key parameter"
            )

        self.timeout = timeout
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        logger.info(f"RemBGClient initialized with timeout={timeout}s")

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
    def _make_request_sync(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Make HTTP request with retry logic (sync version).

        Args:
            data: Request payload

        Returns:
            Response JSON data

        Raises:
            RemBGError: On API errors
        """
        try:
            logger.debug(f"Making sync request to {REMBG_URL}")
            logger.debug(f"Request headers: {self.headers}")

            response = requests.post(
                REMBG_URL, headers=self.headers, json=data, timeout=self.timeout
            )

            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response headers: {dict(response.headers)}")

            response.raise_for_status()

            # Parse JSON response
            try:
                result = response.json()
                logger.debug(
                    f"Parsed JSON response keys: {list(result.keys()) if isinstance(result, dict) else 'non-dict'}"
                )
                return result
            except json.JSONDecodeError as json_err:
                logger.error(f"JSON decode error: {json_err}")
                logger.error(f"Response content: {response.text[:200]}...")
                raise ValueError(f"Invalid JSON response: {json_err}")

        except requests.exceptions.RequestException as e:
            error_msg = f"Request failed: {str(e)}"
            logger.error(error_msg)
            logger.error(f"Request URL: {REMBG_URL}")
            logger.error(f"Request timeout: {self.timeout}s")
            raise RemBGError(error_msg) from e
        except ValueError as e:
            error_msg = f"Response parsing failed: {str(e)}"
            logger.error(error_msg)
            raise RemBGError(error_msg) from e

    async def _make_request_async(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Make HTTP request asynchronously.

        Args:
            data: Request payload

        Returns:
            Response JSON data

        Raises:
            RemBGError: On API errors
        """
        try:
            logger.debug(f"Making async request to {REMBG_URL}")
            logger.debug(f"Request headers: {self.headers}")

            timeout = aiohttp.ClientTimeout(total=self.timeout)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(
                    REMBG_URL, headers=self.headers, json=data
                ) as response:
                    logger.debug(f"Response status: {response.status}")
                    logger.debug(f"Response headers: {dict(response.headers)}")

                    response.raise_for_status()

                    # Parse JSON response
                    try:
                        result = await response.json()
                        logger.debug(
                            f"Parsed JSON response keys: {list(result.keys()) if isinstance(result, dict) else 'non-dict'}"
                        )
                        return result
                    except json.JSONDecodeError as json_err:
                        logger.error(f"JSON decode error: {json_err}")
                        text_content = await response.text()
                        logger.error(f"Response content: {text_content[:200]}...")
                        raise ValueError(f"Invalid JSON response: {json_err}")

        except aiohttp.ClientError as e:
            error_msg = f"Async request failed: {str(e)}"
            logger.error(error_msg)
            logger.error(f"Request URL: {REMBG_URL}")
            logger.error(f"Request timeout: {self.timeout}s")
            raise RemBGError(error_msg) from e
        except ValueError as e:
            error_msg = f"Response parsing failed: {str(e)}"
            logger.error(error_msg)
            raise RemBGError(error_msg) from e

    def remove_sync(self, image_data: bytes, ensure_png: bool = True) -> RemoveResponse:
        """
        Remove background from image synchronously.

        Args:
            image_data: Binary image data
            ensure_png: Convert output to PNG format (default: True)

        Returns:
            RemoveResponse with processed image information
        """
        logger.info("Removing background from image")

        try:
            start_time = time.time()

            # Convert image to base64
            image_b64 = image_to_base64(image_data)

            request_data = RemoveRequest(image_b64=image_b64)

            response_data = self._make_request_sync(request_data.model_dump())
            processing_time = time.time() - start_time

            # Extract image data from response
            output_image_b64 = response_data.get("image")
            if not output_image_b64:
                raise ValueError("No image data in response")

            # Convert to PNG if requested
            if ensure_png:
                output_image_bytes = base64_to_image(output_image_b64)
                output_image_bytes = ensure_png_format(output_image_bytes)
                output_image_b64 = image_to_base64(output_image_bytes)

            return RemoveResponse(
                success=True,
                image_data=output_image_b64,
                processing_time=processing_time,
                metadata={
                    "request_params": request_data.model_dump(),
                    "output_format": "PNG" if ensure_png else "original",
                },
            )

        except Exception as e:
            error_msg = f"Background removal failed: {str(e)}"
            logger.error(error_msg)
            return RemoveResponse(
                success=False,
                error_message=error_msg,
                metadata={"error_type": type(e).__name__},
            )

    async def remove_async(
        self, image_data: bytes, ensure_png: bool = True
    ) -> RemoveResponse:
        """
        Remove background from image asynchronously.

        Args:
            image_data: Binary image data
            ensure_png: Convert output to PNG format (default: True)

        Returns:
            RemoveResponse with processed image information
        """
        logger.info("Removing background from image async")

        try:
            start_time = time.time()

            # Convert image to base64
            image_b64 = image_to_base64(image_data)

            request_data = RemoveRequest(image_b64=image_b64)

            response_data = await self._make_request_async(request_data.model_dump())
            processing_time = time.time() - start_time

            # Extract image data from response
            output_image_b64 = response_data.get("image")
            if not output_image_b64:
                raise ValueError("No image data in response")

            # Convert to PNG if requested
            if ensure_png:
                output_image_bytes = base64_to_image(output_image_b64)
                output_image_bytes = ensure_png_format(output_image_bytes)
                output_image_b64 = image_to_base64(output_image_bytes)

            return RemoveResponse(
                success=True,
                image_data=output_image_b64,
                processing_time=processing_time,
                metadata={
                    "request_params": request_data.model_dump(),
                    "output_format": "PNG" if ensure_png else "original",
                },
            )

        except Exception as e:
            error_msg = f"Async background removal failed: {str(e)}"
            logger.error(error_msg)
            return RemoveResponse(
                success=False,
                error_message=error_msg,
                metadata={"error_type": type(e).__name__},
            )

    def _remove_with_retries(self, **kwargs) -> RemoveResponse:
        """Wrapper that handles final failure after retries are exhausted."""
        try:
            return self.remove_sync(**kwargs)
        except Exception as e:
            error_msg = (
                f"Background removal failed after {MAX_RETRIES} attempts: {str(e)}"
            )
            logger.error(
                error_msg,
                extra={
                    "error_type": type(e).__name__,
                    "final_failure": True,
                    "retry_attempts": MAX_RETRIES,
                },
            )

            return RemoveResponse(
                success=False,
                error_message=error_msg,
                metadata={
                    "retry_attempts": MAX_RETRIES,
                    "error_type": type(e).__name__,
                },
            )


class RemBGCLI:
    """Command-line interface for RemBG client."""

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

        self.client = RemBGClient(api_key=api_key)

    def remove(
        self,
        input: str | Path | None = None,
        output: str | Path | None = None,
        verbose: bool = False,
        ensure_png: bool = True,
    ):
        """
        Remove background from image.

        Args:
            input: Input file path. If None, reads from stdin
            output: Output file path. If None, writes to stdout
            verbose: Enable verbose debug logging
            ensure_png: Convert output to PNG format (default: True)
        """
        if verbose:
            logger.remove()
            logger.add(lambda msg: print(msg, end=""), colorize=True, level="DEBUG")

        try:
            # Read input
            if input:
                # Read from file
                input_path = Path(input)
                if not input_path.exists():
                    print(f"❌ Input file not found: {input}", file=sys.stderr)
                    sys.exit(1)

                with open(input_path, "rb") as f:
                    image_data = f.read()
                logger.info(f"Read {len(image_data)} bytes from {input}")
            else:
                # Read from stdin
                if sys.stdin.isatty():
                    print(
                        "❌ No input file specified and stdin is empty", file=sys.stderr
                    )
                    print(
                        "Usage: python chutes_rembg.py remove --input=image.jpg --output=result.png",
                        file=sys.stderr,
                    )
                    print(
                        "   or: cat image.jpg | python chutes_rembg.py remove > result.png",
                        file=sys.stderr,
                    )
                    sys.exit(1)

                image_data = sys.stdin.buffer.read()
                logger.info(f"Read {len(image_data)} bytes from stdin")

            # Process image
            response = self.client.remove_sync(image_data, ensure_png=ensure_png)

            if response.success:
                if verbose:
                    print(f"✅ Background removal successful!", file=sys.stderr)
                    if response.processing_time:
                        print(
                            f"⏱️  Processing time: {response.processing_time:.2f}s",
                            file=sys.stderr,
                        )

                # Convert base64 to binary
                output_image_data = base64_to_image(response.image_data)

                # Write output
                if output:
                    # Write to file
                    output_path = Path(output)
                    output_path.parent.mkdir(parents=True, exist_ok=True)

                    with open(output_path, "wb") as f:
                        f.write(output_image_data)

                    if verbose:
                        print(f"💾 Image saved to: {output}", file=sys.stderr)
                else:
                    # Write to stdout
                    sys.stdout.buffer.write(output_image_data)
                    sys.stdout.buffer.flush()

            else:
                print(
                    f"❌ Background removal failed: {response.error_message}",
                    file=sys.stderr,
                )
                sys.exit(1)

        except Exception as e:
            print(f"❌ Error: {str(e)}", file=sys.stderr)
            sys.exit(1)

    def test(self, image_path: str, output_dir: str = ".", verbose: bool = False):
        """
        Test background removal with a sample image.

        Args:
            image_path: Path to test image
            output_dir: Directory to save output (default: current directory)
            verbose: Enable verbose debug logging
        """
        if verbose:
            logger.remove()
            logger.add(lambda msg: print(msg, end=""), colorize=True, level="DEBUG")

        input_path = Path(image_path)
        if not input_path.exists():
            print(f"❌ Test image not found: {image_path}")
            return

        output_path = Path(output_dir) / f"{input_path.stem}_no_bg.png"

        print(f"🧪 Testing background removal on {image_path}")

        with open(input_path, "rb") as f:
            image_data = f.read()

        response = self.client.remove_sync(image_data, ensure_png=True)

        if response.success:
            output_image_data = base64_to_image(response.image_data)

            with open(output_path, "wb") as f:
                f.write(output_image_data)

            print(f"✅ Test successful! Output saved to: {output_path}")
            if response.processing_time:
                print(f"⏱️  Processing time: {response.processing_time:.2f}s")
        else:
            print(f"❌ Test failed: {response.error_message}")


def main():
    """Main CLI entry point."""
    fire.Fire(RemBGCLI().remove)


if __name__ == "__main__":
    main()
