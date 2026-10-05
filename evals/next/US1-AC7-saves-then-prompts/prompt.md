---
description: "US1-AC7: Given any s2tdd command other than `/s2tdd-next` finishing normally, When it reaches its last step, Then it runs `/s2tdd-next`, which commits and pushes the active feature's (or epic's) files in the specs repository first and then prints the recap and the next step as a ready-to-paste prompt (T07, T08)."
max_turns: 50
timeout_seconds: 900
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Skill]
---
/s2tdd-specify add a CSV export for notes

Stop after the first draft: enough questions.
