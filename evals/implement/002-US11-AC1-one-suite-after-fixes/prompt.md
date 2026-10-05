---
description: '002-US11-AC1: Given a wave whose review asks for fixes, When the wave completes, Then the full suite ran once, after the fixes.'
max_turns: 150
timeout_seconds: 3600
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, SendMessage, Skill]
runs: 1
---

/s2tdd-implement --nobrakes W0
