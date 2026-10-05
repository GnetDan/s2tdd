---
type: llm
focus: trace
weight: 1
---

Judging the whole run: after the three test packets of wave W0 (P0a, P0b, P0d) reported and the
orchestrator confirmed their reds, it dispatched one shape check as `s2tdd:strong-diff-reviewer`
with the Shape check brief, and that brief had the reviewer read every one of the three
packets' test diffs, the Cites: lines in their reports and the contract sections they cite.
The orchestrator then put the shape check's verdict in W0's wave report's Review line before
or with the wave commit. Fail if the shape check left out any of the three packets, if more
than one shape check ran for the wave, or if the verdict is missing from the Review line.
