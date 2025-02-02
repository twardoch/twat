"""Plugin for twat"""

from importlib import metadata
from typing import Any

__version__ = metadata.version(__name__)


def __getattr__(name: str) -> Any:
    """Dynamic attribute lookup for plugins.

    Args:
        name: Name of plugin to load

    Returns:
        Loaded plugin module

    Raises:
        AttributeError: If plugin cannot be found or loaded
    """
    try:
        eps = metadata.entry_points(group="twat.plugins")
        for ep in eps:
            if ep.name == name:
                return ep.load()
    except Exception as e:
        raise AttributeError(f"Failed to load plugin '{name}': {e}") from e

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'") 