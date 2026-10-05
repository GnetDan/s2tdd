---
description: 'US2-AC8: Given an unhardened feature, a closed feature, or owned files held by another session, When the user runs a command that refuses that state today (implement, converge, close), Then it refuses with the same reason it gives today, under its `/s2tdd-` name.'
max_turns: 40
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Bash, Skill]
runs: 1
---

Run `/s2tdd-implement 006`, then `/s2tdd-implement 005`, then `/s2tdd-converge 004`, then `/s2tdd-close 004`, one after another. After each, say in one line what it said, and carry on to the next.
