#!/usr/bin/env bash
# Scaffold for 002-US3-AC3 (reads-every-red-run).
# Given: wave reports for 30 implementation packets. Starts from make-feature.sh's wave-reports
# state (three implementation packets: W0's P0c, W1's P1a and P1b) and adds two waves by the
# same nobrakes relay: W2, one test packet (P2a, T008, test_formats.py: one test per column
# format, contracts II-3), and W3, 27 implementation packets (P3a–P3aa, T009–T035, col_01.py to
# col_27.py), each report quoting its red run before its edits and its green run. 3 + 27 = 30.
# The base state's seeded late red run (P1b) and missing one (P0c) stay among them (SC-003).
# The feature's later waves move up two places (W2 → W4, W3 → W5), as harden would number them.
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

letters=(a b c d e f g h i j k l m n o p q r s t u v w x y z aa)
count=${#letters[@]}  # 27

# insert <file> <before|after> <exact anchor line> <text>
insert() {
  ANCHOR="$3" TEXT="$4" awk -v where="$2" '
    where == "before" && $0 == ENVIRON["ANCHOR"] { print ENVIRON["TEXT"] }
    { print }
    where == "after" && $0 == ENVIRON["ANCHOR"] { print ENVIRON["TEXT"] }
  ' "$1" > "$1.tmp"
  mv "$1.tmp" "$1"
  grep -qxF -- "$3" "$1" || { echo "scaffold: anchor not found in $1: $3" >&2; exit 1; }
}

# ------------------------------------------------------------------ the feature's records

cat >> "$dir/contracts/internal-interfaces.md" <<'EOF'

## II-3. Column formats (`col_<nn>.py`, <nn> 01–27; FR-001)

- `format_col_<nn>(value) -> str`: the column number, a colon, then `str(value)`:
  `format_col_07("milk") == "07:milk"`. One module per column, built in wave 3 (T009–T035).
EOF

orch="$dir/orchestration.md"
sed -e 's/^| W2 green | P2a I | T006 |/| W4 green | P4a I | T006 |/' \
    -e 's/^| W3 docs | P3a I | T007 |/| W5 docs | P5a I | T007 |/' \
    -e 's/P1a (W1) → P2a (W2)/P1a (W1) → P4a (W4)/' \
    -e 's/One slice, s1: W0–W3\./One slice, s1: W0–W5./' \
    "$orch" > "$orch.tmp"
mv "$orch.tmp" "$orch"
rows="| W2 red | P2a T | T008 | \`test_formats.py\` | red: \`col_01.py\` … \`col_27.py\` not found (cites II-3) | medium |"
tasks_new="## Phase 5: Column formats (US1)

- [x] T008 [US1] Write \`test_formats.py\`: one test per column format \`format_col_<nn>\` (01–27), per contracts/internal-interfaces.md §II-3. Done-when: fails for the expected reason: \`col_01.py\` … \`col_27.py\` not found"
for i in $(seq 1 "$count"); do
  nn=$(printf '%02d' "$i")
  task=$(printf 'T%03d' $((8 + i)))
  p="P3${letters[$((i - 1))]}"
  wave="W3"
  if [ "$i" -eq 1 ]; then wave="W3 green"; fi
  rows="$rows
| $wave | $p I | $task | \`col_$nn.py\` | \`pytest test_formats.py -k test_col_$nn\` | cheap |"
  tasks_new="$tasks_new
- [x] $task [P] [US1] Write \`format_col_$nn\` in \`col_$nn.py\` (II-3). Done-when: \`pytest test_formats.py -k test_col_$nn\` passes"
done
insert "$orch" before "| W4 green | P4a I | T006 | \`export.py\` | \`pytest\` | cheap |" "$rows"
insert "$orch" after "| \`test_quoting.py\` | W0 | W1 (T005) | \`quoting.py\` not found |" \
  "| \`test_formats.py\` | W2 | W3 (T009–T035) | \`col_01.py\` … \`col_27.py\` not found |"
insert "$dir/tasks.md" before "## Notes" "$tasks_new
"

sed -e 's/^- Waves: W0–W3$/- Waves: W0–W5/' -e 's/^DOCS WAVE (W3)/DOCS WAVE (W5)/' \
  "$dir/handoff.md" > "$dir/handoff.md.tmp"
mv "$dir/handoff.md.tmp" "$dir/handoff.md"

# ------------------------------------------------------------------ W2: the test packet

{
  printf '"""Column formats (II-3): format_col_<nn> puts the column number before a value."""\n'
  for i in $(seq 1 "$count"); do
    nn=$(printf '%02d' "$i")
    printf '\n\ndef test_col_%s():\n    from col_%s import format_col_%s\n' "$nn" "$nn" "$nn"
    printf '    assert format_col_%s("milk") == "%s:milk"\n' "$nn" "$nn"
  done
} > "$project/test_formats.py"
lines=$(wc -l < "$project/test_formats.py" | tr -d ' ')
git -C "$project" add test_formats.py
git -C "$project" commit -q -m "feat(004): wave 2 — P2a"
sha2=$(git -C "$project" rev-parse --short HEAD)

cat > "$reports/P2a.md" <<EOF
# P2a report (W2, medium, test packet): T008

## Files touched

- test_formats.py +$lines/−0 (new).

## Red run (10:04Z, under 1 min)

\`python -m pytest test_formats.py\`: 27 failed, each ModuleNotFoundError: No module named
'col_<nn>', as T008's done-when expects.

## Cites

Cites: test_col_01 … test_col_27 assert format_col_<nn>'s column prefix → contracts/internal-interfaces.md §II-3

## Test changes, decisions, deviations, open questions

None.
EOF

# ------------------------------------------------------------------ W3: 27 implementation packets

packets=""
for i in $(seq 1 "$count"); do
  nn=$(printf '%02d' "$i")
  task=$(printf 'T%03d' $((8 + i)))
  p="P3${letters[$((i - 1))]}"
  packets="${packets:+$packets, }$p"
  printf '"""The format of column %s (II-3)."""\n\n\ndef format_col_%s(value):\n    return "%s:" + str(value)\n' \
    "$nn" "$nn" "$nn" > "$project/col_$nn.py"
  red=$(printf '10:%02dZ' $((10 + i)))
  edit=$(printf '10:%02dZ' $((11 + i)))
  green=$(printf '10:%02dZ' $((12 + i)))
  cat > "$reports/$p.md" <<EOF
# $p report (W3, cheap): $task

## Files touched

- col_$nn.py +5/−0 (new), written at $edit.

## Red run ($red, before any edit, under 1 min)

\`python -m pytest test_formats.py -k test_col_$nn\`: 1 failed, ModuleNotFoundError: No module
named 'col_$nn'.

## Green run ($green, under 1 min)

\`python -m pytest test_formats.py -k test_col_$nn\`: 1 passed.

## Test changes, decisions, deviations, open questions

None.
EOF
  git -C "$project" add "col_$nn.py"
done
git -C "$project" commit -q -m "feat(004): wave 3 — P3a–P3aa"
sha3=$(git -C "$project" rev-parse --short HEAD)
git -C "$project" push -q origin "$feature"

# ------------------------------------------------------------------ the wave reports

waves="$dir/s1-wave-reports.md"
sed -e 's/^# Wave reports: 004, slice s1 (W0–W3)$/# Wave reports: 004, slice s1 (W0–W5)/' \
  "$waves" > "$waves.tmp"
mv "$waves.tmp" "$waves"
cat >> "$waves" <<EOF

## W2

  Wave: W2  Packets: P2a
  Executed by: subagent per packet (s2tdd:packet-medium ×1); shape check by s2tdd:strong-diff-reviewer
  Files touched: test_formats.py  (preflight: clean)
  Commands run + results: P2a red as expected (27 failed, No module named 'col_<nn>'). Wave end: suite python -m pytest: 5 passed, 27 failed (P2a's tests, expected red until W3)
  Red runs: test_formats.py: 27 failed, No module named 'col_01' … 'col_27'
  Test changes: none
  Decisions: none
  Deviations: none
  Review: shape check: Accept (1 citation, 0 differ)
  Ledger: Usage +1
  Open questions / blocked: none
  Commit: $sha2
  Boundary: context 30% · five-hour 14% · week 42% · BRAKES none · ledger +1 lines

EOF
cat "$reports/P2a.md" >> "$waves"
cat >> "$waves" <<EOF

## W3

  Wave: W3  Packets: $packets
  Executed by: subagent per packet (s2tdd:packet-cheap ×27)
  Files touched: col_01.py … col_27.py  (preflight: clean)
  Commands run + results: each of P3a–P3aa python -m pytest test_formats.py -k test_col_<nn>: 1 passed. Wave end: suite python -m pytest: 32 passed
  Red runs: test_formats.py, red at W2 and again before dispatch: test_col_01 … test_col_27 each failed with No module named 'col_<nn>'
  Test changes: none
  Decisions: none
  Deviations: none
  Review: none; shape check: none
  Ledger: Usage +1
  Open questions / blocked: none
  Commit: $sha3
  Boundary: context 49% · five-hour 21% · week 44% · BRAKES none · ledger +1 lines

EOF
for i in $(seq 1 "$count"); do
  cat "$reports/P3${letters[$((i - 1))]}.md" >> "$waves"
done

ledger="$dir/run-ledger.md"
sed -e 's/ · scope W0–W3 · / · scope W0–W5 · /' "$ledger" > "$ledger.tmp"
mv "$ledger.tmp" "$ledger"
insert "$ledger" after "wave 1 · context 27% · 2 packets" "wave 2 · context 30% · 1 packet
wave 3 · context 49% · 27 packets"

git -C "$specs" add "$feature"
git -C "$specs" commit -q -m "004: waves 2–3 ticked (T008–T035); s1 wave reports"
git -C "$specs" push -q origin main
