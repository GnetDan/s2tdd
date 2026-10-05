#!/usr/bin/env bash
# Scaffold for 003-US3-AC1 (converge-reuses-green-run).
# Given: a green full run recorded at commit X and a clean tree at X. make-feature.sh's green-run
# state as it stands: one `nobrakes once` relay committed W0-W3 (every task ticked, every wave
# verified) and released the lease `done`; the user's verify-done over W0-W3 then ran the full
# suite green, and its verification-log line ends ` · green at <sha>`, <sha> the project's HEAD
# (short), with the project's tree clean.
# Builds the project in the current directory (on branch 004-csv-export, with a bare local
# remote beside it standing in for GitHub), with specs/ as its own repository and its own bare
# remote. Helpers: evals/fixtures/. Neutral names only.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$(pwd)"

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" green-run
