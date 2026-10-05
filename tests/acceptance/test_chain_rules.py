"""US2 acceptance tests for the chain's carried-over rules and literal command names (T025;
II-3, II-5, II-11).

The II-11 constants live here on purpose: they outlive the preset's removal (T079).

test_001_ec004_git_bash_handoff is retired: superseded by 002 FR-020, R10 (relays print).
"""

from __future__ import annotations

import re

# II-3: tools/check.py's COMMANDS (transcribed).
COMMANDS = ("epic", "specify", "clarify", "plan", "harden", "implement", "verify-done",
            "converge", "pr-review", "close", "next", "foundation-review", "constitution")

# II-11 (transcribed): `skills/s2tdd-harden/SKILL.md` holds each of these.
NOBRAKES_MARKERS = (
    "NOBRAKES (only when MODE is nobrakes; otherwise skip this section)",
    "STATE lives in files, never only in this context.",
    "STRONG-DIFF REVIEW.",
    "FAILED FENCES.",
    "STOP THE RUN (start nothing more; print the RUN SUMMARY) when:",
    "VERIFY GATES at each slice end",
    "TAG after a gate's verdict and its gap fixes",
    "DOCS WAVE (<docs wave>) runs last in the run",
    "HANDOFF. At each wave boundary",
    "BRAKES. When the user asks for brakes in chat",
    "RUN SUMMARY, the last thing you print",
)
STANDARD_BRIEFS = ("### Proxy verifier", "### Strong-diff reviewer (read-only)",
                   "### Test-owner fix", "### Flake diagnosis")

# Usage line: 002 II-8's first Usage sentence (002 FR-021, R5; was 001 II-11's).
USAGE_LINE = (
    "In Claude Code, read usage with the `get_usage` tool (the context window's percent used "
    "and the plan's five-hour, weekly and per-model weekly windows, each with its reset time)."
)

# II-11 EC-006 sentence added to harden's ground rule 17.
NO_QUARANTINE = "A test is never skipped or quarantined to get green."

# `/s2tdd-<x>`, not part of a path (`skills/s2tdd-x`) or a longer token; `<x>` is a hyphenated
# lowercase word, so a placeholder such as `/s2tdd-<name>` does not match.
COMMAND_NAME = re.compile(r"(?<![\w./-])/s2tdd-([a-z]+(?:-[a-z]+)*)")


def test_001_us2_ac7_nobrakes_rules_carried_over(skill):
    """US2-AC7: **Given** a hardened feature, **When** the user runs `/s2tdd-implement
    --nobrakes`, **Then** its run rules, gates, run ledger and reports by exception behave as
    the preset's do today, and its stand-ins for verify-done and the strong-diff read run as
    the proxy-verifier and strong-diff-reviewer agent types (T15).

    Provenance: 001 spec.md
    """
    harden = skill("s2tdd-harden")
    absent = harden.missing(*NOBRAKES_MARKERS)
    assert not absent, f"harden lacks NOBRAKES markers: {absent}"
    absent = harden.missing(*STANDARD_BRIEFS)
    assert not absent, f"harden lacks standard briefs: {absent}"
    absent = harden.missing(USAGE_LINE)
    assert not absent, f"harden lacks 002 II-8's Usage line: {absent}"

    implement = skill("s2tdd-implement")
    absent = implement.missing("s2tdd:proxy-verifier", "s2tdd:strong-diff-reviewer")
    assert not absent, f"implement does not name the agent types: {absent}"


def test_001_us2_ac9_literal_s2tdd_names(repo_root, tool):
    """US2-AC9: **Given** a feature at any step, **When** a command or the next-step prompt
    names another command, **Then** the name is the literal `/s2tdd-<name>`; no `/speckit-`
    name and no command placeholder appears (T06).

    Provenance: 001 spec.md
    """
    result = tool("check", "--root", str(repo_root), "--rule", "placeholders",
                  "--rule", "old-names")
    assert result.returncode == 0, result.stdout + result.stderr

    offences = []
    for top in ("skills", "src"):
        for path in sorted((repo_root / top).rglob("*")):
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue  # not a text file
            rel = path.relative_to(repo_root).as_posix()
            for lineno, line in enumerate(text.split("\n"), start=1):
                for match in COMMAND_NAME.finditer(line):
                    name = match.group(1)
                    if name not in COMMANDS:
                        offences.append(f"{rel}:{lineno}: /s2tdd-{name} is not one of the 13 commands")
                    elif not (repo_root / "skills" / f"s2tdd-{name}" / "SKILL.md").is_file():
                        offences.append(
                            f"{rel}:{lineno}: /s2tdd-{name} names a command without a skill "
                            f"folder (skills/s2tdd-{name}/SKILL.md not found)"
                        )
    assert not offences, "\n".join(offences)


def test_001_ec006_flake_diagnosis(skill):
    """EC-006: **Given** a red test that passes when run alone, **When** implement handles it,
    **Then** it goes to flake diagnosis before any re-dispatch, and is never skipped or
    quarantined (T16).

    Provenance: 001 spec.md
    """
    harden = skill("s2tdd-harden")
    absent = harden.missing("a red that passes when run alone", "flake diagnosis",
                            "before any re-dispatch")
    assert not absent, f"harden's ground rules lack: {absent}"
    absent = harden.missing(NO_QUARANTINE)
    assert not absent, f"harden lacks II-11's no-quarantine sentence: {absent}"
