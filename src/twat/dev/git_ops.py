"""
Git helpers for the twat plugin ecosystem.

Wraps common git commands (`status`, `add`, `commit`, `push`) into a cleaner
Python API. Primarily used by maintenance scripts and CLI tools that need
to manage plugin repositories.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class GitResult:
    """
    The outcome of running a git command.

    Attributes:
        command: The subcommand executed (e.g., "commit").
        returncode: 0 means success. Anything else is an error.
        stdout: The raw text git printed to standard out.
        stderr: The raw text git printed to standard error.
    """

    command: str
    returncode: int
    stdout: str = ""
    stderr: str = ""

    @property
    def ok(self) -> bool:
        """Did the command succeed? (return code 0)"""
        return self.returncode == 0


def _run_git(
    args: list[str],
    *,
    cwd: Path | None = None,
) -> GitResult:
    """
    Execute a git command and grab its output.

    Args:
        args: The arguments to pass to `git` (e.g., ["log", "-n", "1"]).
        cwd: Where to run the command. Defaults to the current directory.

    Returns:
        A GitResult object containing the exit code and outputs.
    """
    cmd = ["git", *args]
    command_name = args[0] if args else "git"
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd,
            check=False,
        )
        return GitResult(
            command=command_name,
            returncode=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
        )
    except FileNotFoundError:
        return GitResult(
            command=command_name,
            returncode=127,
            stderr="git: command not found",
        )
    except OSError as exc:
        return GitResult(
            command=command_name,
            returncode=1,
            stderr=str(exc),
        )


def git_status(
    *,
    porcelain: bool = False,
    cwd: Path | None = None,
) -> GitResult:
    """
    Run `git status`.

    Args:
        porcelain: If True, outputs in a script-friendly format instead of human-readable text.
        cwd: Where to run the command.

    Returns:
        The result of the status command.
    """
    args = ["status"]
    if porcelain:
        args.append("--porcelain")
    return _run_git(args, cwd=cwd)


def has_changes(cwd: Path | None = None) -> bool:
    """
    Are there any modified, added, or deleted files?

    Runs `git status --porcelain` to find out.

    Args:
        cwd: Where to check.

    Returns:
        True if the working directory is dirty.
    """
    result = git_status(porcelain=True, cwd=cwd)
    return bool(result.stdout.strip())


def git_add(
    *paths: str | Path,
    cwd: Path | None = None,
) -> GitResult:
    """
    Stage files for the next commit.

    Args:
        paths: What to stage. Defaults to the current directory (".").
        cwd: Where to run the command.

    Returns:
        The result of the `git add` command.
    """
    targets = [str(p) for p in paths] if paths else ["."]
    return _run_git(["add", *targets], cwd=cwd)


def git_commit(
    message: str,
    *,
    cwd: Path | None = None,
) -> GitResult:
    """
    Record changes to the repository.

    Args:
        message: The commit message.
        cwd: Where to run the command.

    Returns:
        The result of the `git commit` command.
    """
    return _run_git(["commit", "-m", message], cwd=cwd)


def git_push(
    *,
    remote: str = "origin",
    branch: str | None = None,
    cwd: Path | None = None,
) -> GitResult:
    """
    Upload local repository content to a remote repository.

    Args:
        remote: The remote to push to. Defaults to "origin".
        branch: The branch to push. If omitted, uses the current active branch.
        cwd: Where to run the command.

    Returns:
        The result of the `git push` command.
    """
    args = ["push", remote]
    if branch:
        args.append(branch)
    return _run_git(args, cwd=cwd)


def git_current_branch(cwd: Path | None = None) -> str:
    """
    Find out what branch we are currently on.

    Args:
        cwd: Where to run the command.

    Returns:
        The branch name, or "HEAD" if we're in a detached HEAD state.
    """
    result = _run_git(["rev-parse", "--abbrev-ref", "HEAD"], cwd=cwd)
    return result.stdout.strip() if result.ok else "HEAD"
