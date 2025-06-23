"""
Twat Plugin Host System.

This module provides the core functionality for the 'twat' plugin system.
It allows for dynamic discovery and loading of plugins registered via entry points,
and provides a command-line interface to execute plugin functionalities.
"""

from __future__ import annotations

import sys
from importlib import metadata
from types import ModuleType  # Moved to top-level for runtime isinstance check
from typing import TYPE_CHECKING, NoReturn

# if TYPE_CHECKING: # ModuleType is now imported globally
#     pass

__version__ = metadata.version(__name__)

# Enable package-style imports for plugins
__path__ = []
__package__ = "twat"  # noqa: A001 - Intentionally shadows builtin for plugin loading


def _load_plugin(name: str) -> ModuleType | None:
    """
    Load a plugin module by its registered name.

    Searches for a plugin registered under the 'twat.plugins' entry point group
    with the given name. If found and successfully loaded as a module, it's
    registered in `sys.modules` as `twat.<name>` and the module object is returned.

    Args:
        name: The registered name of the plugin.

    Returns:
        The loaded plugin module, or None if the plugin cannot be found,
        fails to load, or the loaded entry point is not a module.
    """
    try:
        eps = metadata.entry_points(group="twat.plugins")
        for ep in eps:
            if ep.name == name:
                loaded_object = ep.load()
                if isinstance(loaded_object, ModuleType):
                    # Register the plugin in sys.modules
                    plugin_name = f"twat.{name}"
                    sys.modules[plugin_name] = loaded_object
                    return loaded_object
                else:
                    # Optionally, log that the loaded object was not a module
                    # For now, conform to signature by returning None
                    return None
    except Exception:
        # Optionally, log the exception
        return None
    return None


def __getattr__(name: str) -> ModuleType:
    """
    Dynamic attribute lookup for plugins.

    This allows accessing registered 'twat' plugins as attributes of this module.
    For example, `import twat; twat.myplugin` will attempt to load the plugin
    named 'myplugin'.

    To register a plugin, add an entry point to its `pyproject.toml` under
    the `twat.plugins` group:

    ```toml
    [project.entry-points."twat.plugins"]
    myplugin = "your_package.module"  # Points to the plugin module
    ```

    Args:
        name: The name of the plugin to load (as used in the entry point).

    Returns:
        The loaded plugin module.

    Raises:
        AttributeError: If the plugin cannot be found, fails to load, or the
                        loaded entry point is not a valid module.
    """
    plugin = _load_plugin(name)
    if plugin is not None:
        return plugin

    msg = f"module '{__name__}' has no attribute '{name}'"
    raise AttributeError(msg)


def run_plugin(plugin_name: str) -> NoReturn:
    """
    Loads and runs the 'main()' function of a specified plugin.

    This function is primarily used by the `main` CLI entry point. It attempts
    to load the plugin, and if successful and the plugin module has a callable
    attribute named 'main', it calls it.

    Note:
        This function calls `sys.exit()` internally with 0 on successful plugin
        execution, or 1 on failure (plugin not found, load error, no 'main'
        attribute, or exception during plugin's main execution).
        The `sys.argv` is expected to be set up by the caller for the plugin.

    Args:
        plugin_name: The name of the plugin to load and run.
    """
    try:
        eps = metadata.entry_points(group="twat.plugins")
        for ep in eps:
            if ep.name == plugin_name:
                plugin = ep.load()  # TODO: Could use _load_plugin here for consistency?
                # However, _load_plugin returns None on error, run_plugin exits.
                # And _load_plugin checks isinstance(module, ModuleType)
                if isinstance(plugin, ModuleType) and hasattr(plugin, "main") and callable(plugin.main):
                    plugin.main()
                    sys.exit(0)
                else:
                    # Error: plugin not a module, no main, or main not callable
                    sys.exit(1)
        # If loop finishes, plugin_name was not found in entry points
        sys.exit(1)  # Plugin not found
    except Exception:
        # Error during ep.load() or other unexpected issue
        sys.exit(1)
    # Should not be reached if plugin is found due to sys.exit calls.
    # If plugin not found, loop finishes and exits.
    # Adding explicit exit in case logic changes, to ensure NoReturn.
    sys.exit(1)  # Fallback, though prior exits should cover all paths.


def main() -> NoReturn:
    """
    Main command-line interface entry point for the twat plugin system.

    Parses `sys.argv` to determine the plugin to run and its arguments.
    Usage: `python -m twat plugin_name [plugin_args...]`
    or if installed: `twat plugin_name [plugin_args...]`

    It modifies `sys.argv` for the target plugin before execution, setting
    `sys.argv[0]` to `twat.plugin_name`.
    """
    if len(sys.argv) < 2:
        print("Usage: twat <plugin_name> [args...]", file=sys.stderr)
        sys.exit(1)

    plugin_name = sys.argv[1]
    # Prepare sys.argv for the plugin:
    # sys.argv[0] becomes "twat.plugin_name"
    # sys.argv[1:] becomes the original arguments to the plugin.
    sys.argv = [f"twat.{plugin_name}", *sys.argv[2:]]
    run_plugin(plugin_name)
