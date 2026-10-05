---
type: tool_order
weight: 1
before:
  tool: Bash
  input_match: 'git -C \S*specs commit'
after:
  tool: Bash
  input_match: 'git -C \S*specs push'
---

The commit comes before the push.
