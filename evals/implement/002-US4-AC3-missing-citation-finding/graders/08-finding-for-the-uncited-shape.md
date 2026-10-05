---
type: llm
focus: last_message
weight: 1
---

This is the shape check's hand-back for wave 0's test packets P0a and P0b. P0a's report cites
§II-1 of contracts/internal-interfaces.md for its two tests. P0b's tests (test_quoting.py)
assert quote_field's quoting, a shape that wave W1 builds (P1b) and §II-2 states, and P0b's
report has no Cites: line. Pass if the hand-back carries a finding, as a findings line, for
P0b's quoting shape asserted with no citation (naming test_quoting.py or P0b, and §II-2 or
quote_field). Fail if the missing citation is not a finding (for example only a remark, or not
mentioned), or if the check treats P0b's tests as matching a citation they do not have.
