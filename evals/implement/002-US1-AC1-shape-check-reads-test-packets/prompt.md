---
description: "002-US1-AC1: Given a wave with three test packets, When the orchestrator reaches that wave's commit, Then one shape check has read all three packets' test diffs and the contract sections they cite, and its verdict is in the wave report's Review line."
max_turns: 90
timeout_seconds: 2700
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, Skill]
runs: 1
---

/s2tdd-implement W0
