#!/usr/bin/env bash
# Scaffold for EC-002: a closed feature named in the arguments
# Builds the fixture in the current directory: it is the project (git repository on main, a
# bare local remote standing in for GitHub), with specs/ as its own repository and its own
# bare remote. Helpers: evals/fixtures/. Neutral names only.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$(pwd)"
feature=004-csv-export

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" closed
