---
description: '002-US7-AC1: Given a relay that reaches its handoff, When it hands off, Then it prints the handoff prompt, sends a push notification where the harness can, and stops; it never starts the next relay as a scheduled task or a background session.'
max_turns: 150
timeout_seconds: 3600
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, Skill]
runs: 1
---

/s2tdd-implement --nobrakes W2-W3
