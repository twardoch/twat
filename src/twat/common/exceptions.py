"""Base exception hierarchy for the twat plugin ecosystem.

All twat plugins should extend these base exceptions to provide
a consistent error handling experience across the ecosystem.

Example usage in a plugin::

    from twat.common.exceptions import TwatError

    class CacheError(TwatError):
        \"\"\"Cache operation failed.\"\"\"

    class CacheConfigError(CacheError):
        \"\"\"Cache configuration is invalid.\"\"\"
"""

from __future__ import annotations

from typing import Any


class TwatError(Exception):
    """
    The root exception for all twat packages.

    Inherit from this to create your own plugin exceptions. It supports attaching
    contextual data to the error, which is great for debugging.

    Attributes:
        message: What went wrong.
        context: Helpful details (e.g., {"file": "/path/to/file.txt", "plugin": "fs"}).
        cause: The original exception that triggered this one, if applicable.
    """

    def __init__(
        self,
        message: str = "",
        *,
        context: dict[str, Any] | None = None,
        cause: BaseException | None = None,
    ) -> None:
        self.context = context or {}
        self.cause = cause
        if cause is not None:
            self.__cause__ = cause
        super().__init__(message)


class PluginError(TwatError):
    """
    Raised when a plugin fails to load or run.

    This usually means the plugin isn't installed properly or has a bug
    in its initialization code.
    """


class ConfigError(TwatError):
    """
    Raised when configuration is missing or invalid.
    """


class DependencyError(TwatError):
    """
    Raised when a required tool or package is missing.
    """
