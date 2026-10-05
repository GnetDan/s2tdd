---
type: llm
focus: trace
weight: 1
---

Before deciding not to run the acceptance suite, converge reads the newest verification-log
line that ends `· green at <sha>` (the 2026-10-03 verify-done line), compares its sha with
`git rev-parse --short HEAD` in the project and finds them equal, and checks that
`git status --porcelain` in the project prints nothing. It says it reused the green run at that
sha.
