# twat: The Extensible Python Plugin System

**twat** (short for "Twardoch's Worskstation Automation Toolkit", but you can call it whatever you want!) is a dynamic, plugin-based Python package system designed to provide a unified and extensible interface for a wide array of utilities and tools.

## Table of Contents
- [What is `twat`?](#what-is-twat)
- [Who is `twat` for?](#who-is-twat-for)
- [Why is `twat` useful?](#why-is-twat-useful)
- [Installation](#installation)
- [Usage](#usage)
  - [As a Library (Programmatic Usage)](#1-as-a-library-programmatic-usage)
  - [From the Command Line (CLI)](#2-from-the-command-line-cli)
- [Technical Details](#technical-details)
  - [How the Code Works (Core System)](#how-the-code-works-core-system)
    - [Plugin Discovery Mechanism](#1-plugin-discovery-mechanism)
    - [Dynamic Plugin Loading (`twat.<plugin_name>`)](#2-dynamic-plugin-loading-twatplugin_name)
    - [Command-Line Interface (CLI) Dispatcher (`twat <plugin_name> ...`)](#3-command-line-interface-cli-dispatcher-twat-plugin_name-)
  - [Plugin Development](#plugin-development)
    - [Package Structure](#1-package-structure)
    - [`pyproject.toml` Configuration for a Plugin](#2-pyprojecttoml-configuration-for-a-plugin)
    - [Package Interface (`src/twat_yourplugin/__init__.py`)](#3-package-interface-srctwat_yourplugin__init__py)
    - [CLI Support (`src/twat_yourplugin/__main__.py`)](#4-cli-support-srctwat_yourplugin__main__py)
  - [Coding and Contribution Rules](#coding-and-contribution-rules)
    - [Coding Standards](#1-coding-standards)
    - [Testing](#2-testing)
    - [Dependencies](#3-dependencies)
    - [Licensing](#4-licensing)
    - [Development Workflow (using Hatch)](#5-development-workflow-using-hatch)
    - [Commit Messages](#6-commit-messages)
    - [AGENTS.md / CLAUDE.md](#7-agentsmd--claudemd)
    - [Branching and Pull Requests](#8-branching-and-pull-requests)
- [License](#license)


## What is `twat`?

At its core, `twat` is a lightweight framework that allows Python developers to build modular applications. It acts as a central hub that can discover, load, and manage "plugins" – independent packages that extend `twat`'s capabilities. Think of it like a versatile multi-tool where each tool (plugin) can be added or removed as needed, without altering the main handle.

## Who is `twat` for?

`twat` is for Python developers who:

*   Want to create applications with a **modular architecture**, making them easier to maintain and scale.
*   Need to **integrate various tools and functionalities** under a common interface.
*   Are looking to build systems where new features can be **added by installing separate packages**.
*   Appreciate the ability to access these tools both **programmatically within Python and via a command-line interface (CLI)**.

## Why is `twat` useful?

*   **Extensibility:** Easily add new functionalities by creating or installing new plugins. If you need a tool for interacting with file systems, there's a plugin for that (e.g., `twat-fs`). Need something for image manipulation? Create or find an image plugin!
*   **Simplified Development:** Plugins are developed as standard Python packages, making them familiar to work with.
*   **Code Reusability:** Common functionalities can be encapsulated within plugins and reused across different projects or by different parts of a larger application.
*   **Unified Interface:** `twat` provides a consistent way to call and manage plugins, whether you're writing a script or working on the command line.
*   **Dynamic Discovery:** Plugins are automatically discovered at runtime if they are installed in the same Python environment and correctly registered.

## Installation

Getting started with `twat` is as simple as installing it via pip:

```bash
pip install twat
```

This will install the core `twat` system. Plugins are separate packages and need to be installed individually (e.g., `pip install twat-fs`).

## Usage

You can interact with `twat` and its plugins in two main ways:

### 1. As a Library (Programmatic Usage)

Once `twat` and desired plugins are installed, you can import `twat` and access plugins as if they were modules directly under the `twat` namespace.

```python
import twat

# Load a plugin (e.g., a hypothetical 'fs' plugin for file system operations)
# This assumes a plugin named 'fs' is registered and installed.
try:
    fs_plugin = twat.fs
    # Now you can use functions from the fs_plugin
    # For example, if fs_plugin has a function list_directory():
    # fs_plugin.list_directory(".")
except AttributeError:
    print("The 'fs' plugin is not installed or could not be loaded.")

# List available plugins
# Plugins are discovered using Python's entry point mechanism.
from importlib.metadata import entry_points

try:
    # Note: The group name is "twat.plugins"
    available_plugin_eps = entry_points()

    # In Python 3.10+ entry_points returns a SelectableGroups object
    # We need to select the group first.
    # For older versions (though project requires 3.10+), .get would be used.
    specific_plugins = available_plugin_eps.select(group="twat.plugins")

    if specific_plugins:
        print("Available twat plugins:")
        for plugin_ep in specific_plugins:
            print(f"- {plugin_ep.name} (from package: {plugin_ep.value.split(':')[0]})")
    else:
        print("No twat plugins found.")
except Exception as e:
    print(f"Error retrieving plugins: {e}")

```

If a plugin (e.g., `your_plugin_name`) is installed and registered correctly, accessing `twat.your_plugin_name` will dynamically load it. If the plugin is not found or fails to load, an `AttributeError` will be raised.

### 2. From the Command Line (CLI)

`twat` provides a command-line dispatcher to run plugins that expose a CLI interface (typically a `main()` function within the plugin).

```bash
# Run a plugin through the twat command
# This will execute the main() function of the 'fs' plugin
twat fs --help  # Example: get help from the 'fs' plugin
twat fs list --path /some/directory # Example: run a 'list' command in 'fs'

# Some plugins might also provide their own direct CLI command
# (if configured in their pyproject.toml). For example:
# twat-fs --help
```

The `twat` CLI tool takes the plugin's registered name as the first argument, followed by any arguments specific to that plugin.

## Technical Details

This section provides a more in-depth look at how `twat` operates, how to develop plugins, and the coding and contribution guidelines for the `twat` ecosystem.

### How the Code Works (Core System)

The `twat` core system, primarily defined in `src/twat/__init__.py`, is responsible for discovering, loading, and dispatching plugins.

**1. Plugin Discovery Mechanism:**

*   Plugins are discovered using Python's standard `importlib.metadata` module, specifically through **entry points**.
*   A package that wishes to register itself as a `twat` plugin must define an entry point in its `pyproject.toml` file under the `[project.entry-points."twat.plugins"]` group.
    ```toml
    # In the plugin's pyproject.toml
    [project.entry-points."twat.plugins"]
    myplugin = "twat_myplugin" # 'myplugin' is the name used to call it
                               # 'twat_myplugin' is the importable package/module
    ```
    Here, `myplugin` is the short name by which the plugin will be known to `twat` (e.g., `twat.myplugin`), and `twat_myplugin` is the actual Python package or module that gets imported.

**2. Dynamic Plugin Loading (`twat.<plugin_name>`):**

*   The `twat` module utilizes Python's `__getattr__(name)` special method to intercept attribute access. When you write `twat.myplugin`, `__getattr__` is called with `name` being `"myplugin"`.
*   `__getattr__` then calls an internal helper function, `_load_plugin(name)`.
*   `_load_plugin(name)` performs the following steps:
    1.  It queries `importlib.metadata.entry_points()` to get all entry points. For Python 3.10+, this returns a `SelectableGroups` object, so it specifically selects those for the `"twat.plugins"` group using `.select(group="twat.plugins")`.
    2.  It iterates through the found entry points, looking for one whose `name` matches the requested plugin name.
    3.  If a match is found, it calls `entry_point.load()` on that entry point. This function, provided by `importlib.metadata`, resolves and imports the package/module specified in the entry point's value (e.g., `twat_myplugin`).
    4.  It checks if the loaded object is a Python module (`types.ModuleType`).
    5.  If it's a valid module, it's "registered" into Python's global module cache by assigning it to `sys.modules[f"twat.{name}"]`. This makes the plugin module behave as if it were `twat.myplugin`.
    6.  The loaded module is then returned by `__getattr__`.
*   If the plugin is not found, fails to load, or the loaded entry point does not point to a module, an `AttributeError` is raised.

**3. Command-Line Interface (CLI) Dispatcher (`twat <plugin_name> ...`):**

*   The `twat` command-line tool is made available through a script definition in `twat`'s own `pyproject.toml`:
    ```toml
    # In twat's core pyproject.toml
    [project.scripts]
    twat = "twat:main"
    ```
    This maps the `twat` command to the `main()` function in `src/twat/__init__.py`.
*   The `main()` function in `src/twat/__init__.py`:
    1.  Parses `sys.argv`. It expects the first argument after `twat` to be the `plugin_name`.
    2.  If no `plugin_name` is provided, it prints usage instructions and exits.
    3.  It then **modifies `sys.argv`** for the target plugin:
        *   `sys.argv[0]` is set to `f"twat.{plugin_name}"` (e.g., `"twat.myplugin"`).
        *   The subsequent elements of `sys.argv` are the arguments originally passed to the plugin (e.g., `sys.argv[1:]` becomes `original_args`).
    4.  Finally, it calls `run_plugin(plugin_name)`.
*   The `run_plugin(plugin_name)` function:
    1.  Similar to `_load_plugin`, it iterates through entry points for the `"twat.plugins"` group to find the entry point for `plugin_name`.
    2.  It loads the plugin module using `entry_point.load()`.
    3.  It checks if the loaded plugin module has a callable attribute named `main` (i.e., a `main()` function).
    4.  If such a `main()` function exists, it calls `plugin.main()`. This function is expected to handle the plugin's CLI logic using the (modified) `sys.argv`.
    5.  `run_plugin` (and consequently the `twat` command) exits with status `0` if the plugin's `main()` executes successfully, or `1` if the plugin is not found, fails to load, doesn't have a `main()` function, or if `plugin.main()` itself raises an exception.

### Plugin Development

Developing a plugin for `twat` involves creating a standard Python package with specific configurations to allow `twat` to discover and integrate it.

**1. Package Structure:**

A typical plugin, say `twat-myfsplugin`, would have a structure like:

```
twat-myfsplugin/
├── src/
│   └── twat_myfsplugin/    # The importable package (use underscores)
│       ├── __init__.py     # Main package interface, exports public API
│       ├── __main__.py     # Optional: CLI entry point for the plugin itself
│       └── core.py         # Core functionality of the plugin
├── tests/
├── pyproject.toml          # Package configuration and plugin registration
├── README.md
└── LICENSE
```

**2. `pyproject.toml` Configuration for a Plugin:**

This is crucial for your plugin to be recognized and work correctly.

```toml
# In your plugin's pyproject.toml
[build-system]
requires = ["hatchling"] # Or your preferred build system like setuptools
build-backend = "hatchling.build"

[project]
name = "twat-myfsplugin"  # Use hyphens for the installable package name
version = "0.1.0"
dependencies = [
    "twat",               # Crucial: depend on the core twat package
    # ... other dependencies for your plugin
]
# ... other metadata (authors, description, readme, license, etc.)

# Optional: If your plugin provides its own direct CLI command (e.g., `twat-myfsplugin --help`)
[project.scripts]
twat-myfsplugin = "twat_myfsplugin.__main__:main_cli" # Point to your CLI function

# Essential: Register as a twat plugin
[project.entry-points."twat.plugins"]
myfsplugin = "twat_myfsplugin" # LHS: name used by twat (twat.myfsplugin or `twat myfsplugin`)
                               # RHS: importable module (src/twat_myfsplugin)
```

*   **Naming Conventions:**
    *   **Installable Package Name** (`project.name`): e.g., `twat-myfsplugin`. Uses hyphens. This is what users `pip install`.
    *   **Plugin Entry Point Name** (in `[project.entry-points."twat.plugins"]`): e.g., `myfsplugin`. This is the name used to access the plugin via `twat` (e.g., `twat.myfsplugin` or `twat myfsplugin ...`). Conventionally lowercase, without the `twat-` prefix.
    *   **Importable Module Name** (RHS of entry point, directory in `src/`): e.g., `twat_myfsplugin`. This is the actual Python package name. Uses underscores.

**3. Package Interface (`src/twat_yourplugin/__init__.py`):**

This file should define the public API of your plugin. It's also where the `main` function (for `twat yourplugin ...` dispatch) should be exposed if applicable.

```python
# src/twat_myfsplugin/__init__.py
"""A twat plugin for file system operations."""

from importlib import metadata

try:
    __version__ = metadata.version(__name__)
except metadata.PackageNotFoundError:
    # Fallback for when the package is not installed (e.g., during development)
    __version__ = "0.0.0-dev"

# Export your public API from core modules
from .core import list_files, read_file

# If your plugin supports `twat yourplugin ...` execution,
# you need to expose a `main` function here.
# This 'main' function will be called by the twat CLI dispatcher.
try:
    from .__main__ import main_cli as main # Assuming main_cli is your CLI handler
except ImportError:
    # Handle cases where __main__ might not exist or main_cli is not defined
    # Or, define a simple main directly here if preferred for simpler plugins
    def main() -> None:
        """Default main function for twat dispatcher if __main__.main_cli is not found."""
        print(f"Plugin {__package__ or 'unknown_plugin'} (via twat dispatcher) needs its main() function configured or implemented.")
        # import sys; sys.exit(1) # Optionally exit with error

__all__ = [
    "list_files",
    "read_file",
    "__version__",
    "main" # Ensure 'main' is in __all__ if you want it to be "public"
]
```

**4. CLI Support (`src/twat_yourplugin/__main__.py`):**

If your plugin provides a command-line interface, either for direct execution (e.g., `twat-myfsplugin`) or via the `twat` dispatcher, you'll typically implement this logic in `__main__.py`.

```python
# src/twat_myfsplugin/__main__.py
"""CLI interface for twat-myfsplugin."""

import sys
from typing import NoReturn
# Consider using a CLI library like 'fire', 'click', or 'argparse'
# For example, using 'fire' as shown in the original README:
# import fire

from .core import list_files # Example function to expose via CLI

def main_cli() -> NoReturn:
    """
    Main CLI entry point.
    This function is called when running `twat-myfsplugin ...` (if configured in project.scripts)
    or can be aliased as `main` in `__init__.py` for `twat myfsplugin ...`.
    """
    print(f"Executing plugin command. sys.argv: {sys.argv}")
    # Example using fire:
    # import fire
    # fire.Fire({
    #     "list": list_files,
    #     # add other commands your plugin offers
    # })
    # Replace with your actual CLI parsing and command execution logic
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        print("Listing files (example command)...")
        # list_files(".") # Example call
    else:
        print(f"Usage: {sys.argv[0]} [list|...]")

    sys.exit(0) # Ensure it exits; fire.Fire handles this automatically

if __name__ == "__main__":
    # This allows running the module directly: python -m twat_myfsplugin ...
    main_cli()
```

### Coding and Contribution Rules

To ensure consistency and quality across `twat` core and its plugins, please adhere to the following:

**1. Coding Standards:**

*   **Python Version:** Compatible with Python 3.10 and newer (as specified in `pyproject.toml`'s `requires-python = ">=3.10"`).
*   **Type Hints:** Comprehensive type hints are required (PEP 484, PEP 585). Use `typing_extensions` for features not yet in older supported Python versions if necessary.
*   **Code Formatting:** Code is formatted using **Ruff**. Configuration is in `pyproject.toml` (`[tool.ruff]`).
*   **Linting & Static Analysis:**
    *   **Ruff** is used for linting (see `[tool.ruff.lint]` in `pyproject.toml`).
    *   **MyPy** is used for static type checking (see `[tool.mypy]` in `pyproject.toml`).
    *   Run these tools via Hatch (see Development Workflow).
*   **Docstrings:** All public modules, classes, functions, and methods should have clear, concise docstrings following standard Python conventions (e.g., Google style or reStructuredText).

**2. Testing:**

*   Comprehensive automated tests are mandatory.
*   **Pytest** is the testing framework (see `[tool.pytest.ini_options]`).
*   Tests should cover both the Python API and any CLI interfaces.
*   Aim for high test coverage. Configuration for coverage is in `pyproject.toml` (`[tool.coverage.run]`).
*   Tests are run via Hatch.

**3. Dependencies:**

*   Dependencies are managed using **Hatch** and defined in `pyproject.toml`.
*   Minimize dependencies where possible. For optional features or integrations (e.g., different cloud providers for a storage plugin), use `project.optional-dependencies`.

**4. Licensing:**

*   `twat` and its first-party plugins are licensed under the **MIT License**.
*   Ensure any contributions are compatible with this license. The `LICENSE` file is in the repository root.

**5. Development Workflow (using Hatch):**

The `twat` project (and recommended for plugins) uses **Hatch** for managing development environments, dependencies, running tests, linting, and building packages. Refer to `pyproject.toml` for specific Hatch environment configurations and scripts.

*   **Set up environment:**
    ```bash
    # Install Hatch (if not already installed, e.g., pipx install hatch)
    # pip install hatch # if not using pipx
    hatch shell # Activates the virtual environment with dev dependencies
    ```
*   **Install in development mode (after activating shell):**
    ```bash
    # For twat core or a plugin, from its root directory:
    pip install -e .[dev,test]
    ```
*   **Run tests:**
    ```bash
    hatch run test             # Standard tests
    hatch run test-cov         # Tests with coverage report
    # Specific test environments might be defined, e.g., hatch run default:test
    ```
*   **Run linting and formatting:**
    (Consult `tool.hatch.envs.lint.scripts` and `tool.hatch.envs.default.scripts` in `pyproject.toml` for exact commands)
    ```bash
    hatch run lint:style       # Runs ruff check and ruff format (check mode)
    hatch run lint:typing      # Runs mypy
    hatch run lint:all         # Runs both style and typing checks (as defined in lint env)

    # For auto-formatting and fixing:
    hatch run lint:fmt         # Runs ruff format and ruff check --fix (as defined in lint env)

    # Alternatively, using default environment scripts if defined:
    # hatch run lint           # Might run ruff check and format (as per default env)
    # hatch run type-check     # Might run mypy (as per default env)
    ```
    It's best to refer to the `[tool.hatch.envs.*.scripts]` sections in `pyproject.toml` for the most up-to-date commands. The `lint` environment seems most comprehensive for these tasks.

**6. Commit Messages:**

*   Follow conventional commit message standards (e.g., `feat: add new feature`, `fix: resolve bug`, `docs: update documentation`). This promotes a clear and understandable project history.

**7. AGENTS.md / CLAUDE.md:**

*   When working on the codebase, especially if using AI-assisted development tools, consult any `AGENTS.md` files in the relevant directory scope for specific instructions or conventions. `CLAUDE.md` was not found in the root of this repository at the time of this writing, but always check for such files as they may provide crucial guidance.

**8. Branching and Pull Requests:**

*   Follow standard GitHub Flow: create feature branches from the main development branch (e.g., `main` or `develop`).
*   Ensure all tests and linters pass locally before submitting a pull request. CI checks (defined in `.github/workflows/`) should also pass.
*   Provide a clear description of changes in the pull request, linking to any relevant issues.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
