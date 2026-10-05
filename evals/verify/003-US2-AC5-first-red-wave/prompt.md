---
description: '003-US2-AC5: Given a slice-end full run that shows a red no per-wave run in the slice showed, When the gate reports it, Then the verdict is Not done, naming the red test and the first wave commit of the slice where that test alone goes red, and that wave''s tasks lead the next wave with the failure attached.'
max_turns: 80
timeout_seconds: 1500
allowed_tools: [Read, Glob, Grep, Bash, Edit, Write, Skill]
---

/s2tdd-verify-done reports: specs/004-csv-export/s1-wave-reports.md
