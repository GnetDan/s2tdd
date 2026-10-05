---
description: '003-US3-AC3: Given a green full run recorded at commit X, When HEAD is past X or the tree is dirty, Then converge and close run the suite as today.'
max_turns: 60
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Bash, Edit, Write, Skill]
---

/s2tdd-converge
