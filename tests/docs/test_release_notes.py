"""The release record: CHANGELOG.md's sections and the plugin version.

002 (T008; II-13, FR-014) pinned the 0.3.0 section, which stays as history. 003 (T022; II-13
Release, R14) adds the 0.4.0 section and moves the plugin version to 0.4.0: expected red until
T025 writes the `## 0.4.0` section and bumps `.claude-plugin/plugin.json`.
Each test file holds its own constants (II-0), transcribed from the contracts.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import re

# II-13: `## 0.3.0 — unreleased`, or `## 0.3.0 — YYYY-MM-DD` once released.
HEADING_0_3_0_RE = re.compile(
    r"^## 0\.3\.0 — (?P<when>unreleased|\d{4}-\d{2}-\d{2})[ \t]*$", re.MULTILINE
)
HEADING_0_3_0_WORDS = "'## 0.3.0 — unreleased' or '## 0.3.0 — YYYY-MM-DD'"
HEADING_0_2_0 = "## 0.2.0 — 2026-10-03"

# II-13: the 0.3.0 section names each of these.
PHRASES_0_3_0 = ("shape check", "opus", "week=", "five-hour=", "Boundary")

# II-13, exact.
WORKFLOW_NOTE = (
    "Projects whose specs/WORKFLOW.md predates 0.3.0: delete it, and the next /s2tdd-specify, "
    "/s2tdd-epic or /s2tdd-constitution copies in the new one."
)

# II-13: 0.2.0's section byte-for-byte unchanged. SHA-256 of the section as released (its
# heading line through the blank line before `## 0.1.0`, LF line endings), at bd6c494.
SECTION_0_2_0_SHA256 = "145c68dc027920ea37318f8207c49b75bcc34b53366d24a17a44452e934a33fe"

# 003 II-13 Release: `## 0.4.0 — unreleased`, or `## 0.4.0 — YYYY-MM-DD` once released,
# above `## 0.3.0 — 2026-10-04`.
HEADING_0_4_0_RE = re.compile(
    r"^## 0\.4\.0 — (?P<when>unreleased|\d{4}-\d{2}-\d{2})[ \t]*$", re.MULTILINE
)
HEADING_0_4_0_WORDS = "'## 0.4.0 — unreleased' or '## 0.4.0 — YYYY-MM-DD'"
HEADING_0_3_0 = "## 0.3.0 — 2026-10-04"

# 003 II-13 Release: the 0.4.0 section names each of these.
PHRASES_0_4_0 = (
    "--nobrakes once",
    "converger",
    "hardener",
    "Per-wave tests:",
    "Full suite:",
    "Per-wave sees:",
    "green at <sha>",
    "ready to close",
)

# 003 II-13 Release, exact.
NOTES_0_4_0 = (
    "Features hardened before 0.4.0 run as before and stop when every task is ticked: "
    "/s2tdd-harden handoff refreshes their handoff.md for the converge loop and the per-wave run.",
    "Projects whose specs/WORKFLOW.md predates 0.4.0: delete it, and the next /s2tdd-specify, "
    "/s2tdd-epic or /s2tdd-constitution copies in the new one.",
)

# 003 R14 (II-13 Release): supersedes 002 II-13's `0.3.0` pin.
PLUGIN_VERSION = "0.4.0"


def _flat(text: str) -> str:
    """Same flattening as Doc.flat (II-0)."""
    return " ".join(text.lower().replace("`", "").replace("*", "").split())


def _changelog(repo_root) -> str:
    """CHANGELOG.md's text from its bytes, CRLF normalised to LF (the repository's eol)."""
    return (repo_root / "CHANGELOG.md").read_bytes().decode("utf-8").replace("\r\n", "\n")


def _heading_0_3_0(text: str) -> "re.Match[str]":
    """The 0.3.0 heading match; a dated heading must be a real calendar date."""
    match = HEADING_0_3_0_RE.search(text)
    assert match, f"no {HEADING_0_3_0_WORDS} heading in CHANGELOG.md"
    when = match.group("when")
    if when != "unreleased":
        try:
            datetime.date.fromisoformat(when)
        except ValueError:
            raise AssertionError(f"the 0.3.0 heading date {when!r} is not a real date") from None
    return match


def _section_from(text: str, start: int, heading_end: int) -> str:
    """The text from `start` up to the next `## ` heading after `heading_end`."""
    following = re.search(r"^## ", text[heading_end:], re.MULTILINE)
    return text[start : heading_end + following.start()] if following else text[start:]


def _heading_0_4_0(text: str) -> "re.Match[str]":
    """The 0.4.0 heading match; a dated heading must be a real calendar date."""
    match = HEADING_0_4_0_RE.search(text)
    assert match, f"no {HEADING_0_4_0_WORDS} heading in CHANGELOG.md"
    when = match.group("when")
    if when != "unreleased":
        try:
            datetime.date.fromisoformat(when)
        except ValueError:
            raise AssertionError(f"the 0.4.0 heading date {when!r} is not a real date") from None
    return match


def _section_0_4_0(text: str) -> str:
    match = _heading_0_4_0(text)
    return _section_from(text, match.end(), match.end())


def _section_0_3_0(text: str) -> str:
    match = _heading_0_3_0(text)
    return _section_from(text, match.end(), match.end())


def test_docs_changelog_has_the_0_3_0_heading_above_0_2_0(repo_root):
    text = _changelog(repo_root)
    match = _heading_0_3_0(text)
    assert HEADING_0_2_0 in text, f"no {HEADING_0_2_0!r} heading in CHANGELOG.md"
    assert match.start() < text.index(HEADING_0_2_0), "the 0.3.0 entry is not above 0.2.0"


def test_docs_changelog_0_3_0_names_what_changed(repo_root):
    section = _flat(_section_0_3_0(_changelog(repo_root)))
    absent = [p for p in PHRASES_0_3_0 if _flat(p) not in section]
    assert not absent, f"the 0.3.0 entry lacks {absent}"


def test_docs_changelog_0_3_0_has_the_workflow_note(repo_root):
    section = _flat(_section_0_3_0(_changelog(repo_root)))
    assert _flat(WORKFLOW_NOTE) in section, f"the 0.3.0 entry lacks the note: {WORKFLOW_NOTE}"


def test_docs_changelog_0_2_0_is_unchanged(repo_root):
    text = _changelog(repo_root)
    start = text.find(HEADING_0_2_0)
    assert start != -1, f"no {HEADING_0_2_0!r} heading in CHANGELOG.md"
    section = _section_from(text, start, start + len(HEADING_0_2_0))
    digest = hashlib.sha256(section.encode("utf-8")).hexdigest()
    assert digest == SECTION_0_2_0_SHA256, "the 0.2.0 section of CHANGELOG.md has changed"


def test_docs_changelog_has_the_0_4_0_heading_above_0_3_0(repo_root):
    text = _changelog(repo_root)
    match = _heading_0_4_0(text)
    assert HEADING_0_3_0 in text, f"no {HEADING_0_3_0!r} heading in CHANGELOG.md"
    assert match.start() < text.index(HEADING_0_3_0), "the 0.4.0 entry is not above 0.3.0"


def test_docs_changelog_0_4_0_names_what_changed(repo_root):
    section = _flat(_section_0_4_0(_changelog(repo_root)))
    absent = [p for p in PHRASES_0_4_0 if _flat(p) not in section]
    assert not absent, f"the 0.4.0 entry lacks {absent}"


def test_docs_changelog_0_4_0_has_the_notes(repo_root):
    section = _flat(_section_0_4_0(_changelog(repo_root)))
    absent = [note for note in NOTES_0_4_0 if _flat(note) not in section]
    assert not absent, f"the 0.4.0 entry lacks the notes: {absent}"


def test_docs_plugin_version_is_0_4_0(repo_root):
    manifest = json.loads((repo_root / ".claude-plugin" / "plugin.json").read_text("utf-8"))
    version = manifest.get("version")
    assert version == PLUGIN_VERSION, (
        f".claude-plugin/plugin.json version {version!r}, not {PLUGIN_VERSION!r}"
    )
