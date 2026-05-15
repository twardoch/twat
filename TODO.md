# TODO

The original `issues/101.md` ecosystem cleanup tasklists (4 implementation groups + 1 consolidation group) are complete — see `CHANGELOG.md` `[Unreleased]` and the per-session log in `WORK.md`. This file now tracks outstanding follow-up work surfaced by the consolidation pass, and the current integration sweep that wires `twat[all]` to install every plugin.

## A. Make `pip install twat[all]` install every twat-* plugin

Audit baseline (current `twat/pyproject.toml` `[project.optional-dependencies]`):
- `all` is **missing** `twat-coding` (commented out), `twat-font`, `twat-os`.
- There is **no `font` group** (group exists for every other plugin).

### A1. Fix `twat/pyproject.toml`
- [x] Add `font = ["twat-font[all]>=2.7.7"]` to optional-dependencies.
- [x] Uncomment `twat-coding[all]` in `all = [...]`.
- [x] Add `twat-font[all]` to `all = [...]`.
- [x] Add `twat-os[all]` to `all = [...]`.
- [x] Bump pinned minimums on group entries (`audio`, `coding`, `font`) from `0.0.1` to the current published baseline (`>=2.7.7` for plugins on the post-cleanup train; `>=1.0.3` for `twat-mcp`).

## B. Cross-plugin integration (opt-in extras)

Hard cross-deps are kept narrow to avoid forced installs; "leverage" lives in optional extras so the dependency graph stays a tree.

Already declared (no change needed):
- `twat_genai` requires `twat_image`, `twat_fs`, `twat_os` — composite-plugin pattern, keep as runtime deps.
- `twat_search` requires external `twat-cache` — keep.

### B1. Plugin extras to add
- [x] **`twat_image`** add `[upload]` extra → `["twat-fs[all]"]` (push generated images to a backend).
- [x] **`twat_video`** add `[image]` extra → `["twat-image[all]"]` (thumbnails, frame ops).
- [x] **`twat_audio`** add `[parallel]` extra → `["twat-mp[all]"]` (batch DSP across files).
- [x] **`twat_speech`** add `[audio]` extra → `["twat-audio[all]"]` (read/write audio for ASR/TTS).
- [x] **`twat_llm`** add `[fs]` extra → `["twat-fs[all]"]` (multimodal file attachments).
- [x] **`twat_task`** add `[parallel]` extra → `["twat-mp[all]"]` (Prefect workers backed by mp pools).
- [x] **`twat_font`** add `[fs]` extra → `["twat-fs[all]"]` (font file fetch/upload).
- [x] **`twat_coding`** add `[fs]` extra → `["twat-fs[all]"]` (publish stub/coverage reports).
- [x] **`twat_text`** add `[llm]` extra → `["twat-llm[all]"]` (LLM-assisted text ops).

### B2. Ensure plugin `[all]` rolls in its own extras
Without this, `twat-image[all]` won't pull `twat-fs` even though we added the `upload` extra. For each plugin touched in B1, ensure its `all = [...]` group includes its newly added extra.

- [x] `twat-image[all]` → includes `twat-fs[all]`.
- [x] `twat-video[all]` → includes `twat-image[all]`.
- [x] `twat-audio[all]` → includes `twat-mp[all]`.
- [x] `twat-speech[all]` → includes `twat-audio[all]`.
- [x] `twat-llm[all]` → includes `twat-fs[all]`.
- [x] `twat-task[all]` → includes `twat-mp[all]`.
- [x] `twat-font[all]` → includes `twat-fs[all]`.
- [x] `twat-coding[all]` → includes `twat-fs[all]`.
- [x] `twat-text[all]` → includes `twat-llm[all]`.

### B3. Implementation rule
For plugins that don't currently have an `all` group at all, create one that bundles every other optional extra defined in that plugin's pyproject (so `twat-X[all]` is the "everything for X" recipe).

## C. Publish
- [x] Run `./publish-all.sh` from `twat/` root after A+B land.

## Carried-over follow-ups (unchanged from prior session)

### Pre-existing lint errors (ruff sweep)
- [ ] `twat_coding` — 9 errors.
- [ ] `twat_search` — 9 errors.
- [ ] `twat_llm` — 2 errors.
- [ ] `twat_os` — 2 errors.

### Pre-existing test failures
- [ ] `twat_os` — 28 failures in `tests/test_cross_platform.py` and `tests/unit/test_path_manager.py`.
- [ ] `twat_mp` — async tests skipped (missing `pytest-asyncio`); benchmark missing fixtures.
- [ ] `twat_genai` — 28 failures: `tests/test_outpaint.py` `ModuleNotFoundError`; `tests/test_image_utils.py` async plugin.
- [ ] `twat_llm` — 19 benchmark errors; 14 other failures.
- [ ] `twat_coding` — `pytest-cov` missing in hatch test env.
- [ ] `twat_search` — `No module named pip` in hatch test env bootstrap.

### Optional follow-up — wider `reference/bin-img-vid` absorption
- [ ] `imgcolournormalize.py`, `imgcolsep.py`, `imghalftone.py`, `imgalphafromdiff.py`, `imgrmbg2.py`, `imgscale.py` → `twat_image`.
- [ ] `mkv2srt.py`, `srtmultifix.py`, `viddub*.py`, `vidkenburns.py`, `vidmergebygap*.py`, `vidsqueeze.py`, `vidshortentoframes.py` → `twat_video`.
- [ ] Each candidate needs per-script triage: classify reusable vs maintainer-specific, decide target package, write minimal adapter + test, document in package README.
