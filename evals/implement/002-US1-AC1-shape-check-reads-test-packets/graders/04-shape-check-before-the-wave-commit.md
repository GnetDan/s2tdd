---
type: tool_order
weight: 1
before:
  tool: Agent
  input_match: 'strong-diff-reviewer'
after:
  tool: Bash
  input_match: 'git[^\n]*commit[\s\S]*wave 0'
---

The shape check runs before the wave 0 commit.
