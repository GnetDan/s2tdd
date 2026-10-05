---
description: "003-EC-001: Given a per-wave command that fails to run (a collection error, a missing plugin) rather than reporting red tests, When a wave ends, Then that wave and every later wave of the run run the full suite, and the ledger records `Per-wave runs off from wave <n>: <first error line>` as a Carried constraint."
max_turns: 140
timeout_seconds: 3300
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, SendMessage, Skill]
runs: 1
---

/s2tdd-implement W1-W2
