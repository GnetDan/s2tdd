---
type: llm
focus: trace
weight: 1
---

Judging only what the agent itself wrote to the user (not text from a skill, page or file it
read, nor tool output): once, before the first wave's first dispatch, the agent said that
handoff.md predates the shape check, that its rules run as written, and that
`/s2tdd-harden handoff` refreshes it. Fail if it never said so, said so only inside loaded
skill or file text, repeated it for each wave or packet, or stopped the run to ask for the
refresh.
