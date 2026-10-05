# Models and budget

[← Back to the README](../README.md)

Where to spend your attention, and your model budget.

## The first steps are where the feature is decided

`/s2tdd-epic`, `/s2tdd-specify` and `/s2tdd-clarify` are the only steps where *you* shape what
gets built. Every step after them faithfully builds whatever the spec says, so a vague scenario
or a hand-waved answer turns into a confidently wrong test, then confidently wrong code that
passes it.

Slow down here:

- **Read the spec's scenarios as if you'll be held to them**, because you will. Each one
  becomes a test.
- **Don't accept a recommended answer you haven't thought about.** "Enough" is for when the
  design really is settled, not when you're tired of questions.
- **If the work is foggy, use the epic.** An hour of decisions there saves days of rework later.

## Match the model to the step

Thinking steps need your strongest model. Building steps follow a plan precise enough that the
implementing session can run on a cheaper one: it only orchestrates, and each packet runs on
Opus at its tier's effort (see [Agent types](#agent-types-keep-the-tiers-honest)).

| Steps | What they need | Use (examples as of October 2026) |
|---|---|---|
| epic → specify → clarify | Judgment, asking the right questions, catching what you didn't say | Your strongest model at high effort, e.g. Opus 5.5 (high) |
| plan → harden, and pr-review | Design, seams and contracts; turning intent into packets that can't drift; judging a finished change | Same: Opus 5.5 (high) |
| implement → verify-done → converge | Following a hardened plan, test-first, inside fences | A cost-efficient model, e.g. Grok 4.6, Sol 6 (medium) or Opus 5.5 (medium) |

This split is the point of hardening: the expensive thinking happens once, up front, and is
written down so precisely that the many implementation waves can run under a cheaper session,
with each packet at the lowest effort its task allows, without drifting.

You don't have to track this yourself. `/s2tdd-next` says when a fresh session or a cheaper
model fits the next step.

## Agent types keep the tiers honest

A subagent with no effort of its own inherits the session's, so lowering the orchestrator would
silently lower every packet. The plugin ships an agent type per role, each with its own model
and effort, and implement dispatches to them as `s2tdd:<name>`. Every one runs on Opus; the
tiers differ in effort, so a packet gets the depth its task needs whatever the session runs on:

| Agent type | Role | Model, effort |
|---|---|---|
| `packet-cheap` | Implements a cheap-tier packet | opus, low |
| `packet-medium` | Implements a medium-tier packet | opus, medium |
| `packet-strong` | Implements a strong-tier packet | opus, high |
| `strong-diff-reviewer` | Reads a strong packet's diff before its wave commit in an [unattended run](nobrakes.md), and each wave's shape check: the wave's test packets against the contract sections they cite | opus, high |
| `proxy-verifier` | Runs verify-done for you in an [unattended run](nobrakes.md) | opus, medium |
| `converger` | Runs converge for you in an [unattended run](nobrakes.md) that loops to ready-to-close | opus, medium |
| `hardener` | Hardens converge's appended tasks for you in an [unattended run](nobrakes.md) | opus, high |

Agent types come with the plugin. A project that runs from a copy of the skills doesn't have
them, and implement falls back to a general subagent; see
[Getting started](getting-started.md#without-the-plugin).
