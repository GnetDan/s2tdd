---
description: "002-US1-AC3: Given an implement run in either mode, When a wave's shape check is due, Then it is dispatched as the `strong-diff-reviewer` agent type with the Shape check brief."
max_turns: 150
timeout_seconds: 3600
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, SendMessage, Skill]
runs: 1
---

/s2tdd-implement --nobrakes W0
