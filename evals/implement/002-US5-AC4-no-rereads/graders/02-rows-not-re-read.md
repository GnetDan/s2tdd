---
type: llm
focus: trace
weight: 1
---

Judging the orchestrator's own tool calls in a run of `/s2tdd-implement W0` (an attended wave
of three packets: test packets P0a and P0b, and P0c), from its first packet dispatch to the
wave commit. Ignore everything before the first dispatch, and everything from the closing
`/s2tdd-next` on. run-ledger.md's Amendments stay empty, so no section changes and none needs a
re-read. Pass if, in that span, the orchestrator never read W0's rows of orchestration.md
again (a grep of `| W0 `, a grep of every row, or a Read or `cat` of the wave table) after
having read them before the first dispatch, and used the rows it had already read to brief
packets, check cards and commit. Fail on any such re-read.
