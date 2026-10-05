---
description: '002-US3-AC1: Given an implementation packet report that says its red run happened after it wrote its implementation files, and the orchestrator''s check before dispatch saw the test red, When verify-done checks the waves, Then the packet is listed as a gap and the verdict is at best Verified with gaps.'
max_turns: 60
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Bash, Edit, Write, Skill]
runs: 3
---

/s2tdd-verify-done reports: specs/004-csv-export/s1-wave-reports.md
