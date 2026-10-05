#!/usr/bin/env bash
# Scaffold for 002-US1-AC6 (strong-review-kept).
# Given: a wave with strong packets and test packets. The hardened-shapes state (II-16) as it
# stands: wave W0 holds the test packets P0a and P0b and the strong packet P0c (the dispatcher);
# handoff.md carries STRONG-DIFF REVIEW, SHAPE CHECK and both briefs; run-ledger.md has an empty
# Lease, so a --nobrakes run can take it.
# Builds the fixture in the current directory: it is the project (a git repository on the
# branch 004-csv-export, a bare local remote standing in for GitHub), with specs/ as its own
# repository and its own bare remote. Helpers: evals/fixtures/. Neutral names only.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$(pwd)"
dir="$project/specs/004-csv-export"

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" hardened-shapes

grep -q '^| W0 | P0c I | T003 | .* | strong |$' "$dir/orchestration.md" \
  || { echo "scaffold: orchestration.md: P0c is not W0's strong packet" >&2; exit 1; }
