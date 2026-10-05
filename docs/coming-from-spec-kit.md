# Coming from spec-kit

[← Back to the README](../README.md)

s2tdd keeps spec-kit's feature layout, so a spec-kit project adopts it without moving a feature
file. What changes is the tooling around those files: s2tdd is one Claude Code plugin, with no
`specify` CLI, presets or extensions, and its commands are named `/s2tdd-<name>`.

This page is for a plain spec-kit project. A project that also ran the earlier preset edition of
this workflow follows [MIGRATING.md](../MIGRATING.md), which has the extra steps for it.

## Same layout

The `specs/NNN-name/` layout is unchanged: `spec.md`, `plan.md`, `research.md`,
`data-model.md`, `quickstart.md`, `contracts/` and `tasks.md` keep their names and places.
s2tdd's own files sit beside them (`orchestration.md`, `handoff.md`, `validation.md`,
`run-ledger.md`, `s<k>-wave-reports.md`, `close-out.md`), and epics go under
`specs/epics/<slug>/`.

Three things move into `specs/`, and `specs/` becomes its own repository:

- **The constitution** lives at `specs/constitution.md`, not `.specify/memory/constitution.md`.
- **The project pages** are `specs/README.md` (the specs lifecycle) and `specs/WORKFLOW.md`
  (the workflow guide). The first `/s2tdd-specify`, `/s2tdd-epic` or `/s2tdd-constitution` in a
  repository copies them in when they are missing.
- **`specs/` is a separate git repository**, usually private, cloned into place in each checkout
  and listed in the project's `.git/info/exclude`. Agents working on the app then never read
  stale intent, and `/s2tdd-next` commits and pushes a feature's files there at the end of
  every step. Step 1 below moves specs that are tracked in the project today.

Templates are bundled inside the commands that use them, with no project override, so any
customised templates under `.specify/templates/` do not carry over.

## What to uninstall

In this order, from the project root:

1. **Give `specs/` its own repository.** s2tdd writes no spec until `specs/` is a separate
   git repository, and first-run setup offers to create one only when `specs/` is missing. If
   your specs are tracked in the project today, turn the folder into that repository where it
   stands:
   - In the project, run `git rm -r --cached specs`, add `specs/` to `.git/info/exclude`, and
     commit the removal. The files stay on disk, now untracked by the project.
   - Make `specs/` a repository of its own and push it to a new (usually private) one:
     `git -C specs init`, `git -C specs add -A`,
     `git -C specs commit -m "Specs, moved from the project"`, then
     `gh repo create <name>-specs --private --source specs --push`.

   This checkout needs no clone. Another checkout of the project pulls the removal, moves
   anything still left in its `specs/` aside, and then clones the new repository into `specs/`.
2. **Keep your constitution.** If `.specify/memory/constitution.md` holds a ratified
   constitution, copy it to `specs/constitution.md` and commit it in the specs repository,
   before anything is deleted.
3. **Presets and extensions.** Run `specify preset remove <id>` for each installed preset and
   `specify extension remove <id>` for each installed extension. If spec-kit's git extension is
   present, remove it too (`specify extension remove git`): `/s2tdd-specify` creates the feature
   branch itself, and two branch makers fight.
4. **Delete the spec-kit files**: `.specify/` (including `feature.json`) and
   `.claude/skills/speckit-*/`, and drop them from `.git/info/exclude` if you listed them there.
5. **Install s2tdd** at user scope, in Claude Code:

   ```text
   /plugin marketplace add GnetDan/s2tdd
   /plugin install s2tdd@s2tdd
   ```

6. **Start.** Run `/s2tdd-next` to check where things stand, then `/s2tdd-specify` or
   `/s2tdd-epic` for new work. The first `/s2tdd-specify`, `/s2tdd-epic` or
   `/s2tdd-constitution` in the repository sets it up (project pages, local excludes) in place
   of `specify init`; `/s2tdd-next` runs no setup.
7. **Last, the CLI.** Once no project of yours still runs spec-kit, uninstall it:
   `uv tool uninstall specify-cli`.

## Which command maps to which

| spec-kit | s2tdd | What's different |
|---|---|---|
| `/speckit-constitution` | `/s2tdd-constitution` | Writes `specs/constitution.md`; grills you for a new one, amends with a version bump and a dated note |
| `/speckit-specify` | `/s2tdd-specify` | Creates the `NNN-short-name` branch first, then drafts ID'd Given/When/Then scenarios and grills you until settled |
| `/speckit-clarify` | `/s2tdd-clarify` | Grills an existing spec again, with no question cap |
| `/speckit-plan` | `/s2tdd-plan` | Records research decisions as R-entries and marks each quickstart run scripted or human |
| `/speckit-tasks` | `/s2tdd-harden` | Writes `tasks.md` test-first, then splits it into file-disjoint packets with an orchestration plan |
| `/speckit-implement` | `/s2tdd-implement` | Orchestrates one wave at a time, a subagent per packet, red before green; `--print` prints the prompt for another session |
| `/speckit-analyze`, `/speckit-checklist`, `/speckit-taskstoissues` | none | No replacement |

s2tdd adds `/s2tdd-epic`, `/s2tdd-verify-done`, `/s2tdd-converge`, `/s2tdd-pr-review`,
`/s2tdd-close`, `/s2tdd-next` and `/s2tdd-foundation-review`; the [README](../README.md) walks
through the whole chain.

The full rename table, which [MIGRATING.md](../MIGRATING.md) also uses, covers the earlier
preset edition's commands and files too:

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

The specific rows apply before the `/speckit-<x>` row.
