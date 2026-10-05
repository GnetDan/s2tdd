#!/usr/bin/env bash
# Scaffold for 002-US6-AC4: a review finding that a packet breaks a spec MUST, in an attended run
# Builds the fixture in the current directory: it is the project (git repository, a bare local
# remote standing in for GitHub), with specs/ as its own repository and its own bare remote.
# Helpers: evals/fixtures/. Neutral names only.
# The Given is seeded, not scripted: spec FR-002 (a MUST) and contract II-2 quote a field with
# a line break, README.md's invariants say so, and T002 (test packet P0b, wave 0) asks
# test_quoting.py to assert such a field comes back unquoted, so wave 0's shape check finds a
# MUST breach. P0c runs at medium here, so attended wave 0 has no strong packet whose diff waits
# for the user's read.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$(pwd)"
feature=004-csv-export
dir="$project/specs/$feature"

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" hardened-shapes

# The spec MUST: FR-002 also quotes a field that holds a line break.
sed -e 's/MUST quote fields that contain a comma\./MUST quote fields that contain a comma, a double quote or a line break./' \
  "$dir/spec.md" > "$dir/spec.md.tmp"
mv "$dir/spec.md.tmp" "$dir/spec.md"
grep -q 'a double quote or a line break' "$dir/spec.md"

# The contract agrees with the spec: II-2 quotes a field that holds a line break too.
sed -e 's/a field that contains a comma or a double quote is wrapped in/a field that contains a comma, a double quote or a line break is wrapped in/' \
  "$dir/contracts/internal-interfaces.md" > "$dir/contracts/internal-interfaces.md.tmp"
mv "$dir/contracts/internal-interfaces.md.tmp" "$dir/contracts/internal-interfaces.md"
grep -q 'a comma, a double quote or a line break is wrapped in' "$dir/contracts/internal-interfaces.md"

# The test packet's task asks for an assertion that breaks both (the seeded defect).
sed -e 's/and a double quote inside it is doubled\. Done-when/and a double quote inside it is doubled; a field with a line break and no comma or double quote is returned unchanged. Done-when/' \
  "$dir/tasks.md" > "$dir/tasks.md.tmp"
mv "$dir/tasks.md.tmp" "$dir/tasks.md"
grep -q 'a field with a line break and no comma' "$dir/tasks.md"

# P0c at medium: no strong packet in wave 0, so the attended wave commits without the user's
# diff read.
sed -e '/^| W0 | P0c I /s/| strong |$/| medium |/' "$dir/orchestration.md" > "$dir/orchestration.md.tmp"
mv "$dir/orchestration.md.tmp" "$dir/orchestration.md"
grep -q '^| W0 | P0c I .*| medium |$' "$dir/orchestration.md"
sed -e 's/The strong packets, P0c (the dispatcher) and P1a (the MVP), get the full/The strong packet, P1a (the MVP), gets the full/' \
  "$dir/handoff.md" > "$dir/handoff.md.tmp"
mv "$dir/handoff.md.tmp" "$dir/handoff.md"
grep -q 'The strong packet, P1a (the MVP), gets the full' "$dir/handoff.md"

git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: FR-002 quotes line breaks; T002 asserts otherwise; P0c medium"
git -C "$project/specs" push -q origin main

# The project's guidance file (handoff.md's READ FIRST 1) states the MUST as an invariant, which
# the shape check reads.
cat >> "$project/README.md" <<'EOF_README'

## Invariants

- CSV output follows spec FR-002, a MUST: a field that contains a comma, a double quote or a
  line break is always quoted.
EOF_README
git -C "$project" add README.md
git -C "$project" commit -q -m "docs: state the CSV quoting invariant"
git -C "$project" push -q origin "$feature"
