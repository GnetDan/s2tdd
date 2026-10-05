---
description: "US9-AC1: Given a feature whose PR has merged and whose branch still exists locally and on the remote, When the user runs `/s2tdd-next`, Then both branches are listed under Watch out with the commands to delete them, and nothing is deleted (T15)."
max_turns: 25
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill, Bash]
---

/s2tdd-next 004

The project is the git repository in ./acme-notes: work there.
