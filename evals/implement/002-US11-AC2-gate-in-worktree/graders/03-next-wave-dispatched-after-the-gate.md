---
type: tool_order
weight: 1
before:
  tool: Agent
  input_match: 'proxy-verifier'
after:
  tool: Agent
  input_match: '(?=[\s\S]*packet-(?:strong|cheap))(?=[\s\S]*\b(?:P1a|P1b|T004|T005)\b)'
---

W1's packets (P1a, P1b) are dispatched after the gate's verifier, not before it.
