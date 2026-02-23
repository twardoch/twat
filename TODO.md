# twat Modernization TODO

Actionable task list derived from the [modernization specs](issues/). Each task is small enough for a single work session.

---


## Phase 0: twat_fs Provider Integration (HIGHEST PRIORITY) (spec a102)

### 0.1 Fix/Deprecate Broken Providers
 [x] Deprecate `bashupload` provider: `get_provider()` returns `None`, remove from `PROVIDERS_PREFERENCE` (ref: [a102](issues/a102.md))
 [x] Fix `www0x0` provider: add `User-Agent: twat-fs/1.0` header to `requests.post()` (ref: [a102](issues/a102.md))
 [x] Fix `pixeldrain` provider: switch from POST to PUT method with `Content-Type: application/octet-stream` (ref: [a102](issues/a102.md))

### 0.2 Add New Verified Providers

 [x] Create `x0at.py` provider for x0.at (POST multipart, plain text URL response) (ref: [a102](issues/a102.md))
 [x] Create `senditsh.py` provider for sendit.sh (PUT, single-download, regex URL parse) (ref: [a102](issues/a102.md))
 [x] Create `tmpfilesorg.py` provider for tmpfiles.org (POST multipart, JSON response, `/dl/` URL transform) (ref: [a102](issues/a102.md))
 [x] Create `tmpfilelink.py` provider for tmpfile.link (POST multipart, JSON `downloadLink` response) (ref: [a102](issues/a102.md))

### 0.3 Update Provider Registry

 [x] Update `PROVIDERS_PREFERENCE` in `__init__.py` with new provider ordering (ref: [a102](issues/a102.md))

### 0.4 Provider Metadata and Tests

 [x] Copy `fileshare.toml` to `src/twat_fs/data/` and create `registry.py` with `ServiceInfo` dataclass (ref: [a102](issues/a102.md))
 [x] Create `tests/test_providers_online.py` with `@pytest.mark.online` integration tests (ref: [a102](issues/a102.md))
 [x] Move `TO-INTEGRATE/pastebin_tester.py` to `tests/tools/` (ref: [a102](issues/a102.md))

---

## Phase 1: Foundation (Infrastructure)

### 1.1 Version Management (spec 01)

 [x] Delete `plugins/repos/twat_coding/src/twat_coding/_version.py` (ref: [01](issues/01.md))
 [x] Delete all `VERSION.txt` files across plugin repos (ref: [01](issues/01.md))
 [x] Add `importlib.metadata` version pattern to `twat_cache/__init__.py` (ref: [01](issues/01.md))
 [x] Add `importlib.metadata` version pattern to `twat_fs/__init__.py` (ref: [01](issues/01.md))
 [x] Add `importlib.metadata` version pattern to `twat_genai/__init__.py` (ref: [01](issues/01.md))
 [x] Add `importlib.metadata` version pattern to `twat_search/__init__.py` (ref: [01](issues/01.md))
 [x] Add `importlib.metadata` version pattern to `twat_coding/__init__.py` (ref: [01](issues/01.md))
 [x] Add `importlib.metadata` version pattern to all remaining plugins (ref: [01](issues/01.md))
 [x] Standardize `[tool.hatch.version]` section in all plugin `pyproject.toml` files to use `hatch-vcs` (ref: [01](issues/01.md))
 [x] Verify `hatch version` works correctly in every plugin repo (ref: [01](issues/01.md))

### 1.2 Unified Cleanup Script (spec 02)

 [x] Create `src/twat/dev/__init__.py` with shared cleanup logic (ref: [02](issues/02.md))
 [x] Create `src/twat/dev/cleanup.py` consolidating the 14 duplicate `cleanup.py` scripts (ref: [02](issues/02.md))
 [x] Create `src/twat/dev/checks.py` with ruff, mypy, pytest runners (ref: [02](issues/02.md))
 [x] Create `src/twat/dev/git_ops.py` with git status/commit/push helpers (ref: [02](issues/02.md))
 [x] Replace all plugin `cleanup.py` files with thin wrappers calling `twat.dev.cleanup.run()` (ref: [02](issues/02.md))
 [x] Replace `twat_image/cleanup.sh` with Python `cleanup.py` wrapper (ref: [02](issues/02.md))

### 1.3 pyproject.toml Standardization (spec 03)

 [x] Define canonical `[tool.ruff]` config: `target-version = "py310"`, `line-length = 120` (ref: [03](issues/03.md))
 [x] Copy canonical `[tool.ruff.lint]` select rules to all 17 plugin `pyproject.toml` files (ref: [03](issues/03.md))
 [x] Set `[tool.mypy] strict = true` in all plugin `pyproject.toml` files (ref: [03](issues/03.md))
 [x] Standardize `[tool.pytest.ini_options]` with `testpaths` and `markers` in all plugins (ref: [03](issues/03.md))
 [x] Set `requires-python = ">=3.10"` in all plugin `pyproject.toml` files (ref: [03](issues/03.md))
 [x] Standardize metadata (author, license, classifiers) in all plugin `pyproject.toml` (ref: [03](issues/03.md))
 [x] Delete `plugins/repos/twat_search/pyproject_next.toml` after merging needed changes (ref: [03](issues/03.md))
 [x] Add consistent `[project.optional-dependencies]` groups (`dev`, `test`, `docs`) to all plugins (ref: [03](issues/03.md))

### 1.4 Type Annotations and MyPy (spec 09)

 [x] Add `py.typed` marker file to all plugins missing it (ref: [09](issues/09.md))
 [x] Enable `strict = true` in mypy config for all plugins (ref: [09](issues/09.md))
 [x] Fix the 28 mypy errors in `twat_fs` upload providers (ref: [09](issues/09.md))
 [x] Add missing type annotations to `twat_search` engines (ref: [09](issues/09.md))
 [x] Complete type annotations in `twat_genai` core/engines (ref: [09](issues/09.md))
 [x] Audit and fix all `# type: ignore` comments lacking specific error codes (ref: [09](issues/09.md))

### 1.5 Ruff Linting (specs 10, 31)

 [x] Run `ruff check --fix` on `twat_fs/src/twat_fs/` and fix auto-fixable errors (ref: [31](issues/31.md))
 [x] Manually fix remaining ruff errors in `twat_fs` upload providers (F401, BLE001) (ref: [31](issues/31.md))
 [x] Remove unnecessary `# noqa` comments from `twat_fs` after fixing issues (ref: [31](issues/31.md))
 [x] Run `ruff check` on all other plugins, fix any violations (ref: [10](issues/10.md))
 [x] Run `ruff format` across all plugins, commit results (ref: [10](issues/10.md))
 [x] Create `.pre-commit-config.yaml` at host root with ruff hooks (ref: [10](issues/10.md))

### 1.6 `__init__.py` Standardization (spec 11)

 [x] Add `__all__` to `twat_coding/__init__.py` (ref: [11](issues/11.md))
 [x] Add `__all__` to `twat_fs/__init__.py` (ref: [11](issues/11.md))
 [x] Add `__all__` to `twat_genai/__init__.py` (ref: [11](issues/11.md))
 [x] Add `__all__` to `twat_search/__init__.py` (ref: [11](issues/11.md))
 [x] Add `__all__` to all remaining plugins missing it (ref: [11](issues/11.md))
 [x] Ensure `main()` is exposed for CLI dispatch in every plugin `__init__.py` (ref: [11](issues/11.md))
 [x] Add module-level docstrings to all plugin `__init__.py` files (ref: [11](issues/11.md))
 [x] Remove re-exports of internal modules, keep only public API in `__init__.py` (ref: [11](issues/11.md))

### 1.7 Build Scripts Consolidation (spec 12)

 [x] Define standard Hatch environments (`default`, `lint`) in canonical `pyproject.toml` (ref: [12](issues/12.md))
 [x] Add `hatch run test`, `hatch run lint:all` scripts to all plugin `pyproject.toml` (ref: [12](issues/12.md))
 [x] Remove `plugins/repos/twat_cache/scripts/` (build.py, release.py, version.py, setup-dev.sh) (ref: [12](issues/12.md))
 [x] Remove `plugins/repos/twat_fs/scripts/` except `build_binary.py` (ref: [12](issues/12.md))
 [x] Remove `plugins/repos/twat_os/scripts/` (build.py, check.py, release.py, test.py) (ref: [12](issues/12.md))
 [x] Remove `plugins/repos/twat_llm/scripts/` shell scripts (ref: [12](issues/12.md))
 [x] Remove `plugins/repos/twat_search/scripts/` shell scripts (ref: [12](issues/12.md))
 [x] Remove `plugins/repos/twat_text/scripts/build.py` (ref: [12](issues/12.md))

### 1.8 Dead Code and Stale File Cleanup (spec 13)

 [x] Delete `twat_search/google_debug_*.html` debug files (ref: [13](issues/13.md))
 [x] Delete `twat_search/debug_fetch.py` (ref: [13](issues/13.md))
 [x] Delete `twat_search/falla_search.py` (or move to examples/) (ref: [13](issues/13.md))
 [x] Delete `twat_search/requirements.txt` (deps in pyproject.toml) (ref: [13](issues/13.md))
 [x] Delete `twat_coding/repomix-output.txt` and add to `.gitignore` (ref: [13](issues/13.md))
 [x] Delete `twat_image/old/` directory (unreferenced legacy code) (ref: [13](issues/13.md))
 [x] Evaluate all `LOG.md` files across plugins, delete stale ones (none found) (ref: [13](issues/13.md))
 [x] Remove all tracked `.DS_Store` files and add to `.gitignore` (ref: [13](issues/13.md))
 [x] Add comprehensive `.gitignore` to every plugin repo (ref: [13](issues/13.md))

### 1.9 Error Handling Standardization (spec 14)

 [x] Create `src/twat/common/exceptions.py` with `TwatError`, `PluginError`, `ConfigError`, `DependencyError` (ref: [14](issues/14.md))
 [x] Update `twat/__init__.py` to use `PluginError` instead of bare `AttributeError` (ref: [14](issues/14.md))
 [x] Make `twat_cache/exceptions.py` extend `TwatError` base (ref: [14](issues/14.md))
 [x] Make `twat_coding/pystubnik/errors.py` extend `TwatError` base (ref: [14](issues/14.md))
 [x] Add custom exceptions to `twat_fs` replacing generic `Exception` usage (ref: [14](issues/14.md))

### 1.10 Logging Standardization (spec 15)

 [x] Create `src/twat/common/logging.py` with `get_logger()` and `configure_logging()` (ref: [15](issues/15.md))
 [x] Migrate `twat_cache/logging.py` to use `twat.common.logging` as a thin wrapper (ref: [15](issues/15.md))
 [x] Add `loguru` as a core dependency of host `twat` package (ref: [15](issues/15.md))
 [x] Replace `print()` statements used for operational output with logger calls in all plugins (ref: [15](issues/15.md))

---

## Phase 2: Fix Critical Issues

### 2.1 Version Conflict in twat_coding (spec 39)

 [x] Delete `plugins/repos/twat_coding/src/twat_coding/_version.py` (ref: [39](issues/39.md))
 [x] Rewrite `twat_coding/__init__.py` to use `importlib.metadata.version("twat-coding")` (ref: [39](issues/39.md))
 [x] Remove hardcoded `__version__ = "0.1.0"` from `twat_coding/twat_coding.py` (ref: [39](issues/39.md))
 [x] Add `_version.py` to `twat_coding/.gitignore` (ref: [39](issues/39.md))
 [x] Update `twat_coding/pyproject.toml` hatch-vcs config to write `__version__.py` only (ref: [39](issues/39.md))

### 2.2 twat_ez pyproject.toml Location (spec 61)

 [x] Move `plugins/pyproject.toml` (actually twat-ez config) into `plugins/repos/twat_ez/` or delete if redundant (ref: [61](issues/61.md))

### 2.3 twat_image Package Naming Fix (spec 70)

 [x] Move source code from `src/image_alpha_utils/` to `src/twat_image/` (ref: [70](issues/70.md))
 [x] Move `gray2alpha.py` from `image_alpha_utils/` to `twat_image/` (ref: [70](issues/70.md))
 [x] Update `twat_image/pyproject.toml` package name to `twat-image` (ref: [70](issues/70.md))
 [x] Update entry point to register under `twat.plugins` group (ref: [70](issues/70.md))
 [x] Update `imagealpha` CLI entry point to point to `twat_image.gray2alpha:cli` (ref: [70](issues/70.md))
 [x] Add deprecation shim in `src/image_alpha_utils/__init__.py` (ref: [70](issues/70.md))
 [x] Rename test file `test_image_alpha_utils.py` to `test_twat_image.py` and update imports (ref: [70](issues/70.md))

### 2.4 twat_audio Missing `__init__.py` (spec 76)

 [x] Create proper `twat_audio/__init__.py` with `__all__`, version, and public API exports (ref: [76](issues/76.md))

### 2.5 Rename twat_video to twat_font (spec 78)

 [x] Rename `plugins/repos/twat_video` directory to `plugins/repos/twat_font` (ref: [78](issues/78.md))
 [x] Update `pyproject.toml` to declare `name = "twat-font"` (ref: [78](issues/78.md))
 [x] Update entry point to register as `font` in `twat.plugins` group (ref: [78](issues/78.md))
 [x] Rename `src/twat_video/` to `src/twat_font/` (ref: [78](issues/78.md))
 [x] Update all imports from `twat_video` to `twat_font` (ref: [78](issues/78.md))
 [x] Update `mkdocs.yml` site name and references (ref: [78](issues/78.md))
 [x] Update all test imports for the new package name (ref: [78](issues/78.md))

### 2.6 font_organizer Source Location Fix (spec 79)

 [x] Move code from `src/font_organizer/` into `src/twat_font/` (ref: [79](issues/79.md))
 [x] Update all internal imports from `font_organizer` to `twat_font` (ref: [79](issues/79.md))
 [x] Delete empty `src/font_organizer/` after migration (ref: [79](issues/79.md))

### 2.7 Misplaced Config in twat_search (spec 52)

 [x] Move stray test files (`test_falla.py`, `test_simple.py`, etc.) from repo root into `tests/` (ref: [52](issues/52.md))
 [x] Delete debug HTML files from `twat_search` root (ref: [52](issues/52.md))
 [x] Delete `twat_search/requirements.txt` (ref: [52](issues/52.md))

---

## Phase 3: Plugin Modernization

### 3.1 twat_cache: Engine Interface Refactoring (spec 21)

- [x] Slim `BaseCacheEngine` to 3 abstract methods: `is_available()`, `cache()`, `clear()` (ref: [21](issues/21.md))
- [x] Remove path management code from `BaseCacheEngine.__init__` (ref: [21](issues/21.md))
- [x] Delete duplicate `CacheEngine` ABC from `type_defs.py` (lines 139-190) (ref: [21](issues/21.md))
- [x] Move path setup into `DiskCacheEngine.__init__` (ref: [21](issues/21.md))
- [x] Move path setup into `JoblibEngine.__init__` (ref: [21](issues/21.md))
- [x] Move path setup into `KleptoEngine.__init__` (ref: [21](issues/21.md))
- [x] Remove unused abstract method stubs from `cachebox.py`, `cachetools.py`, `functools_engine.py` (ref: [21](issues/21.md))
- [x] Extract stats tracking into a `StatsTracker` mixin (ref: [21](issues/21.md))
- [x] Remove `validate_config()` from base class (Pydantic handles it) (ref: [21](issues/21.md))

### 3.2 twat_cache: Decorator API Simplification (spec 22)

- [ ] Remove `mcache`, `bcache`, `fcache` from `decorators.py`, add deprecation shims (ref: [22](issues/22.md))
 [x] Remove `use_sql` parameter from all public APIs (ref: [22](issues/22.md))
- [ ] Consolidate `_select_best_backend` and `_create_engine` into `_resolve_engine()` (ref: [22](issues/22.md))
- [ ] Update README to show only `ucache` and `acache` examples (ref: [22](issues/22.md))

### 3.3 twat_cache: Remove AioCache and Redis (spec 23)

- [ ] Delete `plugins/repos/twat_cache/src/twat_cache/engines/aiocache.py` (ref: [23](issues/23.md))
- [ ] Remove Redis engine import from `manager.py` (lines 70-76) (ref: [23](issues/23.md))
- [ ] Remove `aiocache` registration from `manager.py` (ref: [23](issues/23.md))
- [ ] Rewrite `acache` decorator to wrap sync engines with async (ref: [23](issues/23.md))
- [ ] Remove `aiocache` and `redis` from `pyproject.toml` optional deps (ref: [23](issues/23.md))
- [ ] Remove `HAS_AIOCACHE` checks from `decorators.py` (ref: [23](issues/23.md))
- [ ] Remove `"aiocache"` from `BackendType` literal in `type_defs.py` (ref: [23](issues/23.md))

### 3.4 twat_cache: CacheConfig Consolidation (spec 24)

- [ ] Delete `CacheConfig` protocol from `type_defs.py` (ref: [24](issues/24.md))
- [ ] Delete `CacheStats` ABC from `type_defs.py` (ref: [24](issues/24.md))
- [ ] Move useful type aliases (`BackendType`, type vars) from `type_defs.py` into `config.py` (ref: [24](issues/24.md))
- [ ] Clean up dead `# REMOVED` comments in `config.py` (ref: [24](issues/24.md))
- [ ] Remove getter methods (`get_maxsize`, `get_folder_name`) from `CacheConfig` (ref: [24](issues/24.md))
- [ ] Rename `type_defs.py` to `types.py` or delete it (ref: [24](issues/24.md))

### 3.5 twat_cache: Context Manager Cleanup (spec 25)

- [ ] Delete `CacheContext` class from `context.py` (ref: [25](issues/25.md))
- [ ] Delete `get_or_create_engine()` from `context.py` (ref: [25](issues/25.md))
- [ ] Simplify `engine_context()` to ~25 lines (ref: [25](issues/25.md))
- [ ] Add `CacheEngineManager` singleton at module level (ref: [25](issues/25.md))
- [ ] Remove `CacheContext` and `get_or_create_engine` from `__init__.py` exports (ref: [25](issues/25.md))

### 3.6 twat_cache: Engine Manager Refactoring (spec 26)

- [ ] Rewrite `manager.py` to use lazy imports via `importlib.import_module()` (ref: [26](issues/26.md))
- [ ] Replace `CacheEngineManager` class with stateless `resolve_engine()` function (ref: [26](issues/26.md))
- [ ] Remove `_select_best_backend()` from `decorators.py` (use manager's `resolve_engine`) (ref: [26](issues/26.md))
- [ ] Define clear fallback chain: preferred, diskcache, cachetools, functools (ref: [26](issues/26.md))

### 3.7 twat_cache: Test Suite Rationalization (spec 27)

- [ ] Merge `test_cache.py` + `test_twat_cache.py` + `test_integration.py` into `test_decorators.py` (ref: [27](issues/27.md))
- [ ] Merge `test_exceptions_simple.py` into `test_exceptions.py`, delete the simple file (ref: [27](issues/27.md))
- [ ] Merge `test_context_simple.py` into `test_context.py`, delete the simple file (ref: [27](issues/27.md))
- [ ] Merge `test_fallback.py` into `test_engines.py` (ref: [27](issues/27.md))
- [ ] Merge `test_constants.py` into `test_config.py` (ref: [27](issues/27.md))
- [ ] Simplify `conftest.py` to only shared fixtures (ref: [27](issues/27.md))

### 3.8 twat_cache: Path Management and Benchmarks (specs 28, 29, 30)

- [ ] Remove `get_cache_dir()` from `decorators.py` (lines 88-125) (ref: [28](issues/28.md))
- [ ] Remove `ensure_dir_exists()` from `engines/common.py` (ref: [28](issues/28.md))
- [ ] Fix `cache.py` `clear_cache()` to use `paths.clear_cache_dir()` instead of hardcoded paths (ref: [28](issues/28.md))
- [ ] Remove random UUID fallback from `get_cache_path()` in `paths.py` (ref: [28](issues/28.md))
- [ ] Set up pytest-benchmark in `test_benchmark.py` with proper markers (ref: [29](issues/29.md))
- [ ] Write cache plugin usage examples in README or `docs/` (ref: [30](issues/30.md))

### 3.9 twat_fs: Ruff and MyPy Fixes (specs 31, 32)

- [ ] Fix all unused import (F401) errors in `twat_fs` (ref: [31](issues/31.md))
- [ ] Fix broad exception catches (BLE001) in `twat_fs` upload providers (ref: [31](issues/31.md))
- [ ] Add missing return type annotations to `twat_fs` provider modules (ref: [32](issues/32.md))
- [ ] Fix all 28 mypy errors in `twat_fs` (ref: [32](issues/32.md))

### 3.10 twat_fs: Upload Provider and Factory (specs 33, 34, 35)

- [ ] Define `UploadProvider` Protocol in `twat_fs` with `upload()`, `is_available()`, `name` (ref: [33](issues/33.md))
- [ ] Make all upload providers implement the `UploadProvider` protocol (ref: [33](issues/33.md))
- [ ] Remove async/sync duplication in upload providers (ref: [34](issues/34.md))
- [ ] Create provider registry with `register_provider()` / `get_provider()` (ref: [35](issues/35.md))

### 3.11 twat_fs: CLI and Tests (specs 36, 37, 38)

- [ ] Modernize `twat_fs` CLI with click or fire, add `--help` output (ref: [36](issues/36.md))
- [ ] Remove misplaced files in `twat_fs` (stray configs, artifacts) (ref: [37](issues/37.md))
- [ ] Add tests for each upload provider in `twat_fs` (ref: [38](issues/38.md))
- [ ] Add integration tests for the upload pipeline (ref: [38](issues/38.md))

### 3.12 twat_coding: Cleanup (specs 40, 41, 42, 43, 44, 45)

- [ ] Consolidate pystubnik config into a single `config.py` using Pydantic (ref: [40](issues/40.md))
- [ ] Remove unimplemented mypy backend from pystubnik (ref: [41](issues/41.md))
- [ ] Add tests for pystubnik stub generation (ref: [42](issues/42.md))
- [ ] Clean up pystubnik processor pipeline (ref: [43](issues/43.md))
- [ ] Remove stale `twat_coding.py` at package root (or merge needed code into package) (ref: [44](issues/44.md))
- [ ] Enhance pystubnik CLI with `--help` and proper argument parsing (ref: [45](issues/45.md))

### 3.13 twat_genai: Engine and Config (specs 46, 47, 48, 49, 50)

- [ ] Audit `engines/base.py` for completeness (generate, inpaint, outpaint, upscale) (ref: [46](issues/46.md))
- [ ] Create engine registry in `engines/__init__.py` with `register_engine()` / `get_engine()` (ref: [46](issues/46.md))
- [ ] Refactor fal engine to register itself on import (ref: [46](issues/46.md))
- [ ] Remove fal-specific imports from `core/` modules (ref: [46](issues/46.md))
- [ ] Add a mock engine for testing without API keys (ref: [46](issues/46.md))
- [ ] Delete misplaced files in `twat_genai` (test files at root, stray configs) (ref: [47](issues/47.md))
- [ ] Standardize `twat_genai` config using Pydantic, separate engine-specific config (ref: [48](issues/48.md))
- [ ] Document the image pipeline with diagrams or flowcharts (ref: [49](issues/49.md))
- [ ] Improve LoRA management: validation, path resolution, lazy loading (ref: [50](issues/50.md))

### 3.14 twat_search: lib_falla and Engines (specs 51, 53, 54, 55, 56)

- [ ] Move `web/engines/lib_falla/` to `_vendor/falla/` with proper attribution (ref: [51](issues/51.md))
- [ ] Add license and version tracking to vendored falla code (ref: [51](issues/51.md))
- [ ] Remove embedded `requirements.txt` from lib_falla (ref: [51](issues/51.md))
- [ ] Update `FallaEngine` to handle import gracefully if falla not installed (ref: [51](issues/51.md))
- [ ] Define `BaseSearchEngine` protocol with standard methods (ref: [53](issues/53.md))
- [ ] Make all search engines implement the `BaseSearchEngine` protocol (ref: [53](issues/53.md))
- [ ] Centralize API key management in `twat_search` config (ref: [54](issues/54.md))
- [ ] Add proper error handling with custom exceptions to `twat_search` (ref: [55](issues/55.md))
 [x] Move root-level test files into `tests/` directory (ref: [56](issues/56.md))
- [ ] Add unit tests for each search engine in `twat_search` (ref: [56](issues/56.md))

### 3.15 twat_llm: Cleanup (specs 57, 58, 59, 60)

- [ ] Clean up `twat_llm` module structure (ref: [57](issues/57.md))
- [ ] Migrate shell scripts in `twat_llm/scripts/` to Hatch commands (ref: [58](issues/58.md))
- [ ] Create API abstraction layer for LLM providers (ref: [59](issues/59.md))
- [ ] Clean up stale research docs and examples in `twat_llm/docs/` (ref: [60](issues/60.md))

### 3.16 twat_ez: Modernization (specs 62, 63)

- [ ] Modernize `py_needs` module with proper type annotations (ref: [62](issues/62.md))
- [ ] Add `__all__` and public API declaration to `twat_ez/__init__.py` (ref: [63](issues/63.md))
- [ ] Add docstring to `twat_ez/__init__.py` (ref: [63](issues/63.md))

### 3.17 twat_os: Foundation (specs 64, 65, 66)

- [ ] Establish `twat_os` as the shared path management foundation for all plugins (ref: [64](issues/64.md))
- [ ] Add `get_app_cache_dir()`, `get_app_config_dir()` functions to `twat_os` (ref: [64](issues/64.md))
- [ ] Enhance TOML config handling in `twat_os` (ref: [65](issues/65.md))
- [ ] Use `twat_os` test suite as reference implementation for other plugins (ref: [66](issues/66.md))

### 3.18 twat_hatch: Templates (specs 67, 68, 69)

- [ ] Update `twat_hatch` plugin template to reflect spec 03 pyproject.toml standards (ref: [67](issues/67.md))
- [ ] Update `twat_hatch` plugin template to reflect spec 11 `__init__.py` pattern (ref: [67](issues/67.md))
- [ ] Create AGENTS.md template in `twat_hatch` for AI-assisted development (ref: [68](issues/68.md))
- [ ] Add validation tests for `twat_hatch` themes (generate plugin, run lint/test) (ref: [69](issues/69.md))

### 3.19 twat_image: Legacy Cleanup (specs 71, 72)

 [x] Delete `twat_image/old/imgproxyproc/` directory (ref: [71](issues/71.md))
 [x] Delete `twat_image/old/imgscale.py` (ref: [71](issues/71.md))
 [x] Delete `twat_image/old/` directory entirely (ref: [71](issues/71.md))
- [ ] Standardize build/install scripts in `twat_image` (ref: [72](issues/72.md))

### 3.20 twat_mp: Review (specs 73, 74, 75)

- [ ] Review and simplify `twat_mp` public API (ref: [73](issues/73.md))
- [ ] Add integration path between `twat_mp` and `twat_cache` (ref: [74](issues/74.md))
- [ ] Consolidate `twat_mp` documentation (ref: [75](issues/75.md))

### 3.21 twat_audio: Bootstrap (specs 76, 77)

 [x] Create `twat_audio/__init__.py` with proper exports and `__all__` (ref: [76](issues/76.md))
 [x] Add `py.typed` marker to `twat_audio` (ref: [76](issues/76.md))
- [ ] Define feature expansion roadmap for `twat_audio` (ref: [77](issues/77.md))

### 3.22 twat_font (ex-twat_video): Shell Scripts and Cleanup (specs 80, 79)

 [x] Migrate `build.sh`, `release.sh`, `test.sh` in twat_font to Hatch commands (deleted scripts) (ref: [80](issues/80.md))
 [x] Delete shell scripts from `twat_font/scripts/` after migration (ref: [80](issues/80.md))
 [x] Move `font_organizer` code into `src/twat_font/` namespace (ref: [79](issues/79.md))

### 3.23 twat_task: Cleanup (specs 81, 82)

- [ ] Clean up and simplify `twat_task` module structure (ref: [81](issues/81.md))
- [ ] Remove unused code and stale dependencies from `twat_task` (ref: [81](issues/81.md))
- [ ] Modernize Prefect integration in `twat_task` (ref: [82](issues/82.md))

### 3.24 Skeleton Plugins: Activation (specs 83, 84, 85)

- [ ] Create activation plan for `twat_speech`: define minimal API surface (ref: [83](issues/83.md))
- [ ] Add placeholder `__init__.py` with `__all__` and version to `twat_speech` (ref: [83](issues/83.md))
- [ ] Create activation plan for `twat_text`: define minimal API surface (ref: [84](issues/84.md))
- [ ] Add placeholder `__init__.py` with `__all__` and version to `twat_text` (ref: [84](issues/84.md))
- [ ] Define purpose and scope for `twat_labs` (ref: [85](issues/85.md))
- [ ] Add placeholder `__init__.py` with `__all__` and version to `twat_labs` (ref: [85](issues/85.md))

---

## Phase 4: Integration & Ecosystem

### 4.1 CI/CD Pipeline (spec 04)

- [ ] Create `.github/workflows/ci-plugin.yml` reusable workflow (Python 3.10-3.13 matrix) (ref: [04](issues/04.md))
- [ ] Create `.github/workflows/ci-host.yml` for the host package (ref: [04](issues/04.md))
- [ ] Create `.github/workflows/release-plugin.yml` with PyPI publishing (ref: [04](issues/04.md))
- [ ] Add per-plugin workflow files referencing shared templates (ref: [04](issues/04.md))
- [ ] Remove ad-hoc `scripts/release.py` after CI release workflow works (ref: [04](issues/04.md))

### 4.2 Dependency Management (spec 05)

- [ ] Make `twat` an optional dependency for plugins (move to `[project.optional-dependencies]`) (ref: [05](issues/05.md))
- [ ] Declare `twat-cache` as test dependency in `twat_fs/pyproject.toml` (ref: [05](issues/05.md))
- [ ] Create dependency graph validation script in `src/twat/dev/deps.py` (ref: [05](issues/05.md))
 [x] Remove or relocate `plugins/pyproject.toml` (it's twat-ez's config) (ref: [05](issues/05.md))

### 4.3 Testing Framework (spec 06)

- [ ] Create `src/twat/testing/__init__.py` with shared test utilities (ref: [06](issues/06.md))
 [x] Move `twat_search` root-level test files into `tests/` (ref: [06](issues/06.md))
 [x] Move `twat_genai/test_outpaint.py` into `tests/` (ref: [06](issues/06.md))
- [ ] Create standard `tests/conftest.py` for all plugins missing one (ref: [06](issues/06.md))
- [ ] Add pytest markers (`slow`, `integration`, `benchmark`, `requires_api_key`) to all plugins (ref: [06](issues/06.md))

### 4.4 Documentation (spec 07)

- [ ] Create standardized README.md template (Overview, Installation, Quick Start, API, CLI) (ref: [07](issues/07.md))
- [ ] Update all 17 plugin READMEs to follow the standard template (ref: [07](issues/07.md))
- [ ] Create `mkdocs.yml` at host root for ecosystem-wide documentation (ref: [07](issues/07.md))
- [ ] Add pydocstyle rules (`D`) to ruff config for docstring enforcement (ref: [07](issues/07.md))
- [ ] Archive or delete stale PLAN.md, LOG.md files across plugins (ref: [07](issues/07.md))

### 4.5 Shared Utilities (spec 08)

 [x] Create `src/twat/common/__init__.py` (ref: [08](issues/08.md))
- [ ] Create `src/twat/common/paths.py` wrapping `platformdirs` (ref: [08](issues/08.md))
- [ ] Create `src/twat/common/config.py` with `BasePluginConfig` Pydantic model (ref: [08](issues/08.md))
- [ ] Create `src/twat/common/types.py` with shared type definitions (ref: [08](issues/08.md))
- [ ] Migrate `twat_cache/paths.py` to use `twat.common.paths` (ref: [08](issues/08.md))
- [ ] Migrate `twat_os/paths.py` to use `twat.common.paths` (ref: [08](issues/08.md))
- [ ] Migrate `twat_search/paths.py` to use `twat.common.paths` (ref: [08](issues/08.md))

### 4.6 Host Package Improvements (specs 16, 17, 18, 19, 20)

- [ ] Create `src/twat/registry.py` with `PluginRegistry` and `PluginInfo` dataclass (ref: [16](issues/16.md))
- [ ] Add `twat.plugins.list()` and `twat.plugins.load()` accessors (ref: [16](issues/16.md))
- [ ] Add graceful error handling for broken plugins in discovery (ref: [16](issues/16.md))
- [ ] Create `src/twat/cli.py` with `--help`, `--version`, `list`, `info` commands (ref: [17](issues/17.md))
- [ ] Add rich-formatted CLI output for `twat` command (ref: [17](issues/17.md))
- [ ] Add helpful error message when unknown plugin is requested (ref: [17](issues/17.md))
- [ ] Refactor `twat/__init__.py` to ~30 lines, delegating to `registry.py` and `cli.py` (ref: [18](issues/18.md))
- [ ] Restructure host `pyproject.toml` optional deps into `core`, `ai`, `media`, `dev`, `all` groups (ref: [19](issues/19.md))
- [ ] Document installation groups (`pip install twat[core]`) in README (ref: [19](issues/19.md))
- [ ] Add `twat new <plugin>` command integrating `twat_hatch` (ref: [20](issues/20.md))

### 4.7 twat_os as Shared Foundation (spec 64)

- [ ] Export `get_app_dir()`, `get_cache_dir()`, `get_config_dir()` from `twat_os` (ref: [64](issues/64.md))
- [ ] Wire `twat_cache/paths.py` to optionally use `twat_os` path utilities (ref: [64](issues/64.md))

### 4.8 Dependency Audit (spec 86)

- [ ] Run `pip-audit` across all 17 plugins, fix any known vulnerabilities (ref: [86](issues/86.md))
- [ ] Run `deptry` on all plugins to find unused dependencies (ref: [86](issues/86.md))
- [ ] Create `scripts/dep_matrix.py` showing cross-plugin dependency sharing (ref: [86](issues/86.md))
- [ ] Add `pip-audit` script to Hatch environments in all plugins (ref: [86](issues/86.md))
- [ ] Check for circular dependencies between twat plugins (ref: [86](issues/86.md))

### 4.9 Plugin Interoperability (spec 87)

- [ ] Define plugin interoperability standards (shared types, discovery protocol) (ref: [87](issues/87.md))
- [ ] Document how plugins should declare and consume each other (ref: [87](issues/87.md))

### 4.10 Release Coordination (spec 88)

- [ ] Define ecosystem release coordination process (ref: [88](issues/88.md))
- [ ] Create CHANGELOG.md template for all plugins (ref: [88](issues/88.md))
- [ ] Add automated changelog generation via git tags (ref: [88](issues/88.md))

---

## Phase 5: Polish & Documentation

### 5.1 Developer Onboarding (spec 89)

- [ ] Create `CONTRIBUTING.md` in root repo with setup instructions (ref: [89](issues/89.md))
- [ ] Create plugin scaffold template in `templates/plugin/` (ref: [89](issues/89.md))
- [ ] Create `.github/ISSUE_TEMPLATE/bug_report.yml` (ref: [89](issues/89.md))
- [ ] Create `.github/ISSUE_TEMPLATE/feature_request.yml` (ref: [89](issues/89.md))
- [ ] Create `.github/pull_request_template.md` with review checklist (ref: [89](issues/89.md))
- [ ] Add "Contributing" section to root `README.md` linking to `CONTRIBUTING.md` (ref: [89](issues/89.md))

### 5.2 Monitoring and Health (spec 90)

- [ ] Create a health check script that verifies all plugins import correctly (ref: [90](issues/90.md))
- [ ] Add a dashboard or summary command (`twat status`) showing ecosystem health (ref: [90](issues/90.md))
- [ ] Add import-time checks to catch broken plugins early (ref: [90](issues/90.md))

### 5.3 Final Verification

- [ ] Run `ruff check` across all 17 plugins, confirm zero errors (ref: [10](issues/10.md))
- [ ] Run `ruff format --check` across all plugins, confirm zero changes needed (ref: [10](issues/10.md))
- [ ] Run `mypy --strict` across all plugins, confirm zero errors (ref: [09](issues/09.md))
- [ ] Run `pytest` in every plugin, confirm all tests pass (ref: [06](issues/06.md))
- [ ] Verify `importlib.metadata.version()` works for every installed plugin (ref: [01](issues/01.md))
- [ ] Verify `twat.plugins.list()` shows all plugins with correct metadata (ref: [16](issues/16.md))
- [ ] Verify `twat <plugin> --help` works for every plugin with a CLI (ref: [17](issues/17.md))
- [ ] Verify no `.DS_Store`, `repomix-output.*`, or `__pycache__` tracked in git (ref: [13](issues/13.md))
- [ ] Verify all plugins have `__all__`, docstrings, and `py.typed` (ref: [11](issues/11.md))
- [ ] Verify CI workflows run on push/PR for all plugins (ref: [04](issues/04.md))
- [ ] Verify `pip install twat[all]` installs all plugins without conflicts (ref: [19](issues/19.md))
- [ ] Do a final read-through of all README files for accuracy (ref: [07](issues/07.md))
