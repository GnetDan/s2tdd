---
description: '002-US14-AC1: Given a verify gate, When the orchestrator fills the Proxy verifier brief, Then the brief names the expected-red rows and the accepted deviations for its waves.'
max_turns: 200
timeout_seconds: 5400
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, Skill]
runs: 1
---

/s2tdd-implement --nobrakes W2-W3
