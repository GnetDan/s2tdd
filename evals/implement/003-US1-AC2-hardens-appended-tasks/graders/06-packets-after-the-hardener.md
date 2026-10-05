---
type: tool_order
weight: 1
before:
  tool: Agent
  input_match: 's2tdd:hardener'
after:
  tool: Agent
  input_match: 's2tdd:packet-(cheap|medium|strong)'
---

The run implements the hardened tasks: packets are dispatched after the hardener reports.
