---
type: tool_order
weight: 1
before:
  tool: SendMessage
  input_match: 'test_export_rows|CRLF'
after:
  tool: Bash
  input_match: 'git[^\n]*commit[\s\S]*wave 0'
---

The finding is sent back for a fix before the wave 0 commit.
