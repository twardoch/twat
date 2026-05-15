"""
Run code quality tools across the twat ecosystem.

Wraps `ruff` (linting & formatting), `mypy` (type checking), and `pytest` (testing)
into a unified Python API. Useful for building CI/CD scripts or local dev tools.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class CheckResult:
    """
    The outcome of running a specific code quality tool.

    Attributes:
        tool: Which tool ran (e.g., "ruff check").
        returncode: 0 means success. Anything else is a failure.
        stdout: The tool's standard output.
        stderr: The tool's error output.
    """

    tool: str
    returncode: int
    stdout: str = ""
    stderr: str = ""

    @property
    def ok(self) -> bool:
        """Did the tool complete without errors? (return code 0)"""
        return self.returncode == 0


@dataclass
class CheckSummary:
    """
    A collection of results from running a suite of tools.

    Attributes:
        results: Every tool run and its outcome.
    """

    results: list[CheckResult] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """Did every single tool in the suite pass?"""
        return all(r.ok for r in self.results)

    @property
    def failed(self) -> list[CheckResult]:
        """A list of only the tools that failed."""
        return [r for r in self.results if not r.ok]


def _run_tool(
    cmd: list[str],
    *,
    tool_name: str,
    cwd: Path | None = None,
) -> CheckResult:
    """
    Execute a shell command and capture the output.

    Args:
        cmd: The exact command array to run (e.g., ["python", "-m", "pytest"]).
        tool_name: A friendly name for reporting (e.g., "pytest").
        cwd: Where to run the command. Defaults to the current directory.

    Returns:
        A CheckResult object with the tool's exit code and outputs.
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd,
            check=False,
        )
        return CheckResult(
            tool=tool_name,
            returncode=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
        )
    except FileNotFoundError:
        return CheckResult(
            tool=tool_name,
            returncode=127,
            stderr=f"Command not found: {cmd[0]}",
        )
    except OSError as exc:
        return CheckResult(
            tool=tool_name,
            returncode=1,
            stderr=str(exc),
        )


def run_ruff_check(
    *paths: str | Path,
    fix: bool = True,
    unsafe_fixes: bool = False,
    cwd: Path | None = None,
) -> CheckResult:
    """
    Run `ruff check` to find and fix linting errors.

    Args:
        paths: What to lint. Defaults to "src" and "tests".
        fix: If True, tell ruff to fix whatever it can automatically.
        unsafe_fixes: If True, allow ruff to make riskier auto-fixes.
        cwd: Where to run the command.

    Returns:
        The result of the ruff check.
    """
    targets = [str(p) for p in paths] if paths else ["src", "tests"]
    cmd = ["python", "-m", "ruff", "check"]
    if fix:
        cmd.append("--fix")
    if unsafe_fixes:
        cmd.append("--unsafe-fixes")
    cmd.extend(targets)
    return _run_tool(cmd, tool_name="ruff check", cwd=cwd)


def run_ruff_format(
    *paths: str | Path,
    check_only: bool = False,
    cwd: Path | None = None,
) -> CheckResult:
    """
    Run `ruff format` to auto-format code.

    Args:
        paths: What to format. Defaults to "src" and "tests".
        check_only: If True, don't change files—just return an error if formatting is needed.
        cwd: Where to run the command.

    Returns:
        The result of the formatting run.
    """
    targets = [str(p) for p in paths] if paths else ["src", "tests"]
    cmd = ["python", "-m", "ruff", "format"]
    if check_only:
        cmd.append("--check")
    cmd.extend(["--respect-gitignore", *targets])
    return _run_tool(cmd, tool_name="ruff format", cwd=cwd)


def run_mypy(
    *paths: str | Path,
    cwd: Path | None = None,
) -> CheckResult:
    """
    Run `mypy` to statically type-check the code.

    Args:
        paths: What to type-check. Defaults to "src".
        cwd: Where to run the command.

    Returns:
        The result of the mypy run.
    """
    targets = [str(p) for p in paths] if paths else ["src"]
    cmd = ["python", "-m", "mypy", *targets]
    return _run_tool(cmd, tool_name="mypy", cwd=cwd)


def run_pytest(
    *paths: str | Path,
    cwd: Path | None = None,
    extra_args: list[str] | None = None,
) -> CheckResult:
    """
    Run `pytest` to execute tests.

    Args:
        paths: Where the tests are located. Defaults to "tests".
        cwd: Where to run the command.
        extra_args: Any other flags to pass to pytest (e.g., ["-v", "-k", "foo"]).

    Returns:
        The result of the test run.
    """
    targets = [str(p) for p in paths] if paths else ["tests"]
    cmd = ["python", "-m", "pytest", *targets]
    if extra_args:
        cmd.extend(extra_args)
    return _run_tool(cmd, tool_name="pytest", cwd=cwd)


def run_all_checks(
    cwd: Path | None = None,
    *,
    skip: list[str] | None = None,
    src_paths: list[str] | None = None,
    test_paths: list[str] | None = None,
) -> CheckSummary:
    """
    Run the full suite of quality checks.

    The sequence is:
    1. Lint (`ruff check`)
    2. Format (`ruff format`)
    3. Type-check (`mypy`)
    4. Test (`pytest`)

    Args:
        cwd: The root of the plugin directory.
        skip: A list of tools to ignore (e.g., ["pytest"] if tests are broken).
        src_paths: Where source code lives. Defaults to ["src"].
        test_paths: Where test code lives. Defaults to ["tests"].

    Returns:
        A CheckSummary combining all the individual tool runs.
    """
    skip_set = {s.lower() for s in (skip or [])}
    src = src_paths or ["src"]
    tests = test_paths or ["tests"]
    all_paths = [*src, *tests]
    summary = CheckSummary()

    if "ruff" not in skip_set and "ruff check" not in skip_set:
        summary.results.append(run_ruff_check(*all_paths, cwd=cwd))

    if "ruff" not in skip_set and "ruff format" not in skip_set:
        summary.results.append(run_ruff_format(*all_paths, cwd=cwd))

    if "mypy" not in skip_set:
        summary.results.append(run_mypy(*src, cwd=cwd))

    if "pytest" not in skip_set and "tests" not in skip_set:
        summary.results.append(run_pytest(*tests, cwd=cwd))

    return summary
