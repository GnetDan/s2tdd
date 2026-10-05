---
description: 'US2-AC3: Given a planned feature with no `tasks.md`, When the user runs `/s2tdd-harden`, Then one run writes `tasks.md` test-first and the hardened files (orchestration, handoff, validation, run ledger), and passes its validation gates (T07).'
max_turns: 80
timeout_seconds: 2400
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Skill]
runs: 1
---

/s2tdd-harden
