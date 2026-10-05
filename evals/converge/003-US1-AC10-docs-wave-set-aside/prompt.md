---
description: '003-US1-AC10: Given a ledger recording the docs wave as built and uncommitted, When converge runs, in the loop or by hand, Then it does not refuse for the docs wave''s unticked tasks and lists the docs wave as pending.'
max_turns: 60
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Bash, Edit, Write, Skill]
---

/s2tdd-converge
