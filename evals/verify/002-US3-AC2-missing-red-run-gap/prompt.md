---
description: '002-US3-AC2: Given an implementation packet report that quotes no red run, and the wave report shows the orchestrator saw the test red before dispatch, When verify-done checks the waves, Then the packet is listed as a gap.'
max_turns: 60
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Bash, Edit, Write, Skill]
runs: 3
---

/s2tdd-verify-done reports: specs/004-csv-export/s1-wave-reports.md
