#!/usr/bin/env bash

# List of repositories
repos=(
    "twat"
    "twat_cache"
    "twat_genai"
    "twat_hatch"
    "twat_image"
    "twat_labs"
    "twat_mp"
    "twat_task"
)

for repo in "${repos[@]}"; do
    echo "Processing $repo..."

    # Enter repository directory
    cd "$repo" || continue

    # Get current branch
    current_branch=$(git rev-parse --abbrev-ref HEAD)

    if [ "$current_branch" = "master" ]; then
        echo "Repository $repo is on master branch, migrating to main..."

        # Convert underscore to hyphen for GitHub repo name
        github_repo_name="${repo/_/-}"

        # Create main branch from master
        git branch -m master main

        # Push the main branch to remote
        git push -u origin main

        # Push all tags
        git push origin --tags

        # Change default branch to main on GitHub
        gh api \
            --method PATCH \
            -H "Accept: application/vnd.github+json" \
            "/repos/$GITHUB_USER/$github_repo_name" \
            -f default_branch='main'

        # Delete the remote master branch after changing default branch
        git push origin --delete master

        echo "Successfully migrated $repo from master to main"
    else
        echo "Repository $repo is already on $current_branch branch, skipping..."
    fi

    # Return to parent directory
    cd ..

    echo "------------------------"
done

echo "All repositories processed successfully!"
