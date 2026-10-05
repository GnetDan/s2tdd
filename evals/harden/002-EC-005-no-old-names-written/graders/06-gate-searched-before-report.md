---
type: llm
focus: trace
weight: 1
---

Judging the whole run: after writing orchestration.md and handoff.md and before its completion
report, harden searched both files for old command names (its gate's `grep -lE` for the slash,
the old prefix and a letter, or an equivalent search of those two files), reworded any hit, and
the last search found none. Its completion report does not list an old command name as left in
either file and reports no failed gate. Fail if the report came before any such search, or if
the report says a hit was left in place.
