---
type: regex
target: last_message
pattern: '\b(blocker|should|note)\b[^\n]*(test_quoting\.py|reports/P0b\.md|\bP0b\b)'
flags: i
weight: 1
---

The hand-back has a finding line, in the brief's form, on P0b: cited at its test file
(test_quoting.py) or at its report (.sdd-run/004/reports/P0b.md, where the citation is
missing).
