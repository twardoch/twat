"""
Unified maintenance script for twat plugins.

This tool checks code quality, formats files, and commits changes. It pulls configuration
from `pyproject.toml` so each plugin can customize which checks run.

CLI Usage:
    twat cleanup status     # Run linters and tests.
    twat cleanup update     # Run checks, stage changes, and commit.
    twat cleanup push       # Push to git remote.

Configuration Example (`pyproject.toml`):
    [tool.twat.cleanup]
    skip_checks = ["mypy"]          # Skip specific tools.
    src_paths = ["src"]             # What to lint.
    test_paths = ["tests"]          # What to test.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, NoReturn

try:
    import tomllib  # type: ignore[import-not-found,unused-ignore]
except ModuleNotFoundError:
    try:
        import tomli as tomllib  # type: ignore[no-redef,unused-ignore]
    except ModuleNotFoundError:
        tomllib = None  # type: ignore[assignment,unused-ignore]

from twat.dev.checks import CheckSummary, run_all_checks
from twat.dev.git_ops import git_add, git_commit, git_push, git_status, has_changes


@dataclass
class CleanupConfig:
    """
    Settings for the cleanup tool, parsed from `pyproject.toml`.

    Attributes:
        skip_checks: Tools to ignore (e.g., ["mypy"]).
        extra_steps: Currently unused. Reserved for future hooks.
        repomix: If True, generate an `llms.txt` file using repomix.
        src_paths: Folders containing source code.
        test_paths: Folders containing tests.
    """

    skip_checks: list[str] = field(default_factory=list)
    extra_steps: list[str] = field(default_factory=list)
    repomix: bool = False
    src_paths: list[str] = field(default_factory=lambda: ["src"])
    test_paths: list[str] = field(default_factory=lambda: ["tests"])


def load_config(project_dir: Path | None = None) -> CleanupConfig:
    """
    Find and parse the `[tool.twat.cleanup]` block in `pyproject.toml`.

    If the file or section doesn't exist, returns default settings.

    Args:
        project_dir: The directory containing `pyproject.toml`.

    Returns:
        A CleanupConfig object.
    """
    root = project_dir or Path.cwd()
    pyproject = root / "pyproject.toml"

    if not pyproject.exists():
        return CleanupConfig()

    if tomllib is None:
        return CleanupConfig()

    try:
        with pyproject.open("rb") as f:
            data: dict[str, Any] = tomllib.load(f)
    except Exception:
        return CleanupConfig()

    cleanup_data: dict[str, Any] = data.get("tool", {}).get("twat", {}).get("cleanup", {})
    if not cleanup_data:
        return CleanupConfig()

    return CleanupConfig(
        skip_checks=list(cleanup_data.get("skip_checks", [])),
        extra_steps=list(cleanup_data.get("extra_steps", [])),
        repomix=bool(cleanup_data.get("repomix", False)),
        src_paths=list(cleanup_data.get("src_paths", ["src"])),
        test_paths=list(cleanup_data.get("test_paths", ["tests"])),
    )


def _log(message: str, *, log_file: Path | None = None) -> None:
    """
    Print a message to the console and maybe write it to a file.

    Adds a UTC timestamp prefix.

    Args:
        message: What to say.
        log_file: Where to save it (if anywhere).
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    if log_file is not None:
        with log_file.open("a") as f:
            f.write(line + "\n")


def _print_check_results(summary: CheckSummary) -> None:
    """
    Display the results of the code quality checks.

    Shows PASS/FAIL for each tool, plus a snippet of the output so you can
    see what broke without scrolling up.

    Args:
        summary: The CheckSummary object containing all results.
    """
    for result in summary.results:
        status = "PASS" if result.ok else "FAIL"
        print(f"  [{status}] {result.tool}")
        if result.stdout.strip():
            for line in result.stdout.strip().splitlines()[:20]:
                print(f"    {line}")
        if result.stderr.strip():
            for line in result.stderr.strip().splitlines()[:10]:
                print(f"    {line}")


def cmd_status(config: CleanupConfig, cwd: Path) -> bool:
    """
    Handle the `status` command: check git and run quality tools.

    Args:
        config: What checks to run.
        cwd: Where to run them.

    Returns:
        True if everything is green.
    """
    _log(f"=== Status: {cwd.name} ===")

    _log("--- Git Status ---")
    git_result = git_status(cwd=cwd)
    if git_result.stdout.strip():
        print(git_result.stdout)

    _log("--- Code Quality Checks ---")
    summary = run_all_checks(
        cwd=cwd,
        skip=config.skip_checks,
        src_paths=config.src_paths,
        test_paths=config.test_paths,
    )
    _print_check_results(summary)

    if summary.ok:
        _log("All checks passed.")
    else:
        failed_names = ", ".join(r.tool for r in summary.failed)
        _log(f"Failed checks: {failed_names}")

    return summary.ok


def cmd_update(config: CleanupConfig, cwd: Path, *, message: str | None = None) -> bool:
    """
    Handle the `update` command: run checks, `git add`, and `git commit`.

    If the checks fail, or there are no changes, it skips the commit.

    Args:
        config: What checks to run.
        cwd: Where to run them.
        message: The commit message. Defaults to "chore: cleanup <plugin_name>".

    Returns:
        True if everything worked (or if there were simply no changes to commit).
    """
    checks_ok = cmd_status(config, cwd)

    if not has_changes(cwd=cwd):
        _log("No changes to commit.")
        return checks_ok

    _log("--- Staging Changes ---")
    add_result = git_add(cwd=cwd)
    if not add_result.ok:
        _log(f"git add failed: {add_result.stderr}")
        return False

    commit_msg = message or f"chore: cleanup {cwd.name}"
    _log(f"--- Committing: {commit_msg} ---")
    commit_result = git_commit(commit_msg, cwd=cwd)
    if commit_result.ok:
        _log("Changes committed.")
    else:
        _log(f"Commit failed: {commit_result.stderr}")
        return False

    return checks_ok


def cmd_push(cwd: Path) -> bool:
    """
    Handle the `push` command: run `git push`.

    Args:
        cwd: Where to push from.

    Returns:
        True if the push succeeded.
    """
    _log("--- Pushing ---")
    result = git_push(cwd=cwd)
    if result.ok:
        _log("Pushed successfully.")
    else:
        _log(f"Push failed: {result.stderr}")
    return result.ok


def run(argv: list[str] | None = None) -> int:
    """
    The main routing logic for the cleanup script.

    Parses arguments, loads config, and calls the appropriate `cmd_*` function.

    Args:
        argv: List of arguments. Defaults to `sys.argv[1:]`.

    Returns:
        0 if success, 1 if failure.
    """
    args = argv if argv is not None else sys.argv[1:]
    cwd = Path.cwd()
    config = load_config(cwd)

    if not args:
        _print_usage()
        return 1

    command = args[0].lower()
    if command == "status":
        ok = cmd_status(config, cwd)
    elif command == "update":
        message = args[1] if len(args) > 1 else None
        ok = cmd_update(config, cwd, message=message)
    elif command == "push":
        ok = cmd_push(cwd)
    elif command in {"help", "--help", "-h"}:
        _print_usage()
        return 0
    else:
        print(f"Unknown command: {command}")
        _print_usage()
        return 1

    return 0 if ok else 1


def _print_usage() -> None:
    """Print usage information."""
    print(
        "Usage: twat cleanup <command>\n"
        "\n"
        "Commands:\n"
        "  status    Show repository status and run code quality checks\n"
        "  update    Run checks, stage, and commit changes\n"
        "  push      Push committed changes to remote\n"
        "  help      Show this help message\n"
        "\n"
        "Configuration via pyproject.toml:\n"
        "\n"
        "  [tool.twat.cleanup]\n"
        '  skip_checks = ["mypy"]    # skip specific checks\n'
        "  repomix = false            # run repomix at end\n"
    )


def main() -> NoReturn:
    """
    The script entry point defined in `pyproject.toml`.

    Just calls `run()` and exits with the returned status code.
    """
    sys.exit(run())


if __name__ == "__main__":
    main()
