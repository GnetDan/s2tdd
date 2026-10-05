---
description: '002-US3-AC4: Given an implementation packet whose test neither its report nor the orchestrator''s pre-dispatch check ever shows red, When verify-done checks the waves, Then the verdict is Not done, the task is unticked, and the fix line says the test''s own packet must show it red at the commit before the implementation.'
max_turns: 60
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Bash, Edit, Write, Skill]
---

/s2tdd-verify-done reports: specs/004-csv-export/s1-wave-reports.md
