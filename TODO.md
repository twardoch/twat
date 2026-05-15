# TODO

The original `issues/101.md` ecosystem cleanup tasklists (4 implementation groups + 1 consolidation group) are complete — see `CHANGELOG.md` `[Unreleased]` and the per-session log in `WORK.md`. This file now tracks only outstanding follow-up work surfaced by the consolidation pass.

## Dispatch bugs (host `twat <entry> --help` matrix)

Both fixed. See `CHANGELOG.md` `[Unreleased]` follow-up section.

## Pre-existing lint errors (ruff sweep)

Reproduce with `uvx ruff check plugins/repos/<pkg>/src/<pkg>`.

- [ ] **`twat_coding`** — 9 errors.
- [ ] **`twat_search`** — 9 errors.
- [ ] **`twat_llm`** — 2 errors.
- [ ] **`twat_os`** — 2 errors.

## Pre-existing test failures (categorized in `WORK.md`)

These are unrelated to the plugin-contract surface; they pre-date the ecosystem cleanup and are documented per the plans' acceptance-criteria clause.

- [ ] **`twat_os`** — 28 failures in `tests/test_cross_platform.py` and `tests/unit/test_path_manager.py` (path-handling logic: unicode, env-var expansion, case sensitivity, long paths).
- [ ] **`twat_mp`** — async tests skipped/erroring (missing `pytest-asyncio` in hatch test env); benchmark tests error on missing fixtures.
- [ ] **`twat_genai`** — 28 failures: `tests/test_outpaint.py` `ModuleNotFoundError`; `tests/test_image_utils.py` `async def with no async plugin`.
- [ ] **`twat_llm`** — 19 errors in `tests/test_benchmark.py` (missing `pytest-benchmark` fixtures); 14 other failures (location truncated).
- [ ] **`twat_coding`** — `pytest-cov` missing in hatch test env (`--cov` flags fail).
- [ ] **`twat_search`** — `No module named pip` in hatch test env bootstrap.

## Optional follow-up — wider reference/bin-img-vid absorption

The original `issues/101.md` mandates "ALL or NEARLY ALL tools in `reference/bin-img-vid` which look reusable should be rewritten to utilize our twat code. Only clear one-offs should be left as is." This session absorbed only the 5 explicitly named in plans (`imgquotio`, `imgnanobanatrans`, `chutes_*`). A wider sweep is open follow-up. Candidates that look reusable rather than one-off:

- [ ] `imgcolournormalize.py`, `imgcolsep.py`, `imghalftone.py`, `imgalphafromdiff.py`, `imgrmbg2.py`, `imgscale.py` → could land in `twat_image`.
- [ ] `mkv2srt.py`, `srtmultifix.py`, `viddub*.py`, `vidkenburns.py`, `vidmergebygap*.py`, `vidsqueeze.py`, `vidshortentoframes.py` → could land in `twat_video`.
- [ ] Each candidate needs per-script triage: classify as reusable vs maintainer-specific, decide target package, write minimal adapter + test, document in package README.
