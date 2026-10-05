---
type: llm
focus: trace
weight: 1
---

Judging the whole run: W0's three packets ran in one working tree, so each could see the files
its siblings were writing. No packet's card (the hand-back the orchestrator receives) lists a
sibling's file: no `Out of bounds:`, `Unexpected:` or other line about `test_export_rows.py`,
`test_quoting.py` or `cli.py` from a packet that does not own it, and no "not mine" note about
files in the tree. The orchestrator did not treat a sibling's edits as a packet writing outside
its files. Fail if any packet's card or report spends a line on a sibling's edits.
