#!/usr/bin/env bash
# Scaffold for US8-AC2 (amend).
# Given: an existing constitution at version 1.1.0.
# Builds ./acme-notes in the current directory, with its bare remotes beside it in ./remotes.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$PWD/acme-notes"

bash "$fixtures/make-project.sh" "$project" acme
git -C "$project" config github.user acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" specified

cat > "$project/specs/constitution.md" <<'EOF'
# acme-notes Constitution

## Core Principles

### I. Tests first

Every behavior change starts with a failing test.

### II. Small changes

A pull request changes one thing and stays reviewable.

### III. No secrets in the repository

Credentials live in the environment, never in a commit.

## Governance

Amendments go through `/s2tdd-constitution`. Versions follow semantic versioning.

**Version**: 1.1.0 | **Ratified**: 2026-06-01 | **Last Amended**: 2026-08-15

## Change notes

- 2026-08-15 · 1.0.0 → 1.1.0 (MINOR): added the small-changes principle
- 2026-06-01 · 1.0.0: ratified
EOF

git -C "$project/specs" add -A
git -C "$project/specs" commit -q -m "feat(004): add the constitution"
git -C "$project/specs" push -q origin main
