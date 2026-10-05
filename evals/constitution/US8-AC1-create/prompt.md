---
description: "US8-AC1: Given no `specs/constitution.md`, When the user runs `/s2tdd-constitution`, Then it grills them and writes `specs/constitution.md` from its bundled template (T11)."
max_turns: 40
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Bash, Write, Edit]
---

/s2tdd-constitution Principles: tests come first; changes stay small; no secret is ever committed. That is enough: leave anything else open as a TODO.

The project is the git repository in ./acme-notes: work there.
