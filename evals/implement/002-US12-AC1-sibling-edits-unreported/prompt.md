---
description: '002-US12-AC1: Given a packet whose working tree shows a sibling''s edits, When it reports, Then the report does not list them.'
max_turns: 150
timeout_seconds: 3600
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, SendMessage, Skill]
runs: 1
---

/s2tdd-implement --nobrakes W0
