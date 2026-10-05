#!/usr/bin/env bash
# Scaffold for 002-US1-AC4 (nobrakes-fix-before-commit).
# Given: a --nobrakes run whose shape check finds a test asserting a shape that differs from its
# cited section. The hardened-shapes state (II-16), with T001's task text asking P0a's test for
# CRLF row ends while the section it cites, II-1, says rows end with LF on every platform: the
# test P0a writes from its task differs from its cited section.
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
}

replace_text "$dir/tasks.md" 'one row per note, per contracts/internal-interfaces.md §II-1.' \
  'one row per note, per contracts/internal-interfaces.md §II-1; every row ends with CRLF (`\r\n`), as spreadsheet apps expect.'
grep -qF 'every row ends with CRLF (`\r\n`)' "$dir/tasks.md" || fail "tasks.md: T001 does not ask for CRLF"
grep -qF 'rows end with LF (`\n`) on every platform' "$dir/contracts/internal-interfaces.md" \
  || fail "contracts/internal-interfaces.md: II-1 no longer says LF"

git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: T001 asks for CRLF row ends"
git -C "$project/specs" push -q origin main
