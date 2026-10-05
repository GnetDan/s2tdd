---
description: 'US2-AC5: Given a hardened feature and an orchestrating session started at a lower effort than a packet''s tier, When `/s2tdd-implement` dispatches that packet, Then the packet runs as the agent type for its tier, at that type''s own model and effort (T15).'
max_turns: 60
timeout_seconds: 1800
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, Skill]
runs: 1
---

/s2tdd-implement W2
