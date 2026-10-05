---
description: "US1-AC4: Given a set-up repository on its default branch with features `001`–`003` in `specs/` and a remote-only branch `004-x`, When the user runs `/s2tdd-specify` with a description, Then it creates and switches to branch `005-<short-name>` and writes `specs/005-<short-name>/spec.md` with ID'd scenarios (T07)."
max_turns: 40
timeout_seconds: 600
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Skill]
---
/s2tdd-specify let people pin a note to the top of their list

Use `pin-notes` as the short name.

Stop after the first draft: enough questions.
