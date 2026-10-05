---
type: regex
target: last_message
pattern: 'tasks? in tasks\.md (is|are) unticked|finish implementing \(and verify\)'
match: not_contains
flags: i
weight: 1
---

Converge does not stop with the implementation-complete guard's refusal for the docs wave's
unticked task.
