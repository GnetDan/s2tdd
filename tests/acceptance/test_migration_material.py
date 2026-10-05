"""US3 acceptance tests for the migration material (T067; II-15, II-5).

AC5 reads the README section and the "Coming from spec-kit" page. AC9 checks that the old
packaging is gone; it is a strict xfail until T079 removes `preset/` and `extension/`, and T095
removes the marker.
"""

from __future__ import annotations

import re

import pytest

PAGE = "docs/coming-from-spec-kit.md"
SECTION_HEADING = "## Coming from spec-kit"

# T067 AC5 (transcribed): what the page tells the reader to uninstall, in the task's order.
# `uv tool uninstall specify-cli` comes last.
UNINSTALL_ITEMS = (
    "specify preset remove",
    "specify extension remove",
    "spec-kit's git extension",
    ".specify/",
    ".claude/skills/speckit-*/",
)
UNINSTALL_LAST = "uv tool uninstall specify-cli"

# II-15 (transcribed): the rename table, one entry per row as (old names, new name). The row
# whose new name is "none" is checked on its old names only.
RENAME_ROWS = (
    (("/speckit-<x>",), "/s2tdd-<x>"),
    (("/speckit-tasks", "/speckit-harden"), "/s2tdd-harden"),
    (("/speckit-handoff",), "/s2tdd-implement --print"),
    (("/speckit-save",), "/s2tdd-next"),
    (("/speckit-branch",), "/s2tdd-specify"),
    (("/speckit-analyze", "/speckit-checklist", "/speckit-taskstoissues"), None),
    ((".specify/memory/constitution.md",), "specs/constitution.md"),
    (("docs/sdd-workflow.md",), "specs/WORKFLOW.md"),
)

LAYOUT_PHRASES = ("specs/NNN-name/", "unchanged")

# T067 AC9: the old packaging directories, which the README must not mention either.
OLD_PACKAGING = ("preset/", "extension/")


def _section(text: str, heading: str) -> str | None:
    """The text under `heading` up to the next `## ` heading, else None."""
    lines = text.split("\n")
    start = next((i for i, line in enumerate(lines) if line.rstrip() == heading), None)
    if start is None:
        return None
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")),
               len(lines))
    return "\n".join(lines[start + 1 : end])


def test_001_us3_ac5_coming_from_spec_kit(doc):
    """US3-AC5: **Given** a plain spec-kit user, **When** they read the README's "Coming from
    spec-kit" section and page, **Then** they find what to uninstall and which command maps to
    which (T09).

    Provenance: 001 spec.md
    """
    page = doc(PAGE)
    readme = doc("README.md")

    section = _section(readme.text, SECTION_HEADING)
    assert section is not None, f"README.md has no `{SECTION_HEADING}` heading"
    assert re.search(r"\]\([^)\s]*docs/coming-from-spec-kit\.md[^)]*\)", section), (
        f"README.md's `{SECTION_HEADING}` section does not link {PAGE}"
    )

    wanted = UNINSTALL_ITEMS + (UNINSTALL_LAST,)
    gone = page.missing(*wanted)
    assert not gone, f"{PAGE} does not name what to uninstall: {gone}"

    last_at = page.flat.index(_flat(UNINSTALL_LAST))
    early = [item for item in UNINSTALL_ITEMS if page.flat.index(_flat(item)) > last_at]
    assert not early, f"`{UNINSTALL_LAST}` is not last: first named after it: {early}"

    for olds, new in RENAME_ROWS:
        names = olds + ((new,) if new is not None else ())
        gone = page.missing(*names)
        assert not gone, f"{PAGE} is missing a rename-table row ({olds} -> {new}): {gone}"

    gone = page.missing(*LAYOUT_PHRASES)
    assert not gone, f"{PAGE} does not say the specs/NNN-name/ layout is unchanged: {gone}"


def _flat(phrase: str) -> str:
    """The same flattening as `Doc.flat` (conftest `_flatten`), for positions in the page."""
    phrase = phrase.lower().replace("`", "").replace("*", "")
    return re.sub(r"\s+", " ", phrase).strip()

def test_001_us3_ac9_old_packaging_removed(repo_root, doc):
    """US3-AC9: **Given** this repository past the migration checkpoint, **When** this feature
    closes, **Then** the product repository has no `preset/` or `extension/` directory.

    Provenance: 001 spec.md
    """
    present = [name for name in OLD_PACKAGING if (repo_root / name).is_dir()]
    assert not present, f"{present} exist in the product repository"

    readme = doc("README.md")
    mentioned = [name for name in OLD_PACKAGING if name in readme.text]
    assert not mentioned, f"README.md mentions {mentioned}"
