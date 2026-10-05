---
type: llm
focus: trace
weight: 1
---

At its suite gate (A2), close reads the newest verification-log line that ends
`· green at <sha>` (the 2026-10-03 verify-done line over W0-W3), compares its sha with
`git rev-parse --short HEAD` in the project and finds them equal, and checks that
`git status --porcelain` in the project prints nothing; it then runs no suite and records the
reuse in the close-out's header, with the sha it reused.
