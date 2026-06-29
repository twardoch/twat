"""
twat: A fast, modular plugin host system.

This module is the core engine of the `twat` ecosystem. It finds plugins
registered via Python entry points and loads them into the `twat` namespace.
It also provides the CLI dispatcher to run them.

Plugins are standalone packages (like `twat-fs` or `twat-cache`) that
become available as `twat.fs` or `twat.cache` at runtime.
"""

from __future__ import annotations
from .__version__ import __version__

import sys
from collections.abc import Iterable
from dataclasses import dataclass
from importlib import metadata
from types import ModuleType
from typing import NoReturn

from twat.common.exceptions import PluginError

__version__ = metadata.version(__name__)

__package__ = "twat"

#: Entry-point group every twat plugin registers itself under. The host scans
#: this group to discover plugins; nothing is imported until a plugin is used.
PLUGIN_GROUP = "twat.plugins"


@dataclass(frozen=True)
class AvailablePlugin:
    """A locally-installed ``twat-*`` distribution and its plugin registration.

    Attributes:
        distribution: Canonical PyPI distribution name (e.g. ``twat-fs``).
        version: Installed version string.
        plugin_name: The ``twat.plugins`` entry-point name it registers
            (e.g. ``fs``), or ``None`` if the distribution ships no plugin.
    """

    distribution: str
    version: str
    plugin_name: str | None


@dataclass(frozen=True)
class PluginHealth:
    """Health-check outcome for one ``twat.plugins`` entry point.

    Attributes:
        name: Short plugin name (e.g. ``fs``).
        target: Entry-point target value (e.g. ``twat_fs``).
        ok: True if the plugin imported cleanly to a module.
        error: Failure message when ``ok`` is False, else ``None``.
    """

    name: str
    target: str
    ok: bool
    error: str | None = None


def _plugin_entry_points() -> Iterable[metadata.EntryPoint]:
    """Return twat plugin entry points without importing plugin modules."""
    return metadata.entry_points(group=PLUGIN_GROUP)


def iter_plugins() -> tuple[str, ...]:
    """Return sorted installed twat plugin names without importing plugins."""
    return tuple(sorted({ep.name for ep in _plugin_entry_points()}))


def _get_plugin_entry_point(name: str) -> metadata.EntryPoint | None:
    """Find a plugin entry point by its short name without loading it."""
    for ep in _plugin_entry_points():
        if ep.name == name:
            return ep
    return None


def _is_twat_distribution(name: str) -> bool:
    """True for the host itself or any ``twat-*`` package (name-normalized)."""
    canonical = name.replace("_", "-").lower()
    return canonical == "twat" or canonical.startswith("twat-")


def iter_available_plugins() -> tuple[AvailablePlugin, ...]:
    """Scan installed distributions for ``twat`` / ``twat-*`` packages.

    Unlike :func:`iter_plugins` (which lists registered entry-point names), this
    inspects every installed distribution so it also surfaces ``twat-*`` packages
    that are installed but register no ``twat.plugins`` entry point. No plugin
    module is imported — only static distribution metadata is read.

    Returns:
        Distributions sorted by name, each annotated with its plugin entry-point
        name (or ``None`` when the package ships no plugin).
    """
    found: dict[str, AvailablePlugin] = {}
    for dist in metadata.distributions():
        name = dist.metadata["Name"]
        if not name or not _is_twat_distribution(name):
            continue
        # A distribution registers at most one plugin under PLUGIN_GROUP; the
        # entry-point name (e.g. "fs") is what becomes twat.<name> at runtime.
        plugin_name = next(
            (ep.name for ep in dist.entry_points if ep.group == PLUGIN_GROUP),
            None,
        )
        canonical = name.replace("_", "-").lower()
        # Keep the first record per distribution (dedupes shadowed installs).
        found.setdefault(canonical, AvailablePlugin(canonical, dist.version, plugin_name))
    return tuple(sorted(found.values(), key=lambda item: item.distribution))


def doctor() -> tuple[PluginHealth, ...]:
    """Health-check every installed plugin by importing it.

    Each ``twat.plugins`` entry point is loaded and verified to resolve to a
    module. This *does* import plugins (the whole point is to catch broken ones),
    so it is slower than :func:`iter_plugins`.

    Returns:
        One :class:`PluginHealth` per registered plugin, sorted by name.
    """
    report: list[PluginHealth] = []
    for ep in sorted(_plugin_entry_points(), key=lambda e: e.name):
        try:
            loaded = ep.load()
        except Exception as exc:  # plugin import is untrusted — never crash here
            report.append(PluginHealth(ep.name, ep.value, ok=False, error=str(exc)))
            continue
        if isinstance(loaded, ModuleType):
            report.append(PluginHealth(ep.name, ep.value, ok=True))
        else:
            report.append(
                PluginHealth(
                    ep.name,
                    ep.value,
                    ok=False,
                    error="entry point did not resolve to a module",
                )
            )
    return tuple(report)


def _print_available() -> None:
    """Print installed ``twat-*`` distributions as ``name<TAB>version<TAB>plugin``."""
    available = iter_available_plugins()
    if not available:
        print("No twat-* distributions are installed.")
        return
    for item in available:
        plugin = item.plugin_name if item.plugin_name else "-"
        print(f"{item.distribution}\t{item.version}\t{plugin}")


def _print_doctor() -> bool:
    """Print a per-plugin health report. Return True only if all plugins load."""
    report = doctor()
    if not report:
        print("No twat plugins are installed.")
        return True
    for entry in report:
        status = "OK" if entry.ok else "FAIL"
        line = f"[{status}] {entry.name} -> {entry.target}"
        if entry.error:
            line += f": {entry.error}"
        print(line)
    return all(entry.ok for entry in report)


def _usage() -> str:
    """Return CLI usage text for the host dispatcher."""
    plugins = iter_plugins()
    plugin_block = "Installed plugins:\n  " + "  ".join(plugins) + "\n\n" if plugins else ""
    return (
        "Usage: twat <plugin_name> [args...]\n"
        "       twat --list [--available]\n"
        "       twat --doctor\n"
        "       twat --completions {bash,zsh,fish}\n"
        "       twat --help\n\n"
        "Options:\n"
        "  --list                       List installed twat plugins (entry-point names).\n"
        "  --list --available           List installed twat-* distributions and the\n"
        "  --available                  plugin each one registers (does not import them).\n"
        "  --doctor                     Import every plugin and report load health;\n"
        "                               exits non-zero if any plugin is broken.\n"
        "  --completions SHELL          Emit a shell completion script for installed\n"
        "                               twat-* console scripts. SHELL is bash, zsh, or fish.\n"
        "  --help, -h                   Show this help message.\n\n"
        f"{plugin_block}"
        "Discovery:\n"
        "  Every installed plugin also registers dashed leaf scripts, e.g.\n"
        "  twat-image-gray2alpha, so that 'twat-<TAB>' in your shell lists\n"
        "  dozens of commands. Run `twat --completions zsh > ~/.zfunc/_twat` to\n"
        "  install completions for the dispatcher itself.\n"
    )


def _load_plugin(name: str) -> ModuleType | None:
    """
    Find and load a twat plugin by name.

    Scans the `twat.plugins` entry point group. If a match is found,
    loads the module and registers it in `sys.modules` so future imports
    are fast.

    Args:
        name: The short name of the plugin (e.g., "fs" for "twat-fs").

    Returns:
        The loaded module, or None if the plugin isn't installed or is invalid.

    Raises:
        PluginError: If the plugin exists but crashes during import.
    """
    try:
        ep = _get_plugin_entry_point(name)
        if ep is None:
            return None

        loaded_object = ep.load()
        if isinstance(loaded_object, ModuleType):
            # Register the plugin in sys.modules
            plugin_name = f"twat.{name}"
            sys.modules[plugin_name] = loaded_object
            return loaded_object
        return None
    except PluginError:
        raise
    except Exception as exc:
        msg = f"Failed to load plugin '{name}'"
        raise PluginError(
            msg,
            context={"plugin_name": name},
            cause=exc,
        ) from exc


def __getattr__(name: str) -> ModuleType:
    """
    Load plugins dynamically on attribute access.

    This magic method powers the `twat.<plugin>` syntax. When you run:
        import twat
        twat.myplugin
    This method looks for 'myplugin' in the `twat.plugins` entry points.

    To make your package a twat plugin, add this to your `pyproject.toml`:

    ```toml
    [project.entry-points."twat.plugins"]
    myplugin = "your_package.module"
    ```

    Args:
        name: The short plugin name.

    Returns:
        The loaded module.

    Raises:
        PluginError: If the plugin isn't installed or crashes on load.
    """
    plugin = _load_plugin(name)
    if plugin is not None:
        return plugin

    msg = f"module '{__name__}' has no attribute '{name}'"
    raise PluginError(
        msg,
        context={"plugin_name": name},
    )


def run_plugin(plugin_name: str) -> NoReturn:
    """
    Load and execute a plugin's `main()` function.

    This powers the `twat <plugin>` CLI command. It finds the plugin,
    checks if it has a callable `main`, and runs it.

    Args:
        plugin_name: The short name of the plugin to run.

    Exits:
        0: Plugin ran successfully.
        1: Plugin not found, crashed, or has no `main()` function.
    """
    try:
        ep = _get_plugin_entry_point(plugin_name)
        if ep is not None:
            plugin = ep.load()
            main_func = getattr(plugin, "main", None)
            if isinstance(plugin, ModuleType) and callable(main_func):
                main_func()
                sys.exit(0)
            else:
                print(
                    f"Error: Plugin '{plugin_name}' has no callable main() function.",
                    file=sys.stderr,
                )
                sys.exit(1)
        # Plugin not found in entry points
        print(
            f"Error: Plugin '{plugin_name}' not found.",
            file=sys.stderr,
        )
        sys.exit(1)
    except SystemExit:
        raise
    except PluginError as exc:
        print(f"Error loading plugin '{plugin_name}': {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"Error running plugin '{plugin_name}': {exc}", file=sys.stderr)
        sys.exit(1)


def main() -> NoReturn:
    """
    The main CLI dispatcher for the twat ecosystem.

    Usage: `twat <plugin_name> [args...]`

    This intercepts the CLI call, rewrites `sys.argv` so the target plugin
    thinks it was called directly, and passes control to the plugin's `main()`.
    """
    if len(sys.argv) < 2:
        # No args = treat as `--help`: print to stdout, exit 0.
        print(_usage())
        sys.exit(0)

    plugin_name = sys.argv[1]
    rest = sys.argv[2:]
    if plugin_name in {"--help", "-h"}:
        print(_usage())
        sys.exit(0)

    if plugin_name == "--list":
        # `twat --list --available` widens the listing to installed twat-*
        # distributions; bare `--list` shows only registered plugin names.
        if "--available" in rest:
            _print_available()
            sys.exit(0)
        for name in iter_plugins():
            print(name)
        sys.exit(0)

    if plugin_name == "--available":
        _print_available()
        sys.exit(0)

    if plugin_name == "--doctor":
        sys.exit(0 if _print_doctor() else 1)

    if plugin_name == "--completions":
        from twat.common.cli import emit_completions

        shell = sys.argv[2] if len(sys.argv) > 2 else ""
        if shell not in {"bash", "zsh", "fish"}:
            print(
                "Error: --completions requires SHELL in {bash,zsh,fish}.",
                file=sys.stderr,
            )
            sys.exit(2)
        sys.stdout.write(emit_completions(shell))
        sys.exit(0)

    # Prepare sys.argv for the plugin:
    # sys.argv[0] becomes "twat.plugin_name"
    # sys.argv[1:] becomes the original arguments to the plugin.
    sys.argv = [f"twat.{plugin_name}", *sys.argv[2:]]
    run_plugin(plugin_name)
