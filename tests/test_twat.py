"""Test suite for twat."""

import sys
import pytest  # type: ignore[import-not-found]
from unittest import mock
from importlib.metadata import EntryPoint
from types import ModuleType
from typing import Any  # Only Any is needed from typing
from collections.abc import Callable, Iterator  # Callable and Iterator from collections.abc

import twat


def test_version() -> None:
    """Verify package exposes version."""
    assert twat.__version__


# --- Tests for plugin loading ---


@pytest.fixture  # type: ignore[misc]
def mock_entry_points(monkeypatch: pytest.MonkeyPatch) -> dict[str, list[mock.Mock]]:
    """Fixture to mock importlib.metadata.entry_points."""
    mock_eps: dict[str, list[mock.Mock]] = {}

    def _mock_entry_points_func(group: str) -> list[mock.Mock]:
        return mock_eps.get(group, [])

    monkeypatch.setattr("importlib.metadata.entry_points", _mock_entry_points_func)
    return mock_eps


def test_load_plugin_success(mock_entry_points: dict[str, list[mock.Mock]]) -> None:
    """Test successful loading of a plugin."""
    mock_plugin_module = ModuleType("mock_plugin_module")
    mock_plugin_module.foo = "bar"  # type: ignore[attr-defined]

    ep = mock.Mock(spec=EntryPoint)
    ep.name = "myplugin"
    ep.value = "mock_package:mock_plugin_module"
    ep.group = "twat.plugins"
    ep.load = mock.Mock(return_value=mock_plugin_module)
    mock_entry_points["twat.plugins"] = [ep]

    # Ensure plugin is not in sys.modules before access
    plugin_fqn = "twat.myplugin"
    if plugin_fqn in sys.modules:
        del sys.modules[plugin_fqn]

    loaded_plugin = twat.myplugin

    assert loaded_plugin is mock_plugin_module
    assert loaded_plugin.foo == "bar"
    assert plugin_fqn in sys.modules
    assert sys.modules[plugin_fqn] is mock_plugin_module
    ep.load.assert_called_once()

    # Test that accessing again uses the cached version from sys.modules (via _load_plugin)
    # and doesn't call ep.load() again if __getattr__ is called multiple times.
    # The current _load_plugin will call ep.load() again if the module isn't in sys.modules
    # under the "twat.myplugin" key, or if it is, it returns it.
    # Let's ensure our mock ep.load() isn't called again if it's already in sys.modules.
    # To test this properly, we would need to ensure that __getattr__ itself caches it on the 'twat' module,
    # or that _load_plugin is smart. The current _load_plugin puts it in sys.modules.
    # If we delete it from sys.modules, then _load_plugin will try to load it again.
    # If it's in sys.modules, _load_plugin's loop might not find the EP if mock_entry_points is cleared,
    # but it should return the module from sys.modules if already loaded by a previous call.

    # To clarify: twat.__getattr__ calls _load_plugin.
    # _load_plugin loads and puts into sys.modules['twat.myplugin'].
    # If twat.myplugin is accessed again, __getattr__ is called again.
    # _load_plugin is called again. It will iterate entry points.
    # If the entry point is still there, it will load() and overwrite sys.modules.
    # This is not ideal caching. A better __getattr__ would store it on the module.
    # Let's test the current behavior first.

    # If called again, it should re-load if the EP is still there.
    loaded_plugin_again = twat.myplugin
    assert loaded_plugin_again is mock_plugin_module
    # Depending on how _load_plugin is written, load might be called again or not.
    # Current _load_plugin will call it again if it finds the EP.
    assert ep.load.call_count == 2  # Called again because _load_plugin re-scans.

    # Clean up sys.modules
    if plugin_fqn in sys.modules:
        del sys.modules[plugin_fqn]


def test_load_plugin_not_found(mock_entry_points: dict[str, list[mock.Mock]]) -> None:
    """Test attempting to load a non-existent plugin."""
    mock_entry_points["twat.plugins"] = []

    with pytest.raises(AttributeError, match="module 'twat' has no attribute 'nonexistentplugin'"):
        _ = twat.nonexistentplugin


def test_load_plugin_load_raises_exception(mock_entry_points: dict[str, list[mock.Mock]]) -> None:
    """Test plugin loading when entry_point.load() raises an exception."""
    ep = mock.Mock(spec=EntryPoint)
    ep.name = "failingplugin"
    ep.value = "fp:main"
    ep.group = "twat.plugins"
    ep.load = mock.Mock(side_effect=ImportError("Failed to load plugin"))
    mock_entry_points["twat.plugins"] = [ep]

    plugin_fqn = "twat.failingplugin"
    if plugin_fqn in sys.modules:
        del sys.modules[plugin_fqn]

    with pytest.raises(AttributeError, match="module 'twat' has no attribute 'failingplugin'"):
        _ = twat.failingplugin

    ep.load.assert_called_once()
    assert plugin_fqn not in sys.modules


def test_load_plugin_entry_point_returns_non_module(mock_entry_points: dict[str, list[mock.Mock]]) -> None:
    """Test plugin loading when entry_point.load() returns a non-module."""
    ep = mock.Mock(spec=EntryPoint)
    ep.name = "invalidplugin"
    ep.value = "ip:main"
    ep.group = "twat.plugins"
    ep.load = mock.Mock(return_value="not a module")  # Removed unused type: ignore
    mock_entry_points["twat.plugins"] = [ep]

    plugin_fqn = "twat.invalidplugin"
    if plugin_fqn in sys.modules:
        del sys.modules[plugin_fqn]

    with pytest.raises(AttributeError, match="module 'twat' has no attribute 'invalidplugin'"):
        _ = twat.invalidplugin

    ep.load.assert_called_once()
    assert plugin_fqn not in sys.modules


def test_plugin_loading_is_cached_in_sys_modules(mock_entry_points: dict[str, list[mock.Mock]]) -> None:
    """Test that once a plugin is loaded, subsequent calls to _load_plugin (via __getattr__)
    for the same plugin do not need to call entry_point.load() if already in sys.modules,
    but current implementation of _load_plugin re-scans and re-loads."""

    mock_plugin_module = ModuleType("cached_plugin_module")
    ep = mock.Mock(spec=EntryPoint)
    ep.name = "cachingplugin"
    ep.value = "cp:main"
    ep.group = "twat.plugins"
    ep.load = mock.Mock(return_value=mock_plugin_module)
    mock_entry_points["twat.plugins"] = [ep]

    plugin_fqn = "twat.cachingplugin"
    if plugin_fqn in sys.modules:
        del sys.modules[plugin_fqn]

    # First access: loads and caches in sys.modules
    plugin1 = twat.cachingplugin
    assert plugin1 is mock_plugin_module
    assert ep.load.call_count == 1
    assert sys.modules[plugin_fqn] is mock_plugin_module

    # Second access: __getattr__ calls _load_plugin again.
    # _load_plugin iterates entry points and calls load() again.
    plugin2 = twat.cachingplugin
    assert plugin2 is mock_plugin_module
    assert ep.load.call_count == 2  # This demonstrates the current re-load behavior.

    # If the entry point is removed, but the module is still in sys.modules,
    # _load_plugin should ideally find it in sys.modules.
    # However, the current _load_plugin iterates entry_points first.
    # If it's not found there, it returns None. It doesn't check sys.modules independently.
    # This means if EPs change, previously loaded plugins might not be found by __getattr__
    # even if still in sys.modules under "twat.name".

    # Let's test this: remove EP, keep in sys.modules
    mock_entry_points["twat.plugins"] = []  # Remove the entry point

    # With current _load_plugin, this will now fail as it relies on finding the EP
    with pytest.raises(AttributeError, match="module 'twat' has no attribute 'cachingplugin'"):
        _ = twat.cachingplugin

    # The module is still in sys.modules, but _load_plugin won't find it via EPs
    assert sys.modules[plugin_fqn] is mock_plugin_module
    assert ep.load.call_count == 2  # Not called again

    # Clean up
    if plugin_fqn in sys.modules:
        del sys.modules[plugin_fqn]


# --- Tests for CLI runner ---


@pytest.fixture  # type: ignore[misc]
def mock_sys_argv(monkeypatch: pytest.MonkeyPatch) -> Iterator[list[str]]:
    """Fixture to mock sys.argv."""
    original_argv = sys.argv
    mocked_argv: list[str] = ["twat_script_name"]  # Simulates the script name as argv[0]
    monkeypatch.setattr(sys, "argv", mocked_argv)
    yield mocked_argv
    monkeypatch.setattr(sys, "argv", original_argv)  # Restore original argv


@pytest.fixture  # type: ignore[misc]
def mock_sys_exit(monkeypatch: pytest.MonkeyPatch) -> mock.Mock:
    """Fixture to mock sys.exit."""
    mock_exit = mock.Mock(side_effect=SystemExit)  # So it actually exits if not caught
    monkeypatch.setattr(sys, "exit", mock_exit)
    return mock_exit


def test_cli_run_plugin_success(
    mock_entry_points: dict[str, list[mock.Mock]],
    mock_sys_argv: list[str],
    mock_sys_exit: mock.Mock,
) -> None:
    """Test successful CLI execution of a plugin."""
    mock_plugin_main = mock.Mock()

    # Store original sys.argv to check it from plugin's perspective
    original_sys_argv_at_plugin_call: list[str] | None = None

    def plugin_main_wrapper() -> None:
        nonlocal original_sys_argv_at_plugin_call
        original_sys_argv_at_plugin_call = list(sys.argv)  # Capture current sys.argv
        mock_plugin_main()

    mock_cli_plugin_module = ModuleType("mock_cli_plugin_module")
    mock_cli_plugin_module.main = plugin_main_wrapper  # type: ignore[attr-defined]

    ep = mock.Mock(spec=EntryPoint)
    ep.name = "mycliprovider"
    ep.value = "mcp:main"
    ep.group = "twat.plugins"
    ep.load = mock.Mock(return_value=mock_cli_plugin_module)
    mock_entry_points["twat.plugins"] = [ep]

    mock_sys_argv.extend(["mycliprovider", "arg1", "--option"])

    with pytest.raises(SystemExit):  # Expect sys.exit to be called
        twat.main()

    mock_sys_exit.assert_called_once_with(0)
    mock_plugin_main.assert_called_once()  # type: ignore[unreachable]

    # Check that sys.argv was modified correctly for the plugin
    assert original_sys_argv_at_plugin_call is not None  # Ensuring no ignore on line 243
    assert original_sys_argv_at_plugin_call == ["twat.mycliprovider", "arg1", "--option"]


def test_cli_run_plugin_not_found(
    mock_entry_points: dict[str, list[mock.Mock]],
    mock_sys_argv: list[str],
    mock_sys_exit: mock.Mock,
) -> None:
    """Test CLI execution when plugin is not found."""
    mock_entry_points["twat.plugins"] = []
    mock_sys_argv.append("unknownplugin")

    with pytest.raises(SystemExit):
        twat.main()

    mock_sys_exit.assert_called_once_with(1)  # type: ignore[unreachable]


def test_cli_run_plugin_no_main_attribute(
    mock_entry_points: dict[str, list[mock.Mock]],
    mock_sys_argv: list[str],
    mock_sys_exit: mock.Mock,
) -> None:
    """Test CLI execution when plugin has no main attribute."""
    mock_no_main_plugin_module = ModuleType("mock_no_main_plugin_module")
    # No .main attribute

    ep = mock.Mock(spec=EntryPoint)
    ep.name = "nomainplugin"
    ep.value = "nmp:mod"
    ep.group = "twat.plugins"
    ep.load = mock.Mock(return_value=mock_no_main_plugin_module)
    mock_entry_points["twat.plugins"] = [ep]

    mock_sys_argv.append("nomainplugin")

    with pytest.raises(SystemExit):
        twat.main()

    mock_sys_exit.assert_called_once_with(1)  # type: ignore[unreachable]


def test_cli_run_plugin_main_raises_exception(
    mock_entry_points: dict[str, list[mock.Mock]],
    mock_sys_argv: list[str],
    mock_sys_exit: mock.Mock,
) -> None:
    """Test CLI execution when plugin's main function raises an exception."""
    mock_failing_plugin_main = mock.Mock(side_effect=ValueError("Plugin error"))
    mock_failing_plugin_module = ModuleType("mock_failing_plugin_module")
    mock_failing_plugin_module.main = mock_failing_plugin_main  # type: ignore[attr-defined]

    ep = mock.Mock(spec=EntryPoint)
    ep.name = "failingclplugin"
    ep.value = "fcp:main"
    ep.group = "twat.plugins"
    ep.load = mock.Mock(return_value=mock_failing_plugin_module)
    mock_entry_points["twat.plugins"] = [ep]

    mock_sys_argv.append("failingclplugin")

    with pytest.raises(SystemExit):
        twat.main()

    mock_sys_exit.assert_called_once_with(1)  # type: ignore[unreachable]
    mock_failing_plugin_main.assert_called_once()  # Removed unreachable ignore


def test_cli_no_plugin_name_provided(mock_sys_argv: list[str], mock_sys_exit: mock.Mock) -> None:
    """Test CLI behavior when no plugin name is provided."""
    # mock_sys_argv is already initialized with just ["twat_script_name"]
    # So, len(sys.argv) will be 1. twat.main() expects at least 2.

    with pytest.raises(SystemExit):
        twat.main()

    mock_sys_exit.assert_called_once_with(1)  # type: ignore[unreachable]


def test_cli_run_plugin_load_raises_exception(
    mock_entry_points: dict[str, list[mock.Mock]],
    mock_sys_argv: list[str],
    mock_sys_exit: mock.Mock,
) -> None:
    """Test CLI execution when plugin .load() raises an exception."""
    ep = mock.Mock(spec=EntryPoint)
    ep.name = "loadfailplugin"
    ep.value = "lfp:main"
    ep.group = "twat.plugins"
    ep.load = mock.Mock(side_effect=ImportError("Cannot load this plugin"))
    mock_entry_points["twat.plugins"] = [ep]

    mock_sys_argv.append("loadfailplugin")

    with pytest.raises(SystemExit):
        twat.main()

    mock_sys_exit.assert_called_once_with(1)  # type: ignore[unreachable]
    ep.load.assert_called_once()  # Removed unreachable ignore
