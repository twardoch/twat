# twat_llm Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` or equivalent task-by-task execution. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Own text-heavy LLM APIs, prompt/chat/batch chains, multimodal text interfaces, and LLM-powered text operations used by twat_text.

**Architecture:** Preserve the standard twat plugin contract: PyPI package `twat-llm`, import module `twat_llm`, entry point `llm = twat_llm`, public `main()`, explicit `__all__`, README examples, and tests. Keep provider/API integrations behind thin clients and keep user-facing domain functions small.

**Tech Stack:** Python 3.10+ unless the package already requires 3.12, pytest, ruff, mypy, loguru, fire where the package already uses CLI dispatch.

---

## Current State

- Path: `plugins/repos/twat_llm`.
- Entry point name: `llm`.
- Tier: `medium`.
- See `issues/102-current.md` for repository-wide inventory and reference-code reuse decisions.

## Scope

`twat_llm` is the text-heavy LLM interface. It should be the only package that owns prompt/chat/batch/chain abstractions for text and text-centric multimodal work.

## Files

- Modify/Create under: `plugins/repos/twat_llm/src/twat_llm/`
- Modify: `plugins/repos/twat_llm/README.md`
- Modify/Create: `plugins/repos/twat_llm/tests/`
- Coordinate with: `plugins/repos/twat_text/`

## Tasks

- [ ] Keep current `mallmo.ask`, `ask_chain`, and `ask_batch` behavior covered by tests.
- [ ] Clarify public API names and exports in `__init__.py`.
- [ ] Add `[project.entry-points."twat.plugins"]` with `llm = "twat_llm"` if missing.
- [ ] Decide and implement the direct package CLI surface (`python -m twat_llm` and/or `twat-llm`) without requiring live provider credentials for `--help`.
- [ ] Add a stable adapter surface for `twat_text` operations: summarize, rewrite, extract structured data, classify.
- [ ] Keep image/multimodal support only where it is text-centric; non-text media generation belongs in `twat_genai`.
- [ ] Add mocked tests for provider errors, batch behavior, adapter calls, and CLI help; keep live provider tests separate and opt-in.
- [ ] Update README with boundary statement: `twat_llm` for text-heavy LLM; `twat_genai` for generated media.
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
