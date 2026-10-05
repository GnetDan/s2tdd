#!/usr/bin/env bash
# Scaffold for 003-US3-AC2 (close-reuses-green-run).
# Given: a green full run recorded at commit X and a clean tree at X. Starts from make-feature.sh's
# green-run state (every task ticked; the user's verify-done line over W0-W3 ends
# ` · green at X`, X the project's HEAD; the tree clean), and adds what close's other gates need
# so that it reaches its suite gate: a converged converge at X (it reused the same run) and a
# pr-review line at X. Nothing in the project changes, so X stays HEAD and the tree stays clean.
# Builds the project in the current directory (on branch 004-csv-export, with a bare local
# remote beside it standing in for GitHub), with specs/ as its own repository and its own bare
# remote. Helpers: evals/fixtures/. Neutral names only.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$(pwd)"
feature=004-csv-export
specs="$project/specs"
dir="$specs/$feature"

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" green-run

head=$(git -C "$project" rev-parse --short HEAD)
printf -- '- 2026-10-03 · converge · at %s · converged · suite reused (green at %s)\n' \
  "$head" "$head" >> "$dir/validation.md"
printf -- '- 2026-10-03 · pr-review · #1 at %s · report · 0 confirmed, 0 fixable\n' \
  "$head" >> "$dir/validation.md"
git -C "$specs" add "$feature"
git -C "$specs" commit -q -m "004: converged at $head; PR #1 reviewed"
git -C "$specs" push -q origin main
