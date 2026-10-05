---
type: llm
focus: trace
weight: 1
---

verify-done lists P0c (T003, cli.py) as a gap because its report quotes no red run, while W0's
wave report's Red runs line shows `python cli.py --help` failing before dispatch. Both seeded red-run gaps are reported, the late one and the missing one (SC-003).
