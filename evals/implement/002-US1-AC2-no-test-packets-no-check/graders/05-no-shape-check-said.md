---
type: llm
focus: trace
weight: 1
---

Judging the whole run: wave W2, which holds only the implementation packet P2a, ran to its
commit with no shape check. The orchestrator did not dispatch a reviewer for a shape check, did
not ask for one, and recorded `shape check: none` for the wave. Fail if any shape check ran for
W2 or if the run stopped before W2's commit for a reason to do with a shape check.
