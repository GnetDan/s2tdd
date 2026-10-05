---
description: "002-EC-002: Given a feature hardened before this change (its handoff.md has no shape check), When it is implemented with the new plugin, Then its handoff's rules hold unchanged, and implement says once that the handoff predates the shape check and that `/s2tdd-harden handoff` refreshes it."
max_turns: 90
timeout_seconds: 2700
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, Skill]
runs: 1
---

/s2tdd-implement W0
