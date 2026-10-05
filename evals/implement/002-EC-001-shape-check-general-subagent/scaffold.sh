#!/usr/bin/env bash
# Scaffold for 002-EC-001 (shape-check-general-subagent).
# Given: a project running from a copy of the skills, without the plugin's agent types. The
# hardened-shapes state (II-16), whose wave W0 holds the test packets P0a and P0b, plus the
# project-copy install: make-copy.sh copies this repository's skills/ (and no agents/) into the
# project's .claude/skills/, committed as a project that installs by copy does. P0c runs at
# medium here, so the attended wave reaches its commit without waiting for the user's read of a
# strong packet's diff.
# The runner's arm without the plugin is the one this Given describes: there the copy is the
# only s2tdd, and no s2tdd: agent type exists. With the plugin loaded its agent types exist, and
# the graders allow for that (they are written for both arms).
# Builds the fixture in the current directory: it is the project (a git repository on the
# branch 004-csv-export, a bare local remote standing in for GitHub), with specs/ as its own
# repository and its own bare remote. Helpers: evals/fixtures/. Neutral names only.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fixtures="$(cd "$here/../../fixtures" && pwd)"
plugin="$(cd "$here/../../.." && pwd)"
project="$(pwd)"
feature=004-csv-export
dir="$project/specs/$feature"

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" hardened-shapes

fail() { echo "scaffold: $*" >&2; exit 1; }

# replace_text <file> <old> <new>: the first occurrence of the literal text <old> becomes <new>
# (awk reads both from the environment, so backslashes stay as written).
replace_text() {
  OLD="$2" NEW="$3" awk '!done && (i = index($0, ENVIRON["OLD"])) {
      $0 = substr($0, 1, i - 1) ENVIRON["NEW"] substr($0, i + length(ENVIRON["OLD"])); done = 1
    } { print }' "$1" > "$1.tmp"
  mv "$1.tmp" "$1"
  grep -qF -- "$3" "$1" || fail "$1: no line holds $2"
}

replace_text "$dir/orchestration.md" '`python cli.py --help` exits 0 and lists `export` | strong |' \
  '`python cli.py --help` exits 0 and lists `export` | medium |'
replace_text "$dir/handoff.md" 'The strong packets, P0c (the dispatcher) and P1a (the MVP), get the full' \
  'The strong packet, P1a (the MVP), gets the full'
git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: P0c at medium"
git -C "$project/specs" push -q origin main

bash "$fixtures/make-copy.sh" "$project" "$plugin"
[ -f "$project/.claude/skills/s2tdd-implement/SKILL.md" ] || fail "the copy has no s2tdd-implement"
[ ! -e "$project/.claude/agents" ] || fail "the copy carries agent types"
git -C "$project" add .claude/skills
git -C "$project" commit -q -m "chore: install s2tdd by copying its skills"
git -C "$project" push -q origin "$feature"
