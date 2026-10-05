---
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill, "Bash(printenv:*)"]
description: "US6-AC6: Given a cloud session, When the user starts `/s2tdd-pr-review` there, Then it refuses and says to start it locally with `--cloud` (T05)."
---

/s2tdd-pr-review 1
