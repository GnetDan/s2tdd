---
description: '002-US12-AC2: Given a packet that sees a red outside its own tests, When it reports, Then it reran that test alone first and reports it only if still red.'
max_turns: 100
timeout_seconds: 2400
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, SendMessage, Skill]
runs: 1
---

/s2tdd-implement W2
