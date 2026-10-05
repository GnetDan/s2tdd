---
description: "003-EC-002: Given a nobrakes run that ends its waves with a blocked packet that is neither the MVP nor a guard test's, When no wave is left, Then the run stops before converge, and the run summary names the blocked packets and their skipped dependents."
max_turns: 80
timeout_seconds: 1800
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, SendMessage, Skill]
runs: 1
---

/s2tdd-implement --nobrakes
