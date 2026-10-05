---
description: "US7-AC4: Given duplicate or obsolete tests in a project, When `/s2tdd-foundation-review` or `/s2tdd-close` runs, Then they are listed as findings and no test is removed or skipped (T16)."
max_turns: 60
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Bash, Write, Edit]
---

/s2tdd-foundation-review docs/foundation-review.md

The project is the git repository in ./acme-notes: work there.
