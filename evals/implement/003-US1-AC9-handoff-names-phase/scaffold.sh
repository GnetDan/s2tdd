#!/usr/bin/env bash
# Scaffold for 003-US1-AC9: a relay that reaches its hand-off threshold just after a converge
# round appended tasks
# Builds the fixture in the current directory: it is the project (git repository, a bare local
# remote standing in for GitHub), with specs/ as its own repository and its own bare remote.
# Helpers: evals/fixtures/. Neutral names only.
# The Given is seeded, not scripted. Relay 1 of a looping `nobrakes` run built and verified
# W0-W3, then handed off at the converge phase (RESUME AT: converge (round 1)); this run is
# relay 2, started from the handoff prompt in prompt.md. spec.md holds one scenario nothing
# builds yet, so round 1's converge appends tasks; .sdd-run/004/BRAKES makes the relay hand off
# at the phase change that follows, before the harden step.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$(pwd)"
feature=004-csv-export
dir="$project/specs/$feature"
ledger="$dir/run-ledger.md"

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" looping

# The run is a looping `nobrakes` run (not `once`), and relay 1 handed off at the converge
# phase instead of releasing the lease.
sed -e 's/ · nobrakes once · / · nobrakes · /' \
    -e 's/^released by relay 1: done$/handed off by relay 1/' \
    "$ledger" > "$ledger.tmp"
mv "$ledger.tmp" "$ledger"
grep -q '^run nb-20261002-0900 · nobrakes · scope W0–W3' "$ledger"
grep -q '^handed off by relay 1$' "$ledger"

# The gap round 1 finds: spec.md gains US1-AC3 and FR-003 (a field holding a line break is
# quoted), which no task and no code covers yet, so round 1's converge appends tasks.
awk '{ print }
  /^  the field is quoted\.$/ {
    print "- **US1-AC3**: **Given** a note whose text contains a line break, **When** it is exported,"
    print "  **Then** the field is quoted."
  }
  /^- \*\*FR-002\*\*:/ {
    print "- **FR-003**: The system MUST quote fields that contain a line break. *(US1-AC3)*"
  }' "$dir/spec.md" > "$dir/spec.md.tmp"
mv "$dir/spec.md.tmp" "$dir/spec.md"
grep -q '^- \*\*US1-AC3\*\*' "$dir/spec.md"
grep -q '^- \*\*FR-003\*\*' "$dir/spec.md"

# Relay 1's handoff prompt, in the ledger's Handoff section (the last one) and in the file
# HANDOFF step 3 writes.
handoff_prompt="/s2tdd-implement --nobrakes
Context:
- Relay 2 of nobrakes run nb-20261002-0900 (scope W0–W3). The run's state is in
  specs/004-csv-export/run-ledger.md: read it before any dispatch.
- Carried constraints: see specs/004-csv-export/run-ledger.md; this prompt restates none of them.
- Expect: acme/acme-notes 004-csv-export at its commit \`feat(004): wave 3 — P3a\`, clean; specs
  HEAD is the commit \`004: relay 1 handoff\` or a later verify-done commit; every wave has a
  verify-done line in validation.md; the newest Rounds line is none; the newest Lease line is
  \`handed off by relay 1\`.
- RESUME AT: converge (round 1). If anything does not match, print the RUN SUMMARY from the
  ledger and stop without work or writes."
printf '%s\n' "$handoff_prompt" >> "$ledger"
exclude="$project/.git/info/exclude"
grep -qx '.sdd-run/' "$exclude" 2>/dev/null || printf '.sdd-run/\n' >> "$exclude"
mkdir -p "$project/.sdd-run/004"
printf '%s\n' "$handoff_prompt" > "$project/.sdd-run/004/handoff-2.md"

git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: relay 1 handoff"
git -C "$project/specs" push -q origin main

# BRAKES: the file the relay checks at every boundary, a phase change included (CONVERGE LOOP),
# so this relay reaches its handoff at the first one: just after round 1's converge appended
# tasks. claude -p has no usage tool, so no window can trigger one.
: > "$project/.sdd-run/004/BRAKES"
