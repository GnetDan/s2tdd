#!/usr/bin/env bash
# Scaffold for 002-US13-AC2 (missing-boundary-gap).
# Given: a wave report with no boundary record. make-feature.sh's wave-reports state as it
# stands: waves W0 and W1 committed by one nobrakes relay (run-ledger.md's Runs and Lease cover
# both), W0's wave report carrying its Boundary: line and W1's carrying none.
# Builds the project in the current directory (on branch 004-csv-export, with a bare local
# remote beside it standing in for GitHub), with specs/ as its own repository and its own bare
# remote. Helpers: evals/fixtures/. Neutral names only.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$(pwd)"

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" wave-reports
