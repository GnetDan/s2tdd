---
type: llm
name: uses-main-worktree-specs-and-says-so
weight: 1
focus: last_message
---

The user ran `/s2tdd-harden` from a worktree that has no `./specs`. The reply says it is using `specs/` from the main worktree (a line such as "Using specs/ from the main worktree at <path>.") and describes its spec writes as landing there, not in the worktree.
