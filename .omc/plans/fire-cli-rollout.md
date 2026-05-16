# Plan: Fire CLI rollout across the `twat` ecosystem

**Status:** draft  •  **Date:** 2026-05-16
this_file: .omc/plans/fire-cli-rollout.md

Reads with [/SPEC.md](../../SPEC.md). Numbering is `P{phase}.{step}`.

## Phase 0 — Foundations (meta-repo only)

* **P0.1** Fix host `twat --help` (B2): in `src/twat/__init__.py::main`,
  send usage to `stdout` and exit `0` for `--help`/`-h`/no-args.
* **P0.2** Add `src/twat/common/cli.py` with: `make_version_callable`,
  `error`, `print_data`, `with_logging`, `bash_completions`,
  `zsh_completions`, `fish_completions`.
* **P0.3** Add `twat --completions {bash,zsh,fish}` subcommand using
  `importlib.metadata.entry_points(group="console_scripts")`, filtered by
  `twat-` prefix.
* **P0.4** Add meta-repo dev tests: `tests/test_host_cli.py` — --help on
  stdout, --list, --completions, missing-plugin error message.
* **P0.5** `uvx hatch test`; commit
  `feat(host): fix --help, add common cli helpers, completions`.

## Phase 1 — Hot-fix `twat-fs` SyntaxError (B1)

* **P1.1** `plugins/repos/twat_fs/src/twat_fs/__init__.py`: move
  `from __future__ import annotations` directly under the `# this_file:`
  comment, before the docstring; re-format imports.
* **P1.2** `cd plugins/repos/twat_fs && uvx hatch test`.
* **P1.3** Run plugin's `publish.sh` (commits, tags, pushes, releases).
* **P1.4** Meta-repo: `git add plugins/repos/twat_fs && git commit
  -m "chore: bump twat_fs submodule (fire-cli hotfix)"`.

## Phase 2 — Per-plugin Fire CLI rollout (×17)

Plugin order (independent batches eligible for sub-agents in brackets):

```
twat_fs                                                 # done in P1
twat_image  twat_text  twat_llm  twat_genai             # heavy-ish
twat_video  twat_audio  twat_speech                     # av
twat_search  twat_os  twat_hatch  twat_font             # mixed
twat_mp  twat_task  twat_ez  twat_labs  twat_coding     # trivial / synthesized
```

For each plugin `X`:

* **P2.X.1** Inventory user-facing functions; classify leaf vs. group per
  SPEC §5.
* **P2.X.2** Create/replace `src/twat_X/__main__.py` per SPEC §4.2.
* **P2.X.3** Strip `argparse` (no domain rewrites; argparse handlers become
  plain functions referenced from `COMMANDS`).
* **P2.X.4** Add `version` leaf returning `__version__`.
* **P2.X.5** `pyproject.toml` `[project.scripts]`:
  * `twat-X = "twat_X.__main__:main"`.
  * `twat-X-<leaf> = "twat_X.__main__:cmd_<leaf>"` per leaf and group.
  * Ensure `fire` is in `[project].dependencies`.
* **P2.X.6** Tests in `tests/test_cli.py`:
  * `python -m twat_X --help` exits 0.
  * `python -m twat_X version` prints semver.
  * Each leaf `--help` exits 0.
* **P2.X.7** `uvx hatch test`; ruff fix + format.
* **P2.X.8** Commit: `feat(cli): comprehensive Fire CLI + dashed entries`.
* **P2.X.9** Run plugin's `publish.sh`.
* **P2.X.10** Meta-repo: bump submodule pointer; commit
  `chore: bump <X> submodule (fire-cli)`.

### Library-only plugins (D8 synthesis)

* `twat_mp` → `pmap`, `pfilter`, `bench` (thin wrappers).
* `twat_task` → `run`, `list`, `status` if exposed; else `info`/`version`
  plus TODO in plugin's WORK.md (no fabrication).
* `twat_ez` → `py-needs`, `info`.
* `twat_labs` → `experiments`, `info`.

> If synthesis demands inventing behaviour beyond a wrapper: stop and surface
> as a question. Do not guess.

## Phase 3 — Meta-repo finalization

* **P3.1** Update `src/twat/__init__.py` docstring + `_usage()` to describe
  the dashed-script discovery model.
* **P3.2** Verify `twat[all]` extras list every plugin.
* **P3.3** README: "Discovering commands" section showing `twat-<TAB>`
  and `twat --completions zsh > ~/.zfunc/_twat`.
* **P3.4** `CHANGELOG.md`: comprehensive Fire CLIs + dashed scripts.
* **P3.5** Fresh-venv acceptance run: install `twat[all]`, exercise SPEC §9
  for every plugin.

## Phase 4 — Done

Bump meta-repo minor version; tag; push.

## Risks & mitigations

| Risk | Mitigation |
|------|------------|
| Dashed-script explosion clobbers PATH | Leaves + groups only (D7); never re-export upstream names. |
| Submodule push failures | `git status` per submodule before `publish.sh`; stop on first failure. |
| `publish.sh` version bumps break downstreams | Additive only — no breaking removals. |
| Fire surfacing private internals | `COMMANDS` is an explicit allow-list. |
| Optional-dep import-ordering bugs (the twat_fs B1 case) | P0 audit of every plugin's `__init__.py`. |

## Parallelism plan for Phase 2

* **Trivial** — batch via sub-agents, 2 plugins per agent.
* **Medium** — one agent per plugin.
* **Heavy** (`twat_fs`, `twat_llm`, `twat_genai`) — solo in foreground.

Publish step is **always serialized per plugin**.
