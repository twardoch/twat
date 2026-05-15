#!/usr/bin/env bash

AUTHOR_NAME="Adam Twardoch"
AUTHOR_EMAIL="adam+github@twardoch.com"
GITHUB_USERNAME="twardoch"

# Exit on error
set -e

# Check if package name is provided
if [ -z "$1" ]; then
    echo "Error: Package name must be provided as first argument"
    echo "Usage: $0 <package-name>"
    exit 1
fi

# Set package name and folder name
PKG="$1"
FOLDER_NAME="${PKG//-/_}"

# Initialize plugin package
if [ -n "$2" ] && [ "$2" = "-p" ] && [ -n "$3" ]; then
    PLUGINHOST="$3"
    echo "Creating plugin for host package: $PLUGINHOST"
    twat-hatch init \
        -o "$PKG.toml" \
        -n "$PKG" \
        --author_name "$AUTHOR_NAME" \
        --author_email "$AUTHOR_EMAIL" \
        --github_username "$GITHUB_USERNAME" \
        --use_vcs \
        -t plugin \
        -p "$PLUGINHOST"
else
    twat-hatch init \
        -o "$PKG.toml" \
        -n "$PKG" \
        --author_name "$AUTHOR_NAME" \
        --author_email "$AUTHOR_EMAIL" \
        --github_username "$GITHUB_USERNAME" \
        --use_vcs
fi

echo "Creating package $PKG"

# Create package from config
twat-hatch create -c "$PKG.toml"

# Install package
uv pip install --system --upgrade "./$FOLDER_NAME"

# Verify installation
python -c "from $FOLDER_NAME import *"

echo "Package $PKG successfully initialized and installed"
