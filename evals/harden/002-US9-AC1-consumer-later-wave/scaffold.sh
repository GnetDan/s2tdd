#!/usr/bin/env bash
# Scaffold for 002-US9-AC1 (consumer-later-wave).
# Given: two tasks where one uses a name the other creates. A planned feature with tasks.md and
# contracts/internal-interfaces.md, not yet hardened (no orchestration.md, no handoff.md): T003
# creates quoting.py's quote_field (II-2); T004 writes export.py's export_csv, which passes every
# field through quote_field and cites II-2 as well as II-1. Both are marked [P] and own disjoint
# files, so only the contracts' citations keep them out of one wave.
# Builds the fixture in the current directory: it is the project (a git repository on the
# branch 004-csv-export, a bare local remote standing in for GitHub), with specs/ as its own
# repository and its own bare remote. Helpers: evals/fixtures/. Neutral names only.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$(pwd)"
feature=004-csv-export
dir="$project/specs/$feature"

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" planned

cat > "$dir/plan.md" <<'EOF'
# Implementation Plan: CSV export

**Branch**: `004-csv-export` | **Spec**: [spec.md](spec.md)

## Technical Context

Language: Python 3. Tests: pytest. Every file sits at the project root: `export.py` (the
exporter), `quoting.py` (field quoting), and the tests beside them (`test_*.py`).

**Acceptance tests**: `test_*.py` at the project root, one file per scenario group.

## Constitution Check

No principle is violated.
EOF

mkdir -p "$dir/contracts"
cat > "$dir/contracts/internal-interfaces.md" <<'EOF'
# Internal interfaces: 004 CSV export

Implement to these shapes. While this feature is open, if an implementation must deviate,
update this file in the same commit. At close-out (`/s2tdd-close`) this file is frozen; from
then on the code and its tests are the contract.

Type home: none; every shape below is a plain function.

## II-1. CSV rows (`export.py`; FR-001, US1-AC1)

- `export_csv(notes) -> str`: `notes` is a list of dicts with the keys `id`, `title` and
  `text`. The result is a header row `id,title,text`, then one row per note in the notebook's
  order; rows end with LF (`\n`), the last one too.
- Every field passes through `quote_field` (II-2) before it is joined.
- Produced by T004. Consumes II-2.

## II-2. Field quoting (`quoting.py`; FR-002, US1-AC2)

- `quote_field(text) -> str`: a field that contains a comma or a double quote is wrapped in
  double quotes, and each double quote inside it is doubled; any other field is returned
  unchanged.
- Produced by T003. Consumed by T004 (`export_csv`).
EOF

cat > "$dir/tasks.md" <<'EOF'
# Tasks: CSV export

**Input**: spec.md, plan.md, contracts/internal-interfaces.md.

## Phase 1: Tests (US1)

- [ ] T001 [P] [US1] Write `test_export_rows.py` for US1-AC1: `export_csv`'s header row and one row per note, per contracts/internal-interfaces.md §II-1. Done-when: fails for the expected reason: `export.py` not found
- [ ] T002 [P] [US1] Write `test_quoting.py` for US1-AC2: a field with a comma is wrapped in double quotes, per §II-2. Done-when: fails for the expected reason: `quoting.py` not found

## Phase 2: Implementation (US1)

- [ ] T003 [P] [US1] Write `quote_field` in `quoting.py` (II-2). Done-when: `pytest test_quoting.py` passes
- [ ] T004 [P] [US1] Write `export_csv` in `export.py`, passing every field through `quoting.py`'s `quote_field` (II-1, II-2). Done-when: `pytest test_export_rows.py` passes

## Phase 3: Polish

- [ ] T005 Document `export --csv` in `README.md`. Done-when: the README names the flag
EOF

git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: tasks and contracts, not yet hardened"
git -C "$project/specs" push -q origin main
