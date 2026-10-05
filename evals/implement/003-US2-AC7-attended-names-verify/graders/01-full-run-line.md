---
type: regex
target: last_message
pattern: 'Full run for this slice: `?/s2tdd-verify-done reports: specs/004-csv-export/s1-wave-reports\.md; commits [0-9a-f]{7,40}\.\.[0-9a-f]{7,40}'
weight: 1
---

The final report ends with the attended stop's line (RR-9): the slice's full run is the user's
`/s2tdd-verify-done` on the wave-reports file and the session's commits.
