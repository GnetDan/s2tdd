---
description: "002-US4-AC2: Given a test packet's report with those citations, When the shape check reads it, Then its verdict says, per shape, whether the test matches the cited section."
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Bash, Write, Edit]
runs: 1
---

Shape check (specs/004-csv-export/handoff.md, Standard briefs).

Review wave 0's test packets P0a, P0b before the wave commit. Edit nothing; run only the packets'
own tests, never the full suite.
- Read: each packet's test diff (`git diff -- test_export_rows.py test_quoting.py`), the Cites:
  lines in its report (.sdd-run/004/reports/P0a.md, .sdd-run/004/reports/P0b.md), each cited
  contract section, and README.md's invariants.
- For each citation: matches, or differs: <what the test asserts> vs <what the section says>.
- For each shape a test asserts that another packet or wave builds, with no citation: a
  finding.
- For each Decision line below, one line: CONFIRM or DISPUTE: <why>.
- Findings, one per line: <blocker|should|note>[ · MUST <FR-nnn|US<n>-AC<m>|EC-nnn>] ·
  <file:line> · <failure scenario>. Verdict: Accept | Accept with fixes | Reject. At most 250
  words.
Decisions: none
