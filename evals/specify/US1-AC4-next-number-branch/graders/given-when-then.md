---
type: regex
weight: 1
target:
  source: file
  path: specs/005-pin-notes/spec.md
pattern: 'Given\b\**\s+(?!\[)[^\n]*\bWhen\b\**\s+(?!\[)[^\n]*\bThen\b\**\s+(?!\[)'
---

The written draft states a scenario as Given, When, Then, filled in (not the template's
bracketed placeholders).
