# twat_text Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` or equivalent task-by-task execution. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace scaffold with user-facing text processing package using twat_llm plus deterministic text algorithms.

**Architecture:** Preserve the standard twat plugin contract: PyPI package `twat-text`, import module `twat_text`, entry point `text = twat_text`, public `main()`, explicit `__all__`, README examples, and tests. Keep provider/API integrations behind thin clients and keep user-facing domain functions small.

**Tech Stack:** Python 3.10+ unless the package already requires 3.12, pytest, ruff, mypy, loguru, fire where the package already uses CLI dispatch.

---

## Current State

- Path: `plugins/repos/twat_text`.
- Entry point name: `text`.
- Tier: `skeleton`.
- See `issues/102-current.md` for repository-wide inventory and reference-code reuse decisions.

## Scope

`twat_text` is a scaffold and should become the user-facing text package. Deterministic text utilities live here; LLM-powered operations call `twat_llm`.

## Files

- Modify/Create under: `plugins/repos/twat_text/src/twat_text/`
- Modify: `plugins/repos/twat_text/README.md`
- Modify/Create: `plugins/repos/twat_text/tests/`
- Coordinate with: `plugins/repos/twat_llm/`

## Tasks

- [ ] Replace scaffold API with text cleaning, normalization, chunking, extraction helpers, Markdown/plain/HTML conversion boundaries, and token/context utilities.
- [ ] Add optional LLM-powered summarize/rewrite/extract functions that call `twat_llm` through a narrow adapter.
- [ ] Keep deterministic functions dependency-light and fully tested.
- [ ] Add CLI commands for clean, chunk, convert, summarize, and rewrite.
- [ ] Update README with deterministic and LLM-backed examples.
- [ ] Add tests for chunking edge cases, normalization, and mocked `twat_llm` calls.
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
