---
description: '002-US3-AC3: Given wave reports for 30 implementation packets, When verify-done (or its proxy) checks red-before-green, Then it states that it read all 30 reports'' red runs.'
max_turns: 120
timeout_seconds: 2400
allowed_tools: [Read, Glob, Grep, Bash, Edit, Write, Skill]
---

/s2tdd-verify-done reports: specs/004-csv-export/s1-wave-reports.md
