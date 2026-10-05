#!/usr/bin/env bash
# Scaffold for 002-US14-AC1: a verify gate
# Builds the fixture in the current directory: it is the project (git repository, a bare local
# remote standing in for GitHub), with specs/ as its own repository and its own bare remote.
# Helpers: evals/fixtures/. Neutral names only.
# Waves W0 and W1 are committed by an earlier run, whose relay released the lease, with no
# verify-done line yet. This run builds W2 and the docs wave W3, the end of slice s1, so a gate
# covers W0-W2: orchestration.md's expected-red rows (test_export_rows.py, test_quoting.py, red
# from W0, green at W1) and W0's accepted Decision (P0c's, CONFIRMED in its wave report).
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
