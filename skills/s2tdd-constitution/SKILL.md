---
name: s2tdd-constitution
description: "Create or amend the project constitution, specs/constitution.md: with none yet, grill you one round at a time (each question with a recommended answer) and write it from the bundled template; with one, amend it with a semantic version bump and a dated change note in the file. Writes only specs/constitution.md (s2tdd)."
argument-hint: "Optional amendment text, or principles for a new constitution"
---
<!-- Adapted from github/spec-kit (MIT). -->

## User Input

The text the user typed after the command is optional: principles or values for a new
constitution, or the amendment to make to an existing one.

You **MUST** consider the user input before proceeding (if not empty).

<!-- s2tdd:shared first-run-setup -->
**First-run setup.** Before this command's own work, check that this repository is set up for
s2tdd. Setup only adds: never delete or rewrite an existing file; the one file it changes is
`.git/info/exclude`, by appending lines.

1. **Whose repository.** Read the remote owner from `git remote get-url origin`: the path
   segment after the host, in the https or the ssh form. Find the user's account from the first
   of these that answers: `gh api user --jq .login`; `git config --get github.user`; otherwise
   ask the user once for their account name, and suggest they run
   `git config --global github.user <name>` themselves (setup never writes global config). An
   owner equal to the account (ignoring case), or no remote at all, makes the repository the
   user's own. Any other owner makes it foreign. If the user declines to answer, treat it as
   foreign.
2. **Specs repository.** If there is no `specs/` here or in the main worktree, offer to clone the
   user's existing specs repository into `specs/`, or to create one
   (`gh repo create <name>-specs --private`, then clone it into `specs/`). Write no spec until
   `specs/` is its own repository.
3. **Project pages.** Copy `./pages/README.md` to `specs/README.md` and `./pages/WORKFLOW.md` to
   `specs/WORKFLOW.md`, each only when it is missing; never overwrite one. Leave any older copy
   of a project page elsewhere in the project where it is.
4. **Local excludes.** Append to `.git/info/exclude` each of these lines that is not there yet:
   `specs/`, `.sdd-run/`, and, in a foreign repository only, `.claude/skills/s2tdd-*/`.
5. **Foreign check.** In a foreign repository, run `git status --porcelain` afterwards: nothing
   it shows may come from setup. If something does, stop and tell the user what it is.
6. **Silence.** When nothing was missing, say nothing about setup and go on.
<!-- /s2tdd:shared -->

<!-- s2tdd:shared worktrees -->
**Where specs/ is.** If `./specs` does not exist here, this may be a worktree: run
`git worktree list --porcelain` and use `specs/` in the first worktree it lists (the main
checkout). Say so in one line ("Using specs/ from the main worktree at <path>."), and write every
spec file there, so it lands in the one specs repository.
<!-- /s2tdd:shared -->

## Scope Guard

This command's own work is limited to the project constitution itself, `specs/constitution.md`.
The other s2tdd commands read it at run time and are not modified here.

- Classify every part of the user input as either constitution content or a separate,
  non-governance intent.
- If the input includes feature implementation, code generation, refactoring, building, or
  deployment requests, you **MUST NOT** execute them. Extract them as deferred intents instead.
- You **MUST NOT** create, modify, or delete application source files, feature routes,
  components, tests, deployment files, or other artifacts unrelated to the constitution.
- If it is unclear whether an instruction is constitution content, ask for clarification before
  making changes.
- After completing the constitution update, include a `Next Actions` section for each deferred
  intent. List the original intent and suggest the s2tdd command that fits, such as
  `/s2tdd-specify` or `/s2tdd-epic`, without invoking it.
- If there are no non-governance intents, omit the `Next Actions` section.

## Outline

You are creating or amending the project constitution at `specs/constitution.md`, in the
`specs/` directory found above. Its scaffold is `./constitution-template.md`, bundled beside this
command.

1. **Create or amend.**
   - If `specs/constitution.md` does not exist, this run **creates** it: start from
     `./constitution-template.md` as the initial document, and grill the user for its content
     (step 2).
   - If it exists, this run **amends** it: load it as the source of current project-specific
     values and amendments, and keep its structure. The user input says what to amend; when the
     input is empty, ask what the amendment is (one question, with a recommended answer if the
     repository suggests one).
   - Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]` still in the document.
   **IMPORTANT**: The user might require less or more principles than the ones used in the
   template. If a number is specified, respect that - follow the general template. You will
   update the doc accordingly.

2. **Grill for the values.** Settle each placeholder (when creating) or each change (when
   amending) with the user, one round at a time:
   - **Facts are yours.** A value the user input, the repository (README, docs, the agent
     guidance file `CLAUDE.md` or `AGENTS.md`, the code, git history) or an earlier version of
     the constitution already answers is investigated and proposed, never asked.
   - **Decisions are the user's.** Each round asks a few questions, each with a recommended
     answer and one line of why, which the user can accept in a word. Never answer your own
     question; a question the user skips stays open.
   - **When it ends.** When every principle and section has a value, or the user says enough.
     A value still open then becomes `TODO(<FIELD_NAME>): explanation` and is listed in the
     change note and the final summary.
   - For governance dates: `RATIFICATION_DATE` is the original adoption date (today when
     creating; if an existing constitution lacks it, ask or mark TODO), `LAST_AMENDED_DATE` is
     today if changes are made, otherwise keep previous.

3. **Version bump.** `CONSTITUTION_VERSION` is a semantic version. A new constitution starts at
   `1.0.0`. Every amendment must bump it according to semantic versioning rules:
   - MAJOR: Backward incompatible governance/principle removals or redefinitions.
   - MINOR: New principle/section added or materially expanded guidance.
   - PATCH: Clarifications, wording, typo fixes, non-semantic refinements.
   - If version bump type ambiguous, propose reasoning (as a recommended answer) before
     finalizing.

4. **Draft the constitution** using the template's structure:
   - Replace every placeholder with concrete text (no bracketed tokens left except intentionally
     retained template slots that the project has chosen not to define yet—explicitly justify
     any left).
   - Preserve heading hierarchy; the template's comments can be removed once replaced unless
     they still add clarifying guidance.
   - Ensure each Principle section: succinct name line, paragraph (or bullet list) capturing
     non‑negotiable rules, explicit rationale if not obvious.
   - Ensure the Governance section lists amendment procedure (amendments go through
     `/s2tdd-constitution`), versioning policy, and compliance review expectations.

5. **Dated change note.** The file keeps its history in a `## Change notes` section after
   Governance, the last section of the file, newest note first. Each note is one line, never
   rewritten afterwards:
   `- <YYYY-MM-DD> · <old version> → <new version> (<MAJOR|MINOR|PATCH>): <what changed and why>`,
   naming the principles modified (old title → new title if renamed), the sections added or
   removed, and any TODO deferred. Creating the file writes the section with its first note:
   `- <YYYY-MM-DD> · 1.0.0: ratified`. An amendment to a constitution that has no
   `## Change notes` section yet adds the section with this amendment's note.

6. **Validation before writing:**
   - No remaining unexplained bracket tokens.
   - The version line matches the newest change note.
   - Dates ISO format YYYY-MM-DD.
   - Principles are declarative, testable, and free of vague language ("should" → replace with
     MUST/SHOULD rationale where appropriate).

7. **Write** the completed constitution to `specs/constitution.md` (overwrite when amending).

8. **Final summary** to the user:
   - New version and bump rationale.
   - Any TODO placeholders or deferred items requiring manual follow-up.
   - A `Next Actions` section for any deferred non-governance intents.

Formatting & Style Requirements:

- Use Markdown headings exactly as in the template (do not demote/promote levels).
- Wrap long rationale lines to keep readability (<100 chars ideally) but do not hard enforce
  with awkward breaks.
- Keep a single blank line between sections.
- Avoid trailing whitespace.

If the user supplies partial updates (e.g., only one principle revision), still perform
validation and version decision steps.

**No propagation into project templates.** Write only `specs/constitution.md`. The spec, plan
and tasks templates are bundled with the s2tdd commands and read the constitution at run time;
this command never edits them, nor `./constitution-template.md`, nor any other file.

<!-- s2tdd:shared closing-step -->
**Last step.** Run `/s2tdd-next`. It commits and pushes this feature's specs, then prints the
recap and the next step as a ready-to-paste prompt. Run it as plain text; no hook runs it for
you.
<!-- /s2tdd:shared -->
