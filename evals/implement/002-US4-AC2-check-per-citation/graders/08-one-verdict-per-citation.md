---
type: llm
focus: last_message
weight: 1
---

This is the shape check's hand-back for wave 0's test packets P0a and P0b, whose reports cite
three shapes: P0a's header-and-rows test (§II-1), P0a's line-end test (§II-1) and P0b's quoting
tests (§II-2), all in contracts/internal-interfaces.md. Pass if the hand-back says, for each of
the three citations, whether the test matches the cited section: the header-and-rows and the
quoting citations match, and the line-end citation differs, stating what the test asserts (CRLF
row ends) against what the section says (LF on every platform). Fail if any citation has no
verdict of its own, if the line-end citation is said to match, or if the hand-back gives only
an overall verdict.
