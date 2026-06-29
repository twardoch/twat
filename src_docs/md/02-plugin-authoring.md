<!-- this_file: src_docs/md/02-plugin-authoring.md -->
# Writing a plugin

No SDK, no base class, no registration call. A `twat` plugin is a normal Python
package with **one extra line** in `pyproject.toml`.

## 1. Package structure

```text
twat-myplugin/
├── src/
│   └── twat_myplugin/
│       ├── __init__.py   # Public API — everything here becomes twat.myplugin.*
│       └── __main__.py   # CLI handler — must expose main()
├── pyproject.toml
└── README.md
```

## 2. Register the entry point

This is the only `twat`-specific line in your entire package:

```toml
[project.entry-points."twat.plugins"]
myplugin = "twat_myplugin"
```

To also get a standalone `twat-myplugin` console command, add:

```toml
[project.scripts]
twat-myplugin = "twat_myplugin:main"
```

## 3. Expose your API (`__init__.py`)

```python
from importlib import metadata

try:
    __version__ = metadata.version(__name__)
except metadata.PackageNotFoundError:
    __version__ = "0.0.0-dev"

def do_something() -> str:
    return "result"

# The CLI dispatcher calls plugin.main() — expose it here.
try:
    from .__main__ import main
except ImportError:
    def main() -> None:
        pass

__all__ = ["do_something", "main", "__version__"]
```

## 4. Handle CLI calls (`__main__.py`)

When invoked as `twat myplugin …`, the host has already rewritten `sys.argv[0]`
to `twat.myplugin`, so your plugin behaves exactly as if called directly:

```python
import sys

def main() -> None:
    print(f"Hello from myplugin! Args: {sys.argv[1:]}")
    sys.exit(0)

if __name__ == "__main__":
    main()
```

## Naming conventions

| Thing | Convention | Example |
|---|---|---|
| pip package | `twat-<name>` with hyphens | `twat-myplugin` |
| entry-point name | lowercase, no prefix | `myplugin` |
| Python module | `twat_<name>` with underscores | `twat_myplugin` |

The entry-point name becomes both the attribute on `twat` and the subcommand in
the CLI. Keep the three aligned and there is nothing else to wire up.

## Verify your plugin

```bash
pip install -e .
twat --list        # myplugin should appear
twat --doctor      # [OK] myplugin -> twat_myplugin
twat myplugin --help
```

!!! tip "Keep imports lazy"
    The host imports your package only when it is first used, so heavy
    dependencies (Pillow, ffmpeg bindings, network clients) should be imported
    *inside* the functions that need them — not at module top level. That keeps
    `twat --help` and `--list` instant across the whole ecosystem.
