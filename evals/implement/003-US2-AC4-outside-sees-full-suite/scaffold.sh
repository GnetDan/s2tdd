#!/usr/bin/env bash
# Scaffold for 003-US2-AC4 (outside-sees-full-suite).
# Given: a project whose `Per-wave sees:` line is `*.py` and a wave that changes a prompt file.
# The per-wave state (II-15): the project's CLAUDE.md holds `Per-wave tests: python -m pytest -q
# -m "not slow"`, `Full suite: python -m pytest` and `Per-wave sees: *.py`. The project has a
# prompt file, `assistant-prompt.md` (the notes assistant's prompt), and T007 (W3's only packet,
# P3a) adds the export command to it, in place of the README. An earlier attended session ran
# W0-W2 (committed, T001-T006 ticked, their wave reports in s1-wave-reports.md). This session
# runs W3, which changes only `assistant-prompt.md`: outside Per-wave sees, so its test run is
# the full suite. With MODE: attended, W3 is an ordinary wave (DOCS WAVE is a NOBRAKES rule).
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

# The project's prompt file, on main before the feature's work.
git -C "$project" checkout -q main
cat > "$project/assistant-prompt.md" <<'EOF'
# Notes assistant

You help the user keep their notes. The commands you can offer:

- `add <title> <text>`: add a note.
- `list`: list the notes, newest first.
EOF
git -C "$project" add assistant-prompt.md
git -C "$project" commit -q -m "feat: the notes assistant's prompt"
git -C "$project" push -q origin main
git -C "$project" checkout -q "$feature"
git -C "$project" merge -q --ff-only main

# W3's task changes the prompt file (it was the README's).
replace_text "$dir/tasks.md" 'Document `export --csv` in `README.md`. Done-when: the README names the flag' \
  "Add \`export --csv <path>\` to the notes assistant's prompt, \`assistant-prompt.md\`, so the assistant can offer it. Done-when: \`assistant-prompt.md\` names the flag"
replace_text "$dir/orchestration.md" '| T007 | `README.md` | the README names the flag | cheap |' \
  '| T007 | `assistant-prompt.md` | `assistant-prompt.md` names the flag | cheap |'

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

cat > "$project/export.py" <<'EOF'
"""CSV export of a notebook (II-1, II-2)."""
import json

from quoting import quote_field

HEADER = ("id", "title", "text")


def export_csv(notes):
    """The notebook as CSV text: a header row, then one row per note, every row ending in LF."""
    rows = [",".join(HEADER)]
    rows += [",".join(quote_field(str(note[key])) for key in HEADER) for note in notes]
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

ticked=$(sed -e 's/^- \[ \] \(T00[1-6] \)/- [x] \1/' "$dir/tasks.md")
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

## W1

  Wave: W1  Packets: P1a, P1b
  Executed by: subagent per packet (s2tdd:packet-strong ×1, s2tdd:packet-cheap ×1)
  Files touched: export.py, quoting.py  (preflight: clean)
  Commands run + results: P1a python -m pytest test_export_rows.py 2 passed; P1b python -m pytest test_quoting.py 3 passed
  Test run: per-wave · $per_wave · 5 passed, 0 failed, 5 selected · 0m01s
  Review: P1a: Accept; shape check: none
  Commit: $sha1

## W2

  Wave: W2  Packets: P2a
  Executed by: subagent per packet (s2tdd:packet-cheap ×1)
  Files touched: export.py  (preflight: clean)
  Commands run + results: P2a python -m pytest test_export_rows.py test_quoting.py 5 passed
  Test run: per-wave · $per_wave · 5 passed, 0 failed, 5 selected · 0m01s
  Review: shape check: none
  Commit: $sha2
EOF

git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: waves 0–2 ticked (T001–T006); T007 changes the assistant's prompt; s1 wave reports; P2a's done-when names its tests"
git -C "$project/specs" push -q origin main
