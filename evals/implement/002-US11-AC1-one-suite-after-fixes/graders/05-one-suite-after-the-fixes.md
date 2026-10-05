---
type: llm
focus: trace
weight: 1
---

Judging the whole run: W0's review asked for a fix (its shape check found that P0a's test
asserts CRLF row ends while II-1 says LF, or P0c's strong-diff review asked for a change). The
orchestrator ran the wave's reviews and shape check, then their fixes (and any short re-check of
the disputed items), then the full suite once, then the wave commit. Count the orchestrator's
full-suite runs in W0 (pytest over the whole project, not a run that names test files): exactly
one, and it came after the last fix had landed. Fail if a full suite ran before the fixes and
again after them, if a second full suite ran to check a review fix, or if the wave was committed
with no full suite after the fixes.
