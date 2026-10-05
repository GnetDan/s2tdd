---
type: llm
focus: trace
weight: 1
---

Judging the whole run: the project's `Per-wave sees:` line is `*.py`, and W3 (P3a, T007)
changed `assistant-prompt.md`, the notes assistant's prompt, which no `*.py` glob matches. When
W3 ended, the orchestrator found the wave's changed files (`git diff --name-only HEAD` and the
untracked files), saw a file outside Per-wave sees, and ran the full suite (`python -m pytest`)
in place of the per-wave command, once, before the wave commit; the wave report names why.
Fail if it ran the per-wave command for W3, ran both, or committed W3 with no test run.
