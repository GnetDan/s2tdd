---
description: "002-US1-AC4: Given a `--nobrakes` run whose shape check finds a test asserting a shape that differs from its cited section, When the orchestrator handles the finding, Then the test packet's own agent fixes the test before the wave commit, and a short re-check covers the disputed items."
max_turns: 150
timeout_seconds: 3600
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, SendMessage, Skill]
runs: 1
---

/s2tdd-implement --nobrakes W0
