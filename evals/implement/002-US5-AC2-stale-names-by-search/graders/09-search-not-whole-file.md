---
type: llm
focus: trace
weight: 1
---

Judging the whole run of `/s2tdd-implement` on a feature whose orchestration.md (a long file)
still names an old `/speckit-` command and whose handoff.md names none: the orchestrator found
the stale name with a search that prints only the file names or the matching lines (such as
`grep -lE '/speckit-[a-z]' <both files>`), and stopped, naming orchestration.md and saying to
run `/s2tdd-harden handoff` first. Fail if at any point it loaded handoff.md or orchestration.md
whole into its context (a Read with no line range, `cat`, or a grep that prints the whole file),
or if it dispatched anything or edited either file.
