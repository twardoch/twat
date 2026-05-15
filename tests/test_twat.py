"""Tests for the twat plugin host."""

from __future__ import annotations

import sys
from importlib.metadata import EntryPoint
from types import ModuleType
from unittest import mock

import pytest

import twat


@pytest.fixture
def entry_points(monkeypatch: pytest.MonkeyPatch) -> list[mock.Mock]:
    """Mock the twat plugin entry point group."""
    eps: list[mock.Mock] = []

    def fake_entry_points(*, group: str) -> list[mock.Mock]:
        return eps if group == "twat.plugins" else []

    monkeypatch.setattr("importlib.metadata.entry_points", fake_entry_points)
    return eps


@pytest.fixture
def argv(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    """Provide mutable CLI argv for host tests."""
    value = ["twat"]
    monkeypatch.setattr(sys, "argv", value)
    return value


def make_entry_point(name: str, loaded: object) -> mock.Mock:
    """Create a mocked importlib entry point."""
    ep = mock.Mock(spec=EntryPoint)
    ep.name = name
    ep.group = "twat.plugins"
    ep.value = f"example_{name}"
    ep.load = mock.Mock(return_value=loaded)
    return ep


def test_version() -> None:
    """The host exposes its installed version."""
    assert twat.__version__


def test_iter_plugins_returns_sorted_names_without_importing(entry_points: list[mock.Mock]) -> None:
    """Plugin listing uses entry point metadata and does not import plugins."""
    first = make_entry_point("zeta", ModuleType("zeta"))
    second = make_entry_point("alpha", ModuleType("alpha"))
    entry_points.extend([first, second])

    assert twat.iter_plugins() == ("alpha", "zeta")
    first.load.assert_not_called()
    second.load.assert_not_called()


def test_load_plugin_success(entry_points: list[mock.Mock]) -> None:
    """Attribute access loads and registers a matching plugin module."""
    plugin = ModuleType("example_plugin")
    plugin.answer = 42  # type: ignore[attr-defined]
    ep = make_entry_point("example", plugin)
    entry_points.append(ep)
    sys.modules.pop("twat.example", None)

    assert twat.example is plugin
    assert sys.modules["twat.example"] is plugin
    assert twat.example.answer == 42
    ep.load.assert_called()

    sys.modules.pop("twat.example", None)


def test_load_plugin_not_found(entry_points: list[mock.Mock]) -> None:
    """Missing plugins raise the host plugin error with context."""
    with pytest.raises(twat.PluginError, match="module 'twat' has no attribute 'missing'"):
        _ = twat.missing


def test_cli_help(argv: list[str], capsys: pytest.CaptureFixture[str]) -> None:
    """twat --help prints host usage."""
    argv.append("--help")

    with pytest.raises(SystemExit) as exc_info:
        twat.main()

    assert exc_info.value.code == 0
    output = capsys.readouterr().out
    assert "Usage: twat <plugin_name> [args...]" in output
    assert "twat --list" in output
    assert "twat.plugins" in output


def test_cli_list_does_not_import_plugins(
    entry_points: list[mock.Mock],
    argv: list[str],
    capsys: pytest.CaptureFixture[str],
) -> None:
    """twat --list prints sorted plugin names without loading modules."""
    first = make_entry_point("mp", ModuleType("mp"))
    second = make_entry_point("ez", ModuleType("ez"))
    entry_points.extend([first, second])
    argv.append("--list")

    with pytest.raises(SystemExit) as exc_info:
        twat.main()

    assert exc_info.value.code == 0
    assert capsys.readouterr().out.splitlines() == ["ez", "mp"]
    first.load.assert_not_called()
    second.load.assert_not_called()


def test_cli_dispatch_preserves_plugin_argv(entry_points: list[mock.Mock], argv: list[str]) -> None:
    """twat <plugin> [args...] rewrites argv and calls plugin main()."""
    observed_argv: list[str] = []

    def plugin_main() -> None:
        observed_argv[:] = sys.argv

    plugin = ModuleType("cli_plugin")
    plugin.main = plugin_main  # type: ignore[attr-defined]
    ep = make_entry_point("demo", plugin)
    entry_points.append(ep)
    argv.extend(["demo", "--flag", "value"])

    with pytest.raises(SystemExit) as exc_info:
        twat.main()

    assert exc_info.value.code == 0
    assert observed_argv == ["twat.demo", "--flag", "value"]


def test_cli_missing_plugin(entry_points: list[mock.Mock], argv: list[str], capsys: pytest.CaptureFixture[str]) -> None:
    """Unknown plugin subcommands fail clearly."""
    argv.append("missing")

    with pytest.raises(SystemExit) as exc_info:
        twat.main()

    assert exc_info.value.code == 1
    assert "Plugin 'missing' not found" in capsys.readouterr().err


def test_cli_plugin_with_no_main(
    entry_points: list[mock.Mock],
    argv: list[str],
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Plugins must expose a callable main() for CLI dispatch."""
    entry_points.append(make_entry_point("nomain", ModuleType("nomain")))
    argv.append("nomain")

    with pytest.raises(SystemExit) as exc_info:
        twat.main()

    assert exc_info.value.code == 1
    assert "has no callable main()" in capsys.readouterr().err
