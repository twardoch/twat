# AGENTS.md — twat Codebase Guide for AI Development

> This document provides codebase structure, conventions, and actionable development guidelines for AI coding agents working on the `twat` plugin ecosystem.

## 1. Architecture Overview

**twat** is a lightweight Python plugin framework. It consists of:

- **Host package** (`twat`): Plugin discovery, loading, and CLI dispatch
- **17 plugin packages**: Standalone repos in `plugins/repos/`, each independently installable

The host uses `importlib.metadata` entry points (`twat.plugins` group) to discover plugins at runtime. Plugins are accessed as `twat.<plugin_name>` via `__getattr__` dynamic loading.

```
twat/                          # Host package repo
├── src/twat/__init__.py       # Core: plugin discovery, __getattr__, main(), run_plugin()
├── pyproject.toml             # Host package config
├── issues/                    # 90 modernization spec documents (01.md–90.md)
├── PLAN.md                    # Hyperlinked ToC of all specs
├── TODO.md                    # Actionable task checklist
└── plugins/repos/             # Plugin repositories (standalone)
    ├── twat_audio/            # Audio resampling (Pedalboard)
    ├── twat_cache/            # Multi-backend caching decorators
    ├── twat_coding/           # AST-based stub generation (pystubnik)
    ├── twat_ez/               # Auto dependency install, path discovery
    ├── twat_fs/               # Multi-provider file upload (S3, catbox, etc.)
    ├── twat_genai/            # fal.ai generative image toolkit
    ├── twat_hatch/            # Package scaffolding (Jinja2 templates)
    ├── twat_image/            # Image alpha channel processing
    ├── twat_labs/             # Experimental (skeleton)
    ├── twat_llm/              # LLM integration (ask, chain, batch)
    ├── twat_mp/               # Parallel processing (Pathos)
    ├── twat_os/               # Cross-platform path management
    ├── twat_search/           # Multi-engine web search
    ├── twat_speech/           # Speech processing (skeleton)
    ├── twat_task/             # Task orchestration (Prefect)
    ├── twat_text/             # Text processing (skeleton)
    └── twat_video/            # MISNAMED: actually font_organizer (to be renamed twat_font)
```

### Key Architectural Facts

- **NOT a monorepo**. Each plugin in `plugins/repos/` is a standalone git repo. They are collected here for coordinated development.
- **Plugin registration**: Each plugin's `pyproject.toml` declares an entry point under `[project.entry-points."twat.plugins"]`.
- **CLI dispatch**: `twat <plugin_name> [args...]` calls `plugin.main()`. Plugins must expose a `main()` function.
- **Dynamic loading**: `import twat; twat.fs` triggers `__getattr__("fs")` → entry point lookup → `ep.load()` → `sys.modules["twat.fs"]`.

## 2. Plugin Complexity Tiers

| Tier | Plugins | Notes |
|------|---------|-------|
| **Complex** | `twat_cache`, `twat_fs`, `twat_search`, `twat_coding`, `twat_genai` | Multiple subpackages, significant code, active tech debt |
| **Medium** | `twat_llm`, `twat_os`, `twat_hatch`, `twat_image`, `twat_video`(→`twat_font`) | Working code, needs cleanup |
| **Simple** | `twat_audio`, `twat_mp`, `twat_ez`, `twat_task` | Small, focused, minimal issues |
| **Skeleton** | `twat_speech`, `twat_text`, `twat_labs` | Placeholder code only |

## 3. Standard Plugin Structure

Every plugin should follow this layout:

```
twat_<name>/
├── src/twat_<name>/
│   ├── __init__.py            # Public API, __all__, main() for CLI
│   ├── __main__.py            # python -m twat_<name> entry point
│   └── <modules>.py           # Implementation
├── tests/
│   ├── conftest.py
│   ├── test_<name>.py
│   └── test_*.py
├── pyproject.toml             # Hatch build, entry points, deps
├── README.md
├── LICENSE                    # MIT
└── AGENTS.md                  # Plugin-specific AI guidelines (optional)
```

## 4. Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|
| **PyPI package** | `twat-<name>` (hyphens) | `twat-fs` |
| **Import module** | `twat_<name>` (underscores) | `twat_fs` |
| **Entry point name** | `<name>` (no prefix) | `fs` |
| **CLI command** | `twat <name>` | `twat fs` |
| **Source directory** | `src/twat_<name>/` | `src/twat_fs/` |

## 5. Coding Standards

### Python Version
- **Python 3.10+** minimum. Use `from __future__ import annotations` for modern type syntax.

### Type Hints
- **PEP 484 / PEP 585** type hints on all public functions and methods.
- Use `str | None` instead of `Optional[str]`.
- Use `list[str]` instead of `List[str]`.
- Target: zero `mypy --strict` errors.

### Formatting & Linting
- **Ruff** for both formatting and linting. Configuration in each plugin's `pyproject.toml`.
- Line length: typically 88 or 120 (check per-plugin config).
- Run: `ruff check . --fix && ruff format .`

### Static Analysis
- **MyPy** with strict mode. Run: `mypy src/`
- No `as any`, `@ts-ignore`-equivalent (`# type: ignore` only with specific error codes).

### Error Handling
- Use custom exception hierarchies per plugin (e.g., `TwatCacheError → ConfigurationError`).
- Never use bare `except:`. Always catch specific exceptions.
- Prefer `except Exception as e:` with logging over silent swallowing.

### Logging
- **loguru** is the ecosystem standard logger.
- Never use `logging.basicConfig()` in library code.
- Use `from loguru import logger` then `logger.info(...)`, `logger.error(...)`, etc.

### Imports
- Standard library first, third-party second, local third (enforced by ruff `I` rules).
- Prefer absolute imports: `from twat_cache.engines.base import BaseCacheEngine`.

## 6. Version Management

### Canonical Pattern
```python
# src/twat_<name>/__init__.py
from importlib import metadata

try:
    __version__ = metadata.version("twat-<name>")
except metadata.PackageNotFoundError:
    __version__ = "0.0.0-dev"
```

### Rules
- **DELETE** any `_version.py` or `__version__.py` files — version comes from `importlib.metadata` only.
- Version is set in `pyproject.toml` (static) or derived via `hatch-vcs` from git tags.

## 7. `__init__.py` Standard

Every plugin's `__init__.py` must:

1. Set `__version__` via `importlib.metadata`
2. Define `__all__` listing all public exports
3. Expose a `main()` function for CLI dispatch
4. Import and re-export the plugin's public API

```python
"""twat-<name>: Brief description."""

from importlib import metadata

try:
    __version__ = metadata.version("twat-<name>")
except metadata.PackageNotFoundError:
    __version__ = "0.0.0-dev"

from .<module> import SomeClass, some_function

try:
    from .__main__ import main
except ImportError:
    def main() -> None:
        print(f"Plugin {__package__} CLI dependencies not installed.")

__all__ = ["__version__", "SomeClass", "some_function", "main"]
```

## 8. `pyproject.toml` Standard

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "twat-<name>"
version = "X.Y.Z"
requires-python = ">=3.10"
license = "MIT"
dependencies = [
    # Minimal runtime dependencies
]

[project.optional-dependencies]
all = [
    # All optional features
]
dev = [
    "pytest>=8.0",
    "ruff>=0.4",
    "mypy>=1.10",
]

[project.scripts]
twat-<name> = "twat_<name>:main"

[project.entry-points."twat.plugins"]
<name> = "twat_<name>"

[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "ANN", "B", "A", "COM", "C4", "ISC", "PIE", "PT", "RSE", "RET", "SIM", "TID", "TCH", "ARG", "ERA", "PL"]

[tool.mypy]
python_version = "3.10"
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
```

## 9. Testing Standards

- **Framework**: pytest
- **Location**: `tests/` directory at repo root
- **Naming**: `test_<module>.py` files with `test_<function_name>` functions
- **Structure** (reference: twat_os):
  ```
  tests/
  ├── conftest.py           # Shared fixtures
  ├── unit/                 # Unit tests (no I/O, no network)
  ├── integration/          # Integration tests (may need fixtures)
  ├── test_<name>.py        # Module-level tests
  └── test_package.py       # Import smoke tests
  ```
- **Run**: `hatch run test` or `pytest tests/`
- **Coverage**: Target 80%+ for complex plugins

## 10. Build & Development Workflow

```bash
# Enter plugin directory
cd plugins/repos/twat_<name>

# Create dev environment
hatch shell

# Install in dev mode
pip install -e ".[dev,all]"

# Run tests
pytest tests/

# Run linting
ruff check . --fix
ruff format .

# Run type checking
mypy src/

# Build package
hatch build
```

## 11. Commit Message Convention

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new feature
fix: resolve bug in X
docs: update README
refactor: simplify config loading
test: add tests for Y
chore: update dependencies
```

## 12. Known Issues & Tech Debt

### Critical (Fix First)
- **twat_coding**: Conflicting `__version__.py` and `_version.py` → ValueError on import (spec [39](issues/39.md))
- **twat_ez**: `pyproject.toml` misplaced at `plugins/` root instead of in the plugin dir (spec [61](issues/61.md))
- **twat_image**: Source in `src/image_alpha_utils/` instead of `src/twat_image/` (spec [70](issues/70.md))
- **twat_audio**: Missing `__init__.py` entirely (spec [76](issues/76.md))
- **twat_video**: Misnamed — contains font organizer code, not video (spec [78](issues/78.md))

### High (Fix Soon)
- **twat_fs**: 81 ruff errors, 28 mypy errors (specs [31](issues/31.md), [32](issues/32.md))
- **twat_cache**: `aiocache.py` references removed `redis_host`/`redis_port` config → would crash at runtime (spec [23](issues/23.md))
- **twat_search**: Embedded `lib_falla` sub-package needs extraction (spec [51](issues/51.md))
- **14 repos**: Duplicate `cleanup.py` scripts (spec [02](issues/02.md))

### Medium (Modernization)
- Inconsistent `__init__.py` exports across plugins (spec [11](issues/11.md))
- No unified CI/CD pipeline (spec [04](issues/04.md))
- Test files scattered (some at repo root, some in `tests/`) (specs [52](issues/52.md), [56](issues/56.md))

## 13. Spec Documents Reference

All 90 modernization specs are in `issues/01.md` through `issues/90.md`. See [PLAN.md](PLAN.md) for the hyperlinked table of contents organized by category and implementation phase.

Each spec follows this format:
```markdown
# NN: Title

## Problem        — What's wrong (1-3 sentences)
## Current State   — Bullet list of specifics
## Proposed Changes — Numbered steps with code examples
## Files to Modify  — Specific file paths
## Acceptance Criteria — Checkbox list of testable criteria
## Dependencies    — Cross-references to other specs
```

## 14. Guidelines for AI Agents

### Before Making Changes
1. **Read the relevant spec** in `issues/NN.md` before implementing
2. **Check acceptance criteria** — they define "done"
3. **Read existing code** in the target files before modifying
4. **Follow existing patterns** if the plugin has consistent conventions
5. **Check dependencies** — some specs must be done before others

### When Implementing
1. **One spec at a time** — don't mix changes from multiple specs
2. **Run linting** after every change: `ruff check . --fix && ruff format .`
3. **Run type checking** after adding/changing types: `mypy src/`
4. **Run tests** after every change: `pytest tests/`
5. **Commit atomically** — one logical change per commit, use conventional commit messages

### Common Pitfalls
- **Don't suppress type errors** with `# type: ignore` without specific error codes
- **Don't add `as Any`** casts to fix type errors — fix the actual types
- **Don't delete tests** that fail — fix the code or update the test
- **Don't refactor while fixing bugs** — do one or the other, never both
- **Don't modify files outside the target plugin** unless the spec explicitly says to
- **Watch for `cleanup.py`** — it exists in 14 repos and will be unified (spec [02](issues/02.md)); don't modify individual copies

### Plugin-Specific Notes

| Plugin | Watch Out For |
|--------|--------------|
| `twat_cache` | Most complex plugin. Engine manager has fallback chains. Don't break the `ucache`/`acache` public API. |
| `twat_fs` | 81 ruff errors. Fix incrementally, not all at once. Provider protocol in `protocols.py` is the source of truth. |
| `twat_coding` | `pystubnik` is the real package. `twat_coding.py` at root is dead code. |
| `twat_search` | `lib_falla` is an embedded third-party scraper. Don't modify it unless doing spec [51](issues/51.md). |
| `twat_genai` | Active development. Check for recent changes before modifying. |
| `twat_video` | Will be renamed to `twat_font`. Don't add new features until rename is complete. |
| `twat_image` | Code is in `src/image_alpha_utils/`, NOT `src/twat_image/`. Fix naming first (spec [70](issues/70.md)). |

### Cross-Plugin Changes
Some specs affect multiple plugins simultaneously:
- Spec [01](issues/01.md) (version management) → all 17 plugins
- Spec [02](issues/02.md) (cleanup.py) → 14 plugins
- Spec [03](issues/03.md) (pyproject.toml) → all 17 plugins
- Spec [11](issues/11.md) (__init__.py) → all 17 plugins
- Spec [86](issues/86.md) (dependency audit) → all 17 plugins

For these, implement the pattern in one plugin first (preferably `twat_os` — it has the best conventions), verify it works, then apply to all others.
