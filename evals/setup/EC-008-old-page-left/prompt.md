---
description: "EC-008: Given a project where an earlier, unmigrated copy of a project page exists (`docs/sdd-workflow.md`), When first-run setup copies the pages, Then it writes `specs/WORKFLOW.md`, leaves the old file in place, and `/s2tdd-next` reports it as a leftover (T10)."
max_turns: 50
timeout_seconds: 900
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Skill]
---
/s2tdd-specify add tags so notes can be labelled

Stop after the first draft: enough questions.
