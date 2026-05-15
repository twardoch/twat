"""
twat.dev: Development and maintenance tools.

This module provides a unified set of tools for managing twat plugins. It replaces
the messy situation where every plugin had its own slightly different `cleanup.py` script.

Now, you can just run `twat cleanup status` or `twat cleanup update` in any plugin directory.

CLI Usage:
    twat cleanup status     # Check for uncommitted changes and run linters.
    twat cleanup update     # Run checks, then automatically stage and commit.
    twat cleanup push       # Push your changes to the remote repository.

Configuration:
    Add this to a plugin's `pyproject.toml` to customize the cleanup tool:
    ```toml
    [tool.twat.cleanup]
    skip_checks = ["mypy"] # Skip specific tools
    ```
"""

from __future__ import annotations

from twat.dev.checks import run_mypy, run_pytest, run_ruff_check, run_ruff_format
from twat.dev.cleanup import CleanupConfig, run
from twat.dev.git_ops import git_add, git_commit, git_push, git_status

__all__ = [
    "CleanupConfig",
    "git_add",
    "git_commit",
    "git_push",
    "git_status",
    "run",
    "run_mypy",
    "run_pytest",
    "run_ruff_check",
    "run_ruff_format",
]
