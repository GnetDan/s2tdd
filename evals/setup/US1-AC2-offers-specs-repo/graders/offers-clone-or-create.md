---
type: llm
weight: 1
focus: trace
---

Judging the whole run: before it wrote anything under `specs/`, the agent told the user that
this repository has no specs repository and named the two ways to get one: clone an existing
one, or create a new one. It may then have followed the choice the user stated in the prompt.
Fail if it created `specs/` without ever naming the choice.
