#!/usr/bin/env bash
# publish-all.sh — Run publish.sh in every twat git repo, then the twat root last.
# Sub-repo publishes move submodule HEADs, which dirties the parent. We commit
# those pointer bumps in the root before tagging/publishing it so hatch-vcs gets
# a clean tree (no local-version suffix).
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

fail=0
root_repo=""

# Run sub-repo publishes first
for p in $(gitfind); do
    if [[ "$p" == "$ROOT" ]]; then
        root_repo="$p"
        continue
    fi
    echo "=== $p ==="
    if [[ ! -x "$p/publish.sh" ]]; then
        echo "  no publish.sh — skipping"
        continue
    fi
    if ! "$p/publish.sh"; then
        echo "FAILED: $p" >&2
        fail=1
    fi
done

# Commit any submodule pointer bumps in the root, then publish root
if [[ -n "$root_repo" && -x "$root_repo/publish.sh" ]]; then
    echo "=== $root_repo ==="
    cd "$root_repo"
    if ! git diff --quiet || ! git diff --cached --quiet; then
        git add -A
        git commit -m "chore: bump submodule pointers from publish-all" || true
    fi
    if ! ./publish.sh; then
        echo "FAILED: $root_repo" >&2
        fail=1
    fi
fi

exit $fail
