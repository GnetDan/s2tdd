---
type: llm
focus: trace
weight: 1
---

Close checks the docs wave first: it reads run-ledger.md's `Docs wave 3 built, uncommitted:
README.md`, sees README.md still uncommitted in the project, and stops there. It does not ask
the user to decide T007 (delivered or dropped), run the test suite, commit README.md itself or
write any file in the feature directory before stopping.
