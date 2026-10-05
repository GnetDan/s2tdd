---
description: "003-US2-AC1: Given a project that declares a per-wave test command, When a wave's packets have reported and its reviews are done, Then the orchestrator runs the per-wave command, not the full suite, before the wave commit."
max_turns: 100
timeout_seconds: 2400
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, SendMessage, Skill]
runs: 1
---

/s2tdd-implement W2
