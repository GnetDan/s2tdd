#!/usr/bin/env bash
# Scaffold for 002-US5-AC4 (no-rereads).
# Given: a wave in progress whose packets need rules, rows and tasks the orchestrator has
# already read. The hardened-shapes state (II-16): wave W0 holds three packets (P0a, P0b test
# packets; P0c the dispatcher), so the orchestrator briefs three packets, confirms two reds,
# dispatches the shape check, then ticks T001-T003 and commits, each step needing the ground
# rules, W0's rows or its tasks again. P0c runs at medium here, so the attended wave reaches its
# commit without waiting for the user's read of a strong packet's diff. run-ledger.md's
# Amendments stay empty: no section changes during the wave.
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

rewrite "$dir/orchestration.md" '/^| W0 | P0c I /s/| strong |$/| medium |/'
rewrite "$dir/handoff.md" 's/The strong packets, P0c (the dispatcher) and P1a (the MVP), get the full/The strong packet, P1a (the MVP), gets the full/'
if grep '^| W0[^|]*|' "$dir/orchestration.md" | grep -q '| strong |'; then
  fail "orchestration.md: W0 still holds a strong packet"
fi
grep -q 'The strong packet, P1a (the MVP), gets the full' "$dir/handoff.md" \
  || fail "handoff.md: TIER still names P0c as strong"

git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: P0c at medium"
git -C "$project/specs" push -q origin main
