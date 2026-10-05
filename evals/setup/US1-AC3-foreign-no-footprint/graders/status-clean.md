---
type: llm
weight: 1
focus: trace
---

Judging the whole run: in this repository, whose remote belongs to someone other than the user,
first-run setup left `git status` in the project showing no change. The agent either ran
`git status --porcelain` and it printed nothing that setup caused, or it never touched a
tracked file. Fail if setup edited or added anything the project tracks, or if the agent said
it had to stop because of a change setup made.
