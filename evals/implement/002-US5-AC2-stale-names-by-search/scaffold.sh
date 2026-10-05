#!/usr/bin/env bash
# Scaffold for 002-US5-AC2 (stale-names-by-search).
# Given: implement's check for stale names, on a feature whose orchestration.md still names an
# old command. The hardened-shapes state (II-16), a full-size orchestration.md and handoff.md,
# with one line of orchestration.md carried over from the preset: "Regenerate it with" names the
# old harden command. handoff.md stays clean. Committed and pushed in the specs repository.
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
bash "$fixtures/make-feature.sh" "$project" hardened-shapes

old="/speckit-harden"
text=$(sed -e "s#^Regenerate it with \`/s2tdd-harden\`\.#Regenerate it with \`$old\`.#" "$dir/orchestration.md")
printf '%s\n' "$text" > "$dir/orchestration.md"
grep -q -- "$old" "$dir/orchestration.md" || { echo "scaffold: no old name written" >&2; exit 1; }

git -C "$project/specs" add "$feature/orchestration.md"
git -C "$project/specs" commit -q -m "004: orchestration.md carried over from the preset"
git -C "$project/specs" push -q origin main
