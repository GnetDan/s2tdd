#!/usr/bin/env bash
# Scaffold for 002-US11-AC2 (gate-in-worktree).
# Given: a verify gate at a slice end. The hardened-shapes state (II-16), no wave run yet, with
# orchestration.md's Context budget cut into two slices, s1: W0 and s2: W1–W3, so a
# `--nobrakes W0-W1` run reaches s1's end with W1 still to run: the gate after W0 verifies in a
# scratch worktree while W1 starts. The Proxy verifier brief's PID-record line names the main
# checkout, so the record outlives the gate worktree.
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

# Context budget is orchestration.md's last section: cut it off and write two slices.
orchestration="$dir/orchestration.md"
grep -q '^## Context budget' "$orchestration" || fail "orchestration.md has no Context budget"
kept=$(sed -e '/^## Context budget/,$d' "$orchestration")
printf '%s\n' "$kept" > "$orchestration"
cat >> "$orchestration" <<'EOF'
## Context budget

7 packets × about 15k tokens, plus one shape-check hand-back (about 1k tokens) for W0, the one
wave that holds test packets: about 106k. Two slices, each well inside half the context window:

| Slice | Waves |
|---|---|
| s1 | W0 |
| s2 | W1–W3 |

Each slice's end is where `--nobrakes` runs a verify gate.
EOF
grep -q '^| s2 | W1–W3 |' "$orchestration" || fail "orchestration.md: slices not written"

# The Proxy verifier brief (the fixture's transcription of harden's) names the main checkout's
# PID record, so graders/09 reads it where the run starts.
handoff="$dir/handoff.md"
grep -qF "the main checkout's \`.sdd-run/004/pids/verifier-<k>.txt\` (never the worktree's)" "$handoff" \
  || fail "handoff.md: the verifier's PID line does not name the main checkout"

git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: two slices, s1 W0 and s2 W1–W3"
git -C "$project/specs" push -q origin main
