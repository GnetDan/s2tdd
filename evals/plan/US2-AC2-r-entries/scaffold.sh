#!/usr/bin/env bash
# Scaffold for US2-AC2: a planned feature whose research.md holds R1
# Builds the fixture in the current directory: it is the project (git repository on main, a
# bare local remote standing in for GitHub), with specs/ as its own repository and its own
# bare remote. Helpers: evals/fixtures/. Neutral names only.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$(pwd)"
feature=004-csv-export

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" planned

cat > "$project/specs/constitution.md" <<'EOF_CONSTITUTION'
# acme-notes Constitution

## Core Principles

### I. Plain files only
Notes live as plain files on disk. No database server, no network service.

### II. Standard library first
A feature uses the Python standard library unless a dependency is justified in its plan.

### III. Test-first
Tests are written and seen failing before the code that makes them pass.

**Version**: 1.0.0 | **Ratified**: 2026-10-02 | **Last Amended**: 2026-10-02
EOF_CONSTITUTION
git -C "$project/specs" add constitution.md
git -C "$project/specs" commit -q -m "docs: constitution 1.0.0"
git -C "$project/specs" push -q origin main

dir="$project/specs/$feature"

cat > "$dir/plan.md" <<'EOF_PLAN'
# Implementation Plan: CSV export

**Branch**: `004-csv-export` | **Spec**: [spec.md](spec.md)

## Technical Context

Language: Python 3. Tests: pytest. The exporter is a function in `src/export.py`.
Line endings of the exported file: NEEDS CLARIFICATION (LF, or CRLF as spreadsheet tools expect).
**Acceptance tests**: `tests/acceptance/`, one per scenario ID; all scripted.

## Constitution Check

No principle is violated.

## Complexity Tracking

None.
EOF_PLAN

cat > "$dir/research.md" <<'EOF_RESEARCH'
# Phase 0 Research: CSV export

## R1. The exporter uses the csv module of the standard library

**Decision**: Write the file with the csv module.
**Rationale**: It quotes fields that contain a comma and adds no dependency.
**Alternatives considered**: A third-party writer; rejected as an extra dependency.
*(plan 2026-10-02)*
EOF_RESEARCH

git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "feat($feature): plan with research R1"
git -C "$project/specs" push -q origin main
