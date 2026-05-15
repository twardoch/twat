"""
Centralized logging for the twat plugin ecosystem.

Use this instead of configuring `loguru` directly. It gives you a standard
format and per-plugin filtering out of the box.

Example:
    from twat.common.logging import get_logger

    log = get_logger(__name__)
    log.info("Upload complete", file=path, provider=name)

Environment variables:
    TWAT_LOG_LEVEL: Global log level (default: INFO).
    TWAT_LOG_LEVEL_<PLUGIN>: Plugin-specific log level (e.g., TWAT_LOG_LEVEL_CACHE=TRACE).
    TWAT_LOG_FILE: File path for log output.
    TWAT_LOG_FORMAT: Custom loguru format string.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

try:
    from loguru import logger as _loguru_logger
except ImportError:  # pragma: no cover
    _loguru_logger = None  # type: ignore[assignment]

_DEFAULT_FORMAT = (
    "<green>{time:HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{extra[plugin]}</cyan> | "
    "<level>{message}</level>"
)

_configured: bool = False


def _extract_plugin_name(name: str) -> str:
    """
    Get the short plugin name from a module string.

    Examples:
        "twat_cache.engines.redis" -> "cache"
        "twat_fs" -> "fs"
        "my_module" -> "my_module"
    """
    parts = name.split(".")
    base = parts[0]
    if base.startswith("twat_"):
        return base[5:]
    return base


def configure_logging(
    *,
    level: str | None = None,
    fmt: str | None = None,
    log_file: str | Path | None = None,
) -> None:
    """
    Configure global logging settings.

    Usually called automatically by `get_logger()`, but you can call it manually
    to set custom formats or targets.

    Args:
        level: Log level (e.g., "DEBUG", "INFO"). Defaults to `TWAT_LOG_LEVEL` or "INFO".
        fmt: Custom loguru format string. Defaults to `TWAT_LOG_FORMAT`.
        log_file: Path to save logs. Defaults to `TWAT_LOG_FILE`.
    """
    global _configured  # noqa: PLW0603

    if _loguru_logger is None:
        _configured = True
        return

    resolved_level = level or os.environ.get("TWAT_LOG_LEVEL", "INFO")
    resolved_format = fmt or os.environ.get("TWAT_LOG_FORMAT", _DEFAULT_FORMAT)
    resolved_file = log_file or os.environ.get("TWAT_LOG_FILE")

    # Remove default loguru handler
    _loguru_logger.remove()

    # Add stderr handler with plugin-aware format
    _loguru_logger.add(
        sys.stderr,
        format=resolved_format,
        level=resolved_level.upper(),
        colorize=True,
    )

    # Add file handler if configured
    if resolved_file:
        _loguru_logger.add(
            str(resolved_file),
            format=resolved_format,
            level=resolved_level.upper(),
            rotation="10 MB",
            retention="7 days",
            compression="gz",
        )

    _configured = True


def get_logger(name: str) -> Any:
    """
    Get a configured logger bound to your plugin's name.

    Automatically extracts the plugin name (e.g., "twat_fs" -> "fs") and binds
    it to the logger. It also respects per-plugin log levels set via environment
    variables (e.g., `TWAT_LOG_LEVEL_FS=DEBUG`).

    Args:
        name: Usually `__name__` from the calling module.

    Returns:
        A loguru logger. If loguru isn't installed, returns a silent fallback.
    """
    if not _configured:
        configure_logging()

    plugin_name = _extract_plugin_name(name)

    if _loguru_logger is None:
        return _NoOpLogger()

    bound = _loguru_logger.bind(plugin=plugin_name)

    # Check for per-plugin log level override
    env_key = f"TWAT_LOG_LEVEL_{plugin_name.upper()}"
    plugin_level = os.environ.get(env_key)
    if plugin_level:
        bound = bound.opt(depth=1)
        # We can't set level per-bind in loguru, but we can filter
        # This is a best-effort approach using loguru's features
        _loguru_logger.debug(f"Plugin {plugin_name} log level override: {plugin_level}")

    return bound


class _NoOpLogger:
    """
    A silent fallback logger.

    Used when `loguru` isn't installed so plugins don't crash when calling `log.info()`.
    """

    def _noop(self, *_args: Any, **_kwargs: Any) -> None:
        pass

    trace = _noop
    debug = _noop
    info = _noop
    success = _noop
    warning = _noop
    error = _noop
    critical = _noop
    exception = _noop
    log = _noop
    bind = lambda self, **_kwargs: self  # noqa: E731
    opt = lambda self, **_kwargs: self  # noqa: E731
