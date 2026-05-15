# twat_font Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` or equivalent task-by-task execution. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make this the canonical home for font organizer behavior currently duplicated/misnamed in twat_video.

**Architecture:** Preserve the standard twat plugin contract: PyPI package `twat-font`, import module `twat_font`, entry point `font = twat_font`, public `main()`, explicit `__all__`, README examples, and tests. Keep provider/API integrations behind thin clients and keep user-facing domain functions small.

**Tech Stack:** Python 3.10+ unless the package already requires 3.12, pytest, ruff, mypy, loguru, fire where the package already uses CLI dispatch.

---

## Current State

- Path: `plugins/repos/twat_font`.
- Entry point name: `font`.
- Tier: `medium`.
- See `issues/102-current.md` for repository-wide inventory and reference-code reuse decisions.

## Scope

`twat_font` should be the canonical font organizer package and should absorb/preserve any font functionality still living in `twat_video`.

## Files

- Modify: `plugins/repos/twat_font/pyproject.toml`
- Modify/Create under: `plugins/repos/twat_font/src/twat_font/`
- Modify/Create: `plugins/repos/twat_font/tests/`
- Reference/coordinate: `plugins/repos/twat_video/src/font_organizer/`

## Tasks

- [ ] Fix pyproject build/source/test/type-check paths if they still point at `src/font_organizer` while source lives in `src/twat_font`.
- [ ] Compare `twat_font` and `twat_video/src/font_organizer` for unique functionality.
- [ ] Preserve any unique font behavior in `twat_font` before `twat_video` becomes real video.
- [ ] Fix direct script targets such as `font-organizer = "font_organizer.cli:main"` to canonical `twat_font` module paths.
- [ ] Add `[project.entry-points."twat.plugins"]` with `font = "twat_font"` if missing.
- [ ] Update README with install, CLI, and Python API examples.
- [ ] Run tests, lint, type-check, and CLI help.

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
