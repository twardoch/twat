# twat_hatch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` or equivalent task-by-task execution. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Keep package scaffolding focused and consistent with ecosystem metadata and README conventions.

**Architecture:** Preserve the standard twat plugin contract: PyPI package `twat-hatch`, import module `twat_hatch`, entry point `hatch = twat_hatch`, public `main()`, explicit `__all__`, README examples, and tests. Keep provider/API integrations behind thin clients and keep user-facing domain functions small.

**Tech Stack:** Python 3.10+ unless the package already requires 3.12, pytest, ruff, mypy, loguru, fire where the package already uses CLI dispatch.

---

## Current State

- Path: `plugins/repos/twat_hatch`.
- Entry point name: `hatch`.
- Tier: `medium`.
- See `issues/102-current.md` for repository-wide inventory and reference-code reuse decisions.

## Scope

This package is not a primary media target for `issues/101.md`, but it must remain compatible with the cleaned host/plugin ecosystem.

## Files

- Modify if needed: `plugins/repos/twat_hatch/pyproject.toml`
- Modify if needed: `plugins/repos/twat_hatch/src/twat_hatch/__init__.py`
- Modify if needed: `plugins/repos/twat_hatch/README.md`
- Modify/Create if needed: `plugins/repos/twat_hatch/tests/`

## Tasks

- [ ] Confirm package name, import module, script, and `twat.plugins` entry point follow the ecosystem standard.
- [ ] Confirm `__init__.py` defines metadata version, public exports, and `main()`.
- [ ] Update README with current install, CLI, Python API, and development commands.
- [ ] Add or refresh import/CLI smoke tests if missing.
- [ ] Run package tests, lint, type-check, and CLI help.

## Acceptance Criteria

- [ ] Package installs in editable mode with declared dev/test dependencies.
- [ ] `python -m PACKAGE_OR_MODULE --help` or package CLI help works where applicable.
- [ ] `twat ENTRY --help` dispatch works from the host when the package is installed.
- [ ] Public imports listed in `__all__` import successfully.
- [ ] README matches actual commands and package boundaries.
- [ ] Tests, lint, and type-check pass, or pre-existing unrelated failures are documented with exact commands.

## Dependencies

- Depends on `issues/101.md` and `issues/102-current.md`.
- Media packages must respect the boundary: `twat_llm` owns text-heavy LLM; `twat_genai` owns generative media providers; domain packages call those shared packages.
