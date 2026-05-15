# twat_video Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` or equivalent task-by-task execution. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stop being font-organizer first; only after metadata/import/script identity is fixed and font behavior is preserved should this become a real user-facing video processing package using ffmpeg algorithms and optional twat_genai video backends.

**Architecture:** Preserve the standard twat plugin contract: PyPI package `twat-video`, import module `twat_video`, entry point `video = twat_video`, public `main()`, explicit `__all__`, README examples, and tests. Keep provider/API integrations behind thin clients and keep user-facing domain functions small.

**Tech Stack:** Python 3.10+ unless the package already requires 3.12, pytest, ruff, mypy, loguru, fire where the package already uses CLI dispatch.

---

## Current State

- Path: `plugins/repos/twat_video`.
- Entry point name: `video`.
- Tier: `critical`.
- See `issues/102-current.md` for repository-wide inventory and reference-code reuse decisions.

## Scope

`twat_video` is currently a misnamed font organizer. Replace it with a real video domain package while preserving/migrating font code to `twat_font` first.

## Files

- Modify: `plugins/repos/twat_video/pyproject.toml`
- Replace/Create under: `plugins/repos/twat_video/src/twat_video/`
- Replace/Create: `plugins/repos/twat_video/tests/`
- Modify: `plugins/repos/twat_video/README.md`
- Coordinate with: `plugins/repos/twat_font/`
- Reference: `reference/bin-img-vid/vid*.py`, `vid*` shell scripts, `mkv2srt.py`, `srtmultifix.py`, `scanify.py`

## Tasks

- [ ] Confirm font organizer code exists in `twat_font`; do not delete unique behavior until copied or referenced there.
- [ ] After confirming font behavior is preserved in `twat_font`, change package metadata to `twat-video`, package module `twat_video`, direct script targets, and entry point `video = twat_video`.
- [ ] Implement a small ffmpeg command runner boundary with dry-run/testable command construction.
- [ ] Port reusable video operations into focused modules such as `probe.py`, `transcode.py`, `optimize.py`, `geometry.py`, `timing.py`, `audio.py`, `concat.py`, `effects.py`, and `frames.py`: crop/scale, fps/framedrop, split, reverse, merge-by-gap, ken-burns, grain/reverb, and audio import/replacement.
- [ ] Keep subtitle-only extraction/repair in `twat_text` unless wrapped by a video workflow.
- [ ] Add optional wrappers that call `twat_genai` for SkyReels/WAN video generation.
- [ ] Leave one-off watermark/local workflow scripts in `reference/` and document why.
- [ ] Update README with command examples and dependency requirements (`ffmpeg`, optional providers).
- [ ] Add tests for command construction and mocked file operations.
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
