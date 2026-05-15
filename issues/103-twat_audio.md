# twat_audio Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` or equivalent task-by-task execution. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preserve audio resampling while adding only the small reusable audio helpers surfaced by video workflows; no broad standalone audio toolkit was found in the inspected reference tree.

**Architecture:** Preserve the standard twat plugin contract: PyPI package `twat-audio`, import module `twat_audio`, entry point `audio = twat_audio`, public `main()`, explicit `__all__`, README examples, and tests. Keep deterministic audio helpers local; provider-backed STT/TTS/generation belongs in `twat_genai` or speech-facing adapters, not speculative audio APIs.

**Tech Stack:** Python 3.10+ unless the package already requires 3.12, pytest, ruff, mypy, loguru, fire where the package already uses CLI dispatch.

---

## Current State

- Path: `plugins/repos/twat_audio`.
- Entry point name: `audio`.
- Tier: `simple`.
- See `issues/102-current.md` for repository-wide inventory and reference-code reuse decisions.

## Scope

`twat_audio` is the user-facing audio domain package for deterministic audio transforms. It may expose command construction/helpers used by video dubbing/import workflows, but should not absorb speech or media-provider concerns.

## Files

- Modify/Create under: `plugins/repos/twat_audio/src/twat_audio/`
- Modify: `plugins/repos/twat_audio/README.md`
- Modify/Create: `plugins/repos/twat_audio/tests/`
- Reference: audio portions of `reference/bin-img-vid/vidimportaudio`, `vidpredub.py`, `viddub-*`, `vidreverb.py` only where reusable outside video; treat the absence of a standalone audio toolkit as a scope constraint.

## Tasks

- [ ] Preserve existing resampling behavior.
- [ ] Add audio metadata/probe helpers behind an ffmpeg boundary.
- [ ] Add normalize, trim, extract, replace/import-audio, and simple effect helpers where deterministic.
- [ ] Coordinate speech-oriented dubbing/STT/TTS APIs with `twat_speech`; keep this package focused on audio files/signals.
- [ ] Avoid provider-backed audio generation/transformation in this pass unless `twat_genai` already exposes a stable audio contract; keep this package focused on deterministic audio helpers.
- [ ] Update README and CLI examples.
- [ ] Add tests for command construction and small synthetic audio fixtures if practical.
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
