#!/usr/bin/env bash
# publish-all.sh — Run publish.sh in every twat git repo discovered by `gitfind`.
set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

fail=0
for p in $(gitfind); do
    echo "=== $p ==="
    if [[ -x "$p/publish.sh" ]]; then
        if ! "$p/publish.sh"; then
            echo "FAILED: $p" >&2
            fail=1
        fi
    else
        echo "  no publish.sh — skipping"
    fi
done
exit $fail
