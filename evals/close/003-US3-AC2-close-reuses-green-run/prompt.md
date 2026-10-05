---
description: '003-US3-AC2: Given a green full run recorded at commit X and a clean tree at X, When close reaches its suite gate, Then it starts no suite and records that it reused the run at X.'
max_turns: 80
timeout_seconds: 1500
allowed_tools: [Read, Glob, Grep, Bash, Edit, Write, Skill]
---

/s2tdd-close
