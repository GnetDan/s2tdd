---
description: "002-EC-003: Given a packet escalated after failing its fence twice, When it is re-dispatched one tier up, Then the agent it goes to runs at a higher effort than the first (cheap low → medium medium → strong high), with the failure reports attached."
max_turns: 150
timeout_seconds: 3600
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, Skill]
runs: 1
---

/s2tdd-implement --nobrakes W1
