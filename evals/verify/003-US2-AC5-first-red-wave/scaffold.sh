#!/usr/bin/env bash
# Scaffold for 003-US2-AC5 (first-red-wave).
# Given: a slice-end full run that shows a red no per-wave run in the slice showed. Starts from
# make-feature.sh's per-wave state: the project's CLAUDE.md declares `Per-wave tests: python -m
# pytest -q -m "not slow"`, `Full suite: python -m pytest` and `Per-wave sees: *.py`. Then one
# nobrakes relay runs the waves:
# - W0 (T001-T003) is committed and verified on its own (a verify-done line for W0). P0a's
#   test_export_rows.py holds a test marked slow,
#   test_a_large_notebook_exports_one_row_per_note (20,000 notes, 20,000 rows).
# - The slice under review, W1-W2 (s1-wave-reports.md, with each wave's packet reports): W1
#   (T004, T005) builds export_csv and quote_field, and the slow test passes there; W2 (T006)
#   adds write_csv and quoting, and caps the export at 10,000 rows, which turns only the slow
#   test red. Every wave report's Test run line is a green per-wave run (the slow test
#   deselected), each wave changed only *.py files, and no report names the red.
# - W3, the docs wave (T007), has not run.
# The full suite at HEAD (W2) is red on that one test alone, and the test alone is green at W1's
# commit and red at W2's: verify-done's unexplained-red check should report
# `Red first at W2 (<sha>): ... — green at W1 (<sha>)`, untick T006 and give Not done.
# Builds the project in the current directory (on branch 004-csv-export, with a bare local
# remote beside it standing in for GitHub), with specs/ as its own repository and its own bare
# remote. Helpers: evals/fixtures/. Neutral names only.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$(pwd)"
feature=004-csv-export
specs="$project/specs"
dir="$specs/$feature"
reports="$project/.sdd-run/004/reports"

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" per-wave

exclude="$project/.git/info/exclude"
grep -qx '.sdd-run/' "$exclude" 2>/dev/null || printf '.sdd-run/\n' >> "$exclude"
mkdir -p "$reports"

# The project's pytest marker, registered before the feature's waves.
cat > "$project/pytest.ini" <<'EOF'
[pytest]
markers =
    slow: a long-running test, left out of the per-wave run
EOF
git -C "$project" add pytest.ini
git -C "$project" commit -q -m "chore: register the slow test marker"

# W0: P0a, P0b (test packets), P0c.
cat > "$project/test_export_rows.py" <<'EOF'
"""US1-AC1: a notebook exports a header row and one row per note (II-1)."""
import pytest

from export import export_csv

NOTES = [
    {"id": 1, "title": "groceries", "text": "milk"},
    {"id": 2, "title": "call", "text": "dentist"},
    {"id": 3, "title": "idea", "text": "csv export"},
]


def test_export_csv_writes_a_header_and_one_row_per_note():
    lines = export_csv(NOTES).split("\n")
    assert lines[0] == "id,title,text"
    assert lines[1:4] == ["1,groceries,milk", "2,call,dentist", "3,idea,csv export"]


def test_export_csv_ends_every_row_with_lf():
    assert export_csv(NOTES).endswith("milk\n2,call,dentist\n3,idea,csv export\n")


@pytest.mark.slow
def test_a_large_notebook_exports_one_row_per_note():
    notes = [{"id": n, "title": f"note {n}", "text": "x" * 200} for n in range(1, 20001)]
    lines = export_csv(notes).split("\n")
    assert len(lines) == 1 + 20000 + 1  # the header, one row per note, "" after the last LF
    assert lines[20000].startswith("20000,note 20000,")
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
cat > "$project/cli.py" <<'EOF'
"""The notes command line. Every command is stubbed here once (wave 0); its work lives in the
module it names, which later packets own."""
import argparse
import sys


def main(argv=None):
    parser = argparse.ArgumentParser(prog="notes")
    commands = parser.add_subparsers(dest="command", required=True)
    export = commands.add_parser("export", help="export the notebook")
    export.add_argument("--csv", metavar="PATH", help="write the notes to a CSV file")
    args = parser.parse_args(argv)
    if args.command == "export":
        from export import write_csv  # II-1; built in wave 2 (T006)
        return write_csv(args.csv)
    return 2


if __name__ == "__main__":
    sys.exit(main())
EOF
git -C "$project" add test_export_rows.py test_quoting.py cli.py
git -C "$project" commit -q -m "feat(004): wave 0 — P0a, P0b, P0c"
sha0=$(git -C "$project" rev-parse --short HEAD)
git -C "$project" push -q origin "$feature"

ticked=$(sed -e 's/^- \[ \] \(T00[1-3] \)/- [x] \1/' "$dir/tasks.md")
printf '%s\n' "$ticked" > "$dir/tasks.md"
printf -- '- 2026-10-02 · verify-done · waves W0–W0 (%s..%s) · Verified · proxy · suite 0m01s (no budget)\n' \
  "$sha0" "$sha0" >> "$dir/validation.md"
git -C "$specs" add "$feature"
git -C "$specs" commit -q -m "004: wave 0 ticked (T001–T003); verified"
sleep 1  # the slice's first commit comes after the specs commit that ticked W0

# W1: P1a (T004), P1b (T005).
cat > "$project/export.py" <<'EOF'
"""CSV export of a notebook (II-1)."""

HEADER = ("id", "title", "text")


def export_csv(notes):
    """The notebook as CSV text: a header row, then one row per note, every row ending in LF."""
    rows = [",".join(HEADER)]
    rows += [",".join(str(note[key]) for key in HEADER) for note in notes]
    return "\n".join(rows) + "\n"
EOF
cat > "$project/quoting.py" <<'EOF'
"""CSV field quoting (II-2)."""


def quote_field(text):
    """Wrap a field holding a comma or a double quote in double quotes, doubling inner ones."""
    if "," in text or '"' in text:
        return '"' + text.replace('"', '""') + '"'
    return text
EOF
git -C "$project" add export.py quoting.py
git -C "$project" commit -q -m "feat(004): wave 1 — P1a, P1b"
sha1=$(git -C "$project" rev-parse --short HEAD)

# W2: P2a (T006). The row cap is the regression only the slow test sees.
cat > "$project/export.py" <<'EOF'
"""CSV export of a notebook (II-1, II-2)."""
import json

from quoting import quote_field

HEADER = ("id", "title", "text")
MAX_ROWS = 10_000  # rows per export


def export_csv(notes):
    """The notebook as CSV text: a header row, then one row per note, every row ending in LF."""
    rows = [",".join(HEADER)]
    rows += [",".join(quote_field(str(note[key])) for key in HEADER)
             for note in notes[:MAX_ROWS]]
    return "\n".join(rows) + "\n"


def write_csv(path):
    """Write the notebook (notes.json in the working directory) to path as UTF-8; return 0."""
    with open("notes.json", encoding="utf-8") as notebook:
        notes = json.load(notebook)
    with open(path, "w", encoding="utf-8", newline="") as out:
        out.write(export_csv(notes))
    return 0
EOF
git -C "$project" add export.py
git -C "$project" commit -q -m "feat(004): wave 2 — P2a"
sha2=$(git -C "$project" rev-parse --short HEAD)
git -C "$project" push -q origin "$feature"

# The slice's packet reports.
cat > "$reports/P1a.md" <<'EOF'
# P1a report (W1, strong): T004

## Files touched

- export.py +10/−0 (new).

## Red run (09:41Z, before any edit, under 1 min)

`python -m pytest test_export_rows.py -m "not slow"`: 1 error during collection,
ModuleNotFoundError: No module named 'export'.

## Green run (09:45Z, under 1 min)

`python -m pytest test_export_rows.py -m "not slow"`: 2 passed, 1 deselected.

## Test changes, decisions, deviations, open questions

None.
EOF
cat > "$reports/P1b.md" <<'EOF'
# P1b report (W1, cheap): T005

## Files touched

- quoting.py +8/−0 (new).

## Red run (09:40Z, before any edit, under 1 min)

`python -m pytest test_quoting.py`: 1 error during collection, ModuleNotFoundError: No module
named 'quoting'.

## Green run (09:44Z, under 1 min)

`python -m pytest test_quoting.py`: 3 passed.

## Test changes, decisions, deviations, open questions

None.
EOF
cat > "$reports/P2a.md" <<'EOF'
# P2a report (W2, cheap): T006

## Files touched

- export.py +12/−2.

## Red run (10:02Z, before any edit, under 1 min)

`python cli.py export --csv out.csv`: ImportError: cannot import name 'write_csv' from 'export'.

## Green run (10:07Z, under 1 min)

`python -m pytest -q -m "not slow"`: 5 passed, 1 deselected. `python cli.py export --csv
out.csv` with a three-note notes.json: exit 0, four rows written.

## Test changes, decisions, deviations, open questions

None.
EOF

waves="$dir/s1-wave-reports.md"
cat > "$waves" <<EOF
# Wave reports: 004, slice s1 (W1–W2)

Written by the orchestrator of nobrakes run nb-20261002-0900, relay 1. Each wave report is
followed by its packets' report files.

## W1

  Wave: W1  Packets: P1a, P1b
  Executed by: subagent per packet (s2tdd:packet-strong ×1, s2tdd:packet-cheap ×1); P1a's review by s2tdd:strong-diff-reviewer
  Files touched: export.py, quoting.py  (preflight: clean)
  Commands run + results: P1a python -m pytest test_export_rows.py -m "not slow" 2 passed; P1b python -m pytest test_quoting.py 3 passed
  Test run: per-wave · python -m pytest -q -m "not slow" · 5 passed, 0 failed, 5 selected · 0m01s
  Red runs: test_export_rows.py and test_quoting.py, red at W0 and again before dispatch (No module named 'export'; No module named 'quoting')
  Test changes: none
  Decisions: none
  Deviations: none
  Review: P1a: Accept; shape check: none
  Ledger: Usage +1
  Open questions / blocked: none
  Commit: $sha1
  Boundary: context 27% · five-hour 20% · week 43% · BRAKES none · ledger +1 lines

EOF
cat "$reports/P1a.md" "$reports/P1b.md" >> "$waves"
cat >> "$waves" <<EOF

## W2

  Wave: W2  Packets: P2a
  Executed by: subagent per packet (s2tdd:packet-cheap ×1)
  Files touched: export.py  (preflight: clean)
  Commands run + results: P2a python -m pytest -q -m "not slow" 5 passed; python cli.py export --csv out.csv exit 0
  Test run: per-wave · python -m pytest -q -m "not slow" · 5 passed, 0 failed, 5 selected · 0m01s
  Red runs: P2a: python cli.py export --csv out.csv failed with ImportError: cannot import name 'write_csv' before dispatch
  Test changes: none
  Decisions: none
  Deviations: none
  Review: none
  Ledger: Usage +1
  Open questions / blocked: none
  Commit: $sha2
  Boundary: context 33% · five-hour 26% · week 44% · BRAKES none · ledger +1 lines

EOF
cat "$reports/P2a.md" >> "$waves"

ticked=$(sed -e 's/^- \[ \] \(T00[4-6] \)/- [x] \1/' "$dir/tasks.md")
printf '%s\n' "$ticked" > "$dir/tasks.md"

# run-ledger.md: harden 0.4.0's headings, the run's lines so far (W3, the docs wave, not run).
{
  cat <<'EOF'
# Run ledger: 004 CSV export

Running state of the implementing sessions (orchestration.md ground rules 2, 14–17; handoff.md
NOBRAKES). One line per item, added when it happens; never rewritten. Frozen at close-out.

EOF
  for heading in "Lease" "Runs" "Rounds" "Usage" "Carried constraints" "Amendments" \
    "Test-owner fixes" "Ownership exceptions" "Expected red" "Blocked and skipped" \
    "Open review notes" "Pending checkpoints" "Tags and pushes" "Processes killed" "Handoff"; do
    printf '## %s\n' "$heading"
    case "$heading" in
      "Lease") printf 'session-1, relay 1, since 2026-10-02T09:00Z\n' ;;
      "Runs") printf 'run nb-20261002-0900 · nobrakes · scope W0–W3 · started 2026-10-02T09:00Z\n' ;;
      "Usage") printf 'wave 0 · context 18%% · 3 packets\nwave 1 · context 27%% · 2 packets\nwave 2 · context 33%% · 1 packets\n' ;;
      "Carried constraints") printf 'Usage limits: week 95%%, five-hour 90%% (default)\n' ;;
    esac
  done
} > "$dir/run-ledger.md"

git -C "$specs" add "$feature"
git -C "$specs" commit -q -m "004: waves 1–2 ticked (T004–T006); s1 wave reports"
git -C "$specs" push -q origin main
