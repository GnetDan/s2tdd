#!/usr/bin/env bash
# Scaffold for 003-US1-AC11 (close-needs-docs-commit).
# Given: a docs wave still uncommitted. make-feature.sh's docs-wave state as it stands: one
# `nobrakes once` relay committed W0-W2 and released the lease `done`; handoff.md names
# DOCS WAVE (W3); W3's task T007 is unticked, its file README.md is changed and uncommitted in
# the project, and run-ledger.md says `Docs wave 3 built, uncommitted: README.md` under Blocked
# and skipped. README.md is documentation, not application code: close's preamble step 3
# (uncommitted application code) must not fire for it, so the run reaches A0's docs-wave gate.
# Builds the project in the current directory (on branch 004-csv-export, with a bare local
# remote beside it standing in for GitHub), with specs/ as its own repository and its own bare
# remote. Helpers: evals/fixtures/. Neutral names only.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$(pwd)"

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" docs-wave
