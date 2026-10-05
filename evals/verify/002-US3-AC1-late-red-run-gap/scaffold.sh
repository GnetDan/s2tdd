#!/usr/bin/env bash
# Scaffold for 002-US3-AC1 (late-red-run-gap).
# Given: an implementation packet report that says its red run happened after it wrote its
# implementation files, and the orchestrator's check before dispatch saw the test red.
# make-feature.sh's wave-reports state as it stands: W1's P1b (T005) wrote quoting.py at 09:44Z
# and took its red run at 09:48Z, while W1's wave report shows test_quoting.py red before
# dispatch. The same state seeds a missing red run too (W0's P0c, T003: its report quotes none,
# its wave report's Red runs line shows the check red before dispatch), so the case also checks
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
