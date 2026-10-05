#!/usr/bin/env bash
# Scaffold for 003-EC-001 (per-wave-off).
# Given: a per-wave command that fails to run (here a missing pytest plugin, `-p acme_fast`:
# pytest prints an ImportError and no summary line) rather than reporting red tests. The per-wave
# state (II-15). An earlier attended session ran W0 (committed, T001-T003 ticked, its wave report
# in s1-wave-reports.md); then the project's CLAUDE.md changed its `Per-wave tests:` line to
# `python -m pytest -q -p acme_fast`, and handoff.md's TEST RUN line with it. This session runs
# W1 and W2, which change only `*.py` files, so both would run the per-wave command: W1's fails
# to run, so W1 and W2 run the full suite. P1a runs at medium (so the attended W1 commits without
# the user's read of a strong diff), and P2a's done-when names its tests.
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
bash "$fixtures/make-feature.sh" "$project" per-wave

# The earlier session's step 0: .sdd-run/ is excluded, so packet reports are no changed files.
exclude="$project/.git/info/exclude"
grep -qx '.sdd-run/' "$exclude" 2>/dev/null || printf '.sdd-run/
' >> "$exclude"

fail() { echo "scaffold: $*" >&2; exit 1; }

# replace_text <file> <old> <new>: the first occurrence of the literal text <old> becomes <new>
# (awk reads both from the environment, so backslashes stay as written).
replace_text() {
  OLD="$2" NEW="$3" awk '!done && (i = index($0, ENVIRON["OLD"])) {
      $0 = substr($0, 1, i - 1) ENVIRON["NEW"] substr($0, i + length(ENVIRON["OLD"])); done = 1
    } { print }' "$1" > "$1.tmp"
  mv "$1.tmp" "$1"
  grep -qF -- "$3" "$1" || fail "$1: no line holds $2"
}

per_wave='python -m pytest -q -m "not slow"'
grep -qxF "Per-wave tests: $per_wave" "$project/CLAUDE.md" || fail "CLAUDE.md: no per-wave line"
grep -qF 'TEST RUN (both modes; once per wave)' "$dir/handoff.md" || fail "handoff.md: no TEST RUN"

# Attended, P1a's diff would wait for the user's read: it runs at medium here, so W1 reaches its
# commit unattended.
replace_text "$dir/orchestration.md" '| `pytest test_export_rows.py` | strong |' \
  '| `pytest test_export_rows.py` | medium |'
replace_text "$dir/handoff.md" 'The strong packets, P0c (the dispatcher) and P1a (the MVP), get the full' \
  'The strong packet, P0c (the dispatcher), gets the full'

# P2a's done-when names its tests, as harden 0.4.0 writes it (II-5 D1).
replace_text "$dir/tasks.md" 'Done-when: `pytest` passes' \
  "Done-when: \`python -m pytest test_export_rows.py test_quoting.py\` passes and the wave's test run is green"
replace_text "$dir/orchestration.md" '| T006 | `export.py` | `pytest` | cheap |' \
  '| T006 | `export.py` | `pytest test_export_rows.py test_quoting.py` | cheap |'

# The earlier attended session: W0, as the fixture's 0.3.0 states build it.
cat > "$project/test_export_rows.py" <<'EOF'
"""US1-AC1: a notebook with three notes exports a header row and three rows (II-1)."""
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
EOF
cat > "$project/test_quoting.py" <<'EOF'
"""US1-AC2: a field that contains a comma is quoted."""
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
cat > "$dir/s1-wave-reports.md" <<EOF
# Wave reports: 004, slice s1 (W0–W3)

Written by the orchestrator of an attended session. Each wave report is followed by its
packets' report files.

## W0

  Wave: W0  Packets: P0a, P0b, P0c
  Executed by: subagent per packet (s2tdd:packet-medium ×2, s2tdd:packet-strong ×1); shape check by s2tdd:strong-diff-reviewer
  Files touched: test_export_rows.py, test_quoting.py, cli.py  (preflight: clean)
  Commands run + results: P0a red as expected (No module named 'export'); P0b red as expected (No module named 'quoting'); P0c python cli.py --help exit 0
  Test run: per-wave · $per_wave · 0 passed, 2 failed, 2 selected · 0m01s (expected red until W1)
  Review: P0c: Accept; shape check: Accept (3 citations, 0 differ)
  Commit: $sha0
EOF

git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: wave 0 ticked (T001–T003); s1 wave reports; P1a at medium; P2a's done-when names its tests"
git -C "$project/specs" push -q origin main

# After W0, the project changed its per-wave command (a plugin the project does not have);
# handoff.md's TEST RUN line was refreshed to match, as harden copies it.
new_per_wave='python -m pytest -q -p acme_fast'
replaced=$(sed -e "s/^Per-wave tests: .*/Per-wave tests: $new_per_wave/" "$project/CLAUDE.md")
printf '%s\n' "$replaced" > "$project/CLAUDE.md"
grep -qxF "Per-wave tests: $new_per_wave" "$project/CLAUDE.md" || fail "CLAUDE.md: per-wave line not changed"
git -C "$project" add CLAUDE.md
git -C "$project" commit -q -m "docs: per-wave tests: $new_per_wave"
git -C "$project" push -q origin "$feature"
replace_text "$dir/handoff.md" \
  'Per-wave tests: python -m pytest -q -m "not slow" · Full suite: python -m pytest · Per-wave sees: *.py' \
  "Per-wave tests: $new_per_wave · Full suite: python -m pytest · Per-wave sees: *.py"
git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: handoff.md's TEST RUN line refreshed"
git -C "$project/specs" push -q origin main
