#!/usr/bin/env bash
# Scaffold for 002-US3-AC2 (missing-red-run-gap).
# Given: an implementation packet report that quotes no red run, and the wave report shows the
# orchestrator saw the test red before dispatch. make-feature.sh's wave-reports state as it
# stands: W0's P0c (T003) report quotes no red run, and W0's wave report's Red runs line shows
# `python cli.py --help` failing before dispatch. The same state seeds a late red run too (W1's
# P1b, T005: red run at 09:48Z, after quoting.py was written at 09:44Z), so the case also checks
# that both are reported (SC-003).
# Builds the project in the current directory (on branch 004-csv-export, with a bare local
# remote beside it standing in for GitHub), with specs/ as its own repository and its own bare
# remote. Helpers: evals/fixtures/. Neutral names only.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$(pwd)"

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" wave-reports
