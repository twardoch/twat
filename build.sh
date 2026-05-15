#!/usr/bin/env bash
# this_file: build.sh
# Build script for twat (Python meta-package)
# Lints, formats, tests, and builds the package.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "==> Linting and formatting..."
uvx ruff check --fix src tests || true
uvx ruff format src tests || true

echo "==> Running tests..."
uvx hatch test

echo "==> Building package..."
uvx hatch build

echo "Build complete. Distributions in dist/"
