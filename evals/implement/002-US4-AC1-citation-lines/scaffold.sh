#!/usr/bin/env bash
# Scaffold for 002-US4-AC1 (citation-lines).
# Given: test packets whose tests assert shapes a later wave implements. The hardened-shapes
# state (II-16) as it stands: wave W0's test packets P0a (T001, test_export_rows.py) and P0b
# (T002, test_quoting.py) assert export_csv's rows (contracts/internal-interfaces.md §II-1) and
# quote_field's quoting (§II-2), which wave W1 builds (P1a, P1b). T001 names its section; T002 names
# none, so P0b's citation comes from the packet's own reading of the contract.
# Builds the fixture in the current directory: it is the project (a git repository on the
# branch 004-csv-export, a bare local remote standing in for GitHub), with specs/ as its own
# repository and its own bare remote. Helpers: evals/fixtures/. Neutral names only.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$(pwd)"

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" hardened-shapes
