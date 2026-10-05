---
type: llm
focus: trace
weight: 1
---

Converge compares the sha of the newest `· green at <sha>` verification-log line with
`git rev-parse --short HEAD`, sees that HEAD is the later commit (refactor(004): name the CSV
delimiter), and so runs the suite rather than reusing the green run.
