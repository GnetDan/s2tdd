---
type: tool_used
tool: Agent
input_match: '^(?=[\s\S]*s2tdd:packet-medium)(?=[\s\S]*\bP1b\b)(?![\s\S]*check_quoting[^\n]*(FAIL|failed))'
min: 0
max: 0
weight: 1
---

No escalated P1b dispatch goes out without the failures: every `s2tdd:packet-medium` briefing
for P1b carries the guard's own failure output from the earlier attempts' reports. Any guard
failure line counts: `check_quoting: FAIL …` or the summary line
`check_quoting: <n> of <m> cases failed` (for example `check_quoting: 5 of 14 cases failed`).
No P1b briefing before a failure can hold such a line.
