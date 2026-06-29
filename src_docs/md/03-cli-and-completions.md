<!-- this_file: src_docs/md/03-cli-and-completions.md -->
# CLI & shell completion

The host CLI is a thin dispatcher. Reserved `--flags` are handled by `twat`
itself; anything else is treated as a plugin name and forwarded.

## Commands

```bash
twat --help                  # host usage (also: bare `twat`, exit 0)
twat --list                  # installed plugins (entry-point names)
twat --list --available      # installed twat-* distributions + their plugin
twat --available             # same as `--list --available`
twat --doctor                # import each plugin, report health, exit non-zero on failure
twat --completions SHELL     # emit a completion script (bash|zsh|fish)
twat <plugin> [args...]      # dispatch to a plugin's main()
```

### `--list` vs `--available`

| | `--list` | `--available` |
|---|---|---|
| Source | `twat.plugins` entry points | installed distributions |
| Shows | registered plugin names | `name<TAB>version<TAB>plugin` |
| Surfaces broken/half-installed `twat-*`? | no | yes (plugin column shows `-`) |
| Imports plugins? | no | no |

```console
$ twat --available
twat        2.7.18  -
twat-cache  2.6.7   cache
twat-fs     2.7.17  fs
```

### `--doctor`

`--doctor` imports every registered plugin and prints one line each. It exits
`0` only when all plugins load — handy in CI after installing `twat[all]`.

```console
$ twat --doctor
[OK]   cache -> twat_cache
[OK]   fs -> twat_fs
[FAIL] search -> twat_search: No module named 'some_optional_dep'
$ echo $?
1
```

## Discovering commands

Every plugin ships a Fire-based CLI with two access shapes:

```bash
twat-image gray2alpha input.png output.png   # subcommand form
twat-image-gray2alpha input.png output.png   # dashed form (one script per leaf)
```

Each leaf and group is a real `console_scripts` entry point, so `twat-<TAB>`
offers dozens of completions once `twat[all]` is installed.

## Installing shell completion

`twat --completions` generates a completion script for the `twat` dispatcher
itself, listing all installed `twat-*` console scripts.

=== "zsh"

    ```bash
    twat --completions zsh > ~/.zfunc/_twat
    # ensure ~/.zfunc is on your fpath, then:
    autoload -Uz compinit && compinit
    ```

=== "bash"

    ```bash
    twat --completions bash > ~/.local/share/bash-completion/completions/twat
    # restart your shell, or: source that file
    ```

=== "fish"

    ```bash
    twat --completions fish > ~/.config/fish/completions/twat.fish
    ```

!!! note
    The completion script is a static snapshot of the commands installed when
    you generated it. Re-run `twat --completions` after installing or removing
    plugins to refresh the list.
