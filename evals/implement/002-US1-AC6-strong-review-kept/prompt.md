---
description: "002-US1-AC6: Given a wave with strong packets and test packets, When its commit is due, Then each strong packet still gets its own strong-diff review in `--nobrakes`, as today, besides the wave's one shape check."
max_turns: 150
timeout_seconds: 3600
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, SendMessage, Skill]
runs: 1
---

/s2tdd-implement --nobrakes W0
