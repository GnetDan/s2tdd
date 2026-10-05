---
description: '002-US13-AC1: Given a `--nobrakes` wave commit, When the boundary steps run, Then the wave report carries `Boundary: context <x>% · five-hour <y>% · week <z>% · BRAKES <none|found> · ledger +<n> lines`.'
max_turns: 150
timeout_seconds: 3600
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, Skill]
runs: 1
---

/s2tdd-implement --nobrakes W2
