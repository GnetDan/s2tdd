---
description: 'US2-AC2: Given a plan''s `research.md`, When any s2tdd command writes a decision to it, Then the decision is an R-entry (`## Rn. <the decision as a sentence>`) with its rationale and alternatives under it (T11).'
max_turns: 60
timeout_seconds: 1800
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, Skill]
runs: 1
---

/s2tdd-plan
