---
description: "002-US1-AC5: Given an attended run whose shape check finds the same, When the orchestrator handles it, Then the finding appears in the wave report as a recommendation, and the wave is committed and the run continues as before."
max_turns: 90
timeout_seconds: 2700
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, Skill]
runs: 1
---

/s2tdd-implement W0
