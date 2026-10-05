---
description: '003-US1-AC2: Given a nobrakes run whose converge appends three tasks, When the converge round ends, Then the run hardens those tasks in append mode without asking, implements them, and converges again.'
max_turns: 300
timeout_seconds: 7200
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, SendMessage, Skill]
runs: 1
---

/s2tdd-implement --nobrakes
