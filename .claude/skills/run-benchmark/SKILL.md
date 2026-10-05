---
name: run-benchmark
description: "Benchmark two consecutive features' implement runs in a project that uses s2tdd, to judge what a workflow change did: wrong turns per packet by tier, whether each command's intent was upheld, token and context usage, plus wall time, stalls, human touches and delivery. Reads the project's feature directories and its Claude Code session transcripts read-only, fans the three axes out to subagents, and writes a report under the project's specs/benchmarks/ with ranked candidate findings for the backlog. Use after a pilot run, before specifying the refresh it motivates."
argument-hint: "<project dir> [<earlier feature> <later feature>], e.g. C:\\Git\\acme 003 004"
---

## User Input

`<project dir>` is the project whose runs are compared. The two features default to the newest
feature directory under `<project dir>/specs/` that has wave reports, and the one before it.
Ask only when the project dir is missing.

## Ground rules

- **Read-only on the project, except the report.** Another run may be live there. Never edit,
  create or delete a file in it other than the report (section 4), never run a git command that
  changes state (commit, checkout, switch, stash, reset, pull, tag), and never install, update
  or uninstall a plugin. Read files, run read-only git (`log`, `show`, `diff`), and run
  `tools/run_benchmark_tokens.py` (it only reads). Paths to the script are from this
  repository's root.
- **Names.** The report lives in the analyzed project's specs repository, which may name the
  project. Never write a report into this repository, and name no analyzed project in its
  files.
- **Evidence or label.** Every number carries its source (`file:line`, or a transcript id and a
  short snippet) and is marked **verified** (counted from the record) or **inferred** (judged).
  Say how each count was made; another reader must be able to redo it.
- **Normalize.** Features differ in size and difficulty. Compare per packet, per wave and per
  tier, never raw totals, and compare like slices (attended with attended, waves with reviewer
  subagents with the same). Flag a run that is still going as partial.

## 1. Locate the record

1. **Feature files**, per feature: `spec.md`, `plan.md`, `tasks.md`, `orchestration.md` (wave
   table with its Tier column, ground rules, context budget), `handoff.md`, `run-ledger.md`
   (Lease, Usage, Carried constraints, Amendments, Test-owner fixes, Ownership exceptions,
   Expected red, Blocked and skipped, Open review notes), `s<k>-wave-reports.md`,
   `validation.md` (verification log), `close-out.md`, `contracts/`.
2. **Transcripts**: `~/.claude/projects/<slug>*/`, where the slug is the project path with `:`,
   `\` and `/` turned into `-` (`C:\Git\acme` → `C--Git-acme`); worktree sessions sit in
   `<slug>--claude-worktrees-*`. Subagent transcripts are under `<session id>/subagents/`.
3. **Sessions**: `python -X utf8 tools/run_benchmark_tokens.py <transcripts dir> find
   <feature number> <word>` lists the sessions whose user messages mention them. Classify each
   by its first command (specify, clarify, plan, harden, implement attended or `--nobrakes`
   relay, verify-done, converge, pr-review, close).
4. **Workflow version** per run: the command prefix (`/speckit-` preset or `/s2tdd-` plugin),
   the plugin version in the skills' base-directory lines in the transcripts
   (`…\plugins\cache\s2tdd\s2tdd\<version>\…`), and the handoff's dispatch rules. Then list the
   workflow changes between the two runs: `git log` of this repository between the
   runs' dates, plus any interim rule the user typed into a running session.

## 2. Run profile (both features)

One table: packets per tier, tasks, waves, slices, attended vs `--nobrakes` waves, sessions and
relays, wall time, and the models that actually ran each role — orchestrator, each tier's
packets, diff reviewer, verifier (from each `Agent` tool_use's `subagent_type` and `model`, and
the `model` of the subagent transcripts' assistant entries; a dispatch with neither inherits the
session's model).

## 3. The three axes (fan out)

Dispatch one read-only subagent per axis in a single message, each with the ground rules above,
the located files and session ids, and a word cap (about 600). Run the extras (axis D) yourself
while they work.

### A. Wrong turns

- Count, per packet and charged to the packet that made the mistake, only the checks every packet
  faced: fence failures, test-owner fixes, re-opened or fix packets, unexpected reds traced to a
  real defect, rejected deviations, verify-done unticks and gaps. Report per tier: count,
  per-packet rate, what they were.
- Separately, what the reviewers caught (blockers, Rejects, Accept with fixes) and on which tiers
  — a defect only a reviewer caught shows what an unreviewed tier would have shipped.
- **Wave lag**: defects found waves after the packet that made them (test packets pinning a wrong
  contract shape are the usual case); give the packet, its wave and the wave it surfaced.
- **Red before green**: implementation reports with no red run, or a red taken after the code was
  written; and whether verify-done (attended or proxy) flagged each, or sampled.
- Rework cost: fix packets, second suite runs per wave, minutes lost.
- Caveat platform flakes (Windows timing, file locks) separately from logic defects.

### B. Command intent upheld

For each command the features ran, read its rules from the version that ran it (the plugin
cache, or this repository at that date) and check the record against them. Report each rule
as **upheld / partly / broken**, with evidence, and note rules that changed between the runs.
Rules worth checking for implement (with or without `--nobrakes`):

- dispatch only, never implementing in the orchestrator; dispatch by the tier's agent type;
- red before green, with the orchestrator's pre-dispatch confirmation;
- one live writer per file; owned files only; reports by exception (card size, no code);
- reviews: who was reviewed, versus who the rules say;
- verify gates: when they ran, whether the verifier read everything or sampled;
- wave-boundary bookkeeping: usage read and recorded, stop file checked, ledger appended, tags;
- handoff: clean boundary, "nothing written after the handoff commit", how the next relay
  started, and whether it stalled;
- stop rules (usage limits, blocked guard packets) and what happened when they fired.

For verify-done, converge and close: did each do what its skill promises (every claim checked,
gaps turned into tasks, notes carried to close-out)? **Human interventions** are the sharpest
evidence of intent failing: every user message typed into a running unattended session, quoted
in short with its time and what it corrected.

### C. Token usage

- `python -X utf8 tools/run_benchmark_tokens.py <transcripts dir> session <ids…>` for every
  orchestrator session: context at start and at first dispatch (the fixed overhead of loading
  the feature), max and end; dispatches; compactions; idle gaps; summed tokens for the session
  and its subagents.
- Per packet and per wave: `(end − start) / packets` and `/ waves`, per session and in total.
  Pair like slices.
- Where the context went: shares of characters entering the orchestrator's context, grouped as
  startup reads, packet dispatches and cards, reviewer and verifier hand-backs, test and git
  output, the orchestrator's own text. Name the largest single reads and any re-reads.
- Plan usage: the `get_usage` results and the ledger's Usage lines, per window, at the start and
  end of each relay.
- Cache reads dominate the raw totals; report them, but judge the workflow on context per packet.

### D. The obvious extras (do these yourself)

- **Time**: wall time per wave and per packet, suite minutes per wave against the guidance file's
  suite-time budget, time a verify gate held the tree.
- **Stalls**: idle gaps over 15 minutes in an unattended session, with their cause.
- **Human touches**: messages per session, and how many sessions needed the user mid-run.
- **Delivery**: tasks delivered, blocked, skipped and deferred; verify-done verdicts; converge
  rounds; deviations in close-out; the suite's size and time before and after.

## 4. Write the report

Write the report to the analyzed project's specs repository:
`<project dir>/specs/benchmarks/<project>-<earlier>-vs-<later>.md` (create the directory if
missing). Never write a report into this repository. The report holds:

1. **Verdict** in three to five lines: what changed between the runs, and what the evidence says
   it did.
2. **Run profiles** (section 2's table) and the workflow changes between the runs.
3. **Wrong turns**, **Command intent**, **Token usage**, **Time, stalls, touches and delivery**:
   a table per section, each figure with its source and verified/inferred mark.
4. **What this suggests**: which changes the evidence supports and which it doesn't, with the
   competing explanations (model, review scope, feature difficulty, run shape).
5. **Candidate findings**, ranked by impact: one-line problem, evidence, the s2tdd rule it points
   at (`skills/<command>/SKILL.md:<line>`), how often, one-line suggested change, verified or
   inferred. Skip the project's own product bugs.
6. **Caveats**: counting coarseness, partial runs, flakes, size and difficulty differences.

Then print the verdict and the ranked findings, and offer to log the findings the user picks in
this repository's specs repository, `specs/backlog.md` (why, evidence, what to change, and the
`/s2tdd-specify` prompt that starts it), or to feed them into the spec being written.
