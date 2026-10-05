---
description: "003-US1-AC4: Given a converge round that appended a task citing a scenario without an ID, When the hardener hardens the appended tasks, Then the run stops, and the run summary carries harden's stop message."
max_turns: 150
timeout_seconds: 3600
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, SendMessage, Skill]
runs: 1
---

/s2tdd-implement --nobrakes
