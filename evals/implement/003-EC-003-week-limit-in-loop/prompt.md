---
description: "003-EC-003: Given a converge round in the loop, When weekly usage reaches the run's week limit, Then the run stops with its summary, as at a wave boundary."
max_turns: 120
timeout_seconds: 3000
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, SendMessage, Skill]
runs: 1
---

/s2tdd-implement --nobrakes
