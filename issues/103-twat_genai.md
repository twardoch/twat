# twat_genai Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` or equivalent task-by-task execution. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Become the shared outreach/interface layer for non-text generative AI APIs: image, video, audio, speech, and multimodal media generation.

**Architecture:** Preserve the standard twat plugin contract: PyPI package `twat-genai`, import module `twat_genai`, entry point `genai = twat_genai`, public `main()`, explicit `__all__`, README examples, and tests. Keep provider/API integrations behind thin clients and keep user-facing domain functions small.

**Tech Stack:** Python 3.10+ unless the package already requires 3.12, pytest, ruff, mypy, loguru, fire where the package already uses CLI dispatch.

---

## Current State

- Path: `plugins/repos/twat_genai`.
- Entry point name: `genai`.
- Tier: `complex`.
- See `issues/102-current.md` for repository-wide inventory and reference-code reuse decisions.

## Scope

`twat_genai` is the shared provider layer for non-text generative media APIs. It should absorb reusable provider clients from `reference/chutes_image/`, `reference/bin-img-vid/imgnanobanatrans.py`, and `reference/bin-img-vid/imgquotio.py` behind stable image/video/audio/speech abstractions. Domain packages call this package instead of duplicating API clients.

## Files

- Modify/Create under: `plugins/repos/twat_genai/src/twat_genai/`
- Modify: `plugins/repos/twat_genai/pyproject.toml`
- Modify: `plugins/repos/twat_genai/README.md`
- Modify/Create: `plugins/repos/twat_genai/tests/`
- Reference: `reference/chutes_image/*.py`
- Reference: `reference/bin-img-vid/imgnanobanatrans.py`
- Reference: `reference/bin-img-vid/imgquotio.py`

## Tasks

- [ ] Add provider-neutral request/response models for image generation/editing, video generation, background removal, and media file outputs.
- [ ] Move Chutes image generation client patterns into a `twat_genai.engines.chutes` package with sync and async clients where practical.
- [ ] Move HiDream generation/editing, rembg, SkyReels, and WAN video clients into separate Chutes engine modules.
- [ ] Add OpenAI image generation/editing support based on reusable logic from `imgquotio.py` without shell-script assumptions.
- [ ] Add Gemini/Nano Banana image transform support based on `imgnanobanatrans.py` with explicit API-key configuration.
- [ ] Keep Fal image functionality working and document provider selection.
- [ ] Expose a stable public API from `twat_genai.__init__` and a CLI with subcommands or Fire methods for provider operations.
- [ ] Add tests with mocked HTTP/API clients for model selection, payload construction, output naming, and error handling.
- [ ] Update README with provider matrix, environment variables, and examples used by `twat_image`, `twat_video`, `twat_audio`, and `twat_speech`.
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
