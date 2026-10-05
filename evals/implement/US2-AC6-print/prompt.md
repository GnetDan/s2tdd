---
description: 'US2-AC6: Given a hardened feature, When the user runs `/s2tdd-implement --print`, Then it prints the filled implement prompt for another harness and runs nothing (T07).'
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Bash, Skill]
runs: 1
---

/s2tdd-implement --print
