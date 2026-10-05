#!/usr/bin/env bash
# Scaffold for 003-US3-AC3 (no-reuse-past-the-run).
# Given: a green full run recorded at commit X, and HEAD past X. Starts from make-feature.sh's
# green-run state (the user's verify-done line ends ` · green at X`, X the HEAD it leaves), then
# commits one more change to the project after that run: export.py names its delimiter
# (refactor(004): name the CSV delimiter). The tree stays clean, so only HEAD has moved. The case
# runs converge; close's half of the scenario is pinned by a text test
# (tests/commands/test_full_runs.py).
# Builds the project in the current directory (on branch 004-csv-export, with a bare local
# remote beside it standing in for GitHub), with specs/ as its own repository and its own bare
# remote. Helpers: evals/fixtures/. Neutral names only.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$(pwd)"
feature=004-csv-export

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" green-run

# A commit past the green run: the same rows, the delimiter named once.
renamed=$(awk '/^HEADER = /{print "DELIMITER = \",\""} {gsub(/","\.join\(/, "DELIMITER.join("); print}' \
  "$project/export.py")
printf '%s\n' "$renamed" > "$project/export.py"
git -C "$project" add export.py
git -C "$project" commit -q -m "refactor(004): name the CSV delimiter"
git -C "$project" push -q origin "$feature"
