#!/usr/bin/env bash
# Scaffold for 002-EC-005 (no-old-names-written).
# Given: a feature whose spec or contracts quote old command names. Feature 004 also rewords the
# project README's contributor note, which still names the old commands (`/speckit-plan`,
# `/speckit-implement`): spec.md, contracts/internal-interfaces.md (II-2, a line to transcribe)
# and tasks.md quote them. The feature is planned with tasks.md and contracts, not yet hardened
# (no orchestration.md, no handoff.md). The old names live only in this case's own fixture files.
# Builds the fixture in the current directory: it is the project (a git repository on the
# branch 004-csv-export, a bare local remote standing in for GitHub), with specs/ as its own
# repository and its own bare remote. Helpers: evals/fixtures/. Neutral names only.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$(pwd)"
feature=004-csv-export
dir="$project/specs/$feature"

bash "$fixtures/make-project.sh" "$project" acme

printf '\nContributors: plan with /speckit-plan, then build with /speckit-implement.\n' \
  >> "$project/README.md"
git -C "$project" add README.md
git -C "$project" commit -q -m "docs: contributor note"
git -C "$project" push -q origin main

bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" planned

cat > "$dir/spec.md" <<'EOF'
# Feature Specification: CSV export

**Feature Branch**: `004-csv-export`
**Status**: Draft

## User Stories

### US1 - Export notes as CSV (Priority: P1)

A user exports their notes to a CSV file.

- **US1-AC1**: **Given** a notebook with three notes, **When** the user runs `export --csv`,
  **Then** a file with a header row and three rows is written.

### US2 - The contributor note names the current commands (Priority: P2)

The README's contributor note still says `/speckit-plan` and `/speckit-implement`, commands
that no longer exist; a contributor who follows it gets "unknown command".

- **US2-AC1**: **Given** README.md's contributor note, which names `/speckit-plan` and
  `/speckit-implement`, **When** this feature lands, **Then** it names `/s2tdd-plan` and
  `/s2tdd-implement`, and README.md names no `/speckit-` command.

## Requirements

- **FR-001**: The system MUST write notes to CSV with one row per note. *(US1-AC1)*
- **FR-002**: README.md MUST name `/s2tdd-plan` and `/s2tdd-implement` where it now names
  `/speckit-plan` and `/speckit-implement`. *(US2-AC1)*
EOF

cat > "$dir/plan.md" <<'EOF'
# Implementation Plan: CSV export

**Branch**: `004-csv-export` | **Spec**: [spec.md](spec.md)

## Technical Context

Language: Python 3. Tests: pytest. Every file sits at the project root: `export.py` (the
exporter), `README.md`, and the tests beside them (`test_*.py`).

**Acceptance tests**: `test_*.py` at the project root.

## Constitution Check

No principle is violated.
EOF

mkdir -p "$dir/contracts"
cat > "$dir/contracts/internal-interfaces.md" <<'EOF'
# Internal interfaces: 004 CSV export

Implement to these shapes. While this feature is open, if an implementation must deviate,
update this file in the same commit. At close-out (`/s2tdd-close`) this file is frozen; from
then on the code and its tests are the contract.

## II-1. CSV rows (`export.py`; FR-001, US1-AC1)

- `export_csv(notes) -> str`: `notes` is a list of dicts with the keys `id`, `title` and
  `text`. The result is a header row `id,title,text`, then one row per note; rows end with LF.

## II-2. The contributor note (`README.md`; FR-002, US2-AC1) — transcribe; do not invent

- Old line: `Contributors: plan with /speckit-plan, then build with /speckit-implement.`
- New line: `Contributors: plan with /s2tdd-plan, then build with /s2tdd-implement.`
- After the change, `grep -c '/speckit-' README.md` prints 0.
EOF

cat > "$dir/tasks.md" <<'EOF'
# Tasks: CSV export

**Input**: spec.md, plan.md, contracts/internal-interfaces.md.

## Phase 1: Tests

- [ ] T001 [P] [US1] Write `test_export_rows.py` for US1-AC1: `export_csv`'s header row and one row per note, per contracts/internal-interfaces.md §II-1. Done-when: fails for the expected reason: `export.py` not found
- [ ] T002 [P] [US2] Write `test_readme_note.py` for US2-AC1: README.md holds II-2's new line and no `/speckit-plan` or `/speckit-implement`. Done-when: fails for the expected reason: README.md still names `/speckit-implement`

## Phase 2: Implementation

- [ ] T003 [P] [US1] Write `export_csv` in `export.py` (II-1). Done-when: `pytest test_export_rows.py` passes
- [ ] T004 [P] [US2] Replace README.md's contributor note, `/speckit-plan` and `/speckit-implement`, with II-2's new line. Done-when: `pytest test_readme_note.py` passes
EOF

git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: tasks and contracts, not yet hardened"
git -C "$project/specs" push -q origin main
