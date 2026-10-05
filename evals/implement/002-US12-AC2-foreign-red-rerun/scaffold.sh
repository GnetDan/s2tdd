#!/usr/bin/env bash
# Scaffold for 002-US12-AC2 (foreign-red-rerun).
# Given: a packet that sees a red outside its own tests. The wave-reports state (II-16): W0 and
# W1 committed by nobrakes relay 1, which then released the lease. After W1, feature 003's
# notebook-store test reached the branch; it fails on its own (no `notes.json` in the checkout).
# W2's only packet, P2a (T006, `export.py`), has the done-when `pytest`, so its runs show that
# test red although it is not P2a's.
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

grep -q '^| W2 [^|]*| P2a I | T006 | `export.py` | `pytest` |' "$dir/orchestration.md" \
  || fail "orchestration.md: W2's P2a does not have the done-when pytest"

# Relay 1 released the lease after W1, so an attended session may take the next wave.
ledger="$dir/run-ledger.md"
released=$(awk '{ print } /^session-1, relay 1, since / { print "released by relay 1: stopped: the user ended the run after W1" }' "$ledger")
printf '%s\n' "$released" > "$ledger"
grep -q '^released by relay 1: ' "$ledger" || fail "run-ledger.md: lease not released"
git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: relay 1 released the lease"
git -C "$project/specs" push -q origin main

# Feature 003's test, not a test of feature 004: red when run alone, as in the full run.
cat > "$project/test_notes_store.py" <<'EOF'
"""Feature 003: the notebook store reads notes.json from the working directory."""
from pathlib import Path


def test_the_notebook_file_is_present():
    assert Path("notes.json").is_file(), "notes.json not found: the notebook store is empty"
EOF
git -C "$project" add test_notes_store.py
git -C "$project" commit -q -m "test(003): the notebook store reads notes.json"
git -C "$project" push -q origin "$feature"
