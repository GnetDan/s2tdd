---
description: "002-US5-AC4: Given a wave in progress, When the orchestrator needs a rule, a row or a task it has already read this session, Then it uses what it read rather than re-reading the file."
max_turns: 90
timeout_seconds: 2700
allowed_tools: [Read, Write, Edit, Glob, Bash, Agent, Skill]
runs: 1
---

/s2tdd-implement W0
