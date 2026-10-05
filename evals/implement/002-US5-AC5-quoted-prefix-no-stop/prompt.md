---
description: "002-US5-AC5: Given an orchestration.md that quotes the bare old command prefix (not followed by a command name) and names no old command, When implement runs its stale-name check, Then it does not stop."
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Write, Edit, Glob, Bash, Agent, Skill]
runs: 1
---

/s2tdd-implement W0 --print
