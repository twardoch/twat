"""Tests for the `twat` host CLI dispatcher.

this_file: tests/test_host_cli.py
"""

from __future__ import annotations

import subprocess
import sys


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "twat", *args],
        check=False,
        capture_output=True,
        text=True,
    )


def test_no_args_prints_help_to_stdout_exit_0() -> None:
    res = _run()
    assert res.returncode == 0
    assert "Usage: twat" in res.stdout
    assert res.stdout != ""


def test_help_flag_exit_0_stdout() -> None:
    res = _run("--help")
    assert res.returncode == 0
    assert "Usage: twat" in res.stdout


def test_list_subcommand() -> None:
    res = _run("--list")
    assert res.returncode == 0


def test_available_subcommand() -> None:
    # The host package itself is installed in the test env, so --available
    # lists at least the `twat` distribution.
    res = _run("--available")
    assert res.returncode == 0
    assert "twat" in res.stdout


def test_doctor_subcommand() -> None:
    # No plugins installed in the isolated test env -> all healthy, exit 0.
    res = _run("--doctor")
    assert res.returncode == 0


def test_completions_zsh() -> None:
    res = _run("--completions", "zsh")
    assert res.returncode == 0
    assert "#compdef twat" in res.stdout


def test_completions_bash() -> None:
    res = _run("--completions", "bash")
    assert res.returncode == 0
    assert "complete -F _twat_complete twat" in res.stdout


def test_completions_bad_shell() -> None:
    res = _run("--completions", "tcsh")
    assert res.returncode == 2
    assert "bash" in res.stderr


def test_missing_plugin_error() -> None:
    res = _run("definitely-not-a-plugin")
    assert res.returncode == 1
    assert "not found" in res.stderr.lower()
