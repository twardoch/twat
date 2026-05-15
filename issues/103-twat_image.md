# twat_image Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` or equivalent task-by-task execution. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Become user-facing image manipulation package with algorithmic utilities and wrappers around twat_genai image generation/editing.

**Architecture:** Preserve the standard twat plugin contract: PyPI package `twat-image`, import module `twat_image`, entry point `image = twat_image`, public `main()`, explicit `__all__`, README examples, and tests. Keep provider/API integrations behind thin clients and keep user-facing domain functions small.

**Tech Stack:** Python 3.10+ unless the package already requires 3.12, pytest, ruff, mypy, loguru, fire where the package already uses CLI dispatch.

---

## Current State

- Path: `plugins/repos/twat_image`.
- Entry point name: `image`.
- Tier: `medium`.
- See `issues/102-current.md` for repository-wide inventory and reference-code reuse decisions.

## Scope

`twat_image` is the user-facing image package. It should own deterministic image operations and call `twat_genai` for AI image generation/editing rather than embedding provider clients.

## Files

- Fix/modify: `plugins/repos/twat_image/pyproject.toml`
- Modify/Create under: `plugins/repos/twat_image/src/twat_image/`
- Remove or deprecate: `plugins/repos/twat_image/src/image_alpha_utils/` after preserving import compatibility only if tests require it.
- Modify/Create: `plugins/repos/twat_image/tests/`
- Reference: `reference/bin-img-vid/imggray2alpha`, `imgalphafromdiff.py`, `imgproxyproc/imgproxyproc.py`, `imgrmbg2.py`, `imgcolsep.py`, `imgcolournormalize.py`, `imgrepalette`, `imghalftone.py`, `scanify.py`, `imgscale.py`, `imgdedup`, `imgcrop`, `imgoutcrop`, `imgs2layers`, `imgsortsimi`, `imgrenmatch`, `imgquotio.py`, `imgnanobanatrans.py`

## Tasks

- [ ] Normalize package layout so build packages point to `src/twat_image` and entry point group is `twat.plugins` with `image = twat_image`.
- [ ] Keep existing gray-to-alpha behavior passing.
- [ ] Add focused modules such as `alpha.py`, `background.py`, `color.py`, `scale.py`, `effects.py`, and `proxyproc.py` for deterministic operations where dependencies are acceptable.
- [ ] Treat PSD/layer helpers and image-similarity sorting as optional follow-ups unless their dependencies are already lightweight and testable.
- [ ] Add optional wrappers that call `twat_genai` for OpenAI/Gemini image generation and editing.
- [ ] Design CLI commands around domain actions, not reference script filenames.
- [ ] Update README with algorithmic examples and AI-backend examples.
- [ ] Add tests using small generated images and mocked `twat_genai` calls.
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
