"""The unattended-run pages: docs/nobrakes.md and docs/getting-started.md (T009; II-15, FR-013).

Expected red until T011 updates the pages. Each test file holds its own constants (II-0),
transcribed from the contract.
"""

from __future__ import annotations

import re

NOBRAKES_PAGE = "docs/nobrakes.md"
GETTING_STARTED = "docs/getting-started.md"

# II-15: docs/nobrakes.md holds each of these, `shape check` first.
NOBRAKES_PHRASES = ("shape check", "push notification", "week=", "five-hour=", "Boundary:")

# II-15: gone from docs/nobrakes.md and from getting-started's hand-off bullet.
SCHEDULED_TASK = "one-shot scheduled task"

# 001's FR-032 sentence (001 II-16, exact), which leaves docs/nobrakes.md (II-15).
FR032_NOTE = (
    "`--nobrakes`'s hand-off to a fresh session (including the scheduled-task start) "
    "and its brakes are carried over from the preset but untried in the field."
)

# II-15: the hand-off bullet says the run prints the handoff prompt (either spelling of
# "handoff": the page writes "hand-off").
HANDOFF_PROMPT = re.compile(r"\bhand-?off prompt\b")
PRINTS = re.compile(r"\bprint")

# II-15 (FR-029): the Cursor section lists each of these.
CURSOR_PHRASES = ("no usage tool", "n/a", "no push notification", "general subagent")


def _flat(text: str) -> str:
    """Same flattening as Doc.flat (II-0)."""
    return " ".join(text.lower().replace("`", "").replace("*", "").split())


def _handoff_bullet(body: str) -> str | None:
    """The flattened list item whose first line names the `--nobrakes` hand-off, with its
    indented continuation lines; None when there is none."""
    lines = body.split("\n")
    for i, line in enumerate(lines):
        if not re.match(r"^\s*[-*] ", line):
            continue
        first = _flat(line)
        if "--nobrakes" not in first or "hand" not in first:
            continue
        indent = len(line) - len(line.lstrip())
        item = [line]
        for following in lines[i + 1 :]:
            if not following.strip():
                break
            if len(following) - len(following.lstrip()) <= indent:
                break
            item.append(following)
        return _flat("\n".join(item))
    return None


def _sections(body: str) -> list[str]:
    """The flattened `## ` sections of a page (each to the next `## ` heading)."""
    starts = [m.start() for m in re.finditer(r"^## ", body, re.MULTILINE)]
    return [_flat(body[a:b]) for a, b in zip(starts, [*starts[1:], len(body)])]


def test_docs_nobrakes_page_holds_the_run_changes(doc):
    d = doc(NOBRAKES_PAGE)
    for phrase in NOBRAKES_PHRASES:
        assert not d.missing(phrase), f"{NOBRAKES_PAGE} lacks `{phrase}`"


def test_docs_nobrakes_page_drops_the_scheduled_task_and_the_old_sentence(doc):
    d = doc(NOBRAKES_PAGE)
    assert _flat(SCHEDULED_TASK) not in d.flat, f"{NOBRAKES_PAGE} still says {SCHEDULED_TASK!r}"
    assert _flat(FR032_NOTE) not in d.flat, (
        f"{NOBRAKES_PAGE} still holds 001's FR-032 sentence: {FR032_NOTE}"
    )


def test_docs_getting_started_handoff_bullet_prints_the_prompt(doc):
    bullet = _handoff_bullet(doc(GETTING_STARTED).body)
    assert bullet is not None, f"{GETTING_STARTED} has no `--nobrakes` hand-off bullet"
    assert _flat(SCHEDULED_TASK) not in bullet, (
        f"{GETTING_STARTED}'s hand-off bullet still says {SCHEDULED_TASK!r}"
    )
    assert PRINTS.search(bullet) and HANDOFF_PROMPT.search(bullet), (
        f"{GETTING_STARTED}'s hand-off bullet never says the run prints the handoff prompt"
    )


def test_docs_getting_started_cursor_section_lists_the_fallbacks(doc):
    sections = [s for s in _sections(doc(GETTING_STARTED).body) if "cursor" in s]
    assert sections, f"{GETTING_STARTED} has no section that names Cursor"
    best = min(
        ([p for p in CURSOR_PHRASES if _flat(p) not in s] for s in sections), key=len
    )
    assert not best, f"{GETTING_STARTED}'s Cursor section lacks {best}"
