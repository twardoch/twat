# Changelog

All notable changes to the `twat` project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] — Fire CLI rollout (2026-05)

Comprehensive Fire-based CLIs for every `twat-*` plugin, with dashed
per-leaf entry-point scripts so `twat-<TAB>` completions surface dozens of
commands. See `SPEC.md` and `.omc/plans/fire-cli-rollout.md`.

### Host (`twat`)

- Fix: `twat` / `twat --help` now print usage to stdout and exit `0`
  (previously stderr + exit `1`, invisible to most shells).
- New: `twat --completions {bash,zsh,fish}` emits a completion script for the
  installed `twat-*` console scripts.
- New: `src/twat/common/cli.py` with shared helpers
  (`make_version_callable`, `error`, `print_data`, `emit_completions`).

### Verification-pass fixes (post-rollout)

- `twat-search` 2.7.11 — restrictive `[tool.hatch.build] include` had stripped
  all `.py` files from the wheel; wheel rebuilt with a clean exclude list.
- `twat-coding` 2.7.12 — `dependencies = [...]` had been placed *after*
  `[[project.authors]]`, so TOML attached it to the author entry rather than
  `[project]` and the wheel METADATA had **zero** core `Requires-Dist`
  lines (radon, fire, pydantic, ... all missing at install). Moved `dependencies`
  before `[[project.authors]]`.
- `twat-video` 2.7.6 — an orphan 2.7.5 was already on PyPI from an earlier
  unrelated release; my 2.1.9 was below it and pip preferred the orphan.
  Force-tagged v2.7.6 to supersede.
- `twat-fs` 2.7.16 — added dashed leaf entry points (`twat-fs-version`,
  `twat-fs-upload`, `twat-fs-upload-provider`); Phase 1 was hotfix-only.
- `twat` (host) 2.7.17 — released the Phase 0 changes so end users get the
  updated `twat --help` / `--completions` behaviour.

### Plugins (all 17, released to PyPI)

Every plugin now follows the canonical pattern from `SPEC.md` §4.2: a
`twat_X/__main__.py` Fire dispatcher with an explicit `COMMANDS` allow-list,
a `main()` entry point, and one `cmd_<leaf>()` helper per leaf and group.
Every leaf and group is also registered as a dashed
`twat-<plugin>-<leaf>` script in `[project.scripts]`.

| Plugin | Version | Dashed scripts |
|--------|---------|---------------:|
| twat (host) | 2.7.17 | — |
| twat-fs | 2.7.16 | 4 (3 dashed + base) |
| twat-image | 2.7.9 | 10 |
| twat-video | 2.7.6 | 14 |
| twat-audio | 2.7.10 | 9 |
| twat-speech | 2.7.9 | 7 |
| twat-llm | 2.7.9 | 7 |
| twat-genai | 2.7.8 | 5 |
| twat-search | 2.7.11 | 4 (incl. preserved `twat-search-web`) |
| twat-text | 2.7.10 | 7 |
| twat-os | 2.7.8 | 5 |
| twat-font | 2.7.10 | 4 |
| twat-hatch | 2.7.8 | 5 |
| twat-coding | 2.7.12 | 4 |
| twat-mp | 2.6.5 | 4 |
| twat-task | 2.7.10 | 2 (others gated on Prefect deployment layer) |
| twat-ez | 2.7.9 | 3 |
| twat-labs | 2.7.9 | 3 |

Across the ecosystem: **106 `twat-*` console scripts** on PATH after `uv pip
install --system -U 'twat[all]'`. Acceptance contract from SPEC §9 verified
end-to-end against framework Python 3.13.

`argparse` removed from every plugin that used it; lazy imports for heavy
dependencies (Pillow, ffmpeg-python, fal_client, litellm, ...) so
`--help` is instant.

## [Unreleased] — Ecosystem cleanup (issues/101.md)

Multi-session ecosystem audit, gap-fix, and verification pass covering the host package and all 17 plugin repos.

### Host (`twat`)

- `twat --list` and `twat --help` flags implemented per `issues/103-host.md`.
- 9 host tests pass: `iter_plugins`, plugin caching, missing plugin, plugin without `main()`, CLI dispatch, `--help`, `--list` (no plugin import on list).
- README documents host CLI, plugin contract, naming conventions, and dispatch mechanics.

### Foundations layer (Tasklist 1)

- **`twat_genai`** — provider-neutral models (`models.py`), `chutes/` engine package (sync + async clients, HiDream/rembg/SkyReels/WAN), `openai_image.py` (absorbed `reference/bin-img-vid/imgquotio.py`), `gemini.py` (absorbed `reference/bin-img-vid/imgnanobanatrans.py`), preserved `fal/` engine. Added missing `[project.scripts]` block.
- **`twat_llm`** — text-LLM boundary preserved (`mallmo.ask`/`ask_chain`/`ask_batch`). Stable `twat_text` adapter surface (`summarize_text`, `rewrite_text`, `extract_structured_data`, `classify_text`). Added `[project.entry-points."twat.plugins"]`, `[project.scripts]`, and `src/twat_llm/__main__.py` for `python -m twat_llm`.
- **`twat_text`** — full deterministic text utilities (`normalize_text`, `clean_text`, `chunk_text`, extraction helpers, Markdown/HTML/plain conversion, token estimation) with lazy LLM-backed `summarize`/`rewrite`/`extract_structured`/`classify` via narrow `twat_llm` adapter. CLI subcommands: `clean`, `chunk`, `convert`, `summarize`, `rewrite`.

### Media domain (Tasklist 2)

- **`twat_image`** — package layout normalized; `genai.py` wrapper; deterministic operations (`crop`, `scale`, `gray2alpha`, etc.); 73 tests pass.
- **`twat_video`** — misnamed font-organizer replaced with real video package. `ffmpeg.py` boundary (command builder + dry-run support), `operations.py` (crop/scale/split/reverse/import-audio/ken-burns/grain/reverb/merge-by-gap/extract-subtitles/repair-srt), `genai.py` wrapper. Legacy font code preserved as historical material in `src/font_organizer/`.
- **`twat_audio`** — resampling preserved (pedalboard); added ffmpeg helpers (`normalize_audio`, `trim_audio`, `extract_audio`, `replace_audio`, `simple_effect`); plugin entry point declared.
- **`twat_speech`** — typed `transcribe`/`synthesize`/`repair_subtitles`/`dub_plan` API. Lazy `twat_genai` provider adapters. SRT parsing/repair. Optional `twat_audio` preprocessing.

### Complex support (Tasklist 3)

- **`twat_font`** — canonical font-organizer home; `FontInfo`/`FontManager` core. No unique behavior in legacy `twat_video/font_organizer/` required preservation.
- **`twat_fs`** — provider protocol intact (`ProviderClient`/`Provider`). Contract tests pass in fresh hatch env.
- **`twat_search`** — script target normalized from `twat_search.__main__:main` to `twat_search:main` for ecosystem consistency. Embedded scraper boundary documented in README.
- **`twat_coding`** — pystubnik CLI preserved (AST + MyPy backends). Plugin contract complete with `coding = "twat_coding"` entry and `twat-coding`/`twat coding` dispatch.

### Lightweight (Tasklist 4)

- **`twat_os`**, **`twat_mp`**, **`twat_ez`**, **`twat_hatch`**, **`twat_task`**, **`twat_labs`** — all already met the plugin contract before this work; verified via audit and tests. Host CLI dispatch verified working for each.

### Reference scripts

- `reference/bin-img-vid/imgquotio.py` → `twat_genai.engines.openai_image`.
- `reference/bin-img-vid/imgnanobanatrans.py` → `twat_genai.engines.gemini`.
- `reference/chutes_image/chutes_*.py` → `twat_genai.engines.chutes`.
- Remaining 80+ scripts in `reference/bin-img-vid/` are personal workflow one-offs in a symlinked directory; kept as-is per documentation in `WORK.md`.

### Consolidation (Tasklist 5)

- Cross-pyproject consistency audit found and fixed two real script-target gaps (`twat_genai` missing scripts, `twat_search` wrong target).
- Fresh `.venv` editable install of host + all 17 plugins succeeds.
- `twat --help`, `twat --list`, `twat <entry> --help` matrix run: 14/17 plugins dispatch cleanly to their CLI help; 2 (`coding`, `fs`) surface pre-existing downstream dependency runtime errors; 1 (`search`) emits a warning but works. Matrix recorded in `WORK.md`.
- Ruff sweep across all 17 plugin src trees: 10 clean, 3 have only unsafe-fix opportunities, 4 have pre-existing errors. mypy issues per-package audits report confined mostly to test code.

### Dispatch follow-up (post-consolidation pass)

After the install matrix exposed 2 plugins that failed `twat <entry> --help`:

- **`twat_coding`** — moved top-level imports of `coverage`, `networkx`, and `pydocstyle` in `pystubnik/processors/file_importance.py` into the functions that actually use them. The CLI no longer requires development/analysis dependencies to be importable at help time. (Underlying installation of `radon` was also added to the project venv since the pyproject declares it as a core dep but uv didn't install it during the multi-package editable install.)
- **`twat_fs`** — wrapped `from twat_cache import ucache` in `upload_providers/core.py` with a defensive shim that catches both factory-call and decoration-step exceptions, falling back to a no-op decorator when `twat_cache`'s cache backends are broken (the currently-installed PyPI `twat_cache` has abstract `AioCacheEngine`/`CacheBoxEngine` classes that raise `TypeError` on instantiation). Routed `factory.py` and `dropbox.py` through this defensive `ucache` instead of importing from `twat_cache` directly so all three `@ucache(...)` decoration sites are protected.

After these fixes the `twat <entry> --help` matrix shows 16/17 plugins dispatching cleanly to their CLI help; `twat_search` still emits a non-fatal warning about a web-engine import.

### Documentation

- Per-session audit, verification, and consolidation log accumulated in `WORK.md`.
- `TODO.md` reset to remaining outstanding items only.

## [1.7.6] - 2025-02-15

### Changed

- Updated dependencies in `pyproject.toml`
- Improved README.md documentation
- Refined package configuration

## [1.7.5] - 2025-02-15

### Added

- README.md documentation improvements
- Enhanced package initialization

### Changed

- Refactored `src/twat/__init__.py`
- Updated path handling in `src/twat/paths.py`
- Adjusted package dependencies

## [1.7.0] - 2025-02-13

### Added

- New .gitignore patterns

### Changed

- Restructured project layout
- Streamlined development workflow

## [1.6.2] - 2025-02-06

### Added

- Extended `pyproject.toml` configuration
- Added package metadata
- Improved dependency definitions

## [1.6.1] - 2025-02-06

### Changed

- Refactored initialization code in `src/__init__.py` and `src/twat/__init__.py`
- Improved path resolution in `src/twat/paths.py`
- Expanded test coverage

### Fixed

- Path resolution errors
- Initialization bugs

## [1.6.0] - 2025-02-06

### Added

- GitHub repository setup
- Plugin system implementation
- PEP 621-compliant packaging

### Changed

- Updated documentation
- Refined package structure

## [1.1.0] - 2025-02-03

### Added

- Core functionality in `src/__init__.py`
- Initial test suite in `tests/test_package.py`
- Enhanced `pyproject.toml` configuration

### Changed

- Improved .gitignore settings
- Updated README with additional details

## [1.0.1] - 2025-02-03

### Fixed

- `pyproject.toml` configuration issues
- Repository ignore patterns

## [1.0.0] - 2025-02-03

### Added

- Initial release
- Basic package structure
- Core module
- Package initialization logic
- Version management

[1.7.6]: https://github.com/twardoch/twat/compare/v1.7.5...v1.7.6  
[1.7.5]: https://github.com/twardoch/twat/compare/v1.7.0...v1.7.5  
[1.7.0]: https://github.com/twardoch/twat/compare/v1.6.2...v1.7.0  
[1.6.2]: https://github.com/twardoch/twat/compare/v1.6.1...v1.6.2  
[1.6.1]: https://github.com/twardoch/twat/compare/v1.6.0...v1.6.1  
[1.6.0]: https://github.com/twardoch/twat/compare/v1.1.0...v1.6.0  
[1.1.0]: https://github.com/twardoch/twat/compare/v1.0.1...v1.1.0  
[1.0.1]: https://github.com/twardoch/twat/compare/v1.0.0...v1.0.1  
[1.0.0]: https://github.com/twardoch/twat/releases/tag/v1.0.0