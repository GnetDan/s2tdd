---
description: '002-US7-AC2: Given a ledger whose Carried constraints changed during the run, When a relay writes its handoff prompt, Then the prompt points at Carried constraints and restates none of them.'
max_turns: 150
timeout_seconds: 3600
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, Skill]
runs: 1
---

/s2tdd-implement --nobrakes W2-W3
