---
name: s2tdd-plan
description: "Plan the active feature: fill plan.md from the bundled template (technical context, where the acceptance tests live and which scenarios are scripted or human checkpoints, a constitution gate against specs/constitution.md), research the unknowns with research agents into research.md R-entries, then write data-model.md, contracts/ and quickstart.md with each run marked scripted or human. Refuses closed features and unjustified constitution violations (s2tdd)."
argument-hint: "Optional guidance for the planning phase"
---
<!-- Adapted from github/spec-kit (MIT). -->

## User Input

The text the user typed after the command is optional guidance for the planning phase. It may
also name the feature (`NNN` or `NNN-name`; see *Which feature* below); the rest is guidance.

You **MUST** consider the user input before proceeding (if not empty).

<!-- s2tdd:shared feature-resolution -->
**Which feature.** Work out the feature this command is for, in this order; the first match
wins:

1. **Named.** The text the user typed after the command names a feature, as `NNN` or
   `NNN-name`, and `specs/` has that directory.
2. **Branch.** `git branch --show-current` prints a name, and `specs/<branch>/` exists.
3. **Branch number.** The branch name, after any `prefix/` such as `claude/`, starts with a
   number `NNN`, and exactly one directory `specs/NNN-*` has it.
4. **Ask.** Otherwise, list the open features (the directories in `specs/` whose spec's
   `**Status**:` does not begin with `Closed`) and ask which one.

If two directories share the number, ask; never pick one. Never write a pointer file: work the
answer out again on every run.
<!-- /s2tdd:shared -->

<!-- s2tdd:shared worktrees -->
**Where specs/ is.** If `./specs` does not exist here, this may be a worktree: run
`git worktree list --porcelain` and use `specs/` in the first worktree it lists (the main
checkout). Say so in one line ("Using specs/ from the main worktree at <path>."), and write every
spec file there, so it lands in the one specs repository.
<!-- /s2tdd:shared -->

**Closed-feature guard**: if the spec's `**Status**:` line begins with `Closed`, stop without
writing: "This feature is closed; its spec is a historical intent record. New or changed
behavior belongs in a new feature (`/s2tdd-specify`) with a `**Supersedes**:` line."

**Open-decisions guard**: before writing anything, scan the spec for open decisions: each
`[NEEDS CLARIFICATION` marker, and each `- Deferred:` bullet under Clarifications that no later
bullet answers. These are questions the user deferred, and a deferred decision is still the
user's. If there are any, list them (with the scenario or requirement each sits in) and stop:
"These decisions are still yours. Run `/s2tdd-clarify` to settle them, or say go ahead to plan
with them left open." Never research them, never pick an answer, never write an R-entry for
one. If the user says go ahead, record each one under the plan's Technical Context as an open
user decision and plan around it.

## Outline

1. **Setup** (no setup script): from the feature resolved above, take `FEATURE_DIR`
   (`specs/<NNN-name>/`), `FEATURE_SPEC` (`FEATURE_DIR/spec.md`), `IMPL_PLAN`
   (`FEATURE_DIR/plan.md`) and `BRANCH` (`git branch --show-current`, or "none" outside a
   branch). If `IMPL_PLAN` does not exist, copy `./plan-template.md` (bundled beside this
   command) to it; if it exists, keep it and fill it in place. Never overwrite an existing plan.

2. **Load context**: read `FEATURE_SPEC` and `specs/constitution.md`, and `IMPL_PLAN` (the
   template copied in step 1, or the existing plan). If `specs/constitution.md` does not exist,
   say in one line that `/s2tdd-constitution` creates one, record "no constitution: no gates" in
   the Constitution Check, and carry on.

3. **Execute plan workflow**: follow the structure in `IMPL_PLAN` to:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION"), including its
     **Acceptance tests** field: where the acceptance tests live (one per scenario ID), which
     scenarios need a live service and become scripted checkpoints, and which few need a person
     and become human checkpoints, and why
   - Fill the Constitution Check section from `specs/constitution.md`
   - Evaluate gates (see *Constitution gate* below): an unjustified violation stops the plan
   - Phase 0: generate `research.md` (resolve the technical unknowns this plan marked NEEDS
     CLARIFICATION in Technical Context; the spec's open decisions are the user's, see the
     *Open-decisions guard*)
   - Phase 1: generate `data-model.md`, `contracts/`, `quickstart.md`
   - Re-evaluate the Constitution Check post-design, with the same gate

## Constitution gate

Each principle in `specs/constitution.md` is a gate, checked before Phase 0 and again after
Phase 1. A design choice that breaks a principle is a violation:

- **Justified**: the plan records it in **Complexity Tracking** (the violation, why it is
  needed, and the simpler alternative rejected and why). A justified violation passes the gate.
- **Unjustified**: a violation with no Complexity Tracking row, or with a row that does not
  hold up, stops the plan. ERROR: name the principle and the design choice that breaks it, and
  stop before the next phase. The user either justifies it (a Complexity Tracking row) or
  changes the design; changing the principle itself is an amendment through
  `/s2tdd-constitution`, never a plan decision.

## Completion Report

Command ends after Phase 1 design. Report the branch, the `IMPL_PLAN` path, the generated
artifacts, the R-entries added to `research.md` (their numbers), and the quickstart runs with
their marking (scripted or human).

<!-- s2tdd:shared closing-step -->
**Last step.** Run `/s2tdd-next`. It commits and pushes this feature's specs, then prints the
recap and the next step as a ready-to-paste prompt. Run it as plain text; no hook runs it for
you.
<!-- /s2tdd:shared -->

## Phases

### Phase 0: Outline & Research

1. **Extract unknowns from Technical Context** above:
   - For each technical NEEDS CLARIFICATION this plan marked → research task (never a
     decision the user deferred in the spec: research never settles those)
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:

   ```text
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `FEATURE_DIR/research.md` as R-entries, one per decision:

   ```markdown
   ## R<n>. <the decision, as a sentence>

   **Decision**: <what was chosen>
   **Rationale**: <why it was chosen>
   **Alternatives considered**: <what else was evaluated, and why not>
   *(plan YYYY-MM-DD)*
   ```

   - If `research.md` exists (clarify or an earlier plan run may have written R-entries),
     append after its last entry, numbering on from the highest `R<n>`. Never renumber,
     reorder or rewrite an existing entry: tasks, contracts and close-out cite them by number.
     A decision that changes an earlier one is a new entry that says which `R<n>` it replaces.
   - If it does not exist, create it with `# Phase 0 Research: <feature>` and start at `R1`.

**Output**: research.md with every technical NEEDS CLARIFICATION from Technical Context resolved

### Phase 1: Design & Contracts

**Prerequisites:** `research.md` complete

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Define interface contracts** (if project has external interfaces) → `contracts/`:
   - Identify what interfaces the project exposes to users or other systems
   - Document the contract format appropriate for the project type
   - Examples: public APIs for libraries, command schemas for CLI tools, endpoints for web services, grammars for parsers, UI contracts for applications
   - Skip if project is purely internal (build scripts, one-off tools, etc.)

3. **Create quickstart validation guide** → `quickstart.md`:
   - Document runnable validation scenarios that prove the feature works end-to-end
   - Include prerequisites, setup commands, test/run commands, and expected outcomes
   - Mark each run (`## V<n> — <title>`) **scripted** (fixed inputs, run by the implementer;
     name the live service it needs) or **human** (needs a person: a verdict on feel or
     quality, open-ended exploration, a UX or design call, heavy benefit from the user's
     interaction, or a critical control gate; say why). No human run repeats inputs a script
     can play. The deterministic suite every wave runs gets no V-number. The marking matches
     the **Acceptance tests** field in `IMPL_PLAN`
   - Use links or references to contracts and data model details instead of duplicating them
   - Do not include full implementation code, model/service/controller bodies, migrations, or complete test suites
   - Keep this artifact as a validation/run guide; implementation details belong in `tasks.md` and the implementation phase

**Output**: data-model.md, contracts/*, quickstart.md

## Key rules

- Use absolute paths for filesystem operations; use project-relative paths for references in documentation
- ERROR on an unjustified constitution violation (see *Constitution gate*); stop and ask on the
  spec's open decisions (see *Open-decisions guard*); a technical unknown research cannot
  settle is reported, not guessed
- Write only in `FEATURE_DIR`; `tasks.md` is `/s2tdd-harden`'s, never this command's

## Done When

- [ ] Plan workflow executed and design artifacts generated
- [ ] Constitution gate passed before Phase 0 and after Phase 1 (violations justified in
      Complexity Tracking), or the plan stopped on an unjustified violation
- [ ] The spec's open decisions settled by the user (or left open on their go-ahead), none
      researched into an R-entry
- [ ] research.md decisions appended as R-entries, existing entries untouched
- [ ] Every quickstart run marked scripted or human
- [ ] Completion reported to user with branch, plan path, and generated artifacts
- [ ] `/s2tdd-next` run as the last step
