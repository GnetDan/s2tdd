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

No packet runs before the hardener: the resumed run does not start over at W0.
