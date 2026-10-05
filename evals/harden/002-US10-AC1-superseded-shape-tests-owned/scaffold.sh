#!/usr/bin/env bash
# Scaffold for 002-US10-AC1 (superseded-shape-tests-owned).
# Given: a contract that changes a shape an existing test asserts. An earlier, closed feature
# (003-notes-export) left `export.py` and its test `test_notes_export.py` on main: the header row
# is `title,text`. Feature 004's contract II-1 supersedes that section and widens the header to
# `id,title,text`; no task of 004 names `test_notes_export.py`. The feature is planned with
# tasks.md and contracts, not yet hardened (no orchestration.md, no handoff.md).
# Builds the fixture in the current directory: it is the project (a git repository on the
# branch 004-csv-export, a bare local remote standing in for GitHub), with specs/ as its own
# repository and its own bare remote. Helpers: evals/fixtures/. Neutral names only.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$(pwd)"
feature=004-csv-export
dir="$project/specs/$feature"

bash "$fixtures/make-project.sh" "$project" acme

# Feature 003's code and test, merged on main before 004 starts.
cat > "$project/export.py" <<'EOF'
"""CSV export of a notebook (feature 003, contracts/internal-interfaces.md §II-1)."""

HEADER = ("title", "text")


def export_csv(notes):
    """The notebook as CSV text: a header row, then one row per note, every row ending in LF."""
    rows = [",".join(HEADER)]
    rows += [",".join(str(note[key]) for key in HEADER) for note in notes]
    return "\n".join(rows) + "\n"
EOF
cat > "$project/test_notes_export.py" <<'EOF'
"""Feature 003: a notebook exports as CSV, title then text."""
from export import export_csv

NOTES = [{"id": 1, "title": "groceries", "text": "milk"}]


def test_export_csv_header_is_title_then_text():
    assert export_csv(NOTES).split("\n")[0] == "title,text"


def test_export_csv_row_is_title_then_text():
    assert export_csv(NOTES).split("\n")[1] == "groceries,milk"
EOF
git -C "$project" add export.py test_notes_export.py
git -C "$project" commit -q -m "feat(003): export notes as CSV"
git -C "$project" push -q origin main

bash "$fixtures/make-specs.sh" "$project"

# Feature 003's record: closed, its contract kept as written.
earlier="$project/specs/003-notes-export"
mkdir -p "$earlier/contracts"
cat > "$earlier/spec.md" <<'EOF'
# Feature Specification: Notes export

**Feature Branch**: `003-notes-export`
**Status**: Closed — 2026-09-20 — historical intent record. For current behavior read the code and tests.

## User Stories

### US1 - Export notes (Priority: P1)

- **US1-AC1**: **Given** a notebook, **When** the user exports it, **Then** each note is a row
  of its title and text.
EOF
cat > "$earlier/contracts/internal-interfaces.md" <<'EOF'
# Internal interfaces: 003 Notes export

## II-1. CSV rows (`export.py`)

- `export_csv(notes) -> str`: a header row `title,text`, then one row per note: its title and
  its text; rows end with LF.
EOF
git -C "$project/specs" add 003-notes-export
git -C "$project/specs" commit -q -m "003: closed"

bash "$fixtures/make-feature.sh" "$project" planned

cat > "$dir/spec.md" <<'EOF'
# Feature Specification: CSV export

**Feature Branch**: `004-csv-export`
**Status**: Draft

## User Stories

### US1 - Export notes as CSV with their ids (Priority: P1)

A user exports their notes to a CSV file and can match each row to its note.

- **US1-AC1**: **Given** a notebook with three notes, **When** the user exports it, **Then**
  the header row is `id,title,text` and each row starts with its note's id.

## Requirements

- **FR-001**: The export MUST write each note's id as the first column. *(US1-AC1)*
EOF

cat > "$dir/plan.md" <<'EOF'
# Implementation Plan: CSV export

**Branch**: `004-csv-export` | **Spec**: [spec.md](spec.md)

## Technical Context

Language: Python 3. Tests: pytest. Every file sits at the project root: `export.py` (the
exporter, from feature 003) and the tests beside it (`test_*.py`).

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

## II-1. CSV rows (`export.py`; FR-001, US1-AC1) — supersedes 003 contracts/internal-interfaces.md §II-1

- `export_csv(notes) -> str`: `notes` is a list of dicts with the keys `id`, `title` and
  `text`. The header row is `id,title,text` (was `title,text`), then one row per note: its id,
  title and text; rows end with LF, the last one too.
- Produced by T002.
EOF

cat > "$dir/tasks.md" <<'EOF'
# Tasks: CSV export

**Input**: spec.md, plan.md, contracts/internal-interfaces.md.

## Phase 1: Tests (US1)

- [ ] T001 [US1] Write `test_export_ids.py` for US1-AC1: the header row is `id,title,text` and each row starts with its note's id, per contracts/internal-interfaces.md §II-1. Done-when: fails for the expected reason: the header row has no `id`

## Phase 2: Implementation (US1)

- [ ] T002 [US1] Write the id column first in `export.py`'s `export_csv` (II-1). Done-when: `pytest test_export_ids.py` passes

## Phase 3: Polish

- [ ] T003 Document the id column in `README.md`. Done-when: the README names the `id` column
EOF

git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: tasks and contracts, not yet hardened"
git -C "$project/specs" push -q origin main
