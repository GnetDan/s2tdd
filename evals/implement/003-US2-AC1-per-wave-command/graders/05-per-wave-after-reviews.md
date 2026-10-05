---
type: llm
focus: trace
weight: 1
---

Judging the whole run: the project declares a per-wave test command (CLAUDE.md and handoff.md's
TEST RUN: `Per-wave tests: python -m pytest -q -m "not slow"`, `Full suite: python -m pytest`,
`Per-wave sees: *.py`). W2's only packet, P2a, changed `export.py` alone. After P2a reported and
W2's reviews (if any) were done, the orchestrator ran the per-wave command exactly as written,
passing it nothing (no test paths or `-k` it chose itself), once, and then committed the wave.
It never ran the full suite (`python -m pytest` with no marker filter) in the wave. Fail if the
orchestrator ran the full suite, ran the per-wave command with arguments of its own, or
committed W2 with no wave test run.
