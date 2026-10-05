---
type: regex
target: last_message
pattern: 'docs wave[^\n]{0,120}pending|pending[^\n]{0,120}docs wave'
match: contains
flags: i
weight: 1
---

Converge's summary lists the docs wave as pending (docs wave (pending)).
