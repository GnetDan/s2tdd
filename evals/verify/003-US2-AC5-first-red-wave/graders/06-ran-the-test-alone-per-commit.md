---
type: llm
focus: trace
weight: 1
---

verify-done runs the full suite from CLAUDE.md's `Full suite:` line (python -m pytest), not the
per-wave command, and sees test_a_large_notebook_exports_one_row_per_note red, a red no wave
report names (every Test run line is a green per-wave run). It then runs that one test alone
at the slice's wave commits oldest first (W1's commit, then W2's), in a scratch worktree or
detached checkouts rather than by moving the main checkout's branch, finds it green at W1 and
red at W2, and stops there.
