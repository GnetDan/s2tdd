#!/usr/bin/env bash
# Scaffold for EC-003: a specs repository with no remote, holding a change not yet saved.
# Runs in the case's empty working directory, which becomes the project.
set -euo pipefail

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
fixtures="$here/../../fixtures"
project=$(pwd)

bash "$fixtures/make-project.sh" "$project" acme
git -C "$project" config github.user acme
bash "$fixtures/make-specs.sh" "$project" --no-remote
bash "$fixtures/make-feature.sh" "$project" specified
# A change to save: a clarification session, written and not yet committed.
cat >> "$project/specs/004-csv-export/spec.md" <<'EOF'

## Clarifications

### Session 2026-10-02

- No decisions left open.
EOF
