---
name: s2tdd-epic
description: "Plan work too big and too unclear for one spec: name the destination (one or more feature specs), chart a map of decision tickets under specs/epics/<slug>/, and resolve them one per session (research tickets in parallel) until the way is clear; then hand each feature to /s2tdd-specify seeded with the decisions made. Plans, never builds (s2tdd)."
argument-hint: "A loose idea to chart, or an epic slug (and optional ticket number) to work"
---

## User Input

Consider the text the user typed after the command: a loose idea to chart, or an epic slug (and an
optional ticket number) to work. You **MUST** consider it before proceeding (if not empty).

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

## Goal

Some work is too big for one agent session and too foggy for one spec — a product pivot, a new
front end, a cross-cutting redesign. Charging at it with `/s2tdd-specify` produces a
spec full of guesses. This command finds the way first: it names the **destination**, charts a
**map** of the decisions standing between here and there, and resolves them one at a time with
the user until nothing is left to decide. The destination is always one or more feature specs
handed to `/s2tdd-specify`, each seeded with the decisions made.

Adapted from mattpocock/skills (MIT) — `wayfinder`, with `grilling`, `domain-modeling`,
`research` and `prototype` as its ticket disciplines — reshaped for s2tdd and local
markdown.

**Plan, don't build.** Every ticket resolves a decision. No source, test or feature-spec file is
written here. The pull to "just do it" means you have reached the edge of the map: hand off.

**HITL is sacred.** Grilling and prototype tickets resolve only through the live user. Never
answer your own question, never settle a decision from silence. Facts are yours to find; the
decisions are the user's.

**Refer by name.** Every map and ticket has a name (its title). In everything the user reads,
use the name, linked to its file — never a bare number or slug. A link inside an epic file is
relative to that file; a link in chat is the path from the repo root
(`specs/epics/<slug>/tickets/NN-<slug>.md`), never copied from a file or relative to a `cd`.

## Where an epic lives

```text
specs/epics/<slug>/
├── map.md                  # the index: destination, notes, decisions, fog, out of scope
├── tickets/NN-<slug>.md    # one decision per file, numbered from 01, never renumbered
├── research/NN-<slug>.md   # findings of research ticket NN (cited sources)
└── prototypes/NN-<slug>/   # throwaway artifacts of prototype ticket NN
```

`specs/epics/` sits beside the feature directories and is ignored by feature numbering. Like a
feature directory it is an intent record, not documentation (see `specs/README.md`).

### map.md

```markdown
# Epic: <name>

**Status**: Open
<!-- Open while charting and working. Closed — YYYY-MM-DD — <sha> — specs: <NNN-a>, <NNN-b>
     once every hand-off spec exists; then frozen, never edited. -->

## Destination

<one or two lines: the feature spec(s) this epic finds its way to, and what each is for>

## Notes

<domain; constraints (constitution principles in play, invariants from the agent guidance
file); standing preferences for this epic>

### Language

<resolved terms: `- **Term**: what it is. _Avoid_: synonyms` — carried into the hand-off seeds>

## Decisions so far

<!-- the index: one line per resolved ticket; the ticket holds the detail, never restate it -->

- [<ticket name>](tickets/NN-<slug>.md): <one-line gist of the answer>

## Not yet specified

<!-- fog of war: in-scope questions you cannot yet phrase sharply; graduate into tickets -->

## Out of scope

<!-- ruled beyond the destination: gist + why, linking the closed ticket; never graduates -->

## Hand-off

<!-- empty until the way is clear; one seed per destination spec (see Hand off) -->
```

Open tickets are **not** listed on the map: they are the files under `tickets/` whose Status is
`open`. The map indexes decisions; each decision lives in exactly one place, its ticket.

### tickets/NN-slug.md

```markdown
# <ticket name>

**Type**: research | prototype | grilling | task
**Status**: open
<!-- open | claimed — <session or person> — YYYY-MM-DD | resolved — YYYY-MM-DD | out of scope -->
**Blocked by**: none
<!-- or ticket numbers: 02, 05 -->

## Question

<the one decision or investigation this ticket resolves, sized to one session>

## Answer

<added on resolution: the decision and its why; links to research/ and prototypes/ assets>
```

A ticket is **unblocked** when every ticket it lists is `resolved`. The **frontier** is every
open, unblocked, unclaimed ticket, lowest number first.

## Ticket types

- **research** (AFK): a fact a decision waits on, from outside what you already have loaded —
  library or service docs, APIs, pricing, licences, prior art. Dispatch a subagent per ticket
  (in parallel; without subagents, research them one after another here); it reads **primary sources** (official docs, source code, specs), follows every
  claim to the source that owns it, and writes `research/NN-<slug>.md` citing each claim. The
  Answer is a gist plus that link. The only type you may resolve several of in one session.
- **prototype** (HITL): raise the fidelity of a "how should it look / behave" question with a
  cheap, rough, concrete artifact the user can react to — an outline, a sample transcript, a
  stub, a single-file logic demo. Throwaway from day one: it lives in `prototypes/NN-<slug>/`
  (or a throwaway branch named in the Answer), never in `src/`, no tests, no persistence. If it
  needs a live model, run it yourself by script and show the user the results; hand the user
  steps and wait only when their own interaction is what the prototype tests. The Answer records the verdict and the question it settled.
- **grilling** (HITL, the default): a conversation. Use the `/s2tdd-clarify`
  discipline against the ticket instead of a spec — rounds of questions each with a recommended
  answer, facts investigated not asked, the language challenged, concrete scenarios to probe
  boundaries. Resolved terms go to the map's **Language**.
- **task** (AFK or HITL): work that must happen before a decision can be made — provision
  access, export data to see its shape, sign up to judge an API. The one type that *does*, and
  it earns its place only by unblocking a decision. Drive it yourself where you can; otherwise
  hand the user a precise checklist. The Answer records what was done and the facts later
  tickets depend on (never secrets — where they are kept, not their values).

**Fog or ticket?** Ticket a question you can state precisely now, even if it is blocked. Leave
it in **Not yet specified** if you cannot yet phrase it sharply — do not pre-slice fog into
ticket-sized pieces; one patch may graduate into several tickets or none. Work beyond the
destination is **Out of scope**, not fog: it never graduates.

A decision that would breach a constitution MUST (e.g. a pivot away from a core principle) is
a grilling ticket whose answer may be "amend the constitution" — the epic records the decision;
the amendment is a separate `/s2tdd-constitution` step, itself a ticket of type
task.

## Execution

Read the constitution (`specs/constitution.md`) and the project's agent guidance file first. If
`specs/constitution.md` is missing, say in one line that `/s2tdd-constitution` creates one, then
carry on.

Then pick the mode from the input. Text naming an existing `specs/epics/<slug>` (optionally with
a ticket number) → **Work**; anything else → **Chart**; empty → resolve the epic as below and
**Work** it, or, when more than one is open, list the open epics with their Status and frontier
size and ask which.

<!-- s2tdd:shared epic-resolution -->
**Which epic.** Work out the epic, in this order; the first match wins:

1. **Named.** The text the user typed after the command names a slug, and
   `specs/epics/<slug>/` exists.
2. **Single open epic.** Exactly one epic in `specs/epics/` has a `map.md` whose `**Status**:`
   does not begin with `Closed`.
3. **Ask.** Otherwise, list the open epics and ask which one.
<!-- /s2tdd:shared -->

Refuse any epic whose map Status begins with `Closed`: "This epic is closed; its specs exist and own the work now. New direction is a new epic."

### Chart the map (one session; resolves nothing)

1. **Name the destination.** Grill the user until the destination is settled: which feature
   spec(s) this ends in, what each is for, and what is plainly not part of it. The destination
   fixes the scope, so nothing else is asked first.
2. **Map the frontier, breadth-first.** Grill again, wide rather than deep: surface the open
   decisions across the whole space and the first ones takeable now. If this finds no fog — the
   way is already clear and small enough for one spec — say so and stop: run
   `/s2tdd-specify` directly, no epic.
3. **Create `map.md`**: Status `Open`, Destination and Notes filled, Decisions so far empty, the
   fog sketched into **Not yet specified**, Out of scope from step 1.
4. **Create the tickets you can state now**, then wire `**Blocked by**:` in a second pass (a
   ticket needs its number before others can cite it).
5. **Fire the research subagents** for every research ticket, in parallel (without subagents,
   research them one after another here), then record each one's Answer as it reports.
6. **Stop.** Report the map path, the frontier by name, the fog, and who resolves what next.

### Work the map (one ticket per session, except research)

1. **Load `map.md`** — the low-resolution view; open ticket bodies only as needed.
2. **Choose the ticket**: the one the user named, else the first frontier ticket. **Claim it
   first** — set `**Status**: claimed — <you> — <date>` and save before any other work, so a
   concurrent session skips it. A ticket already claimed by someone else is theirs: pick
   another, or ask the user whether the claim is stale.
3. **Resolve it** by its type (above). Open related or resolved tickets on demand.
4. **Record**: write `## Answer`, set `**Status**: resolved — <date>`, and append one line to the
   map's **Decisions so far** (name, link, gist).
5. **Reshape the map**: add newly surfaced tickets (create, then wire); graduate fog the answer
   made specifiable and delete it from **Not yet specified**; a ticket the answer shows to be past
   the destination is set `out of scope` and gets one line under **Out of scope** (never under
   Decisions so far); a ticket the decision invalidates is rewritten or ruled out, with a note.
6. **Stop** after one ticket (research tickets excepted). Report the decision, the new frontier
   by name, and the fog that remains. Expect other sessions to be editing the map concurrently —
   re-read `map.md` before writing it.

### Hand off (when the frontier and the fog are both empty)

1. Write one **seed** per destination spec under the map's **Hand-off**: the feature
   description to pass to `/s2tdd-specify`, the decisions it must honour (name +
   link + gist, never restated in full), the Language it inherits, and its Out of scope.
2. Ask the user to confirm the seeds reflect a shared understanding before anything else.
3. The user runs `/s2tdd-specify` with each seed (one feature branch each). The
   seeded decisions reach each feature through its spec and `research.md` (clarify and plan
   cite the tickets as rationale).
4. **Close the epic** once every seeded spec exists: set map.md's Status to
   `Closed — <DATE> — <SHA> — specs: <NNN-a>, <NNN-b>`. This is the last edit to the directory;
   from then on it is frozen history, never back-edited. A feature that later changes an epic
   decision records it in its own spec (`**Supersedes**:`), exactly as for closed features.

## Completion Report

- Mode (chart / work / hand off / close) and the epic path.
- Chart: destination, tickets created by name and type, blocked edges, fog, research dispatched.
- Work: the ticket resolved (name, type, answer gist), tickets added / graduated / ruled out.
- Frontier by name and who resolves each next (HITL or AFK); fog remaining.

<!-- s2tdd:shared closing-step -->
**Last step.** Run `/s2tdd-next`. It commits and pushes this feature's specs, then prints the
recap and the next step as a ready-to-paste prompt. Run it as plain text; no hook runs it for
you.
<!-- /s2tdd:shared -->
