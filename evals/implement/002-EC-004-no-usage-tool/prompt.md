---
description: '002-EC-004: Given a `--nobrakes` run in a harness with no usage tool and no plan windows (Cursor, for one), When the run starts, Then it says once that the window limits do not apply, records that as a Carried constraint, and writes `n/a` for the windows in each Boundary line.'
max_turns: 150
timeout_seconds: 3600
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, Skill]
runs: 1
---

/s2tdd-implement --nobrakes W0
