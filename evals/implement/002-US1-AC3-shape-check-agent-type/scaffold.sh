#!/usr/bin/env bash
# Scaffold for 002-US1-AC3 (shape-check-agent-type).
# Given: an implement run (here --nobrakes; 002-US1-AC1 runs attended) whose wave W0 holds test
# packets, so its shape check is due. The hardened-shapes state (II-16) as it stands: W0 holds
# the test packets P0a and P0b and the strong packet P0c; handoff.md carries SHAPE CHECK and the
# Shape check brief; run-ledger.md has an empty Lease.
# Builds the fixture in the current directory: it is the project (a git repository on the
# branch 004-csv-export, a bare local remote standing in for GitHub), with specs/ as its own
# repository and its own bare remote. Helpers: evals/fixtures/. Neutral names only.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$(pwd)"

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" hardened-shapes
