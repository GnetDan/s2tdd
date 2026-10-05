---
description: "US3-AC4: Given a hardened feature whose `handoff.md` or `orchestration.md` still names `/speckit-` commands, When the user runs `/s2tdd-implement`, with or without `--nobrakes`, Then it stops before dispatching anything and says to run `/s2tdd-harden handoff` first."
max_turns: 25
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill, Bash, Write, Edit, Agent]
---

/s2tdd-implement

The project is the git repository in ./acme-notes: work there.
