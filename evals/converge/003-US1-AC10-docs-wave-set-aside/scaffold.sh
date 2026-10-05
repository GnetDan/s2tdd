#!/usr/bin/env bash
# Scaffold for 003-US1-AC10 (docs-wave-set-aside).
# Given: a ledger recording the docs wave as built and uncommitted. make-feature.sh's docs-wave
# state as it stands: one `nobrakes once` relay committed W0-W2 and released the lease `done`;
# handoff.md names DOCS WAVE (W3); W3's task T007 (document `export --csv` in README.md) is
# unticked, README.md is changed and uncommitted in the project, and run-ledger.md says
# `Docs wave 3 built, uncommitted: README.md` under Blocked and skipped. Every other task is
# ticked and verified. The case runs converge by hand; the loop's converger reads the same guard.
# Builds the project in the current directory (on branch 004-csv-export, with a bare local
# remote beside it standing in for GitHub), with specs/ as its own repository and its own bare
# remote. Helpers: evals/fixtures/. Neutral names only.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$(pwd)"

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" docs-wave
