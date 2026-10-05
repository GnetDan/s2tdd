#!/usr/bin/env bash
# Scaffold for EC-005 (no-budget).
# Given: no suite-time budget in the project's guidance file; a suite run recorded without one.
# Builds ./acme-notes in the current directory, with its bare remotes beside it in ./remotes.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$PWD/acme-notes"

bash "$fixtures/make-project.sh" "$project" acme
git -C "$project" config github.user acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" hardened

# The guidance file states no budget; the latest verification-log line records a suite run
# without one (what verify-done and converge append, II-12).
printf '# acme-notes\n\nA small notes app. Run the tests with pytest.\n' > "$project/CLAUDE.md"

git -C "$project" add -- CLAUDE.md
git -C "$project" commit -q -m "docs: add the guidance file"
git -C "$project" push -q origin 004-csv-export

printf -- '- 2026-10-02 · verify-done · waves W1–W1 (1a2b3c4..1a2b3c4) · Verified · suite 7m12s (no budget)\n' \
  >> "$project/specs/004-csv-export/validation.md"

git -C "$project/specs" add -A
git -C "$project/specs" commit -q -m "feat(004): record a suite run"
git -C "$project/specs" push -q origin main
