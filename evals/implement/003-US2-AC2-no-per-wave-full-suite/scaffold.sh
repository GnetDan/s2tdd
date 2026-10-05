#!/usr/bin/env bash
# Scaffold for 003-US2-AC2 (no-per-wave-full-suite).
# Given: a project that declares no per-wave test command. The per-wave state (II-15), with its
# CLAUDE.md rewritten to declare only `Full suite: python -m pytest` (no `Per-wave tests:`, no
# `Per-wave sees:`), and handoff.md's TEST RUN line refreshed to match, as harden copies it:
# `Per-wave tests: none · Full suite: python -m pytest · Per-wave sees: none`. An earlier
# attended session ran W0 and W1 (committed, T001-T005 ticked, their wave reports in
# s1-wave-reports.md). This session runs W2: one cheap packet, P2a (T006, `export.py`), whose
# done-when names its tests, so the orchestrator's wave test run is the only untargeted pytest
# run.
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

full='python -m pytest'
grep -qF 'TEST RUN (both modes; once per wave)' "$dir/handoff.md" || fail "handoff.md: no TEST RUN"

# The project declares no per-wave command: CLAUDE.md keeps only its Full suite: line (on main,
# before the feature's work), and handoff.md's TEST RUN line says so.
git -C "$project" checkout -q main
cat > "$project/CLAUDE.md" <<'EOF'
# acme-notes

A small notes app. The tests are pytest files at the project root.

Full suite: python -m pytest
EOF
git -C "$project" add CLAUDE.md
git -C "$project" commit -q -m "docs: declare only the full test command"
git -C "$project" push -q origin main
git -C "$project" checkout -q "$feature"
git -C "$project" merge -q --ff-only main
if grep -qi '^[[:space:]]*per-wave' "$project/CLAUDE.md"; then
  fail "CLAUDE.md still declares a per-wave line"
fi
replace_text "$dir/handoff.md" \
  'Per-wave tests: python -m pytest -q -m "not slow" · Full suite: python -m pytest · Per-wave sees: *.py' \
  'Per-wave tests: none · Full suite: python -m pytest · Per-wave sees: none'

# P2a's done-when names its tests, as harden 0.4.0 writes it (II-5 D1).
replace_text "$dir/tasks.md" 'Done-when: `pytest` passes' \
  "Done-when: \`python -m pytest test_export_rows.py test_quoting.py\` passes and the wave's test run is green"
replace_text "$dir/orchestration.md" '| T006 | `export.py` | `pytest` | cheap |' \
  '| T006 | `export.py` | `pytest test_export_rows.py test_quoting.py` | cheap |'

# The earlier attended session: W0 and W1, as the fixture's 0.3.0 states build them.
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
git -C "$project" push -q origin "$feature"

ticked=$(sed -e 's/^- \[ \] \(T00[1-5] \)/- [x] \1/' "$dir/tasks.md")
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
  Test run: full (no per-wave command) · $full · 0 passed, 2 failed · 0m01s (expected red until W1)
  Review: P0c: Accept; shape check: Accept (3 citations, 0 differ)
  Commit: $sha0

## W1

  Wave: W1  Packets: P1a, P1b
  Executed by: subagent per packet (s2tdd:packet-strong ×1, s2tdd:packet-cheap ×1)
  Files touched: export.py, quoting.py  (preflight: clean)
  Commands run + results: P1a python -m pytest test_export_rows.py 2 passed; P1b python -m pytest test_quoting.py 3 passed
  Test run: full (no per-wave command) · $full · 5 passed, 0 failed · 0m01s
  Review: P1a: Accept; shape check: none
  Commit: $sha1
EOF

git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: waves 0–1 ticked (T001–T005); s1 wave reports; P2a's done-when names its tests"
git -C "$project/specs" push -q origin main
