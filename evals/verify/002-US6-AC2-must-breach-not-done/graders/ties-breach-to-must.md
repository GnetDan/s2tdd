---
type: llm
focus: trace
weight: 1
---

verify-done finds that W2's export.py leaves out every note whose text is empty, and ties that
committed change to spec.md's FR-001 ("The system MUST write notes to CSV with one row per
note"; US1-AC1) as a change that contradicts a spec MUST, which makes the verdict Not done. It
finds it from the diff against spec.md: no wave report, review or test raised it.
