---
description: 'US2-AC4: Given a hardened feature, When the user runs `/s2tdd-harden` naming one phase, or asking to append new tasks or refresh, Then it runs only that mode, as today''s harden does (T07).'
max_turns: 50
timeout_seconds: 1800
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Skill]
runs: 1
---

/s2tdd-harden handoff
