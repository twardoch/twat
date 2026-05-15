#!/usr/bin/env bash

# List of repositories that need cleanup
repos=(
    "twat-genai"
    "twat-image"
    "twat-labs"
)

GITHUB_USER="twardoch"

for repo in "${repos[@]}"; do
    echo "Processing $repo..."

    # Change default branch to main on GitHub
    echo "Changing default branch to main for $repo..."
    gh api \
        --method PATCH \
        -H "Accept: application/vnd.github+json" \
        "/repos/$GITHUB_USER/$repo" \
        -f default_branch='main'

    # Delete the master branch
    echo "Deleting master branch from $repo..."
    gh api \
        --method DELETE \
        -H "Accept: application/vnd.github+json" \
        "/repos/$GITHUB_USER/$repo/git/refs/heads/master"

    echo "Completed processing $repo"
    echo "------------------------"
done

echo "All repositories processed successfully!"
