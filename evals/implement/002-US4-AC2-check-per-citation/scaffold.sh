#!/usr/bin/env bash
# Scaffold for 002-US4-AC2 (check-per-citation).
# Given: test packets' reports with Cites: lines, at the point where the shape check reads them.
# The hardened-shapes state (II-16), with wave W0's two test packets already reported and their
# reds confirmed: test_export_rows.py (P0a) and test_quoting.py (P0b) written and uncommitted,
# their reports in .sdd-run/004/reports/. Three citations: P0a's header-and-rows test matches
# contracts/internal-interfaces.md §II-1; P0a's line-end test asserts CRLF where §II-1 says LF on
# every platform (it differs); P0b's quoting tests match §II-2.
# Builds the fixture in the current directory: it is the project (a git repository on the
# branch 004-csv-export, a bare local remote standing in for GitHub), with specs/ as its own
# repository and its own bare remote. Helpers: evals/fixtures/. Neutral names only.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$(pwd)"

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" hardened-shapes

# The orchestrator's step 0 of the work: .sdd-run/ is excluded from git.
exclude="$project/.git/info/exclude"
grep -qx '.sdd-run/' "$exclude" 2>/dev/null || printf '.sdd-run/\n' >> "$exclude"

cat > "$project/test_export_rows.py" <<'EOF'
"""US1-AC1: a notebook with three notes exports a header row and three rows (II-1)."""
from export import export_csv

NOTES = [
    {"id": 1, "title": "groceries", "text": "milk"},
    {"id": 2, "title": "call", "text": "dentist"},
    {"id": 3, "title": "idea", "text": "csv export"},
]


def test_export_csv_writes_a_header_and_one_row_per_note():
    lines = export_csv(NOTES).splitlines()
    assert lines[0] == "id,title,text"
    assert lines[1:4] == ["1,groceries,milk", "2,call,dentist", "3,idea,csv export"]


def test_export_csv_ends_every_row_with_crlf():
    assert export_csv(NOTES).endswith("milk\r\n2,call,dentist\r\n3,idea,csv export\r\n")
EOF

cat > "$project/test_quoting.py" <<'EOF'
"""US1-AC2: a field that contains a comma is quoted (II-2)."""
from quoting import quote_field


def test_a_field_with_a_comma_is_quoted():
    assert quote_field("milk, eggs") == '"milk, eggs"'


def test_a_quote_inside_a_quoted_field_is_doubled():
    assert quote_field('say "hi", then go') == '"say ""hi"", then go"'


def test_a_plain_field_is_unchanged():
    assert quote_field("milk") == "milk"
EOF

# Intent to add, so the brief's `git diff -- <test files>` shows the new test files.
git -C "$project" add -N test_export_rows.py test_quoting.py

reports="$project/.sdd-run/004/reports"
mkdir -p "$reports"
cat > "$reports/P0a.md" <<'EOF'
# P0a report (W0, medium, test packet): T001

## Files touched

- test_export_rows.py +19/−0 (new).

## Red run (09:08Z, under 1 min)

`python -m pytest test_export_rows.py`: 1 error during collection, ModuleNotFoundError: No
module named 'export', as T001's done-when expects.

## Cites

Cites: test_export_csv_writes_a_header_and_one_row_per_note asserts export_csv's header and row shape → contracts/internal-interfaces.md §II-1
Cites: test_export_csv_ends_every_row_with_crlf asserts export_csv's row ends → contracts/internal-interfaces.md §II-1

## Test changes, decisions, deviations, open questions

None.
EOF

cat > "$reports/P0b.md" <<'EOF'
# P0b report (W0, medium, test packet): T002

## Files touched

- test_quoting.py +14/−0 (new).

## Red run (09:09Z, under 1 min)

`python -m pytest test_quoting.py`: 1 error during collection, ModuleNotFoundError: No module
named 'quoting', as T002's done-when expects.

## Cites

Cites: test_a_field_with_a_comma_is_quoted, test_a_quote_inside_a_quoted_field_is_doubled, test_a_plain_field_is_unchanged assert quote_field's quoting → contracts/internal-interfaces.md §II-2

## Test changes, decisions, deviations, open questions

None.
EOF
