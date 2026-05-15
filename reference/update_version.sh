#!/usr/bin/env bash

# Check if version argument is provided
if [ -z "$1" ]; then
    echo "Error: Version number must be provided as argument"
    echo "Usage: $0 <version>"
    echo "Example: $0 1.6.1"
    exit 1
fi

VERSION="$1"

# Loop through all twat* directories
for dir in twat*/; do
    if [ -d "$dir" ] && [ -d "$dir/.git" ]; then
        echo "Processing $dir..."
        cd "$dir"

        # Commit changes
        git commit -am "v$VERSION"

        # Create tag
        git tag "v$VERSION"

        # Push changes and tags
        git push
        git push --tags

        cd ..
        echo "Completed $dir"
        echo "-------------------"
    fi
done

echo "Version update complete for all repositories"
