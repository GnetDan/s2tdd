#!/usr/bin/env bash
# Scaffold for 002-US1-AC2 (no-test-packets-no-check).
# Given: a wave with no test packets. The wave-reports state (II-16): W0 and W1 committed and
# ticked; the next wave, W2, holds one implementation packet (P2a, cheap) and no test packet.
# The earlier relay's lease is released, as the user does when that session is gone.
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
bash "$fixtures/make-feature.sh" "$project" wave-reports

fail() { echo "scaffold: $*" >&2; exit 1; }

# insert_after <file> <ERE> <line>: the line goes after the first line matching the ERE.
insert_after() {
  PAT="$2" LINE="$3" awk '{ print } !done && $0 ~ ENVIRON["PAT"] { print ENVIRON["LINE"]; done = 1 }' \
    "$1" > "$1.tmp"
  mv "$1.tmp" "$1"
  grep -qF -- "$3" "$1" || fail "$1: no line matches $2"
}

insert_after "$dir/run-ledger.md" '^session-1, relay 1, since ' 'released by user 2026-10-02'
grep -q '^- \[ \] T006 ' "$dir/tasks.md" || fail "tasks.md: T006 is not the next unticked task"
if grep '^| W2[^|]*|' "$dir/orchestration.md" | grep -q '| P[0-9][a-z] T |'; then
  fail "orchestration.md: W2 holds a test packet"
fi

git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: lease released by user"
git -C "$project/specs" push -q origin main
