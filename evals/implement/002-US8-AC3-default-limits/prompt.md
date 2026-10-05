---
description: '002-US8-AC3: Given a run started without limits named, When it starts, Then it uses week 95% and five-hour 90%, and records them as Carried constraints.'
max_turns: 150
timeout_seconds: 3600
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, Skill]
runs: 1
---

/s2tdd-implement --nobrakes W0
