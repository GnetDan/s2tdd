#!/usr/bin/env bash
# Scaffold for 003-US1-AC4 (harden-stop-in-summary).
# Given: a converge round that appended a task citing a scenario without an ID. The looping
# state (II-15): every task of W0-W3 ticked and verified, the earlier `nobrakes once` run
# released `done`, its Rounds section empty. spec.md then gains an edge case with no ID (a note
# with no title exports an empty title field; export.py raises KeyError today) and FR-003,
# which cites it. The loop's first converge appends a task for that gap, citing FR-003, so no
# stop rule fires (it cites an ID); the hardener then stops on harden's precondition "assign
# scenario IDs first", and the run stops with that message.
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

# The edge case goes after US1's scenarios, before ## Requirements; FR-003 goes last.
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
grep -qF -- '- **Given** a note with no title' "$dir/spec.md" || fail "spec.md: no edge case"
if grep -q 'EC-0' "$dir/spec.md"; then fail "spec.md: the edge case must have no ID"; fi
grep -qF 'str(note[key])' "$project/export.py" || fail "export.py already handles a missing title"

git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: spec: an edge case and FR-003"
git -C "$project/specs" push -q origin main
