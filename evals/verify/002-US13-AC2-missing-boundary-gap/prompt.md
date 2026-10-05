---
description: '002-US13-AC2: Given a wave report with no boundary record, When verify-done checks the waves, Then it lists a gap.'
max_turns: 60
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Bash, Edit, Write, Skill]
---

/s2tdd-verify-done reports: specs/004-csv-export/s1-wave-reports.md
