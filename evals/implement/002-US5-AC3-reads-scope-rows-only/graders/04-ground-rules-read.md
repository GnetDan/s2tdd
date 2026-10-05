---
type: llm
focus: trace
weight: 1
---

Judging the orchestrator's own tool calls in a run of `/s2tdd-implement W8-W10`, up to its
first packet dispatch. Pass if, by then, it had read orchestration.md's Ground rules section
(by its line range, after listing the file's headings), the rows of W8, W9 and W10, and the
tasks T017-T022 (W8's T017-T018, W9's T019-T020, W10's T021-T022). Fail if any of the three is
missing when the first packet is dispatched.
