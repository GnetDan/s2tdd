---
description: "US3-AC3: Given a hardened, unfinished feature carried over from the preset, When the user runs `/s2tdd-harden handoff`, Then its `handoff.md` and `orchestration.md` name only `/s2tdd-` commands, and `/s2tdd-implement` resumes at the wave it had reached (T10)."
max_turns: 60
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Bash, Write, Edit, Agent]
---

/s2tdd-harden handoff

The project is the git repository in ./acme-notes: work there.
