---
description: 'US2-AC1: Given a specified feature and a `specs/constitution.md`, When the user runs `/s2tdd-plan`, Then it writes `plan.md`, `research.md`, `data-model.md`, `contracts/` and `quickstart.md` with the structure and adaptations T11 lists, and a constitution violation stops the plan unless it is justified in the plan (T11).'
max_turns: 60
timeout_seconds: 1800
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, Skill]
runs: 1
---

/s2tdd-plan
