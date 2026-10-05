#!/usr/bin/env bash
# Scaffold for 002-EC-003 (escalation-raises-effort).
# Given: a cheap packet whose fence a first attempt can fail, in a --nobrakes run (FAILED
# FENCES: after two failures, a third attempt in a fresh agent one tier up, with both failure
# reports attached). The hardened-shapes state (II-16) with wave W0 committed and verified
# (T001-T003 ticked). contracts/internal-interfaces.md §II-2 states the full quoting rule
# (comma, double quote, CR or LF, a leading or trailing space or tab; the empty field
# unchanged), and W0's P0b committed the guard check_quoting.py, which checks quote_field
# against that rule case by case. W1's cheap packet P1b (T005, quoting.py) must pass it besides
# test_quoting.py; T005's line summarizes only the comma and double-quote cases. The guard is
# attainable and agrees with the contract and the tests, so a failure is the packet's own (no
# Contract need, no test-owner fix); whether an attempt fails is the model's, so the graders
# check the escalation where it happens.
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

# rewrite <file> <sed script>: portable in-place sed (no -i).
rewrite() {
  local text
  text=$(sed -e "$2" "$1")
  printf '%s\n' "$text" > "$1"
}

# The contract: II-1 as the fixture has it, II-2 with the full quoting rule and the guard.
contract="$dir/contracts/internal-interfaces.md"
ii1=$(awk '/^## II-2\./ { exit } { print }' "$contract")
[ -n "$ii1" ] || fail "contract: II-1 not found"
{
  printf '%s\n' "$ii1"
  cat <<'EOF'
## II-2. Field quoting (`quoting.py`; FR-002, FR-003, US1-AC2)

- `quote_field(text) -> str`: a field is wrapped in double quotes, with each double quote inside
  it doubled, when it contains a comma, a double quote, a CR or an LF, or when it begins or ends
  with a space or a tab; any other field, the empty one included, is returned unchanged.
- The guard `check_quoting.py` (written in wave 0, T002) checks `quote_field` against this rule
  case by case and exits 0 when every case holds; it is never weakened. Built in wave 1 (T005).
- `export_csv` passes every field through `quote_field` from wave 2 (T006).
EOF
} > "$contract"

rewrite "$dir/orchestration.md" 's/^| W0 | P0b T | T002 | `test_quoting.py` |/| W0 | P0b T | T002 | `test_quoting.py`, `check_quoting.py` |/'
rewrite "$dir/orchestration.md" 's/^| W1 | P1b I | T005 | `quoting.py` | `pytest test_quoting.py` |/| W1 | P1b I | T005 | `quoting.py` | `pytest test_quoting.py`; `python check_quoting.py` exits 0 (guard, II-2) |/'
rewrite "$dir/tasks.md" 's/^\(- \[ \] T002 .*\) Done-when:/\1 Also write the guard `check_quoting.py`, II-2'"'"'s rule case by case. Done-when:/'
rewrite "$dir/tasks.md" 's/^- \[ \] T005 .* Done-when: `pytest test_quoting.py` passes$/- [ ] T005 [P] [US1] Write `quote_field` in `quoting.py`: a field with a comma is wrapped in double quotes, a double quote inside it doubled (II-2). Done-when: `pytest test_quoting.py` passes; `python check_quoting.py` exits 0/'
rewrite "$dir/tasks.md" 's/^- \[ \] \(T00[1-3] \)/- [x] \1/'

grep -q 'check_quoting.py` exits 0 (guard, II-2)' "$dir/orchestration.md" || fail "orchestration.md: P1b's row not changed"
grep -q '^- \[x\] T002 .*check_quoting.py' "$dir/tasks.md" || fail "tasks.md: T002 not changed"
grep -q '^- \[ \] T005 .*python check_quoting.py' "$dir/tasks.md" || fail "tasks.md: T005 not changed"
grep -q 'a CR or an LF' "$contract" || fail "contract: II-2 not rewritten"

# Wave W0, committed on the feature branch.
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
"""US1-AC2: a field that contains a comma is quoted (II-2)."""
from quoting import quote_field


def test_a_field_with_a_comma_is_quoted():
    assert quote_field("milk, eggs") == '"milk, eggs"'


def test_a_quote_inside_a_quoted_field_is_doubled():
    assert quote_field('say "hi", then go') == '"say ""hi"", then go"'


def test_a_plain_field_is_unchanged():
    assert quote_field("milk") == "milk"
EOF
cat > "$project/check_quoting.py" <<'EOF'
"""Guard (II-2, FR-003): quote_field follows the contract's quoting rule. Never weaken it."""
import sys

from quoting import quote_field

CASES = [
    ("milk", "milk"),
    ("", ""),
    ("in side", "in side"),
    ("a\tb", "a\tb"),
    ("milk, eggs", '"milk, eggs"'),
    ('say "hi"', '"say ""hi"""'),
    ('"', '""""'),
    ("line one\nline two", '"line one\nline two"'),
    ("cr\rhere", '"cr\rhere"'),
    (" padded", '" padded"'),
    ("padded ", '"padded "'),
    ("\ttab", '"\ttab"'),
    ("tab\t", '"tab\t"'),
    ('x,"y"', '"x,""y"""'),
]


def main():
    failed = 0
    for text, expected in CASES:
        got = quote_field(text)
        if got != expected:
            failed += 1
            print(f"check_quoting: FAIL quote_field({text!r}) returned {got!r}, expected {expected!r}")
    if failed:
        print(f"check_quoting: {failed} of {len(CASES)} cases failed")
        return 1
    print(f"check_quoting: all {len(CASES)} cases pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
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
git -C "$project" add test_export_rows.py test_quoting.py check_quoting.py cli.py
git -C "$project" commit -q -m "feat(004): wave 0 — P0a, P0b, P0c"
sha0=$(git -C "$project" rev-parse --short HEAD)
git -C "$project" push -q origin "$feature"

printf -- '- 2026-10-02 · verify-done · waves W0–W0 (%s..%s) · Verified\n' "$sha0" "$sha0" \
  >> "$dir/validation.md"
git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: wave 0 ticked (T001–T003), verified; II-2 quoting guard"
git -C "$project/specs" push -q origin main
