#!/usr/bin/env bash
# Scaffold for 003-US1-AC6: a converge round that appends as many tasks as the round before it
# or more
# Builds the fixture in the current directory: it is the project (git repository, a bare local
# remote standing in for GitHub), with specs/ as its own repository and its own bare remote.
# Helpers: evals/fixtures/. Neutral names only.
# The Given is seeded, not scripted. Relay 1 of a looping `nobrakes` run built and verified
# W0-W3; its round 1 converge appended one task (T008, US1-AC3: a field holding a line break is
# quoted), which the hardener split test-first into T008 and T009 as waves W4-W5; relay 1 built
# and verified them, then handed off at the converge phase (RESUME AT: converge (round 2)). This
# run is relay 2, started from the handoff prompt in prompt.md. spec.md also holds US1-AC4,
# which nothing builds, so round 2's converge appends at least one task: as many as round 1 or
# more, and the round stops on the no-shrink rule.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$(pwd)"
feature=004-csv-export
dir="$project/specs/$feature"
ledger="$dir/run-ledger.md"

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" looping

sha3=$(git -C "$project" rev-parse --short HEAD)

# spec.md: US1-AC3 and FR-003 (round 1 built them), and US1-AC4 and FR-004 (nothing builds them
# yet: round 2's gap).
awk '{ print }
  /^  the field is quoted\.$/ {
    print "- **US1-AC3**: **Given** a note whose text contains a line break (LF or CR), **When** it"
    print "  is exported, **Then** the field is quoted."
    print "- **US1-AC4**: **Given** a note whose text begins with `=`, **When** it is exported, **Then**"
    print "  the field is written with a single quote before the `=`."
  }
  /^- \*\*FR-002\*\*:/ {
    print "- **FR-003**: The system MUST quote fields that contain a line break. *(US1-AC3)*"
    print "- **FR-004**: The system MUST prefix a field that begins with `=` with a single quote. *(US1-AC4)*"
  }' "$dir/spec.md" > "$dir/spec.md.tmp"
mv "$dir/spec.md.tmp" "$dir/spec.md"
grep -q '^- \*\*US1-AC4\*\*' "$dir/spec.md"
grep -q '^- \*\*FR-004\*\*' "$dir/spec.md"

# Round 1's task, split test-first by the hardener, and its waves W4-W5.
awk '{ print }
  /^- \[x\] T007 / {
    print ""
    print "## Phase 5: Converge round 1"
    print ""
    print "- [x] T008 [US1] Write `test_line_breaks.py` for US1-AC3: a field holding a line break (LF or CR) is wrapped in double quotes (FR-003, II-2). Done-when: fails for the expected reason: the field comes back unquoted"
    print "- [x] T009 [US1] Quote a field holding a line break in `quote_field` (`quoting.py`; US1-AC3, FR-003, II-2). Done-when: `pytest` passes"
  }' "$dir/tasks.md" > "$dir/tasks.md.tmp"
mv "$dir/tasks.md.tmp" "$dir/tasks.md"
grep -q '^- \[x\] T009 ' "$dir/tasks.md"

awk '{ print }
  /^[|] W3 docs [|] P3a I [|] T007 / {
    print "| W4 red | P4a T | T008 | `test_line_breaks.py` | red: the field comes back unquoted (cites II-2) | medium |"
    print "| W5 green | P5a I | T009 | `quoting.py` | `pytest` | cheap |"
  }' "$dir/orchestration.md" > "$dir/orchestration.md.tmp"
mv "$dir/orchestration.md.tmp" "$dir/orchestration.md"
grep -q '^| W5 green | P5a I | T009 ' "$dir/orchestration.md"

cat > "$project/test_line_breaks.py" <<'EOF'
"""US1-AC3: a field holding a line break is quoted (II-2, FR-003)."""
from quoting import quote_field


def test_a_field_with_a_line_feed_is_quoted():
    assert quote_field("buy\nmilk") == '"buy\nmilk"'


def test_a_field_with_a_carriage_return_is_quoted():
    assert quote_field("buy\rmilk") == '"buy\rmilk"'
EOF
git -C "$project" add test_line_breaks.py
git -C "$project" commit -q -m "feat(004): wave 4 — P4a"
sha4=$(git -C "$project" rev-parse --short HEAD)

cat > "$project/quoting.py" <<'EOF'
"""CSV field quoting (II-2)."""


def quote_field(text):
    """Wrap a field holding a comma, a double quote or a line break in double quotes, doubling
    inner double quotes."""
    if any(mark in text for mark in (",", '"', "\n", "\r")):
        return '"' + text.replace('"', '""') + '"'
    return text
EOF
git -C "$project" add quoting.py
git -C "$project" commit -q -m "feat(004): wave 5 — P5a"
sha5=$(git -C "$project" rev-parse --short HEAD)
git -C "$project" push -q origin "$feature"

printf -- '- 2026-10-02 · verify-done · waves W4–W5 (%s..%s) · Verified · proxy · suite 0m02s (no budget)\n' \
  "$sha4" "$sha5" >> "$dir/validation.md"

# The ledger: a looping `nobrakes` run (not `once`), round 1's lines, W4-W5's usage, and relay
# 1's handoff instead of a released lease.
sed -e 's/ · nobrakes once · / · nobrakes · /' \
    -e 's/^released by relay 1: done$/handed off by relay 1/' \
    "$ledger" > "$ledger.tmp"
mv "$ledger.tmp" "$ledger"
awk -v sha="$sha3" '{ print }
  /^## Rounds$/ {
    print "Round 1: converge at " sha " · 1 tasks appended (T008–T008) · cites T008 US1-AC3 FR-003"
    print "Round 1: hardened · W4–W5"
  }
  /^wave 3 · context 38% · 1 packets$/ {
    print "converge round 1 · context 41%"
    print "harden round 1 · context 44%"
    print "wave 4 · context 49% · 1 packets"
    print "wave 5 · context 55% · 1 packets"
  }' "$ledger" > "$ledger.tmp"
mv "$ledger.tmp" "$ledger"
grep -q '^run nb-20261002-0900 · nobrakes · scope W0–W3' "$ledger"
grep -q '^handed off by relay 1$' "$ledger"
grep -q '^Round 1: hardened · W4–W5$' "$ledger"

# Relay 1's handoff prompt, in the ledger's Handoff section (the last one) and in the file
# HANDOFF step 3 writes.
handoff_prompt="/s2tdd-implement --nobrakes
Context:
- Relay 2 of nobrakes run nb-20261002-0900 (scope W0–W5). The run's state is in
  specs/004-csv-export/run-ledger.md: read it before any dispatch.
- Carried constraints: see specs/004-csv-export/run-ledger.md; this prompt restates none of them.
- Expect: acme/acme-notes 004-csv-export at its commit \`feat(004): wave 5 — P5a\`, clean; specs
  HEAD is the commit \`004: relay 1 handoff\` or a later verify-done commit; every wave has a
  verify-done line in validation.md; the newest Rounds line is \`Round 1: hardened · W4–W5\`;
  the newest Lease line is \`handed off by relay 1\`.
- RESUME AT: converge (round 2). If anything does not match, print the RUN SUMMARY from the
  ledger and stop without work or writes."
printf '%s\n' "$handoff_prompt" >> "$ledger"
exclude="$project/.git/info/exclude"
grep -qx '.sdd-run/' "$exclude" 2>/dev/null || printf '.sdd-run/\n' >> "$exclude"
mkdir -p "$project/.sdd-run/004"
printf '%s\n' "$handoff_prompt" > "$project/.sdd-run/004/handoff-2.md"

git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: relay 1 handoff"
git -C "$project/specs" push -q origin main
