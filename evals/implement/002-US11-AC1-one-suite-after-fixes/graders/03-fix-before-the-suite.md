---
type: tool_order
weight: 1
before:
  tool: SendMessage
  input_match: 'test_export_rows|P0a|II-1|CRLF|LF'
after:
  tool: Bash
  input_match: 'command\W+(?:(?:[^"\\]|\\.)*?(?:[;&|(]\s*|\\n\s*|python[\w.]*\s+-m\s+|/))?pytest\b(?:(?!\.py\b|::)(?:\\[^n]|[^"\\\n;&|)]))*(?:$|"|\\n|[\n;&|)])'
---

The review's fix goes back to the test packet's own agent before the full suite runs.
