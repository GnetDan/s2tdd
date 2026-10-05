---
description: '003-US1-AC11: Given a docs wave still uncommitted, When the user runs `/s2tdd-close`, Then close stops and asks for the docs wave to be reviewed and committed first.'
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Bash, Edit, Write, Skill]
---

/s2tdd-close
