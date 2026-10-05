---
type: tool_order
weight: 1
before:
  tool: Agent
  input_match: 's2tdd:hardener'
after:
  tool: Agent
  input_match: 's2tdd:converger'
---

The run resumes at the harden step: the hardener runs before any converger, so round 1's
converge is not run again.
