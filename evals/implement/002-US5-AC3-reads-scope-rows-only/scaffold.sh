#!/usr/bin/env bash
# Scaffold for 002-US5-AC3 (reads-scope-rows-only).
# Given: a slice whose scope is waves 8-10 of 16. The hardened-shapes state (II-16) keeps its
# ground rules, handoff.md, contracts and run-ledger.md; its wave table, tasks and context
# budget become a 16-wave feature: W0 writes test_columns.py (T001, T002), and each wave W<n>
# (1-15) builds col<nn>.py with tasks T<2n+1> and T<2n+2>. Waves W0-W7 are committed on the
# feature branch and their tasks ticked; the slices are s1 W0-W7, s2 W8-W10, s3 W11-W15. So W8's
# tasks are T017-T018, W9's T019-T020, W10's T021-T022; no other wave's row or task is the
# slice's.
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
bash "$fixtures/make-feature.sh" "$project" hardened-shapes

fail() { echo "scaffold: $*" >&2; exit 1; }
nn() { printf '%02d' "$1"; }
task() { printf 'T%03d' "$1"; }

# orchestration.md: the fixture's text up to its wave table (title, ground rules), then a
# 16-wave table and the sections after it; its judgment section is kept as written.
orch="$dir/orchestration.md"
head_part=$(awk '/^## Contention resolutions/ { exit } { print }' "$orch")
judgment=$(awk '/^## Context budget/ { exit } on { print } /^## Dispatching the remaining judgment/ { on = 1; print }' "$orch")
[ -n "$head_part" ] && [ -n "$judgment" ] || fail "orchestration.md's sections not found"
{
  printf '%s\n\n' "$head_part"
  cat <<'EOF'
## Contention resolutions

| Contention | Resolution |
|---|---|
| none: each wave's packet owns one new column module | — |

## Wave table

Packets marked **T** are test packets, **I** implementation packets. Each wave's row is one
table line whose first cell begins W<n>, and each section sits under its own heading, so an
orchestrator can read them by grep.

| Wave | Packets (parallel within wave) | Tasks | Owned files | Done-when | Tier |
|---|---|---|---|---|---|
| W0 red | P0a T | T001, T002 | `test_columns.py` | red: `col01.py` not found | medium |
EOF
  for n in $(seq 1 15); do
    printf '| W%d | P%da I | %s, %s | `col%s.py` | `python -m pytest test_columns.py -k c%s` | cheap |\n' \
      "$n" "$n" "$(task $((2 * n + 1)))" "$(task $((2 * n + 2)))" "$(nn "$n")" "$(nn "$n")"
  done
  cat <<'EOF'

### Superseded-shape searches

| Shape (contract) | Search | Hits | Owner |
|---|---|---|---|
| none: no section supersedes a shape or changes an existing signature | — | none | — |

## Expected red

| Test | Red from | Green at | Reason |
|---|---|---|---|
| `test_columns.py::test_column_names_itself[c<nn>]` | W0 | W<n> (the wave that builds `col<nn>.py`) | `col<nn>` not found |

## Judgment audit

| ID | Task | Judgment | Status | Section |
|---|---|---|---|---|
| — | — | none: every column's name is fixed by its test | — | — |

EOF
  printf '%s\n' "$judgment"
  cat <<'EOF'

## Context budget

16 waves, one packet each (W0 a test packet) × about 15k tokens. Three slices; each slice's end
is where `--nobrakes` runs a verify gate.

| Slice | Waves |
|---|---|
| s1 | W0–W7 |
| s2 | W8–W10 |
| s3 | W11–W15 |
EOF
} > "$orch"

# tasks.md: T001-T032, T001-T016 (waves W0-W7) ticked.
{
  cat <<'EOF'
# Tasks: CSV export

**Input**: spec.md, plan.md, contracts/internal-interfaces.md. Orchestration:
[orchestration.md](orchestration.md).

## Phase 1: Tests (US1)

- [x] T001 [US1] Write `test_columns.py`'s cases for the columns c01–c07: `col<nn>.name()` returns `c<nn>`. Done-when: fails for the expected reason: `col01` not found
- [x] T002 [US1] Add the cases for the columns c08–c15 to `test_columns.py`. Done-when: fails for the expected reason: `col08` not found

## Phase 2: Columns (US1)

EOF
  for n in $(seq 1 15); do
    box=" "
    [ "$n" -le 7 ] && box="x"
    printf -- '- [%s] %s [US1] Write `col%s.py` with `name()` returning `c%s`. Done-when: `python -m pytest test_columns.py -k c%s` passes\n' \
      "$box" "$(task $((2 * n + 1)))" "$(nn "$n")" "$(nn "$n")" "$(nn "$n")"
    printf -- '- [%s] %s [US1] Give `col%s.py` a module docstring naming its column. Done-when: `python -c "import col%s; assert col%s.__doc__"` exits 0\n' \
      "$box" "$(task $((2 * n + 2)))" "$(nn "$n")" "$(nn "$n")" "$(nn "$n")"
  done
  cat <<'EOF'

## Notes

Waves, packets and owned files: [orchestration.md](orchestration.md).
EOF
} > "$dir/tasks.md"

# handoff.md: its TIER and HOW TO WORK name the shapes feature's packets; this feature has no
# strong packet and no dispatcher.
handoff=$(sed -e 's/The strong packets, P0c (the dispatcher) and P1a (the MVP), get the full/The strong packets (none in this feature) get the full/' \
  -e "/^- Transcribe, don't invent: T003's dispatcher/d" "$dir/handoff.md")
printf '%s\n' "$handoff" > "$dir/handoff.md"

[ "$(grep -c '^| W[0-9]* ' "$orch")" -eq 16 ] || fail "orchestration.md does not have 16 wave rows"
grep -q '^- \[ \] T017 ' "$dir/tasks.md" || fail "tasks.md: T017 not open"

git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: 16 waves; W0–W7 ticked (T001–T016)"
git -C "$project/specs" push -q origin main

# The project: waves W0-W7 committed on the feature branch.
cat > "$project/test_columns.py" <<'EOF'
"""US1-AC1: every column module names its column."""
import importlib

import pytest

COLUMNS = [f"c{n:02d}" for n in range(1, 16)]


@pytest.mark.parametrize("column", COLUMNS)
def test_column_names_itself(column):
    module = importlib.import_module("col" + column[1:])
    assert module.name() == column
EOF
git -C "$project" add test_columns.py
git -C "$project" commit -q -m "feat(004): wave 0 — P0a"
for n in $(seq 1 7); do
  printf '"""Column c%s of the CSV export."""\n\n\ndef name():\n    return "c%s"\n' "$(nn "$n")" "$(nn "$n")" \
    > "$project/col$(nn "$n").py"
  git -C "$project" add "col$(nn "$n").py"
  git -C "$project" commit -q -m "feat(004): wave $n — P${n}a"
done
git -C "$project" push -q origin "$feature"
