---
description: "US1-AC2: Given a repository the user owns with no `specs/` directory, When the user runs `/s2tdd-specify` for the first time there, Then it offers to clone or create the specs repository, copies `specs/README.md` and `specs/WORKFLOW.md` in, and adds only `specs/` and `.sdd-run/` to the local excludes (T09, T10)."
max_turns: 40
timeout_seconds: 600
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Skill]
---
/s2tdd-specify add a CSV export for notes

I have no specs repository yet. If you offer a choice, I take creating a new one for this
project, kept local (no GitHub account is connected here). Stop after the first draft: enough
questions.
