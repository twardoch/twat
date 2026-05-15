"""
twat.common: Shared utilities and base classes.

This module provides the core building blocks for twat plugins, ensuring
consistency across the ecosystem. Currently, it exports the base exception
classes that plugins should inherit from.
"""

from __future__ import annotations

from twat.common.exceptions import (
    ConfigError,
    DependencyError,
    PluginError,
    TwatError,
)

__all__ = [
    "ConfigError",
    "DependencyError",
    "PluginError",
    "TwatError",
]
