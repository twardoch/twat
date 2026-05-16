# Spec: Comprehensive Fire CLIs for the `twat` plugin ecosystem

**Status:** draft  •  **Date:** 2026-05-16  •  **Owner:** Adam Twardoch
this_file: SPEC.md

## 1. Goal

Every `twat-*` plugin must ship a powerful, consistent **Fire**-based CLI exposing
its end-user functionality. The host `twat` command continues to dispatch by
plugin name; each plugin additionally exposes its leaf subcommands and groups
as **explicit dashed entry-point scripts**, so that typing `twat-<TAB>` in a
shell with `twat[all]` installed surfaces dozens of completions.

Out-of-scope: rewriting plugin domain logic. We are wrapping existing functionality
in a clean, uniform Fire surface — not redesigning what each plugin does.

## 2. Drivers / observed failures

1. `twat-fs --help` crashes: `from __future__ import annotations` is not at the
   top of `src/twat_fs/__init__.py` (a docstring precedes it).
2. `twat --help` (no arg) prints nothing — the host writes usage to **stderr**
   then `sys.exit(1)`. With most shells this is invisible to the user.
3. Several plugins still use `argparse` (twat_audio, twat_video, twat_speech,
   twat_genai, twat_search, twat_hatch, twat_os, twat_ez, twat_coding).
4. CLI surfaces are inconsistent: some `cli.py`, some `__main__.py`, some
   `<pkg>/<pkg>.py`. Naming and help format differ per plugin.
5. No discoverability: `twat-image<TAB>` shows nothing useful because only one
   dashed script per plugin is registered.

## 3. Decisions (already settled with the user)

| # | Decision | Rationale |
|---|----------|-----------|
| D1 | Work happens in each submodule **and** the meta-repo | Real fix, not a wrapper hack. |
| D2 | Dashed commands via **explicit per-command entry points** in `[project.scripts]` | Shell completion needs real scripts on PATH. |
| D3 | **Full implementation across all 17 plugins** in this initiative | One coherent push, not 17 follow-ups. |
| D4 | Standardize **every** plugin (even those already using Fire) | Uniformity is the deliverable. |
| D5 | Push submodule commits **and** run each plugin's `publish.sh` | The deliverable is on PyPI, not just in git. |
| D6 | Canonical CLI module: **`twat_X/__main__.py` with a Fire dict** | Functional, simple, no class boilerplate. |
| D7 | Dashed scripts for **leaves *and* groups** (`twat-image-gray2alpha` *and* `twat-image-tools`) | Maximal discoverability via TAB. |
| D8 | For library-only plugins (`twat_ez`, `twat_mp`, `twat_task`, `twat_labs`) we **synthesize useful commands** from public API | Uniform namespace; no dead plugins. |

## 4. Architecture

### 4.1 Per-plugin layout

```
plugins/repos/twat_X/
├── pyproject.toml
└── src/twat_X/
    ├── __init__.py         # version + thin re-exports; no side effects
    ├── __main__.py         # Fire dispatcher; defines COMMANDS dict + main()
    ├── _cli/               # optional package of subcommand modules
    │   ├── __init__.py
    │   ├── foo.py
    │   └── bar.py
    ├── ... (domain modules unchanged)
```

### 4.2 Canonical `__main__.py`

```python
# this_file: src/twat_X/__main__.py
"""Fire CLI entry point for twat-X."""
from __future__ import annotations

import fire

from twat_X import operations  # domain logic
from twat_X._cli import group_tools  # group dict


def _version() -> str:
    from twat_X.__version__ import __version__
    return __version__


# Leaves: callable; groups: dict (Fire renders nested help automatically)
COMMANDS: dict[str, object] = {
    "version": _version,
    "gray2alpha": operations.gray2alpha,
    "resize": operations.resize,
    "tools": group_tools.COMMANDS,
    # ...
}


def main() -> None:
    fire.Fire(COMMANDS, name="twat-X")


# Dashed-entry helpers (one per leaf and group). Each is a Fire on a sub-tree.
def cmd_gray2alpha() -> None:
    fire.Fire(operations.gray2alpha, name="twat-X-gray2alpha")


def cmd_resize() -> None:
    fire.Fire(operations.resize, name="twat-X-resize")


def cmd_tools() -> None:
    fire.Fire(group_tools.COMMANDS, name="twat-X-tools")


if __name__ == "__main__":
    main()
```

### 4.3 `pyproject.toml` `[project.scripts]` shape

```toml
[project.scripts]
# Top-level dispatcher (subcommand form)
twat-X            = "twat_X.__main__:main"

# Per-leaf dashed entries
twat-X-gray2alpha = "twat_X.__main__:cmd_gray2alpha"
twat-X-resize     = "twat_X.__main__:cmd_resize"

# Per-group dashed entries
twat-X-tools      = "twat_X.__main__:cmd_tools"
```

This is the only way shell completion (bash/zsh/fish using `compgen -c`-style
prefix matching) lists `twat-X-*` candidates.

### 4.4 Entry point for plugin discovery (unchanged contract)

```toml
[project.entry-points."twat.plugins"]
X = "twat_X"
```

`twat X args...` continues to import `twat_X` and call its `main()`.

### 4.5 Host (`twat`) changes

1. Print `--help` text to **stdout**, exit **0**, when invoked with no args
   (or `--help`).
2. Pretty `--list` showing both plugin name and short description (read from
   the plugin package docstring).
3. New `twat --completions {bash,zsh,fish}` emits a completion script that
   lists installed dashed entry points (queried from `importlib.metadata
   .entry_points(group="console_scripts")` filtered by `twat-` prefix).

### 4.6 Shared CLI utilities (in meta-repo)

`src/twat/common/cli.py`:

* `version_callable(pkg) -> Callable[[], str]` – uniform `version` leaf.
* `print_table(rows, headers)` – Rich table for `list`-style commands.
* `error(msg, code=1)` – consistent stderr formatter.
* `WithLogging(verbose=False, quiet=False)` – mix-in turning loguru level.

Per-plugin code imports these to keep UX identical.

## 5. Command surface per plugin (initial, non-exhaustive)

| Plugin | Top-level Fire commands |
|--------|-------------------------|
| `twat-image` | `gray2alpha`, `resize`, `convert`, `to-alpha`, `info`, `genai` |
| `twat-video` | `info`, `extract-frames`, `transcode`, `thumbnail`, `concat` |
| `twat-audio` | `info`, `transcode`, `normalize`, `silence-trim` |
| `twat-speech` | `transcribe`, `tts`, `list-voices`, `list-engines` |
| `twat-llm` | `ask`, `chat`, `complete`, `embed`, `list-models` |
| `twat-genai` | `image`, `video`, `list-providers`, `list-models` |
| `twat-search` | `web`, `code`, `docs`, `list-engines` |
| `twat-text` | `tokenize`, `clean`, `markdown`, `detect-lang`, `summarize` |
| `twat-fs` | `upload`, `download`, `providers`, `cache-info` |
| `twat-os` | `paths`, `clipboard`, `open`, `info` |
| `twat-hatch` | `init`, `plugin-init`, `bump`, `release` |
| `twat-mp` | `pmap`, `pfilter`, `bench` |
| `twat-task` | `run`, `list`, `status` |
| `twat-ez` | `py-needs`, `info` |
| `twat-labs` | `experiments`, `info` |
| `twat-coding` | `pystubnik`, `imports` |
| `twat-font` | `info`, `convert`, `subset` |

(The detailed leaf-by-leaf inventory lives in `PLAN.md`; commands are
synthesized only where existing modules already implement them.)

## 6. Behavioural contracts (every plugin)

1. `twat-X --help` → stdout, exit 0, complete subcommand listing.
2. `twat-X --version` and `twat-X version` → print package version, exit 0.
3. Errors → stderr, non-zero exit, single line + `--verbose` for traceback.
4. Logging → loguru; default WARNING, `--verbose` → DEBUG, `--quiet` → ERROR.
5. All file path args accept `~` and relative paths; resolved with `pathlib`.
6. Return values that are *data* (dicts/lists/Pydantic models) are pretty-printed
   via Rich; primitive returns print as-is. This is Fire-native behaviour.
7. Every leaf has a docstring whose first line is its `--help` summary.

## 7. Bug-fix items folded into this work

* **B1** `twat_fs/__init__.py` — move `from __future__ import annotations` to
  the first non-comment line.
* **B2** `src/twat/__init__.py::main` — write usage to stdout for `--help`/no-arg
  and exit 0 instead of 1.

## 8. Release / distribution

Each plugin is re-released via its existing `publish.sh` (which tags then
builds via `hatch-vcs`). After all plugins are published, the meta-repo
bumps its submodule pointers in one commit (`chore: bump submodules for fire-cli`).

## 9. Acceptance tests

For every plugin `twat-X`:

```bash
twat-X --help               # exit 0; prints listing
twat-X version              # exit 0; prints semver
twat X version              # exit 0; same semver
twat-X-<leaf> --help        # exit 0; prints leaf help
type twat-X-<leaf>          # resolves to an installed script
```

Plus: `twat --help` prints to stdout; `twat-fs --help` succeeds.

## 10. Non-goals

* Re-architecting plugin internals.
* Adding new domain features beyond exposing what exists.
* Pinning plugin versions in `twat[all]` to exact releases — keep `>=` lower
  bounds as today.
* Cross-plugin command sharing (each plugin owns its commands).
