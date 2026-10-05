---
description: "US7-AC2: Given a suite-time budget stated in the project's agent guidance file and a verify-done or converge run whose full suite exceeds it, When the user runs `/s2tdd-next`, Then the recorded wall time and the budget show under Watch out, and nothing refuses because of it (T16)."
max_turns: 25
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill, Bash]
---

/s2tdd-next

The project is the git repository in ./acme-notes: work there.
