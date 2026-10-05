"""US7 acceptance test for the Test upkeep section and the links to it (T048; II-13, II-4).

The II-13 link set lives here on purpose: this file is the one place the section's links are
pinned.
"""

from __future__ import annotations

import re

# II-13 (transcribed): the section's `http` links are exactly this set (nine distinct URLs).
UPKEEP_LINKS = {
    "https://abseil.io/resources/swe-book/html/ch11.html#test_size",
    "https://abseil.io/resources/swe-book/html/ch11.html#the_pitfalls_of_a_large_test_suite",
    "https://docs.pytest.org/en/stable/how-to/usage.html#profiling-test-execution-duration",
    "https://docs.pytest.org/en/stable/example/simple.html#control-skipping-of-tests-according-to-command-line-option",
    "https://martinfowler.com/articles/nonDeterminism.html",
    "https://testdesiderata.com/",
    "https://git-scm.com/docs/gitattributes#_eol",
    "https://abseil.io/resources/swe-book/html/ch12.html#preventing_brittle_tests",
    "https://abseil.io/resources/swe-book/html/ch13.html#avoid_overspecification",
}

# II-13 (transcribed): T16's five topics, as the section's table names them.
UPKEEP_TOPICS = (
    "suite speed",
    "determinism and flakes",
    "fixtures and platforms",
    "over-specified tests",
    "pruning",
)

# II-4: the page and the three skills that bundle a copy of it.
WORKFLOW_COPIES = (
    "src/pages/WORKFLOW.md",
    "skills/s2tdd-specify/pages/WORKFLOW.md",
    "skills/s2tdd-epic/pages/WORKFLOW.md",
    "skills/s2tdd-constitution/pages/WORKFLOW.md",
)

HEADING = "## Test upkeep"
HARDEN_LINK = "specs/WORKFLOW.md#test-upkeep"
FLAKE_HEADING = "### Flake diagnosis"
EXCLUDED_HOST = "testing.googleblog.com"

_URL = re.compile(r"https?://[^\s)>\]\"'`]+")


def _upkeep_section(text: str) -> str | None:
    """The text under the `## Test upkeep` heading up to the next `## ` heading, else None."""
    lines = text.split("\n")
    start = next((i for i, line in enumerate(lines) if line.rstrip() == HEADING), None)
    if start is None:
        return None
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")),
               len(lines))
    return "\n".join(lines[start + 1 : end])


def _links(section: str) -> set[str]:
    return {m.group(0).rstrip(".,;:") for m in _URL.finditer(section)}


def _flake_brief(text: str) -> str | None:
    """The `### Flake diagnosis` brief: from its heading to the closing fence or next heading."""
    lines = text.split("\n")
    start = next((i for i, line in enumerate(lines) if line.rstrip() == FLAKE_HEADING), None)
    if start is None:
        return None
    end = next((i for i in range(start + 1, len(lines))
                if lines[i].startswith("#") or lines[i].startswith("````")), len(lines))
    return "\n".join(lines[start + 1 : end])


def test_001_us7_ac1_test_upkeep_section(doc, skill):
    """US7-AC1: **Given** a set-up project, **When** the user opens `specs/WORKFLOW.md`,
    **Then** it has a short Test upkeep section with T16's topics and links only to T16's
    sources, and harden's briefs and the flake-diagnosis brief link to it (T16).

    Provenance: 001 spec.md
    """
    for relpath in WORKFLOW_COPIES:
        page = doc(relpath)
        section = _upkeep_section(page.text)
        assert section is not None, f"no `{HEADING}` heading in {relpath}"

        flat = re.sub(r"\s+", " ", section.lower().replace("`", "").replace("*", ""))
        absent = [t for t in UPKEEP_TOPICS if t not in flat]
        assert not absent, f"{relpath}: Test upkeep section lacks topics {absent}"

        found = _links(section)
        assert found == UPKEEP_LINKS, (
            f"{relpath}: Test upkeep links differ from II-13: "
            f"missing {sorted(UPKEEP_LINKS - found)}, extra {sorted(found - UPKEEP_LINKS)}"
        )

        assert EXCLUDED_HOST not in page.text.lower(), (
            f"{relpath} links {EXCLUDED_HOST}; the note names the post in words only"
        )

    harden = skill("s2tdd-harden")
    brief = _flake_brief(harden.text)
    assert brief is not None, f"skills/s2tdd-harden/SKILL.md has no `{FLAKE_HEADING}` brief"
    assert HARDEN_LINK in brief, f"harden's flake-diagnosis brief lacks {HARDEN_LINK}"
    assert harden.text.count(HARDEN_LINK) >= 2, (
        f"harden's packet briefs lack {HARDEN_LINK} beyond the flake-diagnosis brief"
    )
