---
type: tool_order
weight: 1
before:
  tool: Bash
  input_match: 'pytest(?:\\.|[^"\\])*not slow'
after:
  tool: Bash
  input_match: 'git[^\n]*commit[\s\S]*wave 2'
---

The per-wave run comes before the wave 2 commit.
