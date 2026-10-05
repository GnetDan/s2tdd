---
type: regex
target: last_message
pattern: '(\b(no|missing|without|lacks?)\b[^\n]{0,60}\b(citation|cites?|cited)\b|\buncited\b|\bCites:? line\b[^\n]{0,40}\b(missing|absent)\b)'
flags: i
weight: 1
---

A finding says the citation is missing.
