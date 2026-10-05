---
description: "US3-AC2: Given a project that still has `.specify/`, any `speckit-*` skill or `docs/sdd-workflow.md`, When the user runs `/s2tdd-next`, Then each one is listed under Watch out (T10)."
max_turns: 25
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill, Bash]
---

/s2tdd-next

The project is the git repository in ./acme-notes: work there.
