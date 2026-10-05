# Migrating to s2tdd

This guide moves an existing project to the s2tdd plugin. It is written for two starting
points:

- **a project on spec-kit plus the tests-as-spec preset**: it has the preset and its
  extension installed, `speckit-*` skills, `docs/sdd-workflow.md` and a constitution under
  `.specify/memory/`;
- **a plain spec-kit project** (no tests-as-spec): it only needs uninstalling, then a fresh
  start. Skip the steps marked "preset only" and do the ones marked "plain spec-kit".
  [docs/coming-from-spec-kit.md](docs/coming-from-spec-kit.md) is the shorter page written for
  it, and either one works.

There is no migrator. The steps are manual, and each is small. A feature that is mid-flight at
migration time is supported, with one refresh (step 6): its layout is the same, so its files
carry over.

## 1. Close or pause the work in flight

Commit and push the project and, if it has one, its specs repository, and let no session run
in either.

## 2. Uninstall

Per project, in this order:

1. Plain spec-kit, when the project tracks `specs/` (spec-kit's default): give `specs/` its own
   repository first, as step 1 of [docs/coming-from-spec-kit.md](docs/coming-from-spec-kit.md)
   says. s2tdd writes no spec until `specs/` is its own repository, and first-run setup offers
   to create one only when `specs/` is missing.
2. Save the constitution, before `.specify/` goes. Move it from
   `.specify/memory/constitution.md` to `specs/constitution.md`, and if a copy already sits
   there, reconcile the two by diff, as step 4 says.
3. Move `.specify/` (including `feature.json`, which nothing reads any more),
   `.claude/skills/speckit-*/` and, preset only, `docs/sdd-workflow.md` aside into a dated
   backup folder outside the repository, for example `../s2tdd-migration-backup-<date>/`,
   rather than deleting them: where they are untracked (the preset leaves them so), git cannot
   bring them back. Where the project tracks one of them, also commit its removal in the
   project. Leave the project's own skills in `.claude/skills/` alone.
4. Preset only: the `specify preset remove tests-as-spec` and `specify extension remove
   tests-as-spec` commands are optional once the folders are gone; run them only if you want
   the CLI's own records cleared too. The same goes for spec-kit's `git` extension, if it is
   present.

On your machine: retire `/sdd-init`, and any other skill or command that would fight over
`specs/`.

Keep the spec-kit CLI itself for now: it is uninstalled last (step 9).

## 3. Install

In a session, as slash commands:

```
/plugin marketplace add GnetDan/s2tdd
/plugin install s2tdd@s2tdd
```

From a shell, or for an agent that cannot run slash commands:

```
claude plugin marketplace add GnetDan/s2tdd
claude plugin install s2tdd@s2tdd --scope user
```

Install at user scope. Use the copy-into-`.claude/skills/` fallback only where the plugin can't
run, and then use one or the other, never both.

## 4. Keep and move

- `specs/` stays as it is, once it is its own repository (step 2).
- The constitution moves from `.specify/memory/constitution.md` to
  `specs/constitution.md` (step 2). If an older backup already sits there, reconcile the two copies by
  diff, keeping what each has that the other lacks, because drifted copies are common. `/s2tdd-next` commits it with the feature's files from then
  on.
- Preset only: `docs/sdd-workflow.md`, moved aside in step 2, is replaced by
  `specs/WORKFLOW.md`, which first-run setup copies in with the first `/s2tdd-specify`,
  `/s2tdd-epic` or `/s2tdd-constitution` (step 8). Until then the page is missing; step 7 does
  not need it.
- In your local excludes, remove `.specify/`, `.claude/skills/speckit-*/` and
  `docs/sdd-workflow.md`; keep `specs/` and add `.sdd-run/`.

## 5. Rename table

| Old | New |
|---|---|
| `/speckit-<x>` | `/s2tdd-<x>` |
| `/speckit-tasks`, `/speckit-harden` | `/s2tdd-harden` |
| `/speckit-handoff` | `/s2tdd-implement --print` |
| `/speckit-save` | `/s2tdd-next` |
| `/speckit-branch` | `/s2tdd-specify` |
| `/speckit-analyze`, `/speckit-checklist`, `/speckit-taskstoissues` | none |
| `.specify/memory/constitution.md` | `specs/constitution.md` |
| `docs/sdd-workflow.md` | `specs/WORKFLOW.md` |

The specific rows apply before the `/speckit-<x>` row. The three commands marked "none" have
no replacement.

## 6. Mid-flight feature

If a feature is hardened, start a new session in the project (only a session started after
the install loads the plugin's commands) and run `/s2tdd-harden handoff` there once. It rewrites the feature's
`handoff.md` and `orchestration.md` to the new command names. Earlier stages (spec, plan)
continue unchanged.

## 7. Verify

Start a new session in the project first: a session that was open during the migration keeps
its old command list, and only a new one loads the plugin's commands. Then run `/s2tdd-next`.
It should run, name the active feature, and report no spec-kit leftovers (`.specify/`,
`speckit-*` skills, `docs/sdd-workflow.md`) under **Watch out**. Check that the plugin's
commands are listed.

## 8. Start fresh

For new work, run `/s2tdd-epic` or `/s2tdd-specify`, in a new session so the plugin's commands
are loaded. The first `/s2tdd-specify`, `/s2tdd-epic`
or `/s2tdd-constitution` in a repository does the first-run setup: it checks for `specs/` and
offers to clone or create the specs repository, copies in the project pages, and writes the
local excludes (`specs/`, `.sdd-run/`) if they are missing. A repository whose remote owner is
yours, or that has no remote, is treated as yours; any other owner means a foreign repository,
which is kept to zero tracked footprint.

## 9. Last: uninstall the spec-kit CLI

Once no project on your machine still runs plain spec-kit:

```
uv tool uninstall specify-cli
```

## Recommended: automatic deletion of head branches

In the repository's settings, turn on automatic deletion of head branches, so a merged feature
branch is removed by the host and `/s2tdd-next` has no merged leftovers to point out.
