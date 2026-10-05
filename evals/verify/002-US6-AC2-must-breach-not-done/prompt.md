---
description: '002-US6-AC2: Given verify-done finds a committed change that breaks a spec MUST, When it gives its verdict, Then the verdict is Not done and the task is unticked.'
max_turns: 60
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Bash, Edit, Write, Skill]
---

/s2tdd-verify-done reports: specs/004-csv-export/s1-wave-reports.md
