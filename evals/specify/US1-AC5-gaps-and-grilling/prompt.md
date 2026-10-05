---
description: "US1-AC5: Given a description that leaves design questions open, When `/s2tdd-specify` drafts the spec, Then every open gap is marked in the draft with no cap on their number and no informed guesses, and the command grills the user, one round at a time with a recommended answer per question, until the gaps are resolved or the user says enough (T07)."
max_turns: 40
timeout_seconds: 600
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Skill]
---
/s2tdd-specify let people share their notes with other people

Use `note-sharing` as the short name.

I am at the keyboard and will answer your questions.
