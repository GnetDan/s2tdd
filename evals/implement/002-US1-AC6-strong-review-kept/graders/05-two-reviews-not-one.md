---
type: llm
focus: trace
weight: 1
---

Judging the whole run: before W0's wave commit in this --nobrakes run, the strong packet P0c's
uncommitted diff went to its own read-only strong-diff review (the Strong-diff reviewer brief,
with P0c's Decision lines), and, separately, the wave's test packets P0a and P0b got one shape
check (the Shape check brief). The shape check did not replace P0c's review, and P0c's review
did not stand in for the shape check. Fail if either was skipped or the two were merged into
one dispatch.
