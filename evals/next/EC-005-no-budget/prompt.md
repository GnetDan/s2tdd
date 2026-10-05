---
description: "EC-005: Given a project whose agent guidance file states no suite-time budget, When verify-done or converge records a suite run, Then the wall time is recorded and nothing is reported as over budget (T16)."
max_turns: 25
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill, Bash]
---

/s2tdd-next

The project is the git repository in ./acme-notes: work there.
