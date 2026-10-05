---
description: '002-US11-AC2: Given a verify gate at a slice end, When the verifier runs, Then it runs in a scratch worktree at the gate''s tag, and the next wave starts while it runs, its packets holding their test runs until the verifier''s suite ends.'
max_turns: 200
timeout_seconds: 5400
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, SendMessage, Skill]
runs: 1
---

/s2tdd-implement --nobrakes W0-W1
