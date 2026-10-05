---
description: "003-EC-004: Given a wave whose per-wave run selects no tests and prints a summary saying so, When the wave ends, Then the run counts it green, the wave report says `0 selected`, and later waves keep using the per-wave command."
max_turns: 140
timeout_seconds: 3300
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, SendMessage, Skill]
runs: 1
---

/s2tdd-implement W1-W2
