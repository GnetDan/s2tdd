---
description: "002-US4-AC1: Given a test packet whose tests assert a shape a later wave implements, When it reports, Then its report has one line per such shape citing `contracts/<file> §<section>`."
max_turns: 80
timeout_seconds: 2400
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, Skill]
runs: 1
---

/s2tdd-implement W0
