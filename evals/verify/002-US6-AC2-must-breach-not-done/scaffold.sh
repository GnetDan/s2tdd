#!/usr/bin/env bash
# Scaffold for 002-US6-AC2 (must-breach-not-done).
# Given: verify-done finds a committed change that breaks a spec MUST. Starts from
# make-feature.sh's wave-reports state and adds wave W2 by the same nobrakes relay: P2a (T006)
# adds write_csv and passes every field through quote_field, as T006 says, and also leaves out
# every note whose text is empty, which breaks FR-001 ("The system MUST write notes to CSV with
# one row per note"). The suite stays green (no test has a note without text), P2a's report
# quotes its red run before its edits and its green run, and W2's wave report raises no MUST
# finding (a cheap packet: no strong-diff review), so only the diff against spec.md shows it.
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
bash "$fixtures/make-feature.sh" "$project" wave-reports

# W2: P2a (T006) in export.py.
cat > "$project/export.py" <<'EOF'
"""CSV export of a notebook (II-1, II-2)."""
import json

from quoting import quote_field

HEADER = ("id", "title", "text")


def export_csv(notes):
    """The notebook as CSV text: a header row, then one row per note, every row ending in LF.
    Every field goes through quote_field. Blank notes (no text) are left out."""
    rows = [",".join(HEADER)]
    rows += [",".join(quote_field(str(note[key])) for key in HEADER)
             for note in notes if note.get("text")]
    return "\n".join(rows) + "\n"


def write_csv(path):
    """Read the notebook (notes.json in the working directory) and write it to path as CSV."""
    with open("notes.json", encoding="utf-8") as source:
        notes = json.load(source)
    with open(path, "w", encoding="utf-8", newline="") as target:
        target.write(export_csv(notes))
    return 0
EOF
git -C "$project" add export.py
git -C "$project" commit -q -m "feat(004): wave 2 — P2a"
sha2=$(git -C "$project" rev-parse --short HEAD)
git -C "$project" push -q origin "$feature"

cat > "$reports/P2a.md" <<'EOF'
# P2a report (W2, cheap): T006

## Files touched

- export.py +17/−3.

## Red run (10:12Z, before any edit, under 1 min)

`python -c "from export import write_csv"`: ImportError: cannot import name 'write_csv' from
'export'.

## Green run (10:16Z, under 1 min)

`python -c "from export import write_csv"`: exit 0. `python -m pytest`: 5 passed.

## Test changes, decisions, deviations, open questions

None.
EOF

waves="$dir/s1-wave-reports.md"
cat >> "$waves" <<EOF

## W2

  Wave: W2  Packets: P2a
  Executed by: subagent per packet (s2tdd:packet-cheap ×1)
  Files touched: export.py  (preflight: clean)
  Commands run + results: P2a python -c "from export import write_csv" exit 0; python -m pytest 5 passed. Wave end: suite python -m pytest: 5 passed
  Red runs: P2a: python -c "from export import write_csv" failed with ImportError (cannot import name 'write_csv') before dispatch
  Test changes: none
  Decisions: none
  Deviations: none
  Review: none; shape check: none
  Ledger: Usage +1
  Open questions / blocked: none
  Commit: $sha2
  Boundary: context 33% · five-hour 15% · week 42% · BRAKES none · ledger +1 lines

EOF
cat "$reports/P2a.md" >> "$waves"

ticked=$(sed -e 's/^- \[ \] \(T006 \)/- [x] \1/' "$dir/tasks.md")
printf '%s\n' "$ticked" > "$dir/tasks.md"

ledger="$dir/run-ledger.md"
ANCHOR="wave 1 · context 27% · 2 packets" awk '
  { print }
  $0 == ENVIRON["ANCHOR"] { print "wave 2 · context 33% · 1 packet" }
' "$ledger" > "$ledger.tmp"
mv "$ledger.tmp" "$ledger"

git -C "$specs" add "$feature"
git -C "$specs" commit -q -m "004: wave 2 ticked (T006); s1 wave reports"
git -C "$specs" push -q origin main
