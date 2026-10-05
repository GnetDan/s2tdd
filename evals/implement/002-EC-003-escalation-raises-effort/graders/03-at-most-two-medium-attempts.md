---
type: tool_used
tool: Agent
input_match: '(?=[\s\S]*s2tdd:packet-medium)(?=[\s\S]*\bP1b\b)'
min: 0
max: 2
weight: 1
---

An escalated P1b goes one tier up, to `s2tdd:packet-medium` (effort medium, above packet-cheap's
low), for at most two attempts at that tier (Dispatching (5), FAILED FENCES). W1 holds no
medium packet of its own. A P1b that passes at its own tier is never escalated.
