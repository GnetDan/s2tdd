---
type: tool_used
tool: Bash
input_match: 'T0(1[7-9]|2[0-2])\b|T01\[7|T02\[0|T0\\*\((1\\*\[|2\\*\[|17|18|19|20|21|22)'
min: 1
weight: 1
---

It read the tasks of W8-W10 (T017-T022) by their IDs, in any grep form (one ID, a class such as
`T01[7-9]`, or a group such as `T0(1[7-9]|2[0-2])` or `T0(17|18|…)`).
