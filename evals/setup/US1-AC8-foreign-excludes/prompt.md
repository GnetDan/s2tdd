---
description: "US1-AC8: Given a repository whose remote belongs to someone other than the user, When first-run setup writes the local excludes, Then they list `specs/`, `.sdd-run/` and `.claude/skills/s2tdd-*/` (T09, T10)."
max_turns: 40
timeout_seconds: 600
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Skill]
---
/s2tdd-specify add tags so notes can be labelled

Stop after the first draft: enough questions.
