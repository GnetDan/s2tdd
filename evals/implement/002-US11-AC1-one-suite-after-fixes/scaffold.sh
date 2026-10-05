#!/usr/bin/env bash
# Scaffold for 002-US11-AC1 (one-suite-after-fixes).
# Given: a wave whose review asks for fixes. The hardened-shapes state (II-16), wave W0 not yet
# run, with T001's task text asking P0a's test for CRLF row ends while the section it cites,
# II-1, says rows end with LF on every platform: W0's shape check finds the test differing from
# its cited section and asks for a fix before the wave commit.
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

# rewrite <file> <sed script>: portable in-place sed (no -i). A backslash meant literally in the
# replacement is doubled: sed reads `\r` and `\n` there as CR and newline.
rewrite() {
  local text
  text=$(sed -e "$2" "$1")
  printf '%s\n' "$text" > "$1"
}

rewrite "$dir/tasks.md" '/^- \[ \] T001 /s@one row per note, per contracts/internal-interfaces.md §II-1\.@one row per note, per contracts/internal-interfaces.md §II-1; every row ends with CRLF (`\\r\\n`), as spreadsheet apps expect.@'
grep -qF 'every row ends with CRLF (`\r\n`)' "$dir/tasks.md" || fail "tasks.md: T001 does not ask for CRLF"
grep -qF 'rows end with LF (`\n`) on every platform' "$dir/contracts/internal-interfaces.md" \
  || fail "contracts/internal-interfaces.md: II-1 no longer says LF"

git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: T001 asks for CRLF row ends"
git -C "$project/specs" push -q origin main
