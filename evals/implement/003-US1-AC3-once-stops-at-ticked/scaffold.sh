#!/usr/bin/env bash
# Scaffold for 003-US1-AC3 (once-stops-at-ticked).
# Given: a run started with `--nobrakes once`. The per-wave state (II-15): the hardened
# feature with its waves W0-W3 still to run, a handoff.md from harden 0.4.0's prompt text (its
# CONVERGE LOOP included, docs wave W3) and a run-ledger.md with an empty `## Rounds`; the
# project's CLAUDE.md states its per-wave and full test commands. The case's prompt starts the
# run with `--nobrakes once`, so it stops when every task is ticked and runs no converge.
# Builds the fixture in the current directory: it is the project (a git repository on the
# branch 004-csv-export, a bare local remote standing in for GitHub), with specs/ as its own
# repository and its own bare remote. Helpers: evals/fixtures/. Neutral names only.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$(pwd)"
feature=004-csv-export
dir="$project/specs/$feature"

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" per-wave

fail() { echo "scaffold: $*" >&2; exit 1; }

grep -qF 'CONVERGE LOOP (MODE: nobrakes only).' "$dir/handoff.md" \
  || fail "handoff.md has no CONVERGE LOOP: once would not be what stops the run"
grep -q '^- \[ \] T001 ' "$dir/tasks.md" || fail "tasks.md: T001 is already ticked"
grep -q '^## Rounds$' "$dir/run-ledger.md" || fail "run-ledger.md has no Rounds section"
