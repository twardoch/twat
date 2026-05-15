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

# GitHub username
GITHUB_USER="twardoch"

for repo in "${repos[@]}"; do
    echo "Processing $repo..."

    # Enter repository directory
    cd "$repo" || continue

    # 1. Add all changes and commit
    git add -A
    git commit -m "Initial commit for GitHub setup" || true

    # Determine current branch
    current_branch=$(git rev-parse --abbrev-ref HEAD)

    # 2. Create GitHub repository (except for twat_mp)
    if [ "$repo" != "twat_mp" ]; then
        # Convert underscore to hyphen for GitHub repo name
        github_repo_name="${repo/_/-}"

        # Create GitHub repository using GitHub CLI
        gh repo create "$GITHUB_USER/$github_repo_name" --public --source=. || true

        # 3. Set GitHub as upstream
        git remote remove origin 2>/dev/null || true
        git remote add origin "https://github.com/$GITHUB_USER/$github_repo_name.git"
    fi

    # 4. Tag and push
    # Only create tag if it doesn't exist
    if ! git rev-parse "v1.0.0" >/dev/null 2>&1; then
        git tag -a "v1.0.0" -m "Initial release v1.0.0"
    fi

    # Push using the current branch name
    git push -u origin "$current_branch" --tags --force

    # Return to parent directory
    cd ..

    echo "Completed processing $repo"
    echo "------------------------"
done

echo "All repositories processed successfully!"
