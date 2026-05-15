# Host Package Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` or equivalent task-by-task execution. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the `twat` host a reliable plugin discovery and CLI dispatch layer for the cleaned plugin ecosystem.

**Architecture:** Keep the host lightweight. Do not import plugin code directly; use `importlib.metadata` entry points and small CLI helpers for listing, help, and dispatch.

**Tech Stack:** Python 3.10+, importlib.metadata, fire-compatible plugin CLIs, pytest, ruff, mypy.

---

## Problem

The host already discovers plugins dynamically, but its CLI usage text advertises `--list` and `--help` without implementing them. Plain root tests can also import a globally installed `twat` package instead of local `src/twat`, producing misleading success. The ecosystem cleanup needs a dependable local-source surface to discover and smoke-test all plugins.

## Files

- Modify: `src/twat/__init__.py`
- Modify: `tests/test_twat.py`
- Modify: `README.md`
- Reference: `issues/102-current.md`

## Tasks

- [ ] Add tests for `twat --list`, `twat --help`, missing plugin, plugin with no `main()`, plugin caching, and local-source import isolation.
- [ ] Implement a private `iter_plugins()` helper returning sorted entry point names without importing plugin modules.
- [ ] Fix `_load_plugin()` caching by checking `sys.modules["twat.<name>"]` before loading and setting the loaded module as an attribute on the host package.
- [ ] Implement `--list` in `main()` and print one plugin name per line.
- [ ] Implement `--help` in `main()` and document usage, list command, and dispatch behavior.
- [ ] Keep `twat <plugin> [args...]` behavior unchanged for installed plugins.
- [ ] Update README host CLI section with `twat --list`, `twat --help`, plugin dispatch examples, and the relationship between `twat-cleanup` and any documented `twat cleanup` command.
- [ ] Run `hatch run test`, `hatch run lint`, and `hatch run type-check` from repo root.
- [ ] Manually QA with `python -m twat --help`, `twat --help`, and `twat --list` in the active environment.

## Acceptance Criteria

- [ ] `twat --list` works without importing plugin modules.
- [ ] `twat --help` matches README behavior.
- [ ] Existing plugin dispatch continues to call plugin `main()`.
- [ ] Host tests pass.
