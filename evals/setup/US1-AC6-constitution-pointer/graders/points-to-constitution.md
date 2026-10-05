---
type: llm
weight: 1
focus: trace
---

Judging only what the agent itself wrote to the user (not text from a skill, template, page or
file it read, nor tool output): in one of its own messages, the agent said that
`/s2tdd-constitution` creates `specs/constitution.md`. Fail if `/s2tdd-constitution` appears only
inside loaded skill or file text.
