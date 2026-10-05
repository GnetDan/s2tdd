---
description: '003-US1-AC5: Given a run that stopped at its harden step, When the user has fixed the cause and reruns `/s2tdd-implement --nobrakes`, Then the run resumes from the ledger at the harden step.'
max_turns: 300
timeout_seconds: 7200
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, SendMessage, Skill]
runs: 1
---

/s2tdd-implement --nobrakes
