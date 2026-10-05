---
description: "003-US2-AC4: Given a project whose `Per-wave sees:` line is `*.py` and a wave that changes a prompt file, When the wave ends, Then it runs the full suite, not the per-wave command."
max_turns: 90
timeout_seconds: 2400
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, SendMessage, Skill]
runs: 1
---

/s2tdd-implement W3
