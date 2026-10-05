---
type: regex
weight: 1
target:
  source: file
  path: specs/001-note-sharing/spec.md
pattern: '^(?:[\s\S]*?\[NEEDS CLARIFICATION(?!: (?:auth method|retention period) not specified)){4}'
---

Four or more open gaps are marked in the written draft: there is no cap on their number. The
spec template's two example markers do not count.
