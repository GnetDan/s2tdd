---
type: tool_order
weight: 1
before:
  tool: Agent
  input_match: 's2tdd:converger'
after:
  tool: Agent
  input_match: 's2tdd:hardener'
---

The hardener runs after the converge round that appended the tasks.
