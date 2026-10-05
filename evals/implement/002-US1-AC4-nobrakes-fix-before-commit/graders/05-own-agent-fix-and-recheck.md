---
type: llm
focus: trace
weight: 1
---

Judging the whole run: W0's shape check found that P0a's test asserts CRLF row ends while the
section it cites, II-1, says LF. The orchestrator sent that disputed citation back to P0a's own
agent (the agent that wrote the test, continued with its context, not a fresh packet and not the
orchestrator editing the test itself); that agent fixed the test; then a short re-check covered
the disputed items (not a full second shape check of the whole wave); and all of this happened
before W0's wave commit. Fail if the wave was committed with the CRLF test, if the orchestrator
edited the test itself, or if no re-check followed the fix.
