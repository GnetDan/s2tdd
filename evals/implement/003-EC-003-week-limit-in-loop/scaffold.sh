#!/usr/bin/env bash
# Scaffold for 003-EC-003 (week-limit-in-loop).
# Given: a converge round in the loop. The looping state (II-15): every wave of 004 committed
# and verified by an earlier `nobrakes once` run, which released the lease `done`; `## Rounds`
# empty. After that run the spec gained a scenario no task covers (US1-AC3, FR-003: a field
# holding a line break is quoted), so this `--nobrakes` run's first converge round appends work
# and the loop goes on. The usage reading is the case's mock of the desktop app's usage tool
# (mocks/ccd_session_mgmt/get_usage.md): its first answer reads weekly 70%, every later one 96%,
# past the run's default week limit (95%), so weekly usage reaches the limit at the loop's next
# phase change after the first reading.
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

grep -qF 'CONVERGE LOOP (MODE: nobrakes only).' "$dir/handoff.md" || fail "handoff.md: no CONVERGE LOOP"
grep -q '^released by relay 1: done$' "$dir/run-ledger.md" || fail "run-ledger.md: lease not released"
if grep -q '^- \[ \] T' "$dir/tasks.md"; then fail "tasks.md: a task is unticked"; fi

# The gap converge finds: a scenario and a requirement no task covers yet.
awk '
  { print }
  /^  the field is quoted\.$/ && !s {
    print "- **US1-AC3**: **Given** a note whose text holds a line break, **When** it is exported,"
    print "  **Then** the field is quoted, with the line break kept inside the quotes."
    s = 1
  }
  /^- \*\*FR-002\*\*/ && !f {
    print "- **FR-003**: The system MUST quote fields that contain a line break. *(US1-AC3)*"
    f = 1
  }' "$dir/spec.md" > "$dir/spec.md.tmp"
mv "$dir/spec.md.tmp" "$dir/spec.md"
grep -q '^- \*\*US1-AC3\*\*' "$dir/spec.md" || fail "spec.md: US1-AC3 not added"
grep -q '^- \*\*FR-003\*\*' "$dir/spec.md" || fail "spec.md: FR-003 not added"

git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: spec gains US1-AC3 (a line break is quoted)"
git -C "$project/specs" push -q origin main
