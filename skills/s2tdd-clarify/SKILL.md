---
name: s2tdd-clarify
description: "Grill the active feature spec until its design tree is resolved: rounds of questions, each with a recommended answer you can accept in a word; facts the code or docs can answer are investigated, never asked; answers fold into spec.md in place as ID'd Given/When/Then scenarios, terms and research.md decisions. Never answers its own questions. Ends when the frontier is empty or you say enough (s2tdd)."
argument-hint: "Optional areas to clarify in the spec"
---
<!-- Adapted from github/spec-kit (MIT). -->

## User Input

Consider the text the user typed after the command: optionally the feature, and areas of the spec
to clarify. You **MUST** consider it before proceeding (if not empty). If it names areas of the
spec, root the design tree there.

## Goal

Interview the user relentlessly about the active feature spec until you share one
understanding of it, and fold every answer back into `spec.md` in place — before
`/s2tdd-plan`. There is no question quota. The session ends when every branch of
the design tree has been visited with nothing silently assumed, or when the user says
"enough".

The questioning discipline is adapted from mattpocock/skills (MIT) — `grilling` and
`domain-modeling` — reshaped for this workflow's spec conventions and homes for terms and
decisions.

**HITL is sacred.** The decisions are the user's. Never answer your own question, never settle a
decision from silence, and never treat a recommendation the user has not accepted as an answer.
If there is no human to answer (you are a subagent, or the run is non-interactive), ask
nothing and write nothing: report the frontier as open questions and stop.

**Facts are yours.** A question the codebase, the docs, git history, the constitution or the
spec itself can answer is *investigated, not asked*: look it up (dispatch a subagent for a broad
search), then record the fact with its source (`path:line`) as a settled node. Never ask the user
something you could have read.

**Writes**: the feature's `spec.md`; the feature's `research.md` (decision entries only);
the feature's `checklists/requirements.md` (checkbox markers only). Nothing else — no code, no
tests, no constitution, no agent guidance file, no other feature directory.

## Execution Steps

### 1. Initialize

<!-- s2tdd:shared worktrees -->
**Where specs/ is.** If `./specs` does not exist here, this may be a worktree: run
`git worktree list --porcelain` and use `specs/` in the first worktree it lists (the main
checkout). Say so in one line ("Using specs/ from the main worktree at <path>."), and write every
spec file there, so it lands in the one specs repository.
<!-- /s2tdd:shared -->

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

The feature's directory is `specs/<feature>/` and its spec is `specs/<feature>/spec.md`. If the
spec is missing, stop and point at `/s2tdd-specify` (do not create a spec here).

**Closed-feature guard**: if the spec's `**Status**:` line begins with `Closed`, stop without
writing: "This feature is closed; its spec is a historical intent record. New or changed
behavior belongs in a new feature (`/s2tdd-specify`) with a `**Supersedes**:` line."

### 2. Load context

Note `git status --short` now: the session's baseline for the **Writes** check in step 5.

- The spec (every scenario ID, FR, SC, Key Entity, existing `## Clarifications` session).
- `specs/constitution.md` — its MUSTs bound every recommendation.
- The project's agent guidance file — its invariants and vocabulary.
- The feature's `research.md` if present — decisions already made (never re-ask one).
- Acceptance tests already written for this feature (grep the acceptance directory for the
  feature's `test_<NNN>_` prefix) — an answer that changes one of those scenarios has a cost.

### 3. Build the design tree

Scan the spec for what is underspecified: scope and explicit out-of-scope; actors and roles;
entities, identity and lifecycle; critical journeys and their error/empty states;
non-functional targets (latency, capacity, reliability, observability, privacy); external
dependencies and their failure modes; edge cases and conflicts; terminology; testability of
each scenario; `[NEEDS CLARIFICATION]` markers and unquantified adjectives.

Turn each gap into a **decision node** and note which other decisions it hangs on. A node whose
answer is a fact goes to investigation (Goal, *Facts are yours*), not to the user. The
**frontier** is every open decision whose prerequisites are settled — the questions you can ask
now without guessing at answers you have not heard yet. Skip nodes whose answer would not change
a scenario, a requirement, a test or the plan.

If the frontier is empty at the start, say "No decisions left open in this spec", show the
facts you investigated, record a `### Session YYYY-MM-DD` under `## Clarifications` with the
single bullet `- No decisions left open.` (so the next step can see clarify ran), and go to
step 7.

### 4. Ask a round

Ask the **whole frontier** in one round (if it exceeds ~7, the highest-impact first, and say how
many remain). A question whose answer depends on another question in this round belongs to a
later round. While an investigation is still running, only the questions downstream of it wait.

```text
**Round <r>** — <k> questions · <n> open in the tree · facts found this round: <m>

❓ **Q<r>.<i> — <title>**: <the question; the concrete scenario that makes it matter;
lettered options when the choices are discrete>

➡️ **Recommended**: <answer> — <one line of why, citing the spec/constitution/code it rests on>
```

Close every round with: `Reply "yes" to accept every recommendation, "Q<r>.<i>: <letter or
answer>" to choose, or "enough" to stop here.`

While asking, keep the domain honest:

- **Challenge the language.** When the user's term conflicts with the spec, the constitution,
  the guidance file or identifiers in the code, say so on the spot: "The spec calls this X; you
  seem to mean Y. Which is it?"
- **Cross-reference the code.** When the user states how something works, check whether the
  code agrees and surface a contradiction as a question.
- **Probe with concrete scenarios.** Invent the awkward case that forces a boundary decision.
  A scenario the user settles becomes a spec scenario (step 5).

### 5. Fold the answers into the spec (after every round)

Take only what the user actually answered; unanswered questions stay open for the next round.
Ambiguous answers get one disambiguating follow-up (same question, not a new one).

1. **Log it.** Under `## Clarifications` (create it after the overview section if missing) and a
   `### Session YYYY-MM-DD` heading for today, one bullet per accepted answer:
   `- Q: <question> → A: <answer>`. Investigated facts that changed the spec get
   `- Fact: <finding> (<path:line>)`.
2. **Behavior → scenarios.** A new behavior is a new scenario with the **next free ID** in its
   story (`US<n>-AC<m>`) or the next edge case (`EC-<nnn>`) — one concrete **Given** state, one
   **When** action, one observable **Then** outcome, no implementation terms. IDs are never
   renumbered or reused. An answer that changes an existing scenario rewrites it in place,
   keeping its ID; if that scenario already has an acceptance test (step 2), record it for the
   Completion Report — the test owner rewrites that test, never the code that will fail it.
3. **Requirements and outcomes.** Functional ambiguity → an FR; a vague quality → a measurable
   SC; replace the statement the answer invalidates, never leave both.
4. **Supersedes.** If an answer changes behavior an earlier feature's spec defined, add it to
   this spec's `**Supersedes**:` line (e.g. `001 FR-012`). Never edit the earlier spec.
   `**Status**:` stays `Draft`.
5. **Terms.** A resolved term that names a thing goes in `### Key Entities`; any other canonical
   term goes in a `### Terminology` subsection directly after it (create it when the first term
   lands): `- **Term**: one or two sentences — what it is, not what it does. _Avoid_: synonyms`.
   Normalize the term everywhere in the spec. Only project-specific concepts — never general
   programming ones. If the term must outlive the feature (code, UI, or users will use it),
   end its bullet with `*(living)*`; `/s2tdd-close` moves living terms to `docs/`.
6. **Decisions.** Record a decision in the feature's `research.md` only when all three hold: it
   is hard to reverse, a later reader would find it surprising without context, and it was a real
   trade-off between alternatives. Use the next free `## R<n>. <title>` with **Decision**,
   **Rationale**, **Alternatives considered**, and `*(clarify session YYYY-MM-DD)*`. If
   research.md does not exist yet, create it with `# Phase 0 Research: <feature>` and the line
   `R1–R<k> were recorded by clarify; plan appends after them and keeps them.` Anything else
   is fully captured by its Clarifications bullet. A decision that would breach a constitution
   MUST is not recorded — say so; changing the constitution is an amendment, not a clarify
   answer.
7. **Save** the spec (and research.md) before asking the next round.

Then validate: scenario IDs unique, none renumbered; every new scenario is one Given / one When
/ one Then; one Clarifications bullet per accepted answer; no contradicted statement left
behind; the same canonical term everywhere; `git status --short` shows no file outside
**Writes** that was clean when the session started. Recompute the frontier and return to step 4.

### 6. End the session

- **Frontier empty**: summarize the shared understanding in a few lines and ask the user to
  confirm it before you report.
- **User says "enough"** (or "stop", "done"): stop asking. Add
  `- Deferred: <question> (session ended by user)` under today's session for each open frontier
  question. Do not convert them to `[NEEDS CLARIFICATION]` markers — a deferred decision is still
  the user's, not something planning resolves by research.

### 7. Re-validate the spec quality checklist (if it exists)

If the feature's `checklists/requirements.md` exists: re-evaluate each checkbox line (outside code
fences) against the updated spec and toggle **only** the markers whose state changed, touching
nothing else in the file. Record before/after pass counts, newly passing items, regressions and
items still unchecked.

## Completion Report

- Rounds run; questions asked / answered / deferred; how the session ended (frontier empty and
  confirmed, or "enough").
- Facts investigated instead of asked, each with its source.
- Spec sections touched; new scenario IDs; scenarios rewritten in place — flag each that
  already has an acceptance test ("test owner rewrites `<path::test>`").
- `**Supersedes**:` entries added; terms added (living ones marked); `R<n>` entries added to
  research.md.
- Spec quality checklist before/after (if re-validated).

<!-- s2tdd:shared closing-step -->
**Last step.** Run `/s2tdd-next`. It commits and pushes this feature's specs, then prints the
recap and the next step as a ready-to-paste prompt. Run it as plain text; no hook runs it for
you.
<!-- /s2tdd:shared -->
