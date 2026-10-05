#!/usr/bin/env bash
# Scaffold for 002-EC-004: a --nobrakes run in a harness with no usage tool
# Builds the fixture in the current directory: it is the project (git repository, a bare local
# remote standing in for GitHub), with specs/ as its own repository and its own bare remote.
# Helpers: evals/fixtures/. Neutral names only.
# The harness is the Given: claude -p, which runs the eval, has no usage tool (orchestration
# J-10), standing in for Cursor. A hardened feature no run has touched; the run commits wave 0.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$(pwd)"
feature=004-csv-export
dir="$project/specs/$feature"

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" hardened-shapes
