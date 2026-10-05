---
description: '002-US6-AC1: Given a review finding that a packet breaks a spec MUST, When the orchestrator handles it in a `--nobrakes` run, Then the packet fixes it before the wave commit, or is BLOCKED, and the finding is never recorded under Open review notes.'
max_turns: 150
timeout_seconds: 3600
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, Skill]
runs: 1
---

/s2tdd-implement --nobrakes W0
