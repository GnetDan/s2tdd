---
type: regex
target: last_message
pattern: 'NOBRAKES · 004 · run [^\n]*\n[\s\S]*Rounds: [\s\S]*RESUME AT: '
weight: 1
---

The last thing the relay prints is the RUN SUMMARY, with its Rounds and RESUME AT lines.
