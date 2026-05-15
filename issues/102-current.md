# 102: Current State Inventory for twat Ecosystem

## Problem

`issues/101.md` requests ecosystem cleanup across the host package, all plugin repos, and reusable reference code. The current state is uneven: several packages are production-like, several are scaffolds, and `twat_video` is still a misnamed font organizer while reusable media scripts live under `reference/`.

## Current State

### Host package: `twat`

- Path: `src/twat/`.
- Package metadata: top-level `pyproject.toml` builds `src/twat`, uses `hatch-vcs`, writes `src/twat/__version__.py`, and exposes scripts `twat = "twat:main"` and `twat-cleanup = "twat.dev.cleanup:main"`.
- Plugin discovery: `src/twat/__init__.py` loads `importlib.metadata` entry points in group `twat.plugins` and exposes plugins dynamically as `twat.<name>` through `__getattr__`.
- CLI dispatch: `twat <plugin_name> [args...]` rewrites `sys.argv` and calls the plugin module's callable `main()`.
- Gap: usage text mentions `twat --list` and `twat --help`, but current CLI code does not implement these flags.
- Tests: `tests/test_twat.py` exists for host behavior.
- Docs: top-level README describes host/plugin contract and example plugin structure.

### Plugin repos

| Package | Path | State | Main concerns |
| --- | --- | --- | --- |
| `twat_audio` | `plugins/repos/twat_audio` | Simple package with `src/twat_audio/twat_audio.py`, 1 test; currently missing direct script and `twat.plugins` entry point | Preserve resampling; add only reusable audio helpers surfaced by video workflows; do not invent a broad audio-generation layer from this reference batch. Add `audio = "twat_audio"` and a direct script if a package CLI exists. |
| `twat_coding` | `plugins/repos/twat_coding` | Complex `pystubnik`/AST package, Python >=3.12, 31 source files | Keep focused on coding/stub generation; normalize exports/docs/tests without mixing media work. |
| `twat_ez` | `plugins/repos/twat_ez` | Simple dependency/path helper | Stabilize metadata, README, and plugin contract. |
| `twat_font` | `plugins/repos/twat_font` | Modern font organizer copy, but pyproject/script/test/type paths still reference `font_organizer` in places and no `twat.plugins` entry point is present | Make canonical font package; absorb/preserve code currently misnamed under `twat_video`; fix script target to `twat_font`, add `font = "twat_font"`, normalize paths, tests, and docs. |
| `twat_fs` | `plugins/repos/twat_fs` | Complex multi-provider upload package | Provider typing/lint debt; keep upload API stable. |
| `twat_genai` | `plugins/repos/twat_genai` | Fal image-generation package with engine abstraction | Expand into shared non-text generative media layer: Chutes image/video/rembg/hidream, OpenAI image, Gemini/Nano Banana, and video providers; keep speech/audio provider work behind explicit contracts rather than speculative APIs. |
| `twat_hatch` | `plugins/repos/twat_hatch` | Medium package scaffold generator | Normalize plugin contract/docs/tests. |
| `twat_image` | `plugins/repos/twat_image` | Image alpha utility, mixed `image_alpha_utils` and `twat_image` source layout | Fix package layout/entry point, wrap reusable image scripts, call `twat_genai` for AI image operations. |
| `twat_labs` | `plugins/repos/twat_labs` | Skeleton | Keep explicitly experimental and minimal. |
| `twat_llm` | `plugins/repos/twat_llm` | LLM interface with `mallmo.ask`, chain, batch, multimodal image support; currently lacks direct script and `twat.plugins` entry point | Own text-heavy LLM APIs and text operations; provide stable API for `twat_text`; add `llm = "twat_llm"` and decide/implement a direct CLI entry. |
| `twat_mp` | `plugins/repos/twat_mp` | Parallel helpers | Normalize docs/tests/exports. |
| `twat_os` | `plugins/repos/twat_os` | Best-convention reference package | Use as packaging/docs/test template. |
| `twat_search` | `plugins/repos/twat_search` | Complex multi-engine search package with embedded `lib_falla` | Isolate embedded scraper, clean docs/tests/typing incrementally. |
| `twat_speech` | `plugins/repos/twat_speech` | Scaffold; no strong direct ASR/TTS/diarization reference implementation exists in the inspected reference tree | Keep scope narrow: define speech-facing interfaces and future provider adapters through `twat_genai`; keep subtitle-only extraction/repair primarily in `twat_text` unless wrapped by ASR/TTS/dubbing workflows. |
| `twat_task` | `plugins/repos/twat_task` | Task orchestration helper | Normalize plugin contract/docs/tests. |
| `twat_text` | `plugins/repos/twat_text` | Scaffold | Build deterministic text utilities plus `twat_llm` powered operations. |
| `twat_video` | `plugins/repos/twat_video` | Misnamed `font-organizer` package under `src/font_organizer`; metadata/import/script still say `font-organizer`/`font_organizer` and no `twat.plugins` entry point exists | Do not add video behavior until package identity is fixed and font behavior is safely preserved in `twat_font`; then replace with real video package. |

### Reference code

- `reference/bin-img-vid/` is the main media script library. It contains reusable image tools (`imgnanobanatrans.py`, `imgquotio.py`, `imggray2alpha`, `imgdedup`, `imgscale.py`, PSD/layer tools), video tools (`vidkenburns.py`, `vidmergebygap.py`, `vidreverb.py`, `vidcropscale.py`, `viddub-*`, `vidfps`, `vidsplit.py`, `vidsqueeze.py`, etc.), subtitle/audio utilities (`mkv2srt.py`, `srtmultifix.py`), and one-off shell wrappers.
- `reference/bin-img-vid/README.md` documents a mature CLI script set built around `uv`, `ffmpeg`, `fire`, `rich`, and `loguru`.
- `reference/chutes_image/` contains reusable Chutes API clients for image generation, HiDream edit/generate, background removal, SkyReels text/image-to-video, and WAN first-last-frame video. These should be moved into `twat_genai` as provider engines, not copied into domain packages.
- `reference/twat_mcp/` is a separate MCP experiment and should not be part of this cleanup except as future reference.
- `_ignore/` and generated media outputs are examples/artifacts, not library code.

### Additional discovery notes

- `twat_cache` is referenced in older ecosystem guidance but is absent from the current `plugins/repos/` checkout; do not plan work for it unless the repo is restored.
- Host tests must force local source imports (`PYTHONPATH=src` or equivalent), because plain `python -m pytest tests` can import a globally installed `twat` and report misleading success.
- Host plugin caching is incomplete: `_load_plugin()` registers `sys.modules["twat.<name>"]` but does not check it first or set the loaded module as an attribute on `twat`.
- The host usage text advertises `twat --list` and `twat --help`, but current CLI dispatch treats those flags as plugin names.
- High-priority reference migrations by destination: `twat_genai` gets Chutes/OpenAI/Gemini provider clients; `twat_image` gets alpha/background/color/scale/effect/proxy processing algorithms; `twat_video` gets ffmpeg/OpenCV/MoviePy/PyAV command builders and runners; `twat_text` gets subtitle extraction/repair.

### Reuse decisions

- Move reusable provider/API clients into `twat_genai`: Chutes image/video/rembg/hidream, OpenAI image generation/editing from `imgquotio.py`, Gemini/Nano Banana from `imgnanobanatrans.py`.
- Move deterministic image algorithms into `twat_image`: gray-to-alpha, alpha-from-diff, crop/outcrop/recanvas/normalize/scale/dedup, PSD/layer helpers where dependencies are acceptable.
- Move deterministic video algorithms into `twat_video`: ffmpeg crop/scale, merge-by-gap, speed/timing, reverse, split, ken-burns, grain/reverb, subtitle extraction/repair wrappers.
- `twat_audio`: only small shared audio helpers from video workflows (`vidpredub.py`, `viddub-*`, `vidimportaudio`, `vidreverb.py`) are candidates; no large standalone audio toolkit was found.
- `twat_speech`: no direct speech toolkit was found; future STT/TTS provider calls should route through `twat_genai`, while subtitle-only tools should stay in `twat_text`.
- Move text operations into `twat_text` and call `twat_llm` only for LLM-powered transformations.
- Leave true one-offs and local shell workflow glue in `reference/bin-img-vid/` with documentation pointing to the new package APIs.

## Proposed Changes

1. Create package-specific implementation plans in `issues/103-*.md` for the host and every plugin repo.
2. Update `PLAN.md` with links to all plans and the execution order.
3. Update `TODO.md` with four independent parallel tasklists plus a fifth consolidation tasklist.
4. Execute the four independent tasklists in separate agents, partitioned by package ownership to avoid file conflicts.
5. Run a consolidation/testing pass across host and plugin surfaces.

## Files to Modify

- `issues/102-current.md`
- `issues/103-host.md`
- `issues/103-*.md` for every plugin repo under `plugins/repos/`
- `PLAN.md`
- `TODO.md`

## Acceptance Criteria

- [ ] Current state document covers host, all plugin repos, and reference code.
- [ ] Every plugin repo has a corresponding `issues/103-*.md` plan.
- [ ] `PLAN.md` links every plan.
- [ ] `TODO.md` contains exactly four independent implementation tasklists plus one consolidation tasklist.
- [ ] Every `TODO.md` task line begins with `- [ ]`.
- [ ] Reference-code reuse decisions are explicit enough for agents to implement without re-reading the whole conversation.

## Dependencies

- Depends on `issues/101.md`.
- Supersedes ad-hoc planning in empty `PLAN.md` and `TODO.md`.
