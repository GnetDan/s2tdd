# Getting started

[← Back to the README](../README.md)

## Install

In Claude Code, at user scope:

```text
/plugin marketplace add GnetDan/s2tdd
/plugin install s2tdd@s2tdd
```

Updating the plugin updates the commands. Nothing else needs installing at runtime.

## Your first feature

1. **Start.** In your project, run `/s2tdd-specify` with a sentence or two about a feature you
   can already describe, or `/s2tdd-epic` for something big and unclear.
2. **Follow the chain.** Each command ends by printing the next step as a prompt you can paste.
   When you lose your place, run `/s2tdd-next`.
3. **Take your time on the questions.** The spec's scenarios become the tests, so the answers
   you give here decide what gets built. See [Models and budget](models.md).

## First-run setup

Setup happens on its own. The first `/s2tdd-specify`, `/s2tdd-epic` or `/s2tdd-constitution` in
a repository checks that it is set up. It only adds; it never deletes or rewrites.

| It adds | When | Why |
|---|---|---|
| **A specs repository** at `specs/` | There is no `specs/` yet. It offers to clone your existing specs repository into place or create one (usually private, e.g. `<project>-specs`) | Specs kept out of the application's repository are never read as stale intent by agents working on the app, and the same specs follow you to every checkout |
| **The project pages**, `specs/README.md` and `specs/WORKFLOW.md` | They are missing | The spec lifecycle and the workflow rules, where every session can read them |
| **Local excludes** for `specs/` and `.sdd-run/` in `.git/info/exclude` | Always | The project's repository never tracks them |

In a repository you don't own (its remote's owner isn't your account), setup also excludes
`.claude/skills/s2tdd-*/` and checks that it left no tracked footprint.

## Three things to do once

- **Name the specs repository** in your agent guidance file (`CLAUDE.md` / `AGENTS.md`), so
  fresh clones (CI, cloud sessions, `/s2tdd-pr-review`) can fetch it themselves.
- **Turn on automatic deletion of head branches** in the repository's GitHub settings
  ("Automatically delete head branches"), so merged feature branches don't pile up on the
  remote. `/s2tdd-next` lists any that remain, with the commands to delete them.
- **Optionally**, run `/s2tdd-constitution` for the project's principles, and state a
  suite-time budget in your agent guidance file.

After that there's no upkeep: `/s2tdd-next` commits and pushes the feature's spec files at the
end of every step. Commands run from a git worktree use the main checkout's `specs/`.

## Without the plugin

Where the plugin can't run (Cursor Enterprise, where importing Claude Code plugins is off by
default, or a team that pins its tools in the repository), copy the plugin's `skills/` folders
into the project's `.claude/skills/`. Each skill is self-contained, with its bundled files
beside it and the shared rules stamped in, so the copy works as is.

Two things to know:

- **Agent types aren't part of the copy**, so implement falls back to a general subagent.
- **Use the plugin or the copy, never both.** Installing both in one project is not supported:
  Claude Code loads both, and every bare `/s2tdd-<name>` the chain prints runs the copy.
  `/s2tdd-next` warns when it finds a copy while the plugin is installed.

## Works with

| Agent | Support |
|---|---|
| [Claude Code](https://claude.com/claude-code) | Built and tested for it |
| Cursor | Best-effort. It imports user-scope Claude Code plugins (or reads the copy), and the commands use no placeholders that only Claude Code fills in |
| Anything else | Not tested or supported |

## Cursor and other harnesses

A few things an unattended run relies on are Claude Code's. Where one is missing, the run falls
back rather than stopping:

- **No usage tool**, or a plan without usage windows: the `week=` and `five-hour=` limits don't
  apply. The run says so once at the start, records it in the ledger, writes `n/a` for the
  windows in each `Boundary:` line, and estimates its context from the ledger.
- **No push notification**: a hand-off only prints its prompt.
- **No agent types** (a copy of the skills carries none): each packet runs as a general subagent
  with the same briefing, at the session's effort.

Full compatibility with other harnesses isn't a goal.

## Unattended hand-offs

- **`--nobrakes` hand-offs:** when an unattended run hands off, it prints the handoff prompt,
  sends a push notification where the harness can, and stops. Paste the prompt into a fresh
  session to carry on; no session ever starts another by itself. See
  [Running unattended](nobrakes.md).

## Claude desktop app extras

These only apply in the Claude desktop app and do nothing anywhere else.

- **`/s2tdd-pr-review --cloud`:** moves the session to a cloud session before any work and runs
  the review there unattended, cloning the specs repository (`--specs-repo`, or the one your
  agent guidance file names). In the cloud it prints the next step rather than chaining, and
  started from inside a cloud session it refuses. Use it if you'd rather spend cloud capacity
  than tie up a local session; the default local run does the same review.

## Coming from spec-kit?

[Coming from spec-kit](coming-from-spec-kit.md) lists what to uninstall and which command maps
to which. A project that ran the earlier preset edition of this workflow follows
[MIGRATING.md](../MIGRATING.md).
