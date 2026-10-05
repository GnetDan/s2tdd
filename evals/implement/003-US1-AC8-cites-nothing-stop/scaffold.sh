#!/usr/bin/env bash
# Scaffold for 003-US1-AC8: a converge round that appends a task citing nothing in the spec
# Builds the fixture in the current directory: it is the project (git repository, a bare local
# remote standing in for GitHub), with specs/ as its own repository and its own bare remote.
# Helpers: evals/fixtures/. Neutral names only.
# The Given is seeded, not scripted. Relay 1 of a looping `nobrakes` run built and verified
# W0-W3, then handed off at the converge phase (RESUME AT: converge (round 1)); this run is
# relay 2, started from the handoff prompt in prompt.md. Every spec scenario is built; the one
# open item is a Carried constraint marked "carry to converge" that no spec ID names, so round
# 1's converge appends a task that cites nothing and the round stops on that rule.
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

# The open item converge must carry: a constraint from a review, citing no spec ID.
awk '{ print } /^Usage limits: week 95%, five-hour 90% \(default\)$/ { print "export --csv refuses to overwrite an existing file unless --force is given; carry to converge — from P0c'"'"'s strong-diff review" }' \
  "$ledger" > "$ledger.tmp"
mv "$ledger.tmp" "$ledger"
grep -q 'unless --force is given; carry to converge' "$ledger"

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
