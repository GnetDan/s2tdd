---
description: "003-US2-AC7: Given an attended implement session in a project that declares a per-wave command, When its last wave commits, Then its final report says that the slice's full run is the user's `/s2tdd-verify-done`."
max_turns: 100
timeout_seconds: 2400
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, SendMessage, Skill]
runs: 1
---

/s2tdd-implement W2
