#!/usr/bin/env bash
# Scaffold for EC-001: branch claude/004-fix-flake, two directories sharing the number 004.
# Runs in the case's working directory, which becomes the project (acme-notes stand-in);
# its bare remotes land in ../remotes. Neutral names only (acme, 004-csv-export, ...).
set -euo pipefail

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
fixtures="$here/../../fixtures"
project=$(pwd)

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" specified
git -C "$project" checkout -q main

# A second open feature, 004-tags, committed and pushed in the specs repository.
mkdir -p "$project/specs/004-tags"
cat > "$project/specs/004-tags/spec.md" <<'EOF'
# Feature Specification: Note tags

**Feature Branch**: `004-tags`
**Status**: Draft

## User Stories

### US1 - Tag notes (Priority: P1)

A user attaches tags to their notes.

- **US1-AC1**: **Given** a note, **When** the user adds the tag `todo`, **Then** the note lists it.
EOF
git -C "$project/specs" add 004-tags
git -C "$project/specs" commit -q -m "feat(004-tags): specified"
git -C "$project/specs" push -q origin main
git -C "$project" checkout -q -b claude/004-fix-flake
