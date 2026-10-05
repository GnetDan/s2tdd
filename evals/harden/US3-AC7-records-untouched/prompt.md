---
description: "US3-AC7: Given a carried-over feature whose `validation.md`, `run-ledger.md` and `tasks.md` name `/speckit-` commands, When the user runs `/s2tdd-harden handoff`, Then those three files are unchanged."
max_turns: 60
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Bash, Write, Edit, Agent]
---

/s2tdd-harden handoff

The project is the git repository in ./acme-notes: work there.
