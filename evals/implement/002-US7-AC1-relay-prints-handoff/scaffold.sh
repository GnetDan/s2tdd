#!/usr/bin/env bash
# Scaffold for 002-US7-AC1: a relay that reaches its handoff
# Builds the fixture in the current directory: it is the project (git repository, a bare local
# remote standing in for GitHub), with specs/ as its own repository and its own bare remote.
# Helpers: evals/fixtures/. Neutral names only.
# Waves W0 and W1 are committed by an earlier run, whose relay released the lease; this run
# (W2-W3) starts with .sdd-run/004/BRAKES present, so its relay hands off at its first wave
# boundary (handoff.md, BRAKES: HANDOFF steps 2-3, then print and stop).
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$(pwd)"
feature=004-csv-export
dir="$project/specs/$feature"

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" wave-reports

# The earlier run (W0 and W1) ended: relay 1 released the lease, so a new run may take it.
ledger="$dir/run-ledger.md"
awk '{ print } /^session-1, relay 1, since / { print "released by relay 1: stopped: the user ended the run after W1" }' \
  "$ledger" > "$ledger.tmp"
mv "$ledger.tmp" "$ledger"
grep -q '^released by relay 1: ' "$ledger"

git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: lease released by relay 1"
git -C "$project/specs" push -q origin main

# BRAKES: the file the relay checks at every wave boundary (handoff.md, NOBRAKES), so this relay
# reaches its handoff. claude -p has no usage tool, so no window can trigger one.
mkdir -p "$project/.sdd-run/004"
: > "$project/.sdd-run/004/BRAKES"
