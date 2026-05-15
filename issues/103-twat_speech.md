# twat_speech Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` or equivalent task-by-task execution. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace scaffold speech package with narrow speech-facing interfaces while acknowledging that no direct ASR/TTS/diarization reference toolkit was found in the inspected reference tree.

**Architecture:** Preserve the standard twat plugin contract: PyPI package `twat-speech`, import module `twat_speech`, entry point `speech = twat_speech`, public `main()`, explicit `__all__`, README examples, and tests. Delegate future provider-backed generation/transcription to `twat_genai`, pure audio work to `twat_audio`, and subtitle-only extraction/repair to `twat_text` unless a workflow explicitly involves speech recognition or synthesis.

**Tech Stack:** Python 3.10+ unless the package already requires 3.12, pytest, ruff, mypy, loguru, fire where the package already uses CLI dispatch.

---

## Current State

- Path: `plugins/repos/twat_speech`.
- Entry point name: `speech`.
- Tier: `skeleton`.
- See `issues/102-current.md` for repository-wide inventory and reference-code reuse decisions.

## Scope

`twat_speech` is a scaffold and should become the user-facing speech boundary for transcription, TTS, and dubbing orchestration once providers exist. Subtitle/caption file utilities alone should live in `twat_text`.

## Files

- Modify/Create under: `plugins/repos/twat_speech/src/twat_speech/`
- Modify: `plugins/repos/twat_speech/README.md`
- Modify/Create: `plugins/repos/twat_speech/tests/`
- Reference: no direct ASR/TTS reference implementation; `mkv2srt.py` and `srtmultifix.py` are primarily `twat_text` candidates, while dubbing scripts inform boundaries with `twat_audio`/`twat_video`.

## Tasks

- [ ] Replace scaffold API with typed functions for transcribe, synthesize, and dub-plan generation, using provider abstractions or mocks until real `twat_genai` speech providers exist.
- [ ] Use `twat_genai` for speech provider calls; do not embed provider clients here.
- [ ] Use `twat_audio` for audio preprocessing and extraction where needed.
- [ ] Do not port subtitle extraction/repair into `twat_speech` unless it is wrapped by an ASR/TTS/dubbing workflow; otherwise reference `twat_text` APIs.
- [ ] Add CLI commands for transcribe, repair-srt, synthesize, and dub.
- [ ] Update README with provider and local dependency requirements.
- [ ] Add tests for subtitle parsing/repair and mocked backend calls.
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
