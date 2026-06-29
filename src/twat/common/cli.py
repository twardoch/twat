"""Shared CLI helpers for the twat host and plugins.

this_file: src/twat/common/cli.py
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from importlib import metadata
from typing import Any


def make_version_callable(package: str) -> Callable[[], str]:
    """Return a zero-arg callable suitable as a Fire `version` leaf."""

    def _version() -> str:
        return metadata.version(package)

    _version.__doc__ = f"Print the installed version of {package}."
    return _version


def error(msg: str, code: int = 1) -> None:
    """Print a single-line error to stderr and exit with `code`."""
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(code)


def print_data(value: Any) -> None:
    """Render a return value to stdout. Rich for structured data, plain otherwise."""
    if isinstance(value, (str, int, float, bool)) or value is None:
        print(value)
        return
    try:
        from rich import print as rprint

        rprint(value)
    except Exception:
        print(value)


def _twat_console_scripts() -> list[str]:
    """All installed console-script entry-point names starting with 'twat-' or 'twat'.

    Enumerates the ``console_scripts`` entry-point group (not ``twat.plugins``):
    every plugin registers one dashed script per CLI leaf (e.g.
    ``twat-image-gray2alpha``), so this is what shell completion offers after
    ``twat-<TAB>``. The host's own ``twat`` script is always seeded so completion
    works even with no plugins installed. Reads metadata only — nothing imported.
    """
    names: set[str] = {"twat"}
    for ep in metadata.entry_points(group="console_scripts"):
        if ep.name == "twat" or ep.name.startswith("twat-"):
            names.add(ep.name)
    return sorted(names)


def emit_completions(shell: str) -> str:
    """Return a completion script for `shell` listing twat-* commands."""
    cmds = _twat_console_scripts()
    if shell == "bash":
        body = " ".join(cmds)
        return (
            "# twat bash completion (source this file)\n"
            f"_twat_cmds='{body}'\n"
            "_twat_complete() {\n"
            '    local cur="${COMP_WORDS[COMP_CWORD]}"\n'
            '    COMPREPLY=( $(compgen -W "$_twat_cmds" -- "$cur") )\n'
            "}\n"
            "complete -F _twat_complete twat\n"
        )
    if shell == "zsh":
        words = " ".join(f"'{c}'" for c in cmds)
        return (
            "#compdef twat\n"
            "_twat() {\n"
            f"  local -a _twat_cmds=({words})\n"
            "  _describe 'twat plugin' _twat_cmds\n"
            "}\n"
            '_twat "$@"\n'
        )
    if shell == "fish":
        lines = [f"complete -c twat -f -a '{c}'" for c in cmds if c != "twat"]
        return "\n".join(lines) + "\n"
    msg = f"unsupported shell: {shell}"
    raise ValueError(msg)
