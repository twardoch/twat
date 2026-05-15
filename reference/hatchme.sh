#!/bin/bash

# Check if directory argument is provided
if [ -z "$1" ]; then
    echo "Error: Please provide a directory path"
    exit 1
fi

# Change to the specified directory
if ! cd "$1"; then
    echo "Error: Could not change to directory: $1"
    exit 1
fi

# Create virtual environment
if ! uv venv; then
    echo "Error: Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Install package in editable mode with extras
if ! uv pip install -e ".[dev,test,all]"; then
    echo "Error: Failed to install package"
    exit 1
fi

# Run formatting
if ! hatch fmt; then
    echo "Error: Formatting failed"
    exit 1
fi

# Run tests
if ! hatch test; then
    echo "Error: Tests failed"
    exit 1
fi

# Run cleanup script
if ! python cleanup.py update; then
    echo "Error: Cleanup failed"
    exit 1
fi

# Build package
if ! hatch build -c; then
    echo "Error: Build failed"
    exit 1
fi

echo "All operations completed successfully"
