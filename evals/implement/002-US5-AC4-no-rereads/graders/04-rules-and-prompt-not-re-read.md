---
type: llm
focus: trace
weight: 1
---

Judging the orchestrator's own tool calls in a run of `/s2tdd-implement W0`, from its first
packet dispatch to the wave commit. Ignore everything before the first dispatch, and
everything from the closing `/s2tdd-next` on. run-ledger.md's Amendments stay empty
throughout. Pass if, in that span, the orchestrator never re-read a section it had already
read this session: orchestration.md's Ground rules (or its headings list), handoff.md's fenced
prompt, or a Standard brief it had already read. Reading a section for the first time when a
step first needs it (such as the Shape check brief, or Expected red) is not a re-read. Fail on
any re-read.
