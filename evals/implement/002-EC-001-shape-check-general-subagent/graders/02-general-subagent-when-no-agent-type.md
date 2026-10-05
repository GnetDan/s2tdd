---
type: llm
focus: trace
arm: both
weight: 1
---

Judging the whole run. Find out first whether the session offered s2tdd's agent types
(`s2tdd:strong-diff-reviewer`, `s2tdd:packet-medium`, ...): they are missing when the run used
the project's copy of the skills in `.claude/skills/` with no plugin loaded, which shows as a
dispatch to such a type failing or as the type not being among those the session offers.

- If they were missing: W0's shape check still ran, in a general subagent (no `s2tdd:` agent
  type), with the same Shape check brief from handoff.md's Standard briefs, after the test
  packets P0a and P0b reported; and the orchestrator said once, at whatever point it found the
  types missing, that packets run at the session's effort. Fail if the shape check was
  skipped, ran in the orchestrator's own context, or got a brief of the orchestrator's own
  instead of the Shape check brief.
- If they were offered: the shape check ran as `s2tdd:strong-diff-reviewer` with the Shape
  check brief. Fail if it ran as a general subagent while the type was offered.
