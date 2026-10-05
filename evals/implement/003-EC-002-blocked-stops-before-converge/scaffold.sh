#!/usr/bin/env bash
# Scaffold for 003-EC-002 (blocked-stops-before-converge).
# Given: a nobrakes run that ends its waves with a blocked packet that is neither the MVP nor a
# guard test's. The per-wave state (II-15), with handoff.md's docs wave set to none (as the
# looping states have it), so W3 is an ordinary wave. Relay 1 of run nb-20261003-0900 (scope
# W0-W3) ran every wave: W0 committed; in W1, P1a (the MVP) committed and P1b (T005,
# `quoting.py`, cheap) failed its fence three times and is BLOCKED; W2's only packet, P2a (T006),
# passes fields through T005's `quote_field`, so it was skipped as P1b's dependent; W3 (T007, the
# README) committed. At W3's boundary relay 1 found BRAKES and handed off (`handed off by relay
# 1 (brakes)`), and the user then ran verify-done over W2-W3. No wave is left: the relay this
# case starts resumes at converge (round 1), and must stop before it.
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

exclude="$project/.git/info/exclude"
grep -qx '.sdd-run/' "$exclude" 2>/dev/null || printf '.sdd-run/\n' >> "$exclude"

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
grep -qF 'CONVERGE LOOP (MODE: nobrakes only).' "$dir/handoff.md" || fail "handoff.md: no CONVERGE LOOP"

# No docs wave in this run; relay 1's handoff left SCOPE at converge.
replace_text "$dir/handoff.md" 'DOCS WAVE (W3)' 'DOCS WAVE (none)'
replace_text "$dir/handoff.md" '  (W3). If it still stops' '  (none). If it still stops'
if grep -qF '(W3)' "$dir/handoff.md"; then fail "handoff.md still names a docs wave"; fi
replace_text "$dir/handoff.md" '- RESUME AT: wave 0' '- RESUME AT: converge (round 1)'
replace_text "$dir/handoff.md" '- MODE: attended' '- MODE: nobrakes'

# Relay 1's waves. W0: the two test files and the dispatcher.
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

# W1: P1a's export.py only; P1b is blocked, so quoting.py was never committed.
cat > "$project/export.py" <<'EOF'
"""CSV export of a notebook (II-1)."""

HEADER = ("id", "title", "text")


def export_csv(notes):
    """The notebook as CSV text: a header row, then one row per note, every row ending in LF."""
    rows = [",".join(HEADER)]
    rows += [",".join(str(note[key]) for key in HEADER) for note in notes]
    return "\n".join(rows) + "\n"
EOF
git -C "$project" add export.py
git -C "$project" commit -q -m "feat(004): wave 1 — P1a (P1b blocked)"
sha1=$(git -C "$project" rev-parse --short HEAD)

# W2: P2a skipped, so no commit. W3: the README.
cat >> "$project/README.md" <<'EOF'

## Export

`python cli.py export --csv notes.csv` writes the notebook to `notes.csv`: a header row
`id,title,text`, then one row per note; a field holding a comma or a double quote is quoted.
EOF
git -C "$project" add README.md
git -C "$project" commit -q -m "feat(004): wave 3 — P3a"
sha3=$(git -C "$project" rev-parse --short HEAD)
git -C "$project" push -q origin "$feature"
[ -z "$(git -C "$project" status --porcelain)" ] || fail "the project's tree is not clean"

# The specs repository: ticks, wave reports, verify-done lines and relay 1's ledger.
ticked=$(sed -e 's/^- \[ \] \(T00[1-4] \)/- [x] \1/' -e 's/^- \[ \] \(T007 \)/- [x] \1/' "$dir/tasks.md")
printf '%s\n' "$ticked" > "$dir/tasks.md"
grep -q '^- \[ \] T005 ' "$dir/tasks.md" && grep -q '^- \[ \] T006 ' "$dir/tasks.md" \
  || fail "tasks.md: T005 and T006 should stay unticked"

cat > "$dir/s1-wave-reports.md" <<EOF
# Wave reports: 004, slice s1 (W0–W3)

Written by the orchestrator of nobrakes run nb-20261003-0900, relay 1. Each wave report is
followed by its packets' report files.

## W0

  Wave: W0  Packets: P0a, P0b, P0c
  Executed by: subagent per packet (s2tdd:packet-medium ×2, s2tdd:packet-strong ×1); shape check and P0c's review by s2tdd:strong-diff-reviewer
  Files touched: test_export_rows.py, test_quoting.py, cli.py  (preflight: clean)
  Commands run + results: P0a red as expected (No module named 'export'); P0b red as expected (No module named 'quoting'); P0c python cli.py --help exit 0
  Test run: per-wave · $per_wave · 0 passed, 2 failed, 2 selected · 0m01s (expected red until W1)
  Review: P0c: Accept; shape check: Accept (3 citations, 0 differ)
  Commit: $sha0
  Boundary: context 18% · five-hour 12% · week 41% · BRAKES none · ledger +1 lines

## W1

  Wave: W1  Packets: P1a, P1b
  Executed by: subagent per packet (s2tdd:packet-strong ×1, s2tdd:packet-cheap ×2, s2tdd:packet-medium ×1 for P1b's third attempt)
  Files touched: export.py  (preflight: clean)
  Commands run + results: P1a python -m pytest test_export_rows.py 2 passed; P1b python -m pytest test_quoting.py 1 failed, 2 passed (three attempts)
  Test run: per-wave · $per_wave · 2 passed, 1 failed, 3 selected · 0m01s (test_quoting.py: expected red until T005)
  Open questions / blocked: P1b (T005) BLOCKED after its third attempt; P2a (T006) skipped
  Review: P1a: Accept; shape check: none
  Commit: $sha1
  Boundary: context 31% · five-hour 20% · week 43% · BRAKES none · ledger +4 lines

## W2

  Wave: W2  Packets: none (P2a skipped: depends on blocked P1b)
  Commit: none
  Boundary: context 31% · five-hour 20% · week 43% · BRAKES none · ledger +1 lines

## W3

  Wave: W3  Packets: P3a
  Executed by: subagent per packet (s2tdd:packet-cheap ×1)
  Files touched: README.md  (preflight: clean)
  Commands run + results: P3a the README names the flag
  Test run: full (changed README.md outside Per-wave sees) · python -m pytest · 2 passed, 1 failed · 0m02s (test_quoting.py: expected red until T005)
  Review: shape check: none
  Commit: $sha3
  Boundary: context 36% · five-hour 24% · week 44% · BRAKES found · ledger +2 lines
EOF

printf -- '- 2026-10-03 · verify-done · waves W0–W1 (%s..%s) · Verified · proxy · suite 0m02s (no budget)\n' \
  "$sha0" "$sha1" >> "$dir/validation.md"

cat > "$dir/run-ledger.md" <<EOF
# Run ledger: 004 CSV export

Running state of the implementing sessions (orchestration.md ground rules 2, 14–17; handoff.md
NOBRAKES). One line per item, added when it happens; never rewritten. Frozen at close-out.

## Lease
session-1, relay 1, since 2026-10-03T09:00Z
handed off by relay 1 (brakes)
## Runs
run nb-20261003-0900 · nobrakes · scope W0–W3 · started 2026-10-03T09:00Z
## Rounds
## Usage
wave 0 · context 18% · 3 packets
wave 1 · context 31% · 2 packets
wave 2 · context 31% · 0 packets
wave 3 · context 36% · 1 packets
## Carried constraints
Usage limits: week 95%, five-hour 90% (default)
## Amendments
## Test-owner fixes
## Ownership exceptions
## Expected red
Expected red until T005: test_quoting.py — P1b (T005) is blocked, so quoting.py is not built
## Blocked and skipped
BLOCKED P1b (T005): fence failed three times — python -m pytest test_quoting.py: test_a_quote_inside_a_quoted_field_is_doubled failed; its quoting.py was left out of the W1 commit
skipped P2a (T006): passes every field through II-2's quote_field, which T005 builds
## Open review notes
## Pending checkpoints
## Tags and pushes
004-s1a · waves W0–W1 · Verified · verified by proxy (nobrakes) · app $sha1 · pushed app ok, specs ok
## Processes killed
## Handoff
/s2tdd-implement --nobrakes
Context:
- Relay 2 of nobrakes run nb-20261003-0900 (scope W0–W3). The run's state is in
  specs/004-csv-export/run-ledger.md: read it before any dispatch.
- Carried constraints: see specs/004-csv-export/run-ledger.md; this prompt restates none of them.
- Expect: acme/acme-notes 004-csv-export at $sha3, clean except the docs wave's files the ledger
  names; specs HEAD is the commit \`004: relay 1 handoff\` or a later verify-done commit; every
  wave has a verify-done line in validation.md; the newest Rounds line is none; the newest
  Lease line is \`handed off by relay 1 (brakes)\`.
- RESUME AT: converge (round 1). If anything does not match, print the RUN SUMMARY from the
  ledger and stop without work or writes.
EOF

git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: relay 1 handoff"
# After the brakes handoff, the user ran /s2tdd-verify-done over the unverified waves.
printf -- '- 2026-10-03 · verify-done · waves W2–W3 (%s..%s) · Verified · suite 0m02s (no budget)\n' \
  "$sha3" "$sha3" >> "$dir/validation.md"
git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: verify-done waves W2–W3 (Verified)"
git -C "$project/specs" push -q origin main
