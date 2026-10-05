---
type: llm
focus: trace
weight: 1
---

Judging the whole run: when wave W0's shape check was due (its test packets P0a and P0b had
reported and their reds were confirmed), the orchestrator dispatched it as the
`s2tdd:strong-diff-reviewer` agent type, and the briefing was the Shape check brief from
handoff.md's `## Standard briefs` (`### Shape check`), filled for W0's test packets, not the
Strong-diff reviewer brief and not a brief of its own. Fail if the shape check ran as a general
subagent, as a packet agent type, or in the orchestrator's own context.
