---
type: llm
weight: 1
focus: trace
---

Judging the whole run: the agent noticed there is no `specs/constitution.md`, said in about one
line that `/s2tdd-constitution` creates one, and then carried on with the feature instead of
stopping or asking the user to run it first. Fail if it stopped, or if it wrote a constitution
of its own.
