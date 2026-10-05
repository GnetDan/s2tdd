---
max_turns: 40
allowed_tools: [Read, Write, Edit, Glob, Grep, Skill, "Bash(git:*)"]
description: "US6-AC4: Given a desktop-app worktree with no `./specs`, When the user runs a command, Then it uses the main worktree's `specs/`, says so, and its spec writes land in the one specs repository (T08)."
---

I am working in the git worktree ./acme-notes-worktree (its main checkout is ./acme-notes). From the worktree, run /s2tdd-harden.
