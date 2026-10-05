"""Tests of the eval suite's shape (II-14; T080): cases, fixture helpers, scaffolds, names.

Red until T081-T085 write ``evals/``: every test starts from the suite's own files, so each
fails with "evals/ not found". The constants below are transcribed (spec.md for the scenario
text, tasks.md's Scenarios lines for the slugs, contracts/eval-suite.md for the areas); the
tests never import a tool.

Parametrization ids are the scenario IDs with ``-`` replaced by ``_`` (``US2_AC1``, ``EC_002``),
so ``pytest -k "US2 or EC_002"`` selects a task's cases. Test names that ``-k fixtures``
(T081's done-when) must not select do not contain that word.

002 (II-16; T058, R8) adds ``SCENARIOS_002``: its 38 V1 cases live in
``evals/<area>/002-<ID>-<slug>/`` and run through the same coverage, shape and scaffold tests
with ids ``002_<ID with _>`` (``002_US1_AC1``, ``002_EC_003``). The areas gain ``verify`` and
``converge``; ``make-feature.sh`` gains three states, checked for the files II-16 names. These
are red until T059 (the states) and T060-T064 (the cases).

003 (II-15; T023, R13) adds ``SCENARIOS_003``: its 23 V1 cases live in
``evals/<area>/003-<ID>-<slug>/`` with ids ``003_<ID with _>`` (``003_US1_AC2``,
``003_EC_004``), through the same coverage, shape and scaffold tests. The areas gain ``close``;
``make-feature.sh`` gains four states (``looping``, ``per-wave``, ``green-run``, ``docs-wave``),
each checked for what II-15 says it leaves. Red until T026 (the states) and T027-T030 (the
cases). 002's states and cases are history and stay as they are.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlparse

import pytest
import yaml

# The 35 scenario IDs plan.md maps to V5 (US5-AC3 excluded: it is the run itself), each with
# its area (contracts/eval-suite.md), the slug tasks.md's Scenarios lines name, and the
# scenario's text from spec.md (bold markers dropped; compared after whitespace folding).
SCENARIOS = (
    ('US1-AC2', 'setup', 'offers-specs-repo',
     'Given a repository the user owns with no `specs/` directory, When the user runs '
     '`/s2tdd-specify` for the first time there, Then it offers to clone or create the '
     'specs repository, copies `specs/README.md` and `specs/WORKFLOW.md` in, and adds only '
     '`specs/` and `.sdd-run/` to the local excludes (T09, T10).'
     ),
    ('US1-AC3', 'setup', 'foreign-no-footprint',
     'Given a repository whose remote belongs to someone other than the user, When '
     'first-run setup runs there, Then `git status` in the project shows no change '
     "afterwards: nothing tracked is added or modified (T10's ownership rule)."
     ),
    ('US1-AC4', 'specify', 'next-number-branch',
     'Given a set-up repository on its default branch with features `001`–`003` in '
     '`specs/` and a remote-only branch `004-x`, When the user runs `/s2tdd-specify` with '
     'a description, Then it creates and switches to branch `005-<short-name>` and writes '
     "`specs/005-<short-name>/spec.md` with ID'd scenarios (T07)."
     ),
    ('US1-AC5', 'specify', 'gaps-and-grilling',
     'Given a description that leaves design questions open, When `/s2tdd-specify` drafts '
     'the spec, Then every open gap is marked in the draft with no cap on their number and '
     'no informed guesses, and the command grills the user, one round at a time with a '
     'recommended answer per question, until the gaps are resolved or the user says enough '
     '(T07).'
     ),
    ('US1-AC6', 'setup', 'constitution-pointer',
     'Given a repository with no `specs/constitution.md`, When the user runs '
     '`/s2tdd-specify` or `/s2tdd-epic`, Then the command says that `/s2tdd-constitution` '
     'creates one, and carries on (T11).'
     ),
    ('US1-AC7', 'next', 'saves-then-prompts',
     'Given any s2tdd command other than `/s2tdd-next` finishing normally, When it reaches '
     'its last step, Then it runs `/s2tdd-next`, which commits and pushes the active '
     "feature's (or epic's) files in the specs repository first and then prints the recap "
     'and the next step as a ready-to-paste prompt (T07, T08).'
     ),
    ('US1-AC8', 'setup', 'foreign-excludes',
     'Given a repository whose remote belongs to someone other than the user, When '
     'first-run setup writes the local excludes, Then they list `specs/`, `.sdd-run/` and '
     '`.claude/skills/s2tdd-*/` (T09, T10).'
     ),
    ('US2-AC1', 'plan', 'plan-artifacts-and-gate',
     'Given a specified feature and a `specs/constitution.md`, When the user runs '
     '`/s2tdd-plan`, Then it writes `plan.md`, `research.md`, `data-model.md`, '
     '`contracts/` and `quickstart.md` with the structure and adaptations T11 lists, and a '
     'constitution violation stops the plan unless it is justified in the plan (T11).'
     ),
    ('US2-AC2', 'plan', 'r-entries',
     "Given a plan's `research.md`, When any s2tdd command writes a decision to it, Then "
     'the decision is an R-entry (`## Rn. <the decision as a sentence>`) with its '
     'rationale and alternatives under it (T11).'
     ),
    ('US2-AC3', 'harden', 'first-harden',
     'Given a planned feature with no `tasks.md`, When the user runs `/s2tdd-harden`, Then '
     'one run writes `tasks.md` test-first and the hardened files (orchestration, handoff, '
     'validation, run ledger), and passes its validation gates (T07).'
     ),
    ('US2-AC4', 'harden', 'single-phase',
     'Given a hardened feature, When the user runs `/s2tdd-harden` naming one phase, or '
     "asking to append new tasks or refresh, Then it runs only that mode, as today's "
     'harden does (T07).'
     ),
    ('US2-AC5', 'implement', 'agent-type-per-tier',
     'Given a hardened feature and an orchestrating session started at a lower effort than '
     "a packet's tier, When `/s2tdd-implement` dispatches that packet, Then the packet "
     "runs as the agent type for its tier, at that type's own model and effort (T15)."
     ),
    ('US2-AC6', 'implement', 'print',
     'Given a hardened feature, When the user runs `/s2tdd-implement --print`, Then it '
     'prints the filled implement prompt for another harness and runs nothing (T07).'
     ),
    ('US2-AC8', 'refusals', 'refusals',
     'Given an unhardened feature, a closed feature, or owned files held by another '
     'session, When the user runs a command that refuses that state today (implement, '
     'converge, close), Then it refuses with the same reason it gives today, under its '
     '`/s2tdd-` name.'
     ),
    ('US3-AC2', 'next', 'leftovers',
     'Given a project that still has `.specify/`, any `speckit-*` skill or '
     '`docs/sdd-workflow.md`, When the user runs `/s2tdd-next`, Then each one is listed '
     'under Watch out (T10).'
     ),
    ('US3-AC3', 'harden', 'handoff-refresh',
     'Given a hardened, unfinished feature carried over from the preset, When the user '
     'runs `/s2tdd-harden handoff`, Then its `handoff.md` and `orchestration.md` name only '
     '`/s2tdd-` commands, and `/s2tdd-implement` resumes at the wave it had reached (T10).'
     ),
    ('US3-AC4', 'refusals', 'stale-handoff-names',
     'Given a hardened feature whose `handoff.md` or `orchestration.md` still names '
     '`/speckit-` commands, When the user runs `/s2tdd-implement`, with or without '
     '`--nobrakes`, Then it stops before dispatching anything and says to run '
     '`/s2tdd-harden handoff` first.'
     ),
    ('US3-AC7', 'harden', 'records-untouched',
     'Given a carried-over feature whose `validation.md`, `run-ledger.md` and `tasks.md` '
     'name `/speckit-` commands, When the user runs `/s2tdd-harden handoff`, Then those '
     'three files are unchanged.'
     ),
    ('US6-AC1', 'resolution', 'argument',
     'Given `specs/004-csv-export/` and the current branch `main`, When the user runs a '
     'command with `004` as its argument, Then it works on `004-csv-export` (T08).'
     ),
    ('US6-AC2', 'resolution', 'fix-branch',
     'Given the current branch `claude/004-fix-flake` and a single `specs/004-*` '
     'directory, When the user runs a command with no argument, Then it works on that '
     'feature (T08).'
     ),
    ('US6-AC3', 'resolution', 'ask-no-pointer',
     'Given a branch that matches no feature and two open features, When the user runs a '
     'command with no argument, Then it lists the open features and asks which one, and '
     'never writes a pointer file (T08).'
     ),
    ('US6-AC4', 'resolution', 'worktree-specs',
     'Given a desktop-app worktree with no `./specs`, When the user runs a command, Then '
     "it uses the main worktree's `specs/`, says so, and its spec writes land in the one "
     'specs repository (T08).'
     ),
    ('US6-AC6', 'cloud', 'refuse-in-cloud',
     'Given a cloud session, When the user starts `/s2tdd-pr-review` there, Then it '
     'refuses and says to start it locally with `--cloud` (T05).'
     ),
    ('US7-AC2', 'next', 'over-budget',
     "Given a suite-time budget stated in the project's agent guidance file and a "
     'verify-done or converge run whose full suite exceeds it, When the user runs '
     '`/s2tdd-next`, Then the recorded wall time and the budget show under Watch out, and '
     'nothing refuses because of it (T16).'
     ),
    ('US7-AC3', 'upkeep', 'upkeep-task',
     'Given a converge run over the budget, When converge appends its tasks, Then one of '
     'them is a test-upkeep task (T16).'
     ),
    ('US7-AC4', 'upkeep', 'pruning-findings',
     'Given duplicate or obsolete tests in a project, When `/s2tdd-foundation-review` or '
     '`/s2tdd-close` runs, Then they are listed as findings and no test is removed or '
     'skipped (T16).'
     ),
    ('US8-AC1', 'constitution', 'create',
     'Given no `specs/constitution.md`, When the user runs `/s2tdd-constitution`, Then it '
     'grills them and writes `specs/constitution.md` from its bundled template (T11).'
     ),
    ('US8-AC2', 'constitution', 'amend',
     'Given an existing constitution at version 1.1.0, When the user amends a principle '
     "with `/s2tdd-constitution`, Then the file's version is bumped and a dated change "
     'note is added in the file (T11).'
     ),
    ('US9-AC1', 'next', 'merged-branches',
     'Given a feature whose PR has merged and whose branch still exists locally and on the '
     'remote, When the user runs `/s2tdd-next`, Then both branches are listed under Watch '
     'out with the commands to delete them, and nothing is deleted (T15).'
     ),
    ('EC-001', 'resolution', 'ambiguous-number',
     'Given a branch name whose leading number matches two `specs/NNN-*` directories, When '
     'a command resolves the feature, Then it lists the open features and asks, rather '
     'than picking one (T08).'
     ),
    ('EC-002', 'refusals', 'closed-feature',
     'Given a feature named in the arguments that is closed, When a command that refuses '
     'closed features runs, Then it refuses and says the feature is closed.'
     ),
    ('EC-003', 'next', 'no-remote',
     'Given a specs repository with no remote, When `/s2tdd-next` saves, Then it commits, '
     'says the push was skipped and why, and still prints the next step.'
     ),
    ('EC-005', 'next', 'no-budget',
     'Given a project whose agent guidance file states no suite-time budget, When '
     'verify-done or converge records a suite run, Then the wall time is recorded and '
     'nothing is reported as over budget (T16).'
     ),
    ('EC-007', 'setup', 'setup-silent',
     'Given a repository where first-run setup already ran, When another s2tdd command '
     'runs first-run checks, Then it changes nothing and says nothing about setup.'
     ),
    ('EC-008', 'setup', 'old-page-left',
     'Given a project where an earlier, unmigrated copy of a project page exists '
     '(`docs/sdd-workflow.md`), When first-run setup copies the pages, Then it writes '
     '`specs/WORKFLOW.md`, leaves the old file in place, and `/s2tdd-next` reports it as a '
     'leftover (T10).'
     ),
)

# 002 (II-16): the 38 scenario IDs tasks.md's Scenarios lines map to CHECKPOINT V1, in that
# file's order, each with its area and slug (those lines' evals/<area>/002-<ID>-<slug>) and
# the scenario's text from 002's spec.md (bold markers dropped; compared after whitespace
# folding). Each case's directory and description carry the ID behind ``002-``.
SCENARIOS_002 = (
    ('US1-AC1', 'implement', 'shape-check-reads-test-packets',
     "Given a wave with three test packets, When the orchestrator reaches that wave's "
     "commit, Then one shape check has read all three packets' test diffs and the contract"
     " sections they cite, and its verdict is in the wave report's Review line."
     ),
    ('US1-AC2', 'implement', 'no-test-packets-no-check',
     'Given a wave with no test packets, When the orchestrator reaches its commit, Then no'
     ' shape check runs.'
     ),
    ('US1-AC3', 'implement', 'shape-check-agent-type',
     "Given an implement run in either mode, When a wave's shape check is due, Then it is "
     'dispatched as the `strong-diff-reviewer` agent type with the Shape check brief.'
     ),
    ('US1-AC4', 'implement', 'nobrakes-fix-before-commit',
     'Given a `--nobrakes` run whose shape check finds a test asserting a shape that '
     'differs from its cited section, When the orchestrator handles the finding, Then the '
     "test packet's own agent fixes the test before the wave commit, and a short re-check "
     'covers the disputed items.'
     ),
    ('US1-AC5', 'implement', 'attended-report-only',
     'Given an attended run whose shape check finds the same, When the orchestrator '
     'handles it, Then the finding appears in the wave report as a recommendation, and the'
     ' wave is committed and the run continues as before.'
     ),
    ('US1-AC6', 'implement', 'strong-review-kept',
     'Given a wave with strong packets and test packets, When its commit is due, Then each'
     ' strong packet still gets its own strong-diff review in `--nobrakes`, as today, '
     "besides the wave's one shape check."
     ),
    ('EC-001', 'implement', 'shape-check-general-subagent',
     "Given a project running from a copy of the skills, without the plugin's agent types,"
     " When a wave's shape check is due, Then a general subagent runs it with the same "
     'brief, as implement already does for any missing agent type '
     '(`skills/s2tdd-implement/SKILL.md:162-167`).'
     ),
    ('EC-002', 'implement', 'old-handoff-note',
     'Given a feature hardened before this change (its handoff.md has no shape check), '
     "When it is implemented with the new plugin, Then its handoff's rules hold unchanged,"
     ' and implement says once that the handoff predates the shape check and that '
     '`/s2tdd-harden handoff` refreshes it.'
     ),
    ('US6-AC1', 'implement', 'must-breach-blocks-nobrakes',
     'Given a review finding that a packet breaks a spec MUST, When the orchestrator '
     'handles it in a `--nobrakes` run, Then the packet fixes it before the wave commit, '
     'or is BLOCKED, and the finding is never recorded under Open review notes.'
     ),
    ('US6-AC2', 'verify', 'must-breach-not-done',
     'Given verify-done finds a committed change that breaks a spec MUST, When it gives '
     'its verdict, Then the verdict is Not done and the task is unticked.'
     ),
    ('US6-AC3', 'converge', 'ledger-notes-to-tasks',
     'Given run-ledger.md has open review notes and "carry to converge" constraints, When '
     'converge runs, Then each one still open becomes a task in tasks.md or is cited as '
     'resolved.'
     ),
    ('US6-AC4', 'implement', 'must-breach-heads-report',
     'Given a review finding that a packet breaks a spec MUST in an attended run, When the'
     ' wave report is written, Then it heads the report as "MUST breach: fix before the '
     'next wave".'
     ),
    ('US7-AC1', 'implement', 'relay-prints-handoff',
     'Given a relay that reaches its handoff, When it hands off, Then it prints the '
     'handoff prompt, sends a push notification where the harness can, and stops; it never'
     ' starts the next relay as a scheduled task or a background session.'
     ),
    ('US7-AC2', 'implement', 'handoff-points-at-constraints',
     'Given a ledger whose Carried constraints changed during the run, When a relay writes'
     ' its handoff prompt, Then the prompt points at Carried constraints and restates none'
     ' of them.'
     ),
    ('US3-AC1', 'verify', 'late-red-run-gap',
     'Given an implementation packet report that says its red run happened after it wrote '
     "its implementation files, and the orchestrator's check before dispatch saw the test "
     'red, When verify-done checks the waves, Then the packet is listed as a gap and the '
     'verdict is at best Verified with gaps.'
     ),
    ('US3-AC2', 'verify', 'missing-red-run-gap',
     'Given an implementation packet report that quotes no red run, and the wave report '
     'shows the orchestrator saw the test red before dispatch, When verify-done checks the'
     ' waves, Then the packet is listed as a gap.'
     ),
    ('US3-AC3', 'verify', 'reads-every-red-run',
     'Given wave reports for 30 implementation packets, When verify-done (or its proxy) '
     "checks red-before-green, Then it states that it read all 30 reports' red runs."
     ),
    ('US3-AC4', 'verify', 'never-red-not-done',
     "Given an implementation packet whose test neither its report nor the orchestrator's "
     'pre-dispatch check ever shows red, When verify-done checks the waves, Then the '
     "verdict is Not done, the task is unticked, and the fix line says the test's own "
     'packet must show it red at the commit before the implementation.'
     ),
    ('US4-AC1', 'implement', 'citation-lines',
     'Given a test packet whose tests assert a shape a later wave implements, When it '
     'reports, Then its report has one line per such shape citing `contracts/<file> '
     '§<section>`.'
     ),
    ('US4-AC2', 'implement', 'check-per-citation',
     "Given a test packet's report with those citations, When the shape check reads it, "
     'Then its verdict says, per shape, whether the test matches the cited section.'
     ),
    ('US4-AC3', 'implement', 'missing-citation-finding',
     'Given a test packet that asserts a cross-wave shape and cites no section for it, '
     'When the shape check reads it, Then the check carries a finding for the missing '
     'citation.'
     ),
    ('US5-AC2', 'implement', 'stale-names-by-search',
     "Given implement's check for stale `/speckit-` names, When it runs, Then it finds "
     "them without loading handoff.md or orchestration.md whole into the orchestrator's "
     'context.'
     ),
    ('US5-AC3', 'implement', 'reads-scope-rows-only',
     'Given a slice whose scope is waves 8–10 of 16, When the orchestrator prepares them, '
     "Then it has read orchestration.md's ground rules and the rows of waves 8–10, and the"
     " tasks of those waves, and no other waves' rows or tasks."
     ),
    ('US5-AC4', 'implement', 'no-rereads',
     'Given a wave in progress, When the orchestrator needs a rule, a row or a task it has'
     ' already read this session, Then it uses what it read rather than re-reading the '
     'file.'
     ),
    ('US5-AC5', 'implement', 'quoted-prefix-no-stop',
     'Given an orchestration.md that quotes the bare old command prefix (not followed by a'
     ' command name) and names no old command, When implement runs its stale-name check, '
     'Then it does not stop.'
     ),
    ('US8-AC3', 'implement', 'default-limits',
     'Given a run started without limits named, When it starts, Then it uses week 95% and '
     'five-hour 90%, and records them as Carried constraints.'
     ),
    ('EC-004', 'implement', 'no-usage-tool',
     'Given a `--nobrakes` run in a harness with no usage tool and no plan windows '
     '(Cursor, for one), When the run starts, Then it says once that the window limits do '
     'not apply, records that as a Carried constraint, and writes `n/a` for the windows in'
     ' each Boundary line.'
     ),
    ('US9-AC1', 'harden', 'consumer-later-wave',
     'Given two tasks where one uses a name the other creates, When harden builds the wave'
     " table, Then the consumer's packet is in a later wave than the producer's."
     ),
    ('US10-AC1', 'harden', 'superseded-shape-tests-owned',
     'Given a contract that changes a shape an existing test asserts, When harden '
     'finishes, Then that test file is owned by a test packet, with the task that updates '
     'it.'
     ),
    ('US13-AC1', 'implement', 'boundary-line',
     'Given a `--nobrakes` wave commit, When the boundary steps run, Then the wave report '
     'carries `Boundary: context <x>% · five-hour <y>% · week <z>% · BRAKES <none|found> ·'
     ' ledger +<n> lines`.'
     ),
    ('US13-AC2', 'verify', 'missing-boundary-gap',
     'Given a wave report with no boundary record, When verify-done checks the waves, Then'
     ' it lists a gap.'
     ),
    ('US11-AC1', 'implement', 'one-suite-after-fixes',
     'Given a wave whose review asks for fixes, When the wave completes, Then the full '
     'suite ran once, after the fixes.'
     ),
    ('US11-AC2', 'implement', 'gate-in-worktree',
     'Given a verify gate at a slice end, When the verifier runs, Then it runs in a '
     "scratch worktree at the gate's tag, and the next wave starts while it runs, its "
     "packets holding their test runs until the verifier's suite ends."
     ),
    ('US12-AC1', 'implement', 'sibling-edits-unreported',
     "Given a packet whose working tree shows a sibling's edits, When it reports, Then the"
     ' report does not list them.'
     ),
    ('US12-AC2', 'implement', 'foreign-red-rerun',
     'Given a packet that sees a red outside its own tests, When it reports, Then it reran'
     ' that test alone first and reports it only if still red.'
     ),
    ('US14-AC1', 'implement', 'proxy-brief-slots',
     'Given a verify gate, When the orchestrator fills the Proxy verifier brief, Then the '
     'brief names the expected-red rows and the accepted deviations for its waves.'
     ),
    ('EC-003', 'implement', 'escalation-raises-effort',
     'Given a packet escalated after failing its fence twice, When it is re-dispatched one'
     ' tier up, Then the agent it goes to runs at a higher effort than the first (cheap '
     'low → medium medium → strong high), with the failure reports attached.'
     ),
    ('EC-005', 'harden', 'no-old-names-written',
     'Given a feature whose spec or contracts quote old command names, When harden writes '
     'orchestration.md and handoff.md, Then neither names an old command when harden '
     'reports.'
     ),
)

# 003 (II-15): the 23 scenario IDs of II-15's case table, in that table's order, each with its
# area and slug (evals/<area>/003-<ID>-<slug>) and the scenario's text from 003's spec.md (bold
# markers dropped; compared after whitespace folding). Each case's directory and description
# carry the ID behind ``003-``.
SCENARIOS_003 = (
    ('US1-AC2', 'implement', 'hardens-appended-tasks',
     'Given a nobrakes run whose converge appends three tasks, When the converge round ends, '
     'Then the run hardens those tasks in append mode without asking, implements them, and '
     'converges again.'
     ),
    ('US1-AC3', 'implement', 'once-stops-at-ticked',
     'Given a run started with `--nobrakes once`, When every task is ticked, Then it stops '
     "with today's run summary and runs no converge."
     ),
    ('US1-AC4', 'implement', 'harden-stop-in-summary',
     'Given a converge round that appended a task citing a scenario without an ID, When the '
     'hardener hardens the appended tasks, Then the run stops, and the run summary carries '
     "harden's stop message."
     ),
    ('US1-AC5', 'implement', 'resume-at-harden',
     'Given a run that stopped at its harden step, When the user has fixed the cause and '
     'reruns `/s2tdd-implement --nobrakes`, Then the run resumes from the ledger at the harden '
     'step.'
     ),
    ('US1-AC6', 'implement', 'no-shrink-stop',
     'Given a converge round that appends as many tasks as the round before it or more, When '
     "the round ends, Then the run stops, naming both rounds' gap counts."
     ),
    ('US1-AC7', 'implement', 'gap-back-stop',
     "Given a converge round that reports a gap an earlier round's task closed, When the round "
     'ends, Then the run stops, naming the gap and the task that closed it before.'
     ),
    ('US1-AC8', 'implement', 'cites-nothing-stop',
     'Given a converge round that appends a task citing nothing in the spec, When the round '
     'ends, Then the run stops, naming the task.'
     ),
    ('US1-AC9', 'implement', 'handoff-names-phase',
     'Given a relay that reaches its hand-off threshold just after a converge round appended '
     'tasks, When it hands off, Then its handoff prompt names the next phase (harden of the '
     'appended tasks), and the next relay starts there.'
     ),
    ('US1-AC10', 'converge', 'docs-wave-set-aside',
     'Given a ledger recording the docs wave as built and uncommitted, When converge runs, in '
     "the loop or by hand, Then it does not refuse for the docs wave's unticked tasks and "
     'lists the docs wave as pending.'
     ),
    ('US1-AC11', 'close', 'close-needs-docs-commit',
     'Given a docs wave still uncommitted, When the user runs `/s2tdd-close`, Then close stops '
     'and asks for the docs wave to be reviewed and committed first.'
     ),
    ('US2-AC1', 'implement', 'per-wave-command',
     "Given a project that declares a per-wave test command, When a wave's packets have "
     'reported and its reviews are done, Then the orchestrator runs the per-wave command, not '
     'the full suite, before the wave commit.'
     ),
    ('US2-AC2', 'implement', 'no-per-wave-full-suite',
     'Given a project that declares no per-wave test command, When a wave ends, Then the '
     'orchestrator runs the full suite, as today.'
     ),
    ('US2-AC4', 'implement', 'outside-sees-full-suite',
     'Given a project whose `Per-wave sees:` line is `*.py` and a wave that changes a prompt '
     'file, When the wave ends, Then it runs the full suite, not the per-wave command.'
     ),
    ('US2-AC5', 'verify', 'first-red-wave',
     'Given a slice-end full run that shows a red no per-wave run in the slice showed, When '
     'the gate reports it, Then the verdict is Not done, naming the red test and the first '
     'wave commit of the slice where that test alone goes red, and that wave\'s tasks lead the '
     'next wave with the failure attached.'
     ),
    ('US2-AC6', 'implement', 'test-run-line',
     'Given any wave, When its report is written, Then it names which run it was (per-wave or '
     'full), the command, the counts and the wall time.'
     ),
    ('US2-AC7', 'implement', 'attended-names-verify',
     'Given an attended implement session in a project that declares a per-wave command, When '
     "its last wave commits, Then its final report says that the slice's full run is the "
     "user's `/s2tdd-verify-done`."
     ),
    ('US3-AC1', 'converge', 'converge-reuses-green-run',
     'Given a green full run recorded at commit X and a clean tree at X, When converge runs, '
     'Then it starts no suite and records that it reused the run at X.'
     ),
    ('US3-AC2', 'close', 'close-reuses-green-run',
     'Given a green full run recorded at commit X and a clean tree at X, When close reaches '
     'its suite gate, Then it starts no suite and records that it reused the run at X.'
     ),
    ('US3-AC3', 'converge', 'no-reuse-past-the-run',
     'Given a green full run recorded at commit X, When HEAD is past X or the tree is dirty, '
     'Then converge and close run the suite as today.'
     ),
    ('EC-001', 'implement', 'per-wave-off',
     'Given a per-wave command that fails to run (a collection error, a missing plugin) rather '
     'than reporting red tests, When a wave ends, Then that wave and every later wave of the '
     'run run the full suite, and the ledger records '
     '`Per-wave runs off from wave <n>: <first error line>` as a Carried constraint.'
     ),
    ('EC-002', 'implement', 'blocked-stops-before-converge',
     "Given a nobrakes run that ends its waves with a blocked packet that is neither the MVP "
     "nor a guard test's, When no wave is left, Then the run stops before converge, and the "
     'run summary names the blocked packets and their skipped dependents.'
     ),
    ('EC-003', 'implement', 'week-limit-in-loop',
     "Given a converge round in the loop, When weekly usage reaches the run's week limit, Then "
     'the run stops with its summary, as at a wave boundary.'
     ),
    ('EC-004', 'implement', 'zero-selected-green',
     'Given a wave whose per-wave run selects no tests and prints a summary saying so, When '
     'the wave ends, Then the run counts it green, the wave report says `0 selected`, and '
     'later waves keep using the per-wave command.'
     ),
)

AREAS = ("resolution", "next", "refusals", "harden", "cloud", "setup", "specify", "plan",
         "implement", "constitution", "upkeep", "verify", "converge", "close")

FIXTURES_DIR = "evals/fixtures"
HELPERS = ("make-project.sh", "make-specs.sh", "make-feature.sh", "make-copy.sh")
FEATURE_STATES = ("specified", "planned", "hardened", "hardened-old-names", "closed",
                  "merged-branch", "over-budget", "worktree",
                  "hardened-shapes", "wave-reports", "ledger-notes",
                  "looping", "per-wave", "green-run", "docs-wave")

# II-16: the three states 002's cases add, and what each leaves in the feature. Every one is
# hardened-shapes plus its own files; the project stays on the feature's branch.
FEATURE_STATES_002 = ("hardened-shapes", "wave-reports", "ledger-notes")
FEATURE_BRANCH = "004-csv-export"
# Harden's C3: every heading of run-ledger.md.
LEDGER_HEADINGS = (
    "## Lease", "## Runs", "## Usage", "## Carried constraints", "## Amendments",
    "## Test-owner fixes", "## Ownership exceptions", "## Expected red", "## Blocked and skipped",
    "## Open review notes", "## Pending checkpoints", "## Tags and pushes",
    "## Processes killed", "## Handoff",
)
# Harden's 0.3.0 prompt text the hardened-shapes handoff.md transcribes (II-2 1 and 8, II-5).
HANDOFF_PHRASES = (
    "SHAPE CHECK (both modes; every wave that holds a test packet)",
    "MUST BREACH. A review or shape-check finding that cites a spec MUST (MUST <FR-nnn | "
    "US<n>-AC<m> | EC-nnn>) is a blocker.",
    "Review: <packet>: <verdict>; …; shape check: <verdict> (<k> citations, <m> differ) | none",
    "Boundary: context <x>% · five-hour <y>% · week <z>% · BRAKES <none|found> · ledger +<n> "
    "lines",
    "NOBRAKES",
)
HANDOFF_HEADINGS = ("## Standard briefs", "### Shape check")
CONTRACT_SECTIONS = ("II-1", "II-2")  # the sections the wave's two test packets assert
CARRY_TO_CONVERGE = "carry to converge"

# II-15: the four states 003's cases add, each built on hardened-shapes, on the feature's
# branch. Harden's 0.4.0 prompt text their handoff.md transcribes: TR1 (II-3), CL1 (II-7 N3),
# and the two briefs' headings (II-7 N8). A phrase that starts with ``#`` is a whole line.
FEATURE_STATES_003 = ("looping", "per-wave", "green-run", "docs-wave")
HANDOFF_PHRASES_003 = (
    "TEST RUN (both modes; once per wave)",
    "CONVERGE LOOP (MODE: nobrakes only).",
    "### Converger",
    "### Hardener",
    # 003 FR-006: II-7 H3's amended Expect phrase (II-15, amended 2026-10-04).
    "every committed wave before <m> (every committed wave, at a converge, harden or docs-wave "
    "phase) has a verify-done line in validation.md; the docs wave, never committed by the run, "
    "needs none",
    # 003 FR-011b: II-3 TR9 in TEST RUN (II-15, amended 2026-10-04, T048).
    "Per-wave sees: none means the line was not declared: no change is outside it, and the "
    "per-wave command runs for every change.",
    # 003 FR-002, US1-AC3: II-7 S2 as amended (II-15, amended 2026-10-04, T059, round 3).
    "Rounds: <r> · <k1>, <k2>, … tasks appended · converged | stopped: <rule> | none (a once run)",
    # 003 FR-002: II-7 N1d (II-15, amended 2026-10-04, T059, round 3).
    "MODE: nobrakes once counts as nobrakes for this section.",
    # 003 FR-006, EC-003: II-7 BD2 (II-15, amended 2026-10-04, T059, round 3).
    "At a phase change, which has no wave report, write the Boundary line under the ledger's "
    "Usage section instead.",
)
# 003 FR-011b: II-3 TR9 sits in TEST RUN after TR4 and before TR5 (II-3 TR9; II-15, amended
# 2026-10-04): the flattened order TR1 < TR4 < TR9 < TR5.
TEST_RUN_ORDER_003 = (
    "TEST RUN (both modes; once per wave)",
    "It is the full suite instead when no per-wave command is declared, when the wave changed a "
    "file outside Per-wave sees, or when per-wave runs are off.",
    "Per-wave sees: none means the line was not declared: no change is outside it, and the "
    "per-wave command runs for every change.",
    "The wave's changed files are git diff --name-only HEAD and git ls-files --others "
    "--exclude-standard, in the app repository only; each Per-wave sees glob matches "
    "repository-relative paths, with * crossing /.",
)
# 003 FR-006: II-7 N4 H3's gone phrase (the W2 text), absent from the 003 states' handoff.md
# (II-15, amended 2026-10-04).
HANDOFF_GONE_003 = (
    "every wave before <m> (every wave, at a converge, harden or docs-wave phase) has a "
    "verify-done line in validation.md"
)
LEDGER_ROUNDS = "## Rounds"  # the heading the 003 state tests add to LEDGER_HEADINGS (LG1)
LEASE_RELEASED_DONE = "released by relay 1: done"  # looping's newest Lease line
PER_WAVE_SEES = "Per-wave sees: *.py"

# Neutral vocabulary (P7): every directory, branch and owner name a scaffold creates is made of
# these words and numbers (names are split at every non-alphanumeric character). A private
# name cannot slip in: it is not a word here, and this test names none.
NEUTRAL_WORDS = frozenset({
    "acme", "notes", "csv", "export", "tags", "globex",            # project, feature, owner
    "main", "claude", "fix", "flake", "x",                         # branch names (spec.md's)
    "origin", "upstream", "head", "remote", "remotes", "bare",     # remote plumbing
    "specs", "spec", "contracts", "checklists", "checks", "docs",  # the specs repository
    "git", "github", "com", "sdd", "run", "s2tdd",                 # fixed product names
    "worktree", "worktrees", "wt", "work", "project", "foreign", "other", "someone", "else",
    "stranger", "example", "demo", "local", "clone", "copy", "feature", "owner", "user",
    "reports", "shapes",                                           # 002's states (II-16)
})
# Git internals and copied product skills are not fixture names.
PRUNED_DIRS = frozenset({".git", "skills"})
# US3's Givens need a project that still has the old packaging: spec-kit's own directory names
# (``.specify/``, ``skills/``, ``.claude/skills/speckit-<command>/``), not project names. Exact
# directory names only; anything else must still be made of NEUTRAL_WORDS.
OLD_PACKAGING_DIRECTORIES = frozenset({".specify", "skills"})
SPECKIT_COMMAND_WORDS = frozenset({
    "specify", "clarify", "plan", "tasks", "harden", "implement", "analyze", "checklist",
    "constitution", "converge", "verify", "done", "save", "next", "close", "taskstoissues",
})

# Scenarios whose Given leaves out a part of T080's generic scaffold shape.
NO_SPECS_DIRECTORY = {"US1-AC2"}  # "a repository ... with no `specs/` directory"
NO_SPECS_REMOTE = {"EC-003"}      # "a specs repository with no remote"

# The keys the real loader accepts in a case's prompt.md frontmatter (II-14, amended
# 2026-10-02: Claude Code 2.1.286 rejects any other key as "unknown frontmatter key").
LOADER_KEYS = frozenset({
    "schema_version", "name", "description", "tags", "plugins", "runs", "expected_outcome",
    "model", "max_turns", "timeout_seconds", "allowed_tools", "artifact_publish",
    "growthbook_overrides", "append_system_prompt", "env",
})

FALLBACK = 'CLAUDE_CODE_REMOTE=true claude -p "/s2tdd-pr-review 1"'


def _param_id(scenario_id: str) -> str:
    return scenario_id.replace("-", "_")


CASES = [pytest.param(sid, area, slug, text, id=_param_id(sid))
         for sid, area, slug, text in SCENARIOS]

PREFIX_002 = "002-"
CASES_002 = [pytest.param(PREFIX_002 + sid, area, slug, text, id=_param_id(PREFIX_002 + sid))
             for sid, area, slug, text in SCENARIOS_002]
PREFIX_003 = "003-"
CASES_003 = [pytest.param(PREFIX_003 + sid, area, slug, text, id=_param_id(PREFIX_003 + sid))
             for sid, area, slug, text in SCENARIOS_003]
ALL_CASES = CASES + CASES_002 + CASES_003


# ---------------------------------------------------------------------- helpers and fixtures


def _fold(text: object) -> str:
    return re.sub(r"\s+", " ", str(text).replace("**", "")).strip()


def _case_dir(repo_root: Path, area: str, sid: str, slug: str) -> Path:
    assert (repo_root / "evals").is_dir(), f"evals/ not found (under {repo_root})"
    case = repo_root / "evals" / area / f"{sid}-{slug}"
    assert case.is_dir(), f"evals/ not found: no case directory evals/{area}/{sid}-{slug}"
    return case


def _fixtures_dir(repo_root: Path) -> Path:
    path = repo_root / FIXTURES_DIR
    assert path.is_dir(), f"evals/fixtures/ not found (under {repo_root})"
    return path


@pytest.fixture(scope="session")
def bash_exe() -> str:
    found = shutil.which("bash")
    if found and "system32" not in found.lower():  # not the WSL launcher
        return found
    for candidate in (r"C:\Program Files\Git\bin\bash.exe",
                      r"C:\Program Files\Git\usr\bin\bash.exe"):
        if Path(candidate).is_file():
            return candidate
    if found:
        return found
    pytest.fail("bash not found on PATH")


@pytest.fixture(scope="session")
def git_env(tmp_path_factory: pytest.TempPathFactory) -> dict[str, str]:
    """An environment with no inherited git identity or configuration and no signed-in gh: a
    helper must set what it needs itself (CI has none)."""
    home = tmp_path_factory.mktemp("home")
    (home / "gitconfig").write_text("", encoding="utf-8")
    gh_config = tmp_path_factory.mktemp("gh-config")
    env = {k: v for k, v in os.environ.items()
           if not k.startswith("GIT_") and k not in ("GH_TOKEN", "GITHUB_TOKEN",
                                                       "GH_ENTERPRISE_TOKEN",
                                                       "GITHUB_ENTERPRISE_TOKEN")}
    env.update(HOME=str(home), USERPROFILE=str(home), GIT_CONFIG_GLOBAL=str(home / "gitconfig"),
               GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0", GH_CONFIG_DIR=str(gh_config))
    return env


@pytest.fixture
def sh(bash_exe, git_env):
    """sh(script, *args, cwd=...) runs a bash script and returns the CompletedProcess."""

    def run(script: Path, *args: object, cwd: Path) -> subprocess.CompletedProcess[str]:
        cwd.mkdir(parents=True, exist_ok=True)
        argv = [Path(a).as_posix() if isinstance(a, Path) else str(a) for a in args]
        return subprocess.run([bash_exe, Path(script).as_posix(), *argv], cwd=cwd, env=git_env,
                              capture_output=True, text=True, encoding="utf-8", timeout=300)

    return run


@pytest.fixture
def git(git_env):
    def run(repo: Path, *args: str) -> str:
        proc = subprocess.run(["git", "-C", str(repo), *args], env=git_env,
                              capture_output=True, text=True, encoding="utf-8", timeout=120)
        assert proc.returncode == 0, f"git {' '.join(args)} in {repo}: {proc.stderr.strip()}"
        return proc.stdout.strip()

    return run


def _local_path(url: str, repo: Path) -> Path | None:
    """The directory a remote URL names, or None when it is not a local one."""
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*://", url):
        parsed = urlparse(url)
        if parsed.scheme != "file":
            return None
        raw = unquote(parsed.path)
        if re.match(r"^/[A-Za-z]:", raw):
            raw = raw[1:]
    elif re.match(r"^[^/\\]+@[^/\\]+:", url):  # scp-like: a remote host
        return None
    else:
        raw = url
    msys = re.match(r"^/([A-Za-z])/(.*)$", raw)  # /c/Users/... as Git Bash prints it
    if os.name == "nt" and msys:
        raw = f"{msys.group(1)}:/{msys.group(2)}"
    path = Path(raw)
    return path if path.is_absolute() else repo / path


def _assert_bare_remote(git, repo: Path, what: str) -> None:
    remotes = git(repo, "remote").split()
    assert remotes, f"{what} ({repo}) has no remote"
    for name in remotes:
        url = git(repo, "remote", "get-url", name)
        target = _local_path(url, repo)
        assert target is not None, f"{what}: remote {name} is {url}, not a local bare repository"
        assert target.is_dir(), f"{what}: remote {name} names {target}, which does not exist"
        assert git(target, "rev-parse", "--is-bare-repository") == "true", \
            f"{what}: remote {name} ({target}) is not a bare repository"


def _assert_own_repository(git, parent: Path, name: str) -> Path:
    inner = parent / name
    assert (inner / ".git").exists(), f"{inner} is not its own git repository (no .git)"
    top = Path(git(inner, "rev-parse", "--show-toplevel")).resolve()
    assert top == inner.resolve(), f"{inner} belongs to the repository at {top}"
    return inner


def _find_project(work: Path) -> Path:
    """The project a scaffold built: the working directory itself, or its one child that is a
    git repository (a directory .git; a worktree's .git is a file)."""
    if (work / ".git").is_dir():
        return work
    children = sorted(p for p in work.iterdir() if (p / ".git").is_dir())
    assert len(children) == 1, \
        f"expected the scaffold to leave one git repository in {work}, found {children}"
    return children[0]


def _is_bare(path: Path) -> bool:
    return ((path / "HEAD").is_file() and (path / "objects").is_dir()
            and (path / "refs").is_dir())


def _owner_part(url: str, base: Path) -> str:
    """The part of a remote URL that names owners and repositories: no scheme, no drive,
    nothing above ``base``."""
    local = _local_path(url, base)
    if local is not None:
        try:
            return local.resolve().relative_to(base.resolve()).as_posix()
        except ValueError:
            return "/".join(local.parts[-2:])
    if "://" in url:
        parsed = urlparse(url)
        return parsed.netloc + parsed.path
    return url


def _names_in(base: Path, git) -> list[tuple[str, str]]:
    """Every (kind, name) the tree under ``base`` creates: directories, branches, owners."""
    names: list[tuple[str, str]] = []
    repositories: list[Path] = []
    for root, dirs, _files in os.walk(base):
        here = Path(root)
        if (here / ".git").exists() or _is_bare(here):
            repositories.append(here)
        kept = []
        for d in dirs:
            names.append(("directory", d))
            if d not in PRUNED_DIRS and not _is_bare(here / d):
                kept.append(d)
            elif _is_bare(here / d):
                repositories.append(here / d)
        dirs[:] = kept
    for repo in repositories:
        for ref in git(repo, "for-each-ref", "--format=%(refname)").split():
            names.append(("branch", re.sub(r"^refs/(heads|remotes|tags)/", "", ref)))
        if (repo / ".git").exists() and git(repo, "remote"):
            listed = git(repo, "config", "--local", "--get-regexp", r"^remote\..*\.url$")
            for line in listed.splitlines():
                key, _, url = line.partition(" ")
                names.append(("remote", key.split(".")[1]))
                names.append(("owner", _owner_part(url, base)))
    return names


def _old_packaging_name(kind: str, name: str) -> bool:
    """spec-kit's own directory names: ``.specify``, ``skills`` and ``speckit-<command>``."""
    if kind != "directory":
        return False
    if name in OLD_PACKAGING_DIRECTORIES:
        return True
    if name.startswith("speckit-"):
        tokens = [t for t in re.split(r"[^A-Za-z0-9]+", name[len("speckit-"):].lower()) if t]
        return bool(tokens) and all(t in SPECKIT_COMMAND_WORDS for t in tokens)
    return False


def _not_neutral(names: list[tuple[str, str]]) -> list[tuple[str, str]]:
    bad = []
    for kind, name in names:
        if _old_packaging_name(kind, name):
            continue
        for token in filter(None, re.split(r"[^A-Za-z0-9]+", name.lower())):
            if not token.isdigit() and token not in NEUTRAL_WORDS:
                bad.append((kind, name))
                break
    return bad


def _assert_neutral(base: Path, git) -> None:
    names = _names_in(base, git)
    assert any(kind == "branch" for kind, _ in names), f"no git repository found under {base}"
    bad = _not_neutral(names)
    assert not bad, f"names outside the neutral allowlist: {sorted(set(bad))}"


def _scaffold_script_name(case: Path, sid: str) -> str:
    """The scaffold script a case names: case.yaml's ``context.scaffold_script`` (II-14,
    amended 2026-10-02), never prompt.md's frontmatter."""
    case_yaml = case / "case.yaml"
    assert case_yaml.is_file(), f"{sid}: no case.yaml (a scaffolding case holds one, II-14)"
    loaded = yaml.safe_load(case_yaml.read_text(encoding="utf-8")) or {}
    context = loaded.get("context") if isinstance(loaded, dict) else None
    value = context.get("scaffold_script") if isinstance(context, dict) else None
    assert value, f"{sid}: case.yaml has no context.scaffold_script"
    return str(value)


@dataclass
class Scaffolded:
    base: Path
    work: Path
    proc: subprocess.CompletedProcess[str]


@pytest.fixture(scope="session")
def scaffold(repo_root, bash_exe, git_env, tmp_path_factory):
    """scaffold(sid, area, slug): run the case's scaffold script once under bash in a fresh
    temporary directory (the cwd) and keep the result for every test of that case."""
    cache: dict[str, Scaffolded] = {}

    def run(sid: str, area: str, slug: str) -> Scaffolded:
        if sid in cache:
            return cache[sid]
        case = _case_dir(repo_root, area, sid, slug)
        value = _scaffold_script_name(case, sid)
        script = (case / str(value)).resolve()
        assert not Path(str(value)).is_absolute() and case.resolve() in script.parents, \
            f"{sid}: context.scaffold_script {value} must name a file inside the case directory"
        assert script.is_file(), f"{sid}: context.scaffold_script {value} does not exist"
        base = tmp_path_factory.mktemp(_param_id(sid))
        work = base / "work"
        work.mkdir()
        proc = subprocess.run([bash_exe, script.as_posix()], cwd=work, env=git_env,
                              capture_output=True, text=True, encoding="utf-8", timeout=300)
        cache[sid] = Scaffolded(base, work, proc)
        return cache[sid]

    return run


# ------------------------------------------------------------------------------- Coverage


@pytest.mark.parametrize("sid, area, slug, text", ALL_CASES)
def test_coverage_one_case_directory_per_scenario(repo_root, sid, area, slug, text):
    assert (repo_root / "evals").is_dir(), f"evals/ not found (under {repo_root})"
    found = sorted(p.relative_to(repo_root).as_posix()
                   for p in (repo_root / "evals").glob(f"*/{sid}-*") if p.is_dir())
    assert found == [f"evals/{area}/{sid}-{slug}"], \
        f"{sid}: expected exactly evals/{area}/{sid}-{slug}/, found {found}"


@pytest.mark.parametrize("area", AREAS)
def test_coverage_area_holds_exactly_its_cases(repo_root, area):
    assert (repo_root / "evals").is_dir(), f"evals/ not found (under {repo_root})"
    folder = repo_root / "evals" / area
    assert folder.is_dir(), f"evals/ not found: no area directory evals/{area}"
    expected = sorted([f"{sid}-{slug}" for sid, a, slug, _text in SCENARIOS if a == area]
                      + [f"{PREFIX_002}{sid}-{slug}" for sid, a, slug, _text in SCENARIOS_002
                         if a == area]
                      + [f"{PREFIX_003}{sid}-{slug}" for sid, a, slug, _text in SCENARIOS_003
                         if a == area])
    found = sorted(p.name for p in folder.iterdir() if p.is_dir())
    assert found == expected, (
        f"evals/{area}: not found {sorted(set(expected) - set(found))}; "
        f"not a case {sorted(set(found) - set(expected))}")


# ---------------------------------------------------------------------------------- Shape


@pytest.mark.parametrize("sid, area, slug, text", ALL_CASES)
def test_shape_prompt_has_parsed_frontmatter(repo_root, doc, sid, area, slug, text):
    case = _case_dir(repo_root, area, sid, slug)
    assert (case / "prompt.md").is_file(), f"{sid}: no prompt.md"
    frontmatter = doc(f"evals/{area}/{sid}-{slug}/prompt.md").frontmatter
    assert frontmatter, f"{sid}: prompt.md has no frontmatter that parses"
    assert isinstance(frontmatter.get("max_turns"), int), f"{sid}: no max_turns"
    assert isinstance(frontmatter.get("allowed_tools"), list), f"{sid}: no allowed_tools"
    assert "env" not in frontmatter, f"{sid}: a case sets no env (J-17: EVAL_* keys only)"
    assert "CLAUDE_CODE_REMOTE" not in str(frontmatter), f"{sid}: a case cannot set it (J-17)"
    case_yaml = case / "case.yaml"
    if case_yaml.is_file():
        loaded = yaml.safe_load(case_yaml.read_text(encoding="utf-8")) or {}
        assert "env" not in loaded, f"{sid}: case.yaml sets env (J-17)"


@pytest.mark.parametrize("sid, area, slug, text", ALL_CASES)
def test_shape_prompt_frontmatter_has_no_scaffold_script(repo_root, doc, sid, area, slug, text):
    _case_dir(repo_root, area, sid, slug)
    frontmatter = doc(f"evals/{area}/{sid}-{slug}/prompt.md").frontmatter
    assert "scaffold_script" not in frontmatter, (
        f"{sid}: prompt.md names scaffold_script; the loader rejects it (II-14): use case.yaml")


@pytest.mark.parametrize("sid, area, slug, text", ALL_CASES)
def test_shape_prompt_frontmatter_keys_are_the_loaders(repo_root, doc, sid, area, slug, text):
    _case_dir(repo_root, area, sid, slug)
    frontmatter = doc(f"evals/{area}/{sid}-{slug}/prompt.md").frontmatter
    unknown = sorted(set(frontmatter) - LOADER_KEYS)
    assert not unknown, f"{sid}: prompt.md frontmatter keys outside II-14's loader list: {unknown}"


@pytest.mark.parametrize("sid, area, slug, text", ALL_CASES)
def test_shape_has_graders_with_type_and_weight(repo_root, doc, sid, area, slug, text):
    case = _case_dir(repo_root, area, sid, slug)
    graders = sorted((case / "graders").glob("*.md"))
    assert graders, f"{sid}: no graders/*.md"
    for grader in graders:
        frontmatter = doc(f"evals/{area}/{sid}-{slug}/graders/{grader.name}").frontmatter
        assert "type" in frontmatter and "weight" in frontmatter, \
            f"{sid}: graders/{grader.name} frontmatter lacks type or weight: {frontmatter}"


@pytest.mark.parametrize("sid, area, slug, text", ALL_CASES)
def test_shape_description_carries_scenario_id_and_text(repo_root, doc, sid, area, slug, text):
    _case_dir(repo_root, area, sid, slug)
    frontmatter = doc(f"evals/{area}/{sid}-{slug}/prompt.md").frontmatter
    assert "description" in frontmatter, f"{sid}: prompt.md has no description key (J-9)"
    assert _fold(frontmatter["description"]) == _fold(f"{sid}: {text}"), \
        f"{sid}: description is not '<ID>: <scenario text verbatim>'"


@pytest.mark.parametrize("sid, area, slug", [pytest.param(
    "US6-AC6", "cloud", "refuse-in-cloud", id="US6_AC6")])
def test_shape_cloud_case_documents_claude_p_fallback(repo_root, sid, area, slug):
    case = _case_dir(repo_root, area, sid, slug)
    written = "\n".join(p.read_text(encoding="utf-8", errors="replace")
                        for p in sorted(case.rglob("*")) if p.is_file())
    assert FALLBACK in written, \
        f"{sid}: the case does not document the fallback (J-17): {FALLBACK}"


# ------------------------------------------------------------------------------ Fixtures


@pytest.mark.parametrize("helper", HELPERS, ids=lambda h: h[:-3].replace("-", "_"))
def test_fixtures_helper_is_lf_strict_bash(repo_root, bash_exe, git_env, helper):
    script = _fixtures_dir(repo_root) / helper
    assert script.is_file(), f"evals/fixtures/{helper} not found"
    data = script.read_bytes()
    assert b"\r" not in data, f"{helper} has CRLF line endings"
    assert b"set -euo pipefail" in data, f"{helper} lacks 'set -euo pipefail'"
    syntax = subprocess.run([bash_exe, "-n", script.as_posix()], env=git_env,
                            capture_output=True, text=True, encoding="utf-8")
    assert syntax.returncode == 0, syntax.stderr


@pytest.mark.parametrize("owner", ["acme", "globex"])
def test_fixtures_make_project_leaves_repository_with_bare_remote(
        repo_root, sh, git, tmp_path, owner):
    project = tmp_path / "acme-notes"
    project.mkdir()
    proc = sh(_fixtures_dir(repo_root) / "make-project.sh", project, owner, cwd=tmp_path)
    assert proc.returncode == 0, proc.stderr
    assert (project / ".git").is_dir(), f"{project} is not a git repository"
    _assert_bare_remote(git, project, "make-project.sh's project")
    assert owner in git(project, "config", "--local", "--list"), \
        f"the owner {owner} is not recorded in the project's configuration"
    _assert_neutral(tmp_path, git)


@pytest.mark.parametrize("flag", [None, "--no-remote"], ids=["with_remote", "no_remote"])
def test_fixtures_make_specs_makes_its_own_repository(repo_root, sh, git, tmp_path, flag):
    fixtures = _fixtures_dir(repo_root)
    project = tmp_path / "acme-notes"
    project.mkdir()
    assert sh(fixtures / "make-project.sh", project, "acme", cwd=tmp_path).returncode == 0
    args = [project] + ([flag] if flag else [])
    proc = sh(fixtures / "make-specs.sh", *args, cwd=tmp_path)
    assert proc.returncode == 0, proc.stderr
    specs = _assert_own_repository(git, project, "specs")
    if flag:
        assert git(specs, "remote") == "", "specs/ has a remote despite --no-remote"
    else:
        _assert_bare_remote(git, specs, "specs/")
    _assert_neutral(tmp_path, git)


@pytest.mark.parametrize("state", FEATURE_STATES, ids=lambda s: s.replace("-", "_"))
def test_fixtures_make_feature_succeeds_for_every_state(repo_root, sh, git, tmp_path, state):
    fixtures = _fixtures_dir(repo_root)
    project = tmp_path / "acme-notes"
    project.mkdir()
    assert sh(fixtures / "make-project.sh", project, "acme", cwd=tmp_path).returncode == 0
    assert sh(fixtures / "make-specs.sh", project, cwd=tmp_path).returncode == 0
    proc = sh(fixtures / "make-feature.sh", project, state, cwd=tmp_path)
    assert proc.returncode == 0, proc.stderr
    handoffs = sorted((project / "specs").glob("*/handoff.md"))
    orchestrations = sorted((project / "specs").glob("*/orchestration.md"))
    if state == "hardened-old-names":
        for found in (handoffs, orchestrations):
            assert found, f"{state}: the feature lacks handoff.md or orchestration.md"
            assert all("/speckit-" in f.read_text(encoding="utf-8") for f in found), \
                f"{state}: {found} name no /speckit- command"
    elif state == "hardened":
        assert handoffs and orchestrations, "hardened: handoff.md or orchestration.md missing"
        assert not any("/speckit-" in f.read_text(encoding="utf-8")
                       for f in handoffs + orchestrations), "hardened: names /speckit- commands"
    _assert_neutral(tmp_path, git)


def _flatten(s: str) -> str:
    return " ".join(s.lower().replace("`", "").replace("*", "").split())


def _feature_file(project: Path, state: str, name: str) -> Path:
    path = project / "specs" / FEATURE_BRANCH / name
    assert path.is_file(), f"{state}: specs/{FEATURE_BRANCH}/{name} not found"
    return path


def _ledger_section(text: str, heading: str) -> list[str]:
    """The non-blank lines under a run-ledger heading, up to the next ``## `` heading."""
    lines = [line.rstrip() for line in text.split("\n")]
    assert heading in lines, f"run-ledger.md lacks `{heading}`"
    section = []
    for line in lines[lines.index(heading) + 1:]:
        if line.startswith("## "):
            break
        if line.strip():
            section.append(line)
    return section


@pytest.mark.parametrize("state", FEATURE_STATES_002, ids=lambda s: s.replace("-", "_"))
def test_fixtures_make_feature_002_states_leave_their_files(repo_root, sh, git, tmp_path, state):
    fixtures = _fixtures_dir(repo_root)
    project = tmp_path / "acme-notes"
    project.mkdir()
    assert sh(fixtures / "make-project.sh", project, "acme", cwd=tmp_path).returncode == 0
    assert sh(fixtures / "make-specs.sh", project, cwd=tmp_path).returncode == 0
    proc = sh(fixtures / "make-feature.sh", project, state, cwd=tmp_path)
    assert proc.returncode == 0, \
        f"make-feature.sh {state} exited {proc.returncode}: {proc.stderr.strip()}"
    assert git(project, "rev-parse", "--abbrev-ref", "HEAD") == FEATURE_BRANCH, \
        f"{state}: the project is not on branch {FEATURE_BRANCH}"

    # hardened-shapes, which the other two build on.
    for name in ("tasks.md", "validation.md"):
        _feature_file(project, state, name)
    handoff = _feature_file(project, state, "handoff.md").read_text(encoding="utf-8")
    orchestration = _feature_file(project, state, "orchestration.md").read_text(encoding="utf-8")
    assert "/speckit-" not in handoff + orchestration, f"{state}: names /speckit- commands"
    contracts = _feature_file(project, state, "contracts/internal-interfaces.md")
    contract_text = contracts.read_text(encoding="utf-8")
    for section in CONTRACT_SECTIONS:
        assert re.search(rf"^## {re.escape(section)}\b", contract_text, re.M), \
            f"{state}: contracts/internal-interfaces.md has no `## {section}` section"
    rows = [line for line in orchestration.split("\n") if re.match(r"^\| W\d+ ", line)]
    assert rows, f"{state}: orchestration.md has no wave row read by grep '^| W<n> '"
    assert any(re.search(r"\|\s*strong\s*\|", row) for row in rows), \
        f"{state}: orchestration.md's wave table has no strong packet"
    flat = _flatten(handoff)
    missing = [p for p in HANDOFF_PHRASES if _flatten(p) not in flat]
    assert not missing, f"{state}: handoff.md lacks harden's 0.3.0 text: {missing}"
    handoff_lines = [line.rstrip() for line in handoff.split("\n")]
    missing = [h for h in HANDOFF_HEADINGS if h not in handoff_lines]
    assert not missing, f"{state}: handoff.md lacks the headings {missing}"
    ledger = _feature_file(project, state, "run-ledger.md").read_text(encoding="utf-8")
    ledger_lines = [line.rstrip() for line in ledger.split("\n")]
    missing = [h for h in LEDGER_HEADINGS if h not in ledger_lines]
    assert not missing, f"{state}: run-ledger.md lacks harden's C3 headings {missing}"

    if state == "wave-reports":
        _feature_file(project, state, "s1-wave-reports.md")
    elif state == "ledger-notes":
        notes = _ledger_section(ledger, "## Open review notes")
        assert len(notes) >= 2, f"{state}: run-ledger.md holds {len(notes)} Open review notes"
        carried = _ledger_section(ledger, "## Carried constraints")
        assert any(CARRY_TO_CONVERGE in line for line in carried), \
            f"{state}: no Carried constraint is marked `{CARRY_TO_CONVERGE}`"
    _assert_neutral(tmp_path, git)


# II-15's four states. Each test builds its state and checks what II-15's table says it leaves.

def _make_state(repo_root: Path, sh, git, tmp_path: Path, state: str) -> Path:
    fixtures = _fixtures_dir(repo_root)
    project = tmp_path / "acme-notes"
    project.mkdir()
    assert sh(fixtures / "make-project.sh", project, "acme", cwd=tmp_path).returncode == 0
    assert sh(fixtures / "make-specs.sh", project, cwd=tmp_path).returncode == 0
    proc = sh(fixtures / "make-feature.sh", project, state, cwd=tmp_path)
    assert proc.returncode == 0, \
        f"make-feature.sh {state} exited {proc.returncode}: {proc.stderr.strip()}"
    assert git(project, "rev-parse", "--abbrev-ref", "HEAD") == FEATURE_BRANCH, \
        f"{state}: the project is not on branch {FEATURE_BRANCH}"
    return project


def _assert_handoff_040(project: Path, state: str) -> str:
    """handoff.md written from harden's 0.4.0 prompt text (HANDOFF_PHRASES_003)."""
    handoff = _feature_file(project, state, "handoff.md").read_text(encoding="utf-8")
    flat = _flatten(handoff)
    lines = [line.rstrip() for line in handoff.split("\n")]
    missing = [p for p in HANDOFF_PHRASES_003
               if (p not in lines if p.startswith("#") else _flatten(p) not in flat)]
    assert not missing, f"{state}: handoff.md lacks harden's 0.4.0 text: {missing}"
    positions = [flat.find(_flatten(p)) for p in TEST_RUN_ORDER_003]
    assert -1 not in positions and positions == sorted(positions), (
        f"{state}: handoff.md's TEST RUN is not in II-3's order TR1, TR4, TR9, TR5: {positions}"
    )
    assert _flatten(HANDOFF_GONE_003) not in flat, (
        f"{state}: handoff.md still holds II-7 H3's gone phrase: {HANDOFF_GONE_003!r}"
    )
    return handoff


def _assert_ledger_with_rounds(project: Path, state: str) -> str:
    ledger = _feature_file(project, state, "run-ledger.md").read_text(encoding="utf-8")
    ledger_lines = [line.rstrip() for line in ledger.split("\n")]
    missing = [h for h in LEDGER_HEADINGS + (LEDGER_ROUNDS,) if h not in ledger_lines]
    assert not missing, f"{state}: run-ledger.md lacks the headings {missing}"
    return ledger


def _tasks(project: Path, state: str) -> dict[str, bool]:
    """tasks.md's tasks: ID → ticked."""
    text = _feature_file(project, state, "tasks.md").read_text(encoding="utf-8")
    found = {m.group(2): m.group(1).lower() == "x"
             for m in re.finditer(r"^- \[([ xX])\] (T\d+)\b", text, re.M)}
    assert found, f"{state}: tasks.md holds no task line"
    return found


def _wave_tasks(project: Path, state: str) -> dict[int, set[str]]:
    """orchestration.md's wave table (rows read by grep '^| W<n> '): wave → its tasks."""
    text = _feature_file(project, state, "orchestration.md").read_text(encoding="utf-8")
    waves: dict[int, set[str]] = {}
    for line in text.split("\n"):
        m = re.match(r"^\| W(\d+)\b", line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        tasks = set(re.findall(r"\bT\d+\b", cells[2])) if len(cells) > 2 else set()
        waves.setdefault(int(m.group(1)), set()).update(tasks)
    assert waves, f"{state}: orchestration.md has no wave row read by grep '^| W<n> '"
    return waves


def _verify_done_lines(project: Path, state: str) -> list[str]:
    validation = _feature_file(project, state, "validation.md").read_text(encoding="utf-8")
    return [line.rstrip() for line in validation.split("\n") if " · verify-done · " in line]


def _verified_waves(lines: list[str]) -> set[int]:
    waves: set[int] = set()
    for line in lines:
        m = re.search(r"waves W(\d+)\s*[–-]\s*W(\d+)", line)
        if m:
            waves.update(range(int(m.group(1)), int(m.group(2)) + 1))
    return waves


def _assert_looping(project: Path, state: str, docs_wave: int | None = None) -> str:
    """looping: handoff.md from 0.4.0's text, every task ticked (but the docs wave's, for
    docs-wave), a verify-done line for every wave (but the docs wave), and run-ledger.md with
    ``## Rounds`` and a newest Lease line ``released by relay 1: done``."""
    _assert_handoff_040(project, state)
    waves = _wave_tasks(project, state)
    left_out = waves.get(docs_wave, set()) if docs_wave is not None else set()
    unticked = sorted(t for t, ticked in _tasks(project, state).items()
                      if not ticked and t not in left_out)
    assert not unticked, f"{state}: tasks still unticked: {unticked}"
    verified = _verified_waves(_verify_done_lines(project, state))
    unverified = sorted(w for w in waves if w != docs_wave and w not in verified)
    assert not unverified, f"{state}: no verify-done line covers the waves {unverified}"
    ledger = _assert_ledger_with_rounds(project, state)
    lease = _ledger_section(ledger, "## Lease")
    assert lease, f"{state}: run-ledger.md's Lease is empty"
    assert LEASE_RELEASED_DONE in lease[-1], \
        f"{state}: the newest Lease line is not `{LEASE_RELEASED_DONE}`: {lease[-1]}"
    return ledger


def test_fixtures_make_feature_looping_state_leaves_its_files(repo_root, sh, git, tmp_path):
    project = _make_state(repo_root, sh, git, tmp_path, "looping")
    _assert_looping(project, "looping")
    _assert_neutral(tmp_path, git)


def test_fixtures_make_feature_per_wave_state_leaves_its_files(repo_root, sh, git, tmp_path):
    state = "per-wave"
    project = _make_state(repo_root, sh, git, tmp_path, state)
    _assert_handoff_040(project, state)
    _assert_ledger_with_rounds(project, state)
    ticked = sorted(t for t, done in _tasks(project, state).items() if done)
    assert not ticked, f"{state}: its waves are still to run, yet {ticked} are ticked"
    guidance = project / "CLAUDE.md"
    assert guidance.is_file(), f"{state}: the project has no CLAUDE.md"
    lines = [line.strip() for line in guidance.read_text(encoding="utf-8").split("\n")]
    per_wave = [line for line in lines if line.startswith("Per-wave tests:")]
    full = [line for line in lines if line.startswith("Full suite:")]
    sees = [line for line in lines if line.startswith("Per-wave sees:")]
    assert len(per_wave) == 1 and len(full) == 1 and len(sees) == 1, \
        f"{state}: CLAUDE.md needs one line each of Per-wave tests:, Full suite:, Per-wave sees:"
    per_wave_cmd = per_wave[0][len("Per-wave tests:"):].strip()
    full_cmd = full[0][len("Full suite:"):].strip()
    assert per_wave_cmd and per_wave_cmd.lower() != "none", \
        f"{state}: Per-wave tests: names no command"
    assert full_cmd, f"{state}: Full suite: names no command"
    assert per_wave_cmd != full_cmd, \
        f"{state}: Per-wave tests: is the whole test command, not a fast subset"
    assert sees[0] == PER_WAVE_SEES, f"{state}: the line is {sees[0]!r}, not {PER_WAVE_SEES!r}"
    assert git(project, "ls-files", "CLAUDE.md") == "CLAUDE.md", \
        f"{state}: CLAUDE.md is not committed"
    assert git(project, "status", "--porcelain", "--", "CLAUDE.md") == "", \
        f"{state}: CLAUDE.md has uncommitted changes"
    _assert_neutral(tmp_path, git)


def test_fixtures_make_feature_green_run_state_leaves_its_files(repo_root, sh, git, tmp_path):
    state = "green-run"
    project = _make_state(repo_root, sh, git, tmp_path, state)
    _assert_looping(project, state)
    head = git(project, "rev-parse", "--short", "HEAD")
    lines = _verify_done_lines(project, state)
    assert lines and lines[-1].endswith(f" · green at {head}"), \
        f"{state}: the newest verify-done line does not end ` · green at {head}`: {lines[-1:]}"
    assert git(project, "status", "--porcelain") == "", f"{state}: the project's tree is dirty"
    _assert_neutral(tmp_path, git)


def test_fixtures_make_feature_docs_wave_state_leaves_its_files(repo_root, sh, git, tmp_path):
    state = "docs-wave"
    project = _make_state(repo_root, sh, git, tmp_path, state)
    handoff = _feature_file(project, state, "handoff.md").read_text(encoding="utf-8")
    named = re.search(r"DOCS WAVE \(W(\d+)\)", handoff)
    assert named, f"{state}: handoff.md names no `DOCS WAVE (W<n>)`"
    n = int(named.group(1))
    ledger = _assert_looping(project, state, docs_wave=n)
    docs_tasks = _wave_tasks(project, state).get(n, set())
    assert docs_tasks, f"{state}: orchestration.md's wave W{n} has no tasks"
    tasks = _tasks(project, state)
    ticked = sorted(t for t in docs_tasks if tasks.get(t, False))
    assert not ticked, f"{state}: the docs wave W{n}'s tasks {ticked} are ticked"
    built = [m for m in (re.search(r"Docs wave W?(\d+) built, uncommitted: (.+)$", line)
                         for line in _ledger_section(ledger, "## Blocked and skipped")) if m]
    assert built and int(built[-1].group(1)) == n, \
        f"{state}: no `Docs wave {n} built, uncommitted: <files>` line under Blocked and skipped"
    files = [f.strip().strip("`") for f in built[-1].group(2).split(",") if f.strip()]
    assert files, f"{state}: the ledger line names no files"
    # The git fixture strips its output, so the path is read after the status field.
    changed = {line.strip().split(None, 1)[1].strip('"')
               for line in git(project, "status", "--porcelain", "-uall").split("\n")
               if line.strip()}
    uncommitted = [f for f in files if f not in changed]
    assert not uncommitted, \
        f"{state}: the docs wave's files {uncommitted} are not changed and uncommitted"
    _assert_neutral(tmp_path, git)


def test_fixtures_make_copy_copies_skills_into_dot_claude(repo_root, sh, tmp_path):
    fixtures = _fixtures_dir(repo_root)
    project = tmp_path / "acme-notes"
    project.mkdir()
    assert sh(fixtures / "make-project.sh", project, "acme", cwd=tmp_path).returncode == 0
    plugin = tmp_path / "plugin"
    (plugin / "skills" / "s2tdd-next").mkdir(parents=True)
    (plugin / "skills" / "s2tdd-next" / "SKILL.md").write_text("# next\n", encoding="utf-8")
    proc = sh(fixtures / "make-copy.sh", project, plugin, cwd=tmp_path)
    assert proc.returncode == 0, proc.stderr
    copied = project / ".claude" / "skills" / "s2tdd-next" / "SKILL.md"
    assert copied.is_file() and copied.read_text(encoding="utf-8") == "# next\n", \
        f"{copied} is not a copy of skills/s2tdd-next/SKILL.md"


# ------------------------------------------------------------------------------ Scaffold


@pytest.mark.parametrize("sid, area, slug, text", ALL_CASES)
def test_scaffold_builds_project_and_specs_repositories(scaffold, git, sid, area, slug, text):
    built = scaffold(sid, area, slug)
    assert built.proc.returncode == 0, \
        f"{sid}: scaffold exited {built.proc.returncode}: {built.proc.stderr.strip()}"
    project = _find_project(built.work)
    assert git(project, "rev-parse", "--git-dir"), f"{sid}: {project} is not a git repository"
    if sid in NO_SPECS_DIRECTORY:
        assert not (project / "specs").exists(), f"{sid}: the Given has no specs/ directory"
        return
    specs = _assert_own_repository(git, project, "specs")
    if sid in NO_SPECS_REMOTE:
        assert git(specs, "remote") == "", f"{sid}: the Given has specs/ with no remote"
    else:
        _assert_bare_remote(git, specs, f"{sid}'s specs/")
    _assert_bare_remote(git, project, f"{sid}'s project")


@pytest.mark.parametrize("sid, area, slug, text", ALL_CASES)
def test_scaffold_names_are_neutral(scaffold, git, sid, area, slug, text):
    built = scaffold(sid, area, slug)
    assert built.proc.returncode == 0, \
        f"{sid}: scaffold exited {built.proc.returncode}: {built.proc.stderr.strip()}"
    _assert_neutral(built.base, git)
