"""MIGRATING.md and the "Coming from spec-kit" page can be followed literally, by an agent,
without improvising (spec Clarifications 2026-10-03: MIGRATING executable end to end;
first-run setup leaves the old `docs/sdd-workflow.md`, and deleting it is the user's
MIGRATING.md step).

Assertion style (II-5): listed phrases in flattened text, per `## N.` section.
"""

from __future__ import annotations

import re

MIGRATING = "MIGRATING.md"
PAGE = "docs/coming-from-spec-kit.md"


def _flat(text: str) -> str:
    """Same flattening as Doc.flat: lowercase, no backticks or asterisks, one space."""
    text = text.lower().replace("`", "").replace("*", "")
    return re.sub(r"\s+", " ", text).strip()


def _section(body: str, heading_re: str) -> str:
    """The raw text under the first heading matching `heading_re`, to the next `## `."""
    match = re.search(heading_re, body, re.MULTILINE)
    assert match, f"no heading matching {heading_re!r}"
    rest = body[match.end() :]
    following = re.search(r"^## ", rest, re.MULTILINE)
    return rest[: following.start()] if following else rest


def _step(body: str, number: int) -> str:
    return _flat(_section(body, rf"^## {number}\. .*$"))


def _items(raw: str) -> list[str]:
    """The flattened list items (`1.` or `-` bullets) of a raw section, each with its
    continuation lines."""
    items: list[str] = []
    for line in raw.split("\n"):
        if re.match(r"^(\d+\.|-) ", line):
            items.append(line)
        elif items and line.startswith(" "):
            items[-1] += " " + line
        elif not line.strip():
            continue
        else:
            items.append("")
    return [_flat(item) for item in items if item]


# --- the old workflow page (S1, Q5-1) -------------------------------------------


def test_migrating_step_2_moves_the_old_workflow_page_aside(doc):
    """Step 7 expects no `docs/sdd-workflow.md` leftover, so an earlier step must move it."""
    step = _step(doc(MIGRATING).body, 2)
    assert "docs/sdd-workflow.md" in step, (
        "step 2 never moves docs/sdd-workflow.md aside, yet step 7 expects no such leftover"
    )


def test_migrating_says_where_specs_workflow_md_comes_from(doc):
    step = _step(doc(MIGRATING).body, 4)
    assert "specs/workflow.md" in step and "first-run setup" in step, (
        "step 4 never says that specs/WORKFLOW.md arrives with first-run setup"
    )


# --- a new session before the first plugin command (Q5-2) -------------------------


def test_migrating_starts_a_new_session_before_the_handoff_refresh(doc):
    body = doc(MIGRATING).body
    run = " ".join(_step(body, n) for n in (3, 4, 5, 6))
    refresh = run.find("/s2tdd-harden handoff")
    assert refresh != -1, "steps 3-6 never run /s2tdd-harden handoff"
    assert re.search(r"\bnew session\b", run[:refresh]), (
        "steps 3-6 run /s2tdd-harden handoff before saying to start a new session, "
        "yet only a new session loads the plugin's commands"
    )


# --- the plain spec-kit path (Q5-3) ---------------------------------------------


def test_migrating_saves_the_constitution_on_both_paths(doc):
    """Plain spec-kit keeps its constitution at .specify/memory/constitution.md too."""
    body = doc(MIGRATING).body
    marked = [
        item
        for n in (2, 4)
        for item in _items(_section(body, rf"^## {n}\. .*$"))
        if ".specify/memory/constitution.md" in item and item.startswith(("1. preset only", "- preset only", "preset only"))
    ]
    assert not marked, f"the constitution move is marked preset only: {marked}"


def test_migrating_gives_a_tracked_specs_folder_its_own_repository(doc):
    d = doc(MIGRATING)
    assert "its own repository" in d.flat, (
        "MIGRATING.md never says that specs/ must be its own repository"
    )
    assert re.search(r"\]\([^)\s]*docs/coming-from-spec-kit\.md[^)]*\)", d.body), (
        "MIGRATING.md never links docs/coming-from-spec-kit.md"
    )


# --- the coming-from page's step 1 (Q5-4) -----------------------------------------


def _page_step_1(doc) -> str:
    raw = _section(doc(PAGE).body, r"^## What to uninstall$")
    items = _items(raw)
    assert items and items[0].startswith("1."), "the uninstall list has no step 1"
    return items[0]


def test_coming_from_step_1_commits_the_index_removal(doc):
    step = _page_step_1(doc)
    at = step.find("git rm -r --cached specs")
    assert at != -1, "step 1 never runs git rm -r --cached specs"
    assert re.search(r"\bcommit", step[at:]), (
        "step 1 never says to commit the git rm -r --cached specs removal"
    )


def test_coming_from_step_1_never_clones_onto_the_files_left_in_place(doc):
    """`git rm --cached` keeps specs/ on disk, so a clone into specs/ right after it fails."""
    step = _page_step_1(doc)
    at = step.find("git rm -r --cached specs")
    after = step[at:]
    clone = re.search(r"clone [^.]*into specs/", after)
    if clone:
        assert re.search(r"\b(aside|rename|move)\b", after[: clone.start()]), (
            "step 1 clones into specs/ while git rm --cached left the files there"
        )
