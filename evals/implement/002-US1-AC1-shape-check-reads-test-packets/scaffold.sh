#!/usr/bin/env bash
# Scaffold for 002-US1-AC1 (shape-check-reads-test-packets).
# Given: a wave with three test packets. The hardened-shapes state (II-16), whose wave W0 holds
# P0a and P0b, gains a third test packet P0d (T008, test_write_csv.py, citing II-1); P0c runs at
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

# insert_after <file> <ERE> <line>: the line goes after the first line matching the ERE.
insert_after() {
  PAT="$2" LINE="$3" awk '{ print } !done && $0 ~ ENVIRON["PAT"] { print ENVIRON["LINE"]; done = 1 }' \
    "$1" > "$1.tmp"
  mv "$1.tmp" "$1"
  grep -qF -- "$3" "$1" || fail "$1: no line matches $2"
}

# rewrite <file> <sed script>: portable in-place sed (no -i).
rewrite() {
  local text
  text=$(sed -e "$2" "$1")
  printf '%s\n' "$text" > "$1"
}

insert_after "$dir/tasks.md" '^- \[ \] T002 ' \
  '- [ ] T008 [P] [US1] Write `test_write_csv.py` for US1-AC1'"'"'s file: `write_csv(path)` writes `export_csv`'"'"'s text to `path` as UTF-8 and returns 0, per contracts/internal-interfaces.md §II-1. Done-when: fails for the expected reason: `export.py` not found'
insert_after "$dir/orchestration.md" '^\| W0 \| P0b T ' \
  '| W0 | P0d T | T008 | `test_write_csv.py` | red: `export.py` not found (cites II-1) | medium |'
insert_after "$dir/orchestration.md" '^\| `test_quoting.py` \|' \
  '| `test_write_csv.py` | W0 | W2 (T006) | `export.py` not found |'

rewrite "$dir/orchestration.md" '/^| W0 | P0c I /s/| strong |$/| medium |/'
rewrite "$dir/handoff.md" 's/The strong packets, P0c (the dispatcher) and P1a (the MVP), get the full/The strong packet, P1a (the MVP), gets the full/'
if grep '^| W0[^|]*|' "$dir/orchestration.md" | grep -q '| strong |'; then
  fail "orchestration.md: W0 still holds a strong packet"
fi
grep -q 'The strong packet, P1a (the MVP), gets the full' "$dir/handoff.md" \
  || fail "handoff.md: TIER still names P0c as strong"
[ "$(grep -c '^| W0[^|]*| P0[a-z] T ' "$dir/orchestration.md")" -eq 3 ] \
  || fail "orchestration.md: W0 does not hold three test packets"

git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: W0 holds three test packets (P0a, P0b, P0d)"
git -C "$project/specs" push -q origin main
