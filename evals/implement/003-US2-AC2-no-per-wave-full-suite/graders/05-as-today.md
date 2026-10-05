---
type: llm
focus: trace
weight: 1
---

Judging the whole run: the project declares no per-wave test command (CLAUDE.md has only
`Full suite: python -m pytest`; handoff.md's TEST RUN line reads `Per-wave tests: none`). When
W2 ended (P2a reported and the reviews, if any, were done), the orchestrator ran the full suite,
`python -m pytest`, once, and then committed the wave, as before 0.4.0. It did not invent a
per-wave command or pick a subset of the tests itself (no test paths, `-k` or `-m` of its own).
Fail if W2 was committed with no full-suite run, or if the wave's run was a subset.
