---
type: llm
focus: trace
weight: 1
---

Judging the orchestrator's own tool calls in a run of `/s2tdd-implement W8-W10` on a 16-wave
feature (W0-W15; W0-W7 done), from the start of the run up to its first packet dispatch. Pass
if in that span it read no row of another wave (W0-W7, W11-W15) of orchestration.md's wave
table. Fail if it did: a grep naming another wave's row, a grep that prints every wave row
(such as `grep '^| W'`), `cat` of orchestration.md, or a Read of orchestration.md whose range
takes in the wave table's other rows. Listing headings, and reading another section by its line
range when a step needs it (such as Expected red or Context budget), is allowed. Ignore
everything after the first dispatch, the closing `/s2tdd-next` included.
