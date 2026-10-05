---
description: '003-US3-AC1: Given a green full run recorded at commit X and a clean tree at X, When converge runs, Then it starts no suite and records that it reused the run at X.'
max_turns: 60
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Bash, Edit, Write, Skill]
---

/s2tdd-converge
