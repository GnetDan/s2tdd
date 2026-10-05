---
type: tool_order
weight: 1
before:
  tool: Bash
  input_match: 'command\W+(?:(?:[^"\\]|\\.)*?(?:[;&|(]\s*|\\n\s*|python[\w.]*\s+-m\s+|/))?pytest\b(?!(?:\\[^n]|[^"\\\n;&|)])*?not slow)(?:(?!\.py\b|::)(?:\\[^n]|[^"\\\n;&|)]))*(?:$|"|\\n|[\n;&|)])'
after:
  tool: Bash
  input_match: 'git[^\n]*commit[\s\S]*wave 3'
---

The full suite runs before the wave 3 commit.
