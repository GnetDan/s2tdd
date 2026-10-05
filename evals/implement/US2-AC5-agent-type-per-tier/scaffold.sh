#!/usr/bin/env bash
# Scaffold for US2-AC5: a hardened feature whose packets carry tiers
# Builds the fixture in the current directory: it is the project (git repository on main, a
# bare local remote standing in for GitHub), with specs/ as its own repository and its own
# bare remote. Helpers: evals/fixtures/. Neutral names only.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$(pwd)"
feature=004-csv-export

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" hardened

dir="$project/specs/$feature"

cat > "$dir/tasks.md" <<'EOF_TASKS'
# Tasks: CSV export

## Phase 1: Export

- [x] T001 [US1] Write `test_export.py` for US1-AC1 and US1-AC2. Done-when: fails for the expected reason: `export.py` not found
- [ ] T002 [US1] Write `export.py`. Done-when: `python -m pytest test_export.py` passes
- [ ] T003 [US1] Document `export --csv` in `README.md`. Done-when: the README names the flag
EOF_TASKS

cat > "$dir/orchestration.md" <<'EOF_ORCH'
# Orchestration: CSV export

## Ground rules

1. **File ownership.** A packet edits only the files its row lists.
4. **Reports by exception.** A packet hands back a card, not a transcript.
12. **Test ownership.** Test packets own tests; implementation packets never edit them.

## Waves

| Wave | Packet | Tasks | Owned files | Done-when | Tier |
|---|---|---|---|---|---|
| W1 | P1a | T001 | `test_export.py` | fails for the expected reason: `export.py` not found | cheap |
| W2 | P2a | T002 | `export.py` | `python -m pytest test_export.py` passes | medium |
| W3 | P3a | T003 | `README.md` | the README names the flag | cheap |

## Context budget

| Slice | Waves |
|---|---|
| S1 | W1-W3 |
EOF_ORCH

cat > "$dir/handoff.md" <<'EOF_HANDOFF'
# Handoff: CSV export

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

SCOPE
Waves W1-W3. Off-limits: every file that no packet row owns.
RESUME AT: wave 0
MODE: attended

HOW TO WORK
One wave at a time. Preflight before every dispatch: `git status --short` on the packet's
owned files. Dispatch each packet in a subagent at the tier orchestration.md names. Every
briefing ends with ground rule 4. After each wave run the full suite once; green: tick the
wave's tasks and commit.
```

## Standard briefs

Briefing text for the subagents that stand in for the user, kept on disk.
EOF_HANDOFF

cat > "$dir/run-ledger.md" <<'EOF_LEDGER'
# Run ledger: 004 CSV export

## Lease
## Runs
## Carried constraints
## Handoff
EOF_LEDGER

git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "feat($feature): hardened with tiers"
git -C "$project/specs" push -q origin main

cat > "$project/test_export.py" <<'EOF_TEST'
from export import export_csv


def test_header_and_rows():
    lines = export_csv([{"text": "a"}, {"text": "b"}, {"text": "c"}]).splitlines()
    assert lines[0] == "text"
    assert len(lines) == 4


def test_comma_is_quoted():
    assert '"a,b"' in export_csv([{"text": "a,b"}])
EOF_TEST
git -C "$project" add test_export.py
git -C "$project" commit -q -m "test($feature): export tests"
git -C "$project" push -q origin "$feature"
