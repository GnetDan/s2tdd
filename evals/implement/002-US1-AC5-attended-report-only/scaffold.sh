#!/usr/bin/env bash
# Scaffold for 002-US1-AC5 (attended-report-only).
# Given: an attended run whose shape check finds a test asserting a shape that differs from its
# cited section (as in 002-US1-AC4). The hardened-shapes state (II-16), with T001's task text
# asking P0a's test for CRLF row ends while the section it cites, II-1, says LF; P0c runs at
# medium here, so the attended wave reaches its commit without waiting for the user's read of a
# strong packet's diff.
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

# replace_text <file> <old> <new>: the first occurrence of the literal text <old> becomes <new>
# (awk reads both from the environment, so backslashes stay as written).
replace_text() {
  OLD="$2" NEW="$3" awk '!done && (i = index($0, ENVIRON["OLD"])) {
      $0 = substr($0, 1, i - 1) ENVIRON["NEW"] substr($0, i + length(ENVIRON["OLD"])); done = 1
    } { print }' "$1" > "$1.tmp"
  mv "$1.tmp" "$1"
  grep -qF -- "$3" "$1" || fail "$1: no line holds $2"
}

replace_text "$dir/tasks.md" 'one row per note, per contracts/internal-interfaces.md §II-1.' \
  'one row per note, per contracts/internal-interfaces.md §II-1; every row ends with CRLF (`\r\n`), as spreadsheet apps expect.'
grep -qF 'rows end with LF (`\n`) on every platform' "$dir/contracts/internal-interfaces.md" \
  || fail "contracts/internal-interfaces.md: II-1 no longer says LF"

replace_text "$dir/orchestration.md" '`python cli.py --help` exits 0 and lists `export` | strong |' \
  '`python cli.py --help` exits 0 and lists `export` | medium |'
replace_text "$dir/handoff.md" 'The strong packets, P0c (the dispatcher) and P1a (the MVP), get the full' \
  'The strong packet, P1a (the MVP), gets the full'
if grep '^| W0[^|]*|' "$dir/orchestration.md" | grep -q '| strong |'; then
  fail "orchestration.md: W0 still holds a strong packet"
fi

git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: T001 asks for CRLF row ends; P0c at medium"
git -C "$project/specs" push -q origin main
