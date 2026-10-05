---
description: '003-US1-AC6: Given a converge round that appends as many tasks as the round before it or more, When the round ends, Then the run stops, naming both rounds'' gap counts.'
max_turns: 150
timeout_seconds: 3600
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, SendMessage, Skill]
runs: 1
---

/s2tdd-implement --nobrakes
Context:
- Relay 2 of nobrakes run nb-20261002-0900 (scope W0–W5). The run's state is in
  specs/004-csv-export/run-ledger.md: read it before any dispatch.
- Carried constraints: see specs/004-csv-export/run-ledger.md; this prompt restates none of them.
- Expect: acme/acme-notes 004-csv-export at its commit `feat(004): wave 5 — P5a`, clean; specs
  HEAD is the commit `004: relay 1 handoff` or a later verify-done commit; every wave has a
  verify-done line in validation.md; the newest Rounds line is `Round 1: hardened · W4–W5`;
  the newest Lease line is `handed off by relay 1`.
- RESUME AT: converge (round 2). If anything does not match, print the RUN SUMMARY from the
  ledger and stop without work or writes.
