---
description: "002-US5-AC3: Given a slice whose scope is waves 8–10 of 16, When the orchestrator prepares them, Then it has read orchestration.md's ground rules and the rows of waves 8–10, and the tasks of those waves, and no other waves' rows or tasks."
max_turns: 60
timeout_seconds: 2400
allowed_tools: [Read, Write, Edit, Glob, Bash, Agent, Skill]
runs: 1
---

/s2tdd-implement W8-W10
