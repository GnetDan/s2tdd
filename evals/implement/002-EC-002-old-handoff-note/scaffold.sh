#!/usr/bin/env bash
# Scaffold for 002-EC-002 (old-handoff-note).
# Given: a feature hardened before this change: its handoff.md has no shape check. The
# hardened-shapes state (II-16), whose wave W0 holds the test packets P0a and P0b, with its
# handoff.md replaced by the shape an older harden wrote: a fenced prompt with no SHAPE CHECK,
# no MUST BREACH and no Shape check brief; orchestration.md's shape-check mentions removed.
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

cat > "$dir/handoff.md" <<'EOF_HANDOFF'
# Handoff: 004 CSV export

This file is the prompt `/s2tdd-implement` runs in-session and `/s2tdd-implement --print`
prints. Preconditions: branch `004-csv-export` exists, spec artifacts are committed, the tree
is clean.

```text
You are the ORCHESTRATOR for feature 004 of acme-notes, following
specs/004-csv-export/orchestration.md exactly. You do not implement packets in this context.

STEP 0 — CAPABILITY CHECK
Determine whether this harness can run subagents (a Task/Agent tool). Report one line before
any work: `Subagents: yes (<mechanism>)` or `Subagents: no`. If yes, every packet runs in a
subagent briefed with pointers only.

READ FIRST, IN THIS ORDER
1. specs/004-csv-export/run-ledger.md
2. specs/004-csv-export/orchestration.md (ground rules, then the rows of the waves in SCOPE)
3. specs/004-csv-export/tasks.md (the task range)
4. specs/004-csv-export/contracts/internal-interfaces.md (frozen; stop and report, never
   deviate silently)

SCOPE
Waves W0-W3. Off-limits: every file that no packet row owns.
RESUME AT: wave 0
MODE: attended

HOW TO WORK
One wave at a time. Preflight before every dispatch: `git status --short` on the packet's
owned files. Dispatch each packet in a subagent at the tier orchestration.md names. Every
briefing ends with ground rule 4. Red → green: run the test packet's done-when, confirm the
expected failure, then dispatch the implementation packet. After each wave run the full suite
once; green (the expected-red table's reds aside): tick the wave's tasks, commit
`feat(004): wave <n> — <packets>`, append your wave report to
specs/004-csv-export/s1-wave-reports.md and commit the ticks and that file in the specs
repository.

REPORT AFTER EVERY WAVE, in this format, no code:
  Wave: <id>  Packets: <list>
  Files touched: <paths>
  Commands run + results: <test summary line, done-when outputs>
  Red runs: <test ids and the failure each showed before implementation>
  Decisions: <one line each>
  Commit: <hash>
With `MODE: attended`, stop after the last wave in SCOPE and print the RESUME AT line.
```

## Standard briefs

Briefing text for the subagents that stand in for the user, kept on disk.
EOF_HANDOFF

# orchestration.md as the same older harden wrote it: its Dispatching (1) and Context budget
# name no shape check. Each line is replaced whole or dropped (awk on ENVIRON: no escapes).
OLD1="   user's when attended, the reviewer's in --nobrakes), and every wave that holds test packets" \
NEW1="   user's when attended, the reviewer's in --nobrakes)." \
DROP1="   gets the shape check, in both modes." \
OLD2="7 packets × about 15k tokens, plus one shape-check hand-back (about 1k tokens) for W0, the one" \
NEW2="7 packets × about 15k tokens: about 105k. One slice, s1: W0–W3. Its end is where \`--nobrakes\`" \
DROP2="wave that holds test packets: about 106k. One slice, s1: W0–W3. Its end is where \`--nobrakes\`" \
  awk '$0 == ENVIRON["OLD1"] { print ENVIRON["NEW1"]; next }
       $0 == ENVIRON["DROP1"] { next }
       $0 == ENVIRON["OLD2"] { print ENVIRON["NEW2"]; next }
       $0 == ENVIRON["DROP2"] { next }
       { print }' "$dir/orchestration.md" > "$dir/orchestration.md.tmp"
mv "$dir/orchestration.md.tmp" "$dir/orchestration.md"

for file in handoff.md orchestration.md; do
  if grep -qi 'shape.check' "$dir/$file"; then
    echo "scaffold: $file names a shape check" >&2
    exit 1
  fi
done
grep -qF 'about 105k. One slice, s1: W0–W3.' "$dir/orchestration.md" \
  || { echo "scaffold: orchestration.md's Context budget not rewritten" >&2; exit 1; }

# The run is attended and a one-prompt eval has no user to read a strong packet's diff before
# the wave commit, so W0 holds no strong packet: P0c is demoted to medium (the old handoff has
# no TIER text naming it). Portable in-place sed (no -i).
text=$(sed -e '/^| W0 | P0c I /s/| strong |$/| medium |/' "$dir/orchestration.md")
printf '%s\n' "$text" > "$dir/orchestration.md"
if grep '^| W0[^|]*|' "$dir/orchestration.md" | grep -q '| strong |'; then
  echo "scaffold: orchestration.md: W0 still holds a strong packet" >&2
  exit 1
fi

git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: handoff.md as an older harden wrote it"
git -C "$project/specs" push -q origin main
