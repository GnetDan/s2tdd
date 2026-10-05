---
description: "003-US2-AC2: Given a project that declares no per-wave test command, When a wave ends, Then the orchestrator runs the full suite, as today."
max_turns: 100
timeout_seconds: 2400
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, SendMessage, Skill]
runs: 1
---

/s2tdd-implement W2
