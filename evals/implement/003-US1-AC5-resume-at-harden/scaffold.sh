#!/usr/bin/env bash
# Scaffold for 003-US1-AC5 (resume-at-harden).
# Given: a run that stopped at its harden step, whose cause the user has fixed. The looping
# state (II-15), then the run 003-US1-AC4 plays out, recorded as it would be: spec.md gained an
# edge case with no ID and FR-003, which cites it; a second nobrakes run's round 1 converge
# appended T008 (citing FR-003) under `## Phase 5: Convergence` and wrote its verification-log
# line; its hardener stopped on "assign scenario IDs first", recorded under Rounds as
# `Round 1: stopped · harden: …`, and the relay released the lease `stopped: …`. Then the user
# fixed the cause: the edge case now has the ID EC-001, committed in the specs repository.
# Rerunning `/s2tdd-implement --nobrakes` resumes from the ledger at the harden step (round 1).
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
bash "$fixtures/make-feature.sh" "$project" looping

fail() { echo "scaffold: $*" >&2; exit 1; }

# add_line <file> <heading> <line>: append <line> at the end of the section `## <heading>`.
add_line() {
  H="## $2" LINE="$3" awk '
    in_section && /^## / { print ENVIRON["LINE"]; in_section = 0; added = 1 }
    { print }
    $0 == ENVIRON["H"] { in_section = 1 }
    END { if (in_section && !added) print ENVIRON["LINE"] }' "$1" > "$1.tmp"
  mv "$1.tmp" "$1"
}

# The spec as the stopped run found it: the edge case without an ID, and FR-003 citing it.
awk '/^## Requirements$/ && !done {
    print "### Edge Cases"
    print ""
    print "- **Given** a note with no title, **When** it is exported, **Then** its title field is"
    print "  empty and the row is still written."
    print ""
    done = 1
  } { print }' "$dir/spec.md" > "$dir/spec.md.tmp"
mv "$dir/spec.md.tmp" "$dir/spec.md"
cat >> "$dir/spec.md" <<'EOF'
- **FR-003**: The system MUST export a note with no title, writing an empty title field.
EOF
git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: spec: an edge case and FR-003"

# The second run: converge round 1 appended T008, then harden stopped.
sha=$(git -C "$project" rev-parse --short HEAD)
stop='assign scenario IDs first (spec template convention); IDs are never renumbered'
cat >> "$dir/tasks.md" <<'EOF'

## Phase 5: Convergence

- [ ] T008 Export a note with no title, writing an empty title field, per FR-003 (missing)
EOF
printf -- '- 2026-10-03 · converge · at %s · 1 tasks appended (T008–T008) · suite 0m02s (no budget)\n' \
  "$sha" >> "$dir/validation.md"
ledger="$dir/run-ledger.md"
add_line "$ledger" "Lease" "session-2, relay 1, since 2026-10-03T09:00Z"
add_line "$ledger" "Lease" "released by relay 1: stopped: harden: $stop"
add_line "$ledger" "Runs" "run nb-20261003-0900 · nobrakes · scope W0–W3 · started 2026-10-03T09:00Z"
add_line "$ledger" "Rounds" "Round 1: converge at $sha · 1 tasks appended (T008–T008) · cites T008 FR-003"
add_line "$ledger" "Rounds" "Round 1: stopped · harden: $stop"

grep -q '^Round 1: stopped · harden: assign scenario IDs first' "$ledger" \
  || fail "run-ledger.md: no harden stop under Rounds"
[ "$(sed -n '/^## Lease$/,/^## /p' "$ledger" | grep -c '^released by relay')" = 2 ] \
  || fail "run-ledger.md: the Lease does not end with the second release"
git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: run nb-20261003-0900 stopped at harden (round 1)"

# The user fixes the cause: the edge case gets its ID.
sed -e 's/^- \*\*Given\*\* a note with no title,/- **EC-001**: **Given** a note with no title,/' \
  -e 's/^\(- \*\*FR-003\*\*: .*field\.\)$/\1 *(EC-001)*/' "$dir/spec.md" > "$dir/spec.md.tmp"
mv "$dir/spec.md.tmp" "$dir/spec.md"
grep -qF -- '- **EC-001**: **Given** a note with no title' "$dir/spec.md" || fail "spec.md: no EC-001"
grep -qF -- 'title field. *(EC-001)*' "$dir/spec.md" || fail "spec.md: FR-003 does not cite EC-001"
git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: spec: the no-title edge case is EC-001"
git -C "$project/specs" push -q origin main
