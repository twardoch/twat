# twat Package

twat metapackage: host for plugins

Not used directly, but used to host plugins for other packages.

## Installation

```bash
pip install twat
```

## Usage

```python
import twat

# Load a plugin
plugin = twat.plugin_name

# List available plugins
from importlib.metadata import entry_points
plugins = entry_points(group="twat.plugins")
```

## Development

This project uses [Hatch](https://hatch.pypa.io/) for development workflow management.

### Setup Development Environment

```bash
# Install hatch if you haven't already
pip install hatch

# Create and activate development environment
hatch shell

# Run tests
hatch run test

# Run tests with coverage
hatch run test-cov

# Run linting
hatch run lint

# Format code
hatch run format
```

## License

MIT License 