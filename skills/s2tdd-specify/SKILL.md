---
name: s2tdd-specify
description: "Start a feature: create the next NNN-short-name branch (numbered past specs/ and every local and remote branch), draft specs/NNN-short-name/spec.md with ID'd scenarios and every open gap marked (no cap, no informed guesses), then grill you one round at a time, each question with a recommended answer, until the design is settled or you say enough (s2tdd)."
argument-hint: "Describe the feature you want to specify"
---
<!-- Adapted from github/spec-kit (MIT). -->

## User Input

The text the user typed after the command **is** the feature description (an epic seed reference
such as "seed 1" counts), optionally with `GIT_BRANCH_NAME=<name>`. Assume you always have it in
this conversation. Do not ask the user to repeat it unless they typed nothing after the command.

You **MUST** consider the user input before proceeding.

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

## Outline

Given that feature description, do this:

1. **Generate a concise short name** (2-4 words) for the feature:
   - Analyze the feature description and extract the most meaningful keywords
   - Create a 2-4 word short name, lowercase kebab words, that captures the essence of the feature
   - Use action-noun format when possible (e.g., "add-user-auth", "fix-payment-bug")
   - Preserve technical terms and acronyms (OAuth2, API, JWT, etc.)
   - Keep it concise but descriptive enough to understand the feature at a glance
   - For an epic seed, read the seed's heading in `specs/epics/<slug>/map.md` §Hand-off
   - Examples:
     - "I want to add user authentication" → "user-auth"
     - "Implement OAuth2 integration for the API" → "oauth2-api-integration"
     - "Create a dashboard for analytics" → "analytics-dashboard"
     - "Fix payment processing timeout bug" → "fix-payment-timeout"

2. **Branch first.** Create or switch to the feature branch before anything is written, so the
   branch and the spec directory share one name. Never commit, stash, reset or push here.

   1. **Git or not.** Run `git rev-parse --is-inside-work-tree`. Outside a repository, say in
      one line that no branch was made, number the feature from `specs/` alone (step 2.2), and
      carry on without a branch.
   2. **Name.**
      - If the input gives `GIT_BRANCH_NAME`, use it exactly and skip to step 2.3.
      - Number: one past the highest three-digit prefix among the top-level directories under
        `specs/` (not `specs/epics/`) and all local and remote branch names
        (`git branch -a --format='%(refname:short)'`), zero-padded to three digits.
      - `BRANCH_NAME` is `NNN-<short-name>`.
   3. **Switch.**
      - A branch named `BRANCH_NAME` already exists (locally, or only on the remote): switch to
        it with `git switch <name>`. A remote-only branch gets its tracking branch that way.
      - Otherwise: `git switch -c <name>` from the current HEAD.
      - Uncommitted changes carry over; list them (`git status --short`) in the report. Never
        stash, reset, commit or push.
      - If HEAD is not on the default branch (`git symbolic-ref --short refs/remotes/origin/HEAD`
        without its `origin/`, falling back to `main`), branch anyway and say which branch it was
        made from.
      - If the switch fails (a conflicting local change, for example), print the error and say
        in bold that no branch was made and the spec will be written on the current branch
        `<name>`; carry on.
   4. **Report** in one line. Only when the switch succeeded inside a repository, print
      `Branch ready: <BRANCH_NAME>.`; otherwise say what happened instead (outside a repository,
      or the switch failed and the spec goes on the current branch). Either way the feature
      directory must be exactly `specs/<BRANCH_NAME>` (not a renumbered one), so later steps can
      find the spec from the branch name.

3. **Create the spec feature directory**:
   - `FEATURE_DIR` is `specs/<BRANCH_NAME>` (`NNN-<short-name>`), under the `specs/` the
     worktree rule above found.
   - `mkdir -p FEATURE_DIR`
   - Set `SPEC_FILE` to `FEATURE_DIR/spec.md`. Only when `SPEC_FILE` is missing, copy
     `./spec-template.md` (bundled beside this command) to it as the starting point. Never
     overwrite an existing feature's spec: if `SPEC_FILE` already exists, say so in one line and
     work on it in place.
   - Write no pointer file: later commands find the feature from the branch name.

   **IMPORTANT**:
   - You must only create one feature per `/s2tdd-specify` invocation
   - The spec directory and a missing spec file are always created by this command

4. Load `./spec-template.md` to understand required sections.

5. **Load context.**
   - **Constitution.** Load `specs/constitution.md` for project principles and governance
     constraints — its MUSTs bound every recommendation in the grilling (step 8). If
     `specs/constitution.md` is missing, say in one line that `/s2tdd-constitution` creates one,
     then carry on.
   - **Agent guidance file.** Load the project's agent guidance file (`CLAUDE.md`, else
     `AGENTS.md`), if present — its invariants and vocabulary, which the grilling checks terms
     and recommendations against.

6. Follow this execution flow:
    1. Parse the feature description
       If empty: ERROR "No feature description provided"
    2. Extract key concepts from description
       Identify: actors, actions, data, constraints
    3. For unclear aspects:
       - A fact the codebase, the docs, git history, the constitution or the description can
         answer is investigated, not asked: look it up and write it in with its source.
       - Every other open gap is marked in place with
         `[NEEDS CLARIFICATION: specific question]`. **No cap** on the number of markers, and
         **no informed guesses**: a choice the description leaves open is the user's, settled
         in the grilling (step 8), never silently filled.
       - Order the gaps by impact: scope > security/privacy > user experience > technical
         details
    4. Fill User Scenarios & Testing section, every scenario with its ID (`US<n>-AC<m>`,
       `EC-<nnn>`) as one concrete Given, one When, one observable Then
       If no clear user flow: ERROR "Cannot determine user scenarios"
    5. Generate Functional Requirements
       Each requirement must be testable
       An unspecified detail is a marked gap, not a default; the Assumptions section records
       only what the description states or the grilling settles
    6. Define Success Criteria
       Create measurable, technology-agnostic outcomes
       Include both quantitative metrics (time, performance, volume) and qualitative measures (user satisfaction, task completion)
       Each criterion must be verifiable without implementation details
    7. Identify Key Entities (if data involved)
    8. Return: SUCCESS (draft ready for grilling)

7. Write the draft to SPEC_FILE using the template structure, replacing placeholders with
   concrete details derived from the feature description while preserving section order and
   headings, with every open gap marked.

8. **Grill until settled.** Interview the user about the draft until you share one
   understanding of it, folding every answer back into `spec.md` in place. There is no question
   quota. The grilling ends when every branch of the design tree has been visited with nothing
   silently assumed, or when the user says "enough".

   The questioning discipline is adapted from mattpocock/skills (MIT) — `grilling` and
   `domain-modeling` — reshaped for this workflow's spec conventions and homes for terms and
   decisions.

   **HITL is sacred.** The decisions are the user's. Never answer your own question, never
   settle a decision from silence, and never treat a recommendation the user has not accepted as
   an answer. If there is no human to answer (you are a subagent, or the run is
   non-interactive), ask nothing: keep the draft with its markers, report the frontier as open
   questions, and go to step 9.

   **Facts are yours.** A question the codebase, the docs, git history, the constitution or the
   spec itself can answer is *investigated, not asked*: look it up (dispatch a subagent for a
   broad search), then record the fact with its source (`path:line`) as a settled node. Never
   ask the user something you could have read.

   1. **Build the design tree.** Every `[NEEDS CLARIFICATION]` marker is a decision node; scan
      the draft for more that is underspecified: scope and explicit out-of-scope; actors and
      roles; entities, identity and lifecycle; critical journeys and their error/empty states;
      non-functional targets (latency, capacity, reliability, observability, privacy); external
      dependencies and their failure modes; edge cases and conflicts; terminology; testability
      of each scenario; unquantified adjectives. Note which decisions each node hangs on. A node
      whose answer is a fact goes to investigation, not to the user. The **frontier** is every
      open decision whose prerequisites are settled — the questions you can ask now without
      guessing at answers you have not heard yet. Skip nodes whose answer would not change a
      scenario, a requirement, a test or the plan. If the frontier is empty, say "No decisions
      left open in this spec", show the facts you investigated, record a
      `### Session YYYY-MM-DD` under `## Clarifications` with the single bullet
      `- No decisions left open.` (so the next step can see the grilling ran), and go to step 9.

   2. **Ask a round**, one round at a time. Ask the **whole frontier** in one round (if it
      exceeds ~7, the highest-impact first, and say how many remain). A question whose answer
      depends on another question in this round belongs to a later round. Where a reasonable
      default exists (industry practice, the project's own patterns), it is the recommended
      answer, never a silent fill.

      ```text
      **Round <r>** — <k> questions · <n> open in the tree · facts found this round: <m>

      ❓ **Q<r>.<i> — <title>**: <the question; the concrete scenario that makes it matter;
      lettered options when the choices are discrete>

      ➡️ **Recommended**: <answer> — <one line of why, citing the spec/constitution/code it rests on>
      ```

      Close every round with: `Reply "yes" to accept every recommendation, "Q<r>.<i>: <letter or
      answer>" to choose, or "enough" to stop here.`

      While asking, keep the domain honest:

      - **Challenge the language.** When the user's term conflicts with the spec, the
        constitution, the guidance file or identifiers in the code, say so on the spot: "The spec
        calls this X; you seem to mean Y. Which is it?"
      - **Cross-reference the code.** When the user states how something works, check whether
        the code agrees and surface a contradiction as a question.
      - **Probe with concrete scenarios.** Invent the awkward case that forces a boundary
        decision. A scenario the user settles becomes a spec scenario.

   3. **Fold the answers into the spec** (after every round). Take only what the user actually
      answered; unanswered questions stay open for the next round. Ambiguous answers get one
      disambiguating follow-up (same question, not a new one).
      - **Log it.** Under `## Clarifications` (create it after the overview section if missing)
        and a `### Session YYYY-MM-DD` heading for today, one bullet per accepted answer:
        `- Q: <question> → A: <answer>`. Investigated facts that changed the spec get
        `- Fact: <finding> (<path:line>)`.
      - **Markers.** Replace each `[NEEDS CLARIFICATION]` marker the answer settles with the
        settled text.
      - **Behavior → scenarios.** A new behavior is a new scenario with the **next free ID** in
        its story (`US<n>-AC<m>`) or the next edge case (`EC-<nnn>`) — one concrete **Given**
        state, one **When** action, one observable **Then** outcome, no implementation terms. IDs
        are never renumbered or reused. An answer that changes an existing scenario rewrites it
        in place, keeping its ID.
      - **Requirements and outcomes.** Functional ambiguity → an FR; a vague quality → a
        measurable SC; replace the statement the answer invalidates, never leave both.
      - **Supersedes.** If an answer changes behavior an earlier feature's spec defined, add it to
        this spec's `**Supersedes**:` line (e.g. `001 FR-012`). Never edit the earlier spec.
        `**Status**:` stays `Draft`.
      - **Terms.** A resolved term that names a thing goes in `### Key Entities`; any other
        canonical term goes in a `### Terminology` subsection directly after it (create it when
        the first term lands): `- **Term**: one or two sentences — what it is, not what it does.
        _Avoid_: synonyms`. Normalize the term everywhere in the spec. Only project-specific
        concepts — never general programming ones. If the term must outlive the feature (code,
        UI, or users will use it), end its bullet with `*(living)*`; `/s2tdd-close` moves living
        terms to `docs/`.
      - **Decisions.** Record a decision in `FEATURE_DIR/research.md` only when all three hold:
        it is hard to reverse, a later reader would find it surprising without context, and it
        was a real trade-off between alternatives. Use the next free `## R<n>. <decision
        sentence>` with **Decision**, **Rationale**, **Alternatives considered**, and
        `*(specify session YYYY-MM-DD)*`. If research.md does not exist yet, create it with
        `# Phase 0 Research: <feature>` and the line `R1–R<k> were recorded while specifying;
        plan appends after them and keeps them.` Anything else is fully captured by its
        Clarifications bullet. A decision that would breach a constitution MUST is not recorded
        — say so; changing the constitution is an amendment (`/s2tdd-constitution`), not an
        answer here.
      - **Save** the spec (and research.md) before asking the next round.

      Then validate: scenario IDs unique, none renumbered; every new scenario is one Given / one
      When / one Then; one Clarifications bullet per accepted answer; no contradicted statement
      left behind; the same canonical term everywhere. Recompute the frontier and ask the next
      round.

   4. **End the grilling.**
      - **Frontier empty**: summarize the shared understanding in a few lines and ask the user
        to confirm it before you go on.
      - **User says "enough"** (or "stop", "done"): stop asking. Add
        `- Deferred: <question> (session ended by user)` under today's session for each open
        frontier question, and leave its `[NEEDS CLARIFICATION]` marker in place: a deferred
        decision is still the user's, and `/s2tdd-clarify` picks it up later.

9. **Specification Quality Validation**: After the grilling, validate the spec against quality
   criteria:

   a. **Create Spec Quality Checklist**: Generate a checklist file at `FEATURE_DIR/checklists/requirements.md` using the checklist template structure with these validation items:

      ```markdown
      # Specification Quality Checklist: [FEATURE NAME]

      **Purpose**: Validate specification completeness and quality before proceeding to planning
      **Created**: [DATE]
      **Feature**: [Link to spec.md]

      ## Content Quality

      - [ ] No implementation details (languages, frameworks, APIs)
      - [ ] Focused on user value and business needs
      - [ ] Written for non-technical stakeholders
      - [ ] All mandatory sections completed

      ## Requirement Completeness

      - [ ] No [NEEDS CLARIFICATION] markers remain
      - [ ] Requirements are testable and unambiguous
      - [ ] Success criteria are measurable
      - [ ] Success criteria are technology-agnostic (no implementation details)
      - [ ] All acceptance scenarios are defined
      - [ ] Edge cases are identified
      - [ ] Scope is clearly bounded
      - [ ] Dependencies and assumptions identified

      ## Feature Readiness

      - [ ] All functional requirements have clear acceptance criteria
      - [ ] User scenarios cover primary flows
      - [ ] Feature meets measurable outcomes defined in Success Criteria
      - [ ] No implementation details leak into specification

      ## Notes

      - Items marked incomplete require spec updates before `/s2tdd-clarify` or `/s2tdd-plan`
      ```

   b. **Run Validation Check**: Review the spec against each checklist item:
      - For each item, determine if it passes or fails
      - Document specific issues found (quote relevant spec sections)

   c. **Handle Validation Results**:

      - **If all items pass**: Mark checklist complete and proceed to the Completion Report

      - **If items fail (excluding [NEEDS CLARIFICATION])**:
        1. List the failing items and specific issues
        2. Update the spec to address each issue; an issue that needs a decision is a new
           question for the user (one more grilling round, step 8), never a guess. If the user
           already said "enough" (or there is no human to ask), ask nothing more: mark the issue
           `[NEEDS CLARIFICATION: <question>]` in place and add a `- Deferred: <question>
           (session ended by user)` bullet (or `(no human to ask)`) under today's session
           instead
        3. Re-run validation until all items pass (max 3 iterations)
        4. If still failing after 3 iterations, document remaining issues in checklist notes and warn user

      - **If [NEEDS CLARIFICATION] markers remain** (questions the user deferred, or no human
        to ask): leave the item unchecked and list the markers in the Completion Report.

   d. **Update Checklist**: After each validation iteration, update the checklist file with current pass/fail status

**Writes**: the branch (step 2), `FEATURE_DIR/spec.md`, `FEATURE_DIR/checklists/requirements.md`
and `FEATURE_DIR/research.md` (decision entries only), plus whatever first-run setup adds.
Nothing else — no code, no tests, no constitution, no agent guidance file, no other feature
directory.

## Completion Report

Report completion to the user with:
- The branch (and the branch it was made from, if not the default), or why none was made
- `FEATURE_DIR` — the feature directory path, and `SPEC_FILE` — the spec file path
- Rounds run; questions asked / answered / deferred; how the grilling ended (frontier empty and
  confirmed, "enough", or no human to ask)
- Facts investigated instead of asked, each with its source
- New scenario IDs; `**Supersedes**:` entries added; terms added (living ones marked); `R<n>`
  entries added to research.md
- `[NEEDS CLARIFICATION]` markers still open
- Checklist results summary
- Readiness for the next phase (`/s2tdd-plan`, or `/s2tdd-clarify` while questions stay open)

<!-- s2tdd:shared closing-step -->
**Last step.** Run `/s2tdd-next`. It commits and pushes this feature's specs, then prints the
recap and the next step as a ready-to-paste prompt. Run it as plain text; no hook runs it for
you.
<!-- /s2tdd:shared -->

## Quick Guidelines

- Focus on **WHAT** users need and **WHY**.
- Avoid HOW to implement (no tech stack, APIs, code structure).
- Written for business stakeholders, not developers.
- DO NOT create any checklists that are embedded in the spec. That will be a separate command.

### Section Requirements

- **Mandatory sections**: Must be completed for every feature
- **Optional sections**: Include only when relevant to the feature
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

### For AI Generation

When creating this spec from a user prompt:

1. **Mark every gap**: no informed guesses and no cap on `[NEEDS CLARIFICATION]` markers; each
   one becomes a question in the grilling
2. **Investigate facts**: what the code, the docs or the constitution already answer is looked
   up and written in with its source, never asked
3. **Recommend, don't assume**: a reasonable default (industry practice, the project's own
   patterns) is the question's recommended answer, accepted by the user in a word; it never
   fills the spec unasked
4. **Prioritize questions**: scope > security/privacy > user experience > technical details
5. **Think like a tester**: Every vague requirement should fail the "testable and unambiguous" checklist item
6. **Common areas needing clarification**:
   - Feature scope and boundaries (include/exclude specific use cases)
   - User types and permissions (if multiple conflicting interpretations possible)
   - Security/compliance requirements (when legally/financially significant)

**Examples of reasonable defaults** (offer them as recommended answers):

- Data retention: Industry-standard practices for the domain
- Performance targets: Standard web/mobile app expectations unless specified
- Error handling: User-friendly messages with appropriate fallbacks
- Authentication method: Standard session-based or OAuth2 for web apps
- Integration patterns: Use project-appropriate patterns (REST/GraphQL for web services, function calls for libraries, CLI args for tools, etc.)

### Success Criteria Guidelines

Success criteria must be:

1. **Measurable**: Include specific metrics (time, percentage, count, rate)
2. **Technology-agnostic**: No mention of frameworks, languages, databases, or tools
3. **User-focused**: Describe outcomes from user/business perspective, not system internals
4. **Verifiable**: Can be tested/validated without knowing implementation details

**Good examples**:

- "Users can complete checkout in under 3 minutes"
- "System supports 10,000 concurrent users"
- "95% of searches return results in under 1 second"
- "Task completion rate improves by 40%"

**Bad examples** (implementation-focused):

- "API response time is under 200ms" (too technical, use "Users see results instantly")
- "Database can handle 1000 TPS" (implementation detail, use user-facing metric)
- "React components render efficiently" (framework-specific)
- "Redis cache hit rate above 80%" (technology-specific)

## Done When

- [ ] Branch `NNN-<short-name>` created or switched to before anything was written (or the
      reason none was made reported)
- [ ] Specification written to `SPEC_FILE`, grilled until settled or the user said enough, and
      validated against the quality checklist
- [ ] Completion reported to user with branch, feature directory, spec file path, grilling
      summary and checklist results
- [ ] `/s2tdd-next` run as the last step
