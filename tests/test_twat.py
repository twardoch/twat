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


def make_distribution(name: str, version: str, plugin: str | None = None) -> mock.Mock:
    """Create a mocked installed distribution, optionally exposing a plugin EP."""
    dist = mock.Mock()
    dist.metadata = {"Name": name}
    dist.version = version
    eps: list[mock.Mock] = []
    if plugin is not None:
        ep = mock.Mock(spec=EntryPoint)
        ep.name = plugin
        ep.group = "twat.plugins"
        ep.value = name.replace("-", "_")
        eps.append(ep)
    dist.entry_points = eps
    return dist


@pytest.fixture
def distributions(monkeypatch: pytest.MonkeyPatch) -> list[mock.Mock]:
    """Mock the set of installed distributions seen by importlib.metadata."""
    dists: list[mock.Mock] = []

    def fake_distributions() -> list[mock.Mock]:
        return dists

    monkeypatch.setattr("importlib.metadata.distributions", fake_distributions)
    return dists


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
    assert "--completions" in output


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


# --- Plugin registry contract -------------------------------------------------


def test_plugin_registry_group_is_stable() -> None:
    """The host scans a single, well-known entry-point group for plugins."""
    assert twat.PLUGIN_GROUP == "twat.plugins"


def test_plugin_registry_discovers_registered_entry_point(entry_points: list[mock.Mock]) -> None:
    """A package registered under twat.plugins is discoverable and loadable."""
    plugin = ModuleType("registered")
    plugin.greeting = "hi"  # type: ignore[attr-defined]
    entry_points.append(make_entry_point("registered", plugin))
    sys.modules.pop("twat.registered", None)

    # Discoverable by name without importing...
    assert "registered" in twat.iter_plugins()
    # ...and resolvable via the namespace proxy.
    assert twat.registered is plugin
    assert twat.registered.greeting == "hi"

    sys.modules.pop("twat.registered", None)


# --- iter_available_plugins / --available ------------------------------------


def test_iter_available_plugins_filters_and_annotates(distributions: list[mock.Mock]) -> None:
    """Only twat / twat-* distros are returned, annotated with their plugin name."""
    distributions.extend(
        [
            make_distribution("twat", "2.7.18"),
            make_distribution("twat-fs", "2.7.17", plugin="fs"),
            make_distribution("twat_cache", "2.6.7", plugin="cache"),  # underscore form
            make_distribution("requests", "2.32.0"),  # unrelated, excluded
        ]
    )

    available = twat.iter_available_plugins()
    names = [a.distribution for a in available]

    assert names == ["twat", "twat-cache", "twat-fs"]
    by_name = {a.distribution: a for a in available}
    assert by_name["twat-fs"].plugin_name == "fs"
    assert by_name["twat-cache"].plugin_name == "cache"  # normalized from twat_cache
    assert by_name["twat"].plugin_name is None


def test_cli_available_lists_distributions(
    distributions: list[mock.Mock],
    argv: list[str],
    capsys: pytest.CaptureFixture[str],
) -> None:
    """twat --available prints distribution / version / plugin rows."""
    distributions.append(make_distribution("twat-fs", "2.7.17", plugin="fs"))
    argv.append("--available")

    with pytest.raises(SystemExit) as exc_info:
        twat.main()

    assert exc_info.value.code == 0
    assert capsys.readouterr().out.splitlines() == ["twat-fs\t2.7.17\tfs"]


def test_cli_list_available_combination(
    distributions: list[mock.Mock],
    argv: list[str],
    capsys: pytest.CaptureFixture[str],
) -> None:
    """twat --list --available widens listing to installed distributions."""
    distributions.append(make_distribution("twat-os", "2.7.8", plugin="os"))
    argv.extend(["--list", "--available"])

    with pytest.raises(SystemExit) as exc_info:
        twat.main()

    assert exc_info.value.code == 0
    assert "twat-os\t2.7.8\tos" in capsys.readouterr().out


# --- doctor / --doctor -------------------------------------------------------


def test_doctor_reports_health_per_plugin(entry_points: list[mock.Mock]) -> None:
    """doctor() imports each plugin and flags the ones that fail to load."""
    good = make_entry_point("good", ModuleType("good"))
    bad = make_entry_point("bad", None)
    bad.load = mock.Mock(side_effect=RuntimeError("boom"))
    entry_points.extend([good, bad])

    report = {h.name: h for h in twat.doctor()}

    assert report["good"].ok is True
    assert report["bad"].ok is False
    assert report["bad"].error is not None
    assert "boom" in report["bad"].error


def test_cli_doctor_exit_code_reflects_health(
    entry_points: list[mock.Mock],
    argv: list[str],
    capsys: pytest.CaptureFixture[str],
) -> None:
    """twat --doctor exits non-zero when any plugin is broken."""
    bad = make_entry_point("broken", None)
    bad.load = mock.Mock(side_effect=ImportError("missing dep"))
    entry_points.append(bad)
    argv.append("--doctor")

    with pytest.raises(SystemExit) as exc_info:
        twat.main()

    assert exc_info.value.code == 1
    out = capsys.readouterr().out
    assert "[FAIL] broken" in out


def test_cli_doctor_all_healthy_exit_zero(
    entry_points: list[mock.Mock],
    argv: list[str],
    capsys: pytest.CaptureFixture[str],
) -> None:
    """twat --doctor exits 0 when every plugin loads cleanly."""
    entry_points.append(make_entry_point("ok", ModuleType("ok")))
    argv.append("--doctor")

    with pytest.raises(SystemExit) as exc_info:
        twat.main()

    assert exc_info.value.code == 0
    assert "[OK] ok" in capsys.readouterr().out
