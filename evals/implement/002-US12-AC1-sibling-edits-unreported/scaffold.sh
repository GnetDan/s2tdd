#!/usr/bin/env bash
# Scaffold for 002-US12-AC1 (sibling-edits-unreported).
# Given: a packet whose working tree shows a sibling's edits. The hardened-shapes state (II-16),
# no wave run yet: wave W0 holds three parallel packets in one tree, P0a (test_export_rows.py),
# P0b (test_quoting.py) and P0c (cli.py), so each packet's working tree shows the files its
# siblings write.
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

fail() { echo "scaffold: $*" >&2; exit 1; }

# The three W0 packets own disjoint files and run in parallel.
rows=$(grep '^| W0 ' "$dir/orchestration.md")
for owned in test_export_rows.py test_quoting.py cli.py; do
  printf '%s\n' "$rows" | grep -q "\`$owned\`" || fail "orchestration.md: no W0 packet owns $owned"
done
