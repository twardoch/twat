# twat

**Twardoch's Workstation Automation Toolkit.** A minimal plugin host for Python: install small, focused packages and access them all through one namespace and one CLI.

`twat` does nothing on its own. Install plugins, and they snap into place.

## How it works

Python has a built-in mechanism for packages to register themselves with a group name — called *entry points*. `twat` uses this to build a dynamic namespace: when you access `twat.fs`, it looks up the `twat.plugins` entry point named `fs`, loads the module, and hands it back. No configuration files, no registration steps beyond a normal `pip install`.

```python
import twat

# twat-fs registered itself as a "twat.plugins" entry point named "fs"
files = twat.fs.list_directory(".")

# twat-cache registered as "cache"
@twat.cache.memoize()
def expensive():
    ...
```

The CLI works the same way. `twat fs list /tmp` finds the `fs` plugin, rewrites `sys.argv` so the plugin thinks it was called directly, and calls `twat_fs.main()`.

## Discovering commands

Every plugin ships a Fire-based CLI with two access shapes:

```bash
twat-image gray2alpha input.png output.png   # subcommand form
twat-image-gray2alpha input.png output.png   # dashed form (one script per leaf)
```

Each leaf (and each command group) is registered as a real `console_scripts`
entry point, so typing `twat-<TAB>` in your shell offers dozens of completions
once you have `twat[all]` installed:

```
twat-audio              twat-image-gray2alpha       twat-search-web
twat-audio-normalize    twat-llm-ask                twat-speech-transcribe
twat-fs-upload          twat-os-clipboard           twat-video-probe
... (~90 more)
```

To wire completion of the `twat` dispatcher itself:

```bash
twat --completions zsh  > ~/.zfunc/_twat       # zsh
twat --completions bash > ~/.local/share/bash-completion/completions/twat
twat --completions fish > ~/.config/fish/completions/twat.fish
```

## Install

```bash
pip install twat
```

`twat` is an empty host. Install plugins separately:

```bash
pip install twat-fs twat-cache twat-os
```

## CLI

```bash
twat --help          # show host usage
twat --list          # list installed plugin entry point names
twat <plugin_name> [args...]

# Examples:
twat --list
twat fs list /tmp
twat cache clear
```

`twat --list` reads only plugin entry point metadata, so it does not import
plugin modules just to show what is installed. Dispatch still works by loading
the selected plugin, rewriting `sys.argv` so the plugin sees `twat.<plugin>` as
its executable name, and calling the plugin module's callable `main()`.

## Writing a plugin

No SDK required. A plugin is a normal Python package that declares one entry point.

### 1. Package structure

```
twat-myplugin/
├── src/
│   └── twat_myplugin/
│       ├── __init__.py    # Public API — everything here becomes twat.myplugin.*
│       └── __main__.py    # CLI handler — must expose a main() function
├── pyproject.toml
└── README.md
```

### 2. Register the entry point (`pyproject.toml`)

```toml
[project.entry-points."twat.plugins"]
myplugin = "twat_myplugin"
```

This is the only `twat`-specific line in your entire package.

### 3. Expose your API (`__init__.py`)

```python
from importlib import metadata

try:
    __version__ = metadata.version(__name__)
except metadata.PackageNotFoundError:
    __version__ = "0.0.0-dev"

def do_something():
    return "result"

# The CLI dispatcher calls plugin.main() — expose it here
try:
    from .__main__ import main
except ImportError:
    def main() -> None:
        pass

__all__ = ["do_something", "main", "__version__"]
```

### 4. Handle CLI calls (`__main__.py`)

```python
import sys

def main() -> None:
    # sys.argv[0] is already "twat.myplugin" when called via `twat myplugin`
    print(f"Hello from myplugin! Args: {sys.argv[1:]}")
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### Naming conventions

| Thing | Convention | Example |
|-------|-----------|---------|
| pip package | `twat-<name>` with hyphens | `twat-myplugin` |
| entry point name | lowercase, no prefix | `myplugin` |
| Python module | `twat_<name>` with underscores | `twat_myplugin` |

The entry point name becomes the attribute on `twat` and the subcommand in the CLI.

## How plugin loading works

`twat.__getattr__` is called whenever you access an attribute that doesn't exist on the module. It scans the `twat.plugins` entry point group for a matching name, loads the module, registers it in `sys.modules` as `twat.<name>` (so subsequent accesses skip the lookup), and returns it.

If no plugin matches, a `PluginError` is raised with a clear message.

The CLI entry point (`twat.main`) intercepts `sys.argv`, pulls out the plugin name, rewrites `sys.argv[0]` to `twat.<plugin>` and `sys.argv[1:]` to the remaining arguments, then calls the plugin's `main()`. The plugin never knows it was dispatched through `twat`.

## Development

```bash
git clone https://github.com/twardoch/twat
cd twat
uv venv && uv sync
pytest -xvs
```

## License

MIT
