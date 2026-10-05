---
type: llm
focus: trace
weight: 1
---

Judging the orchestrator's own tool calls in a run of `/s2tdd-implement W8-W10` on a 16-wave
feature whose tasks are T001-T032 (W8-W10's are T017-T022; W0-W7's T001-T016 are ticked), from
the start of the run up to its first packet dispatch. Pass if in that span it read no task of
another wave (T001-T016, T023-T032). Fail if it did: a grep naming another wave's task, a grep
that prints every open task (W11-W15's included; taking only the first open task, as with
`grep -m 1`, is allowed), `cat` of tasks.md, or a Read of tasks.md whose range takes in other
waves' tasks. Ignore everything after the first dispatch, the closing `/s2tdd-next` included.
