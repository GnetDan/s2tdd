"""T062: the copy-beside-plugin Watch out item of `skills/s2tdd-next/SKILL.md` (US4, R5).

Pins the item's literals and listed phrases through `Doc.missing` (II-5). Every test first
requires `claude plugin list --json` itself: without the item none of the rest can hold, and
that is the reason these fail until T064.
"""

from __future__ import annotations

import re

SKILL = "s2tdd-next"
PLUGIN_LIST = "claude plugin list --json"
COPY_DIR = ".claude/skills/s2tdd-"
INSTALL_RECORDS = "~/.claude/plugins/installed_plugins.json"
USER_SETTINGS = "~/.claude/settings.json"


def _has_the_item(d):
    assert not d.missing(PLUGIN_LIST), f"`{PLUGIN_LIST}` is missing from the command"


def test_runs_the_plugin_list_when_a_copy_exists(skill):
    d = skill(SKILL)
    _has_the_item(d)
    assert not d.missing(COPY_DIR), d.missing(COPY_DIR)


def test_looks_for_an_enabled_s2tdd_id(skill):
    d = skill(SKILL)
    _has_the_item(d)
    assert not d.missing("s2tdd@", "enabled"), d.missing("s2tdd@", "enabled")


def test_falls_back_to_the_install_records_and_enabled_plugins(skill):
    d = skill(SKILL)
    _has_the_item(d)
    phrases = (INSTALL_RECORDS, "enabledPlugins", USER_SETTINGS)
    assert not d.missing(*phrases), d.missing(*phrases)


def test_names_the_copy_under_watch_out_and_says_its_commands_run(skill):
    d = skill(SKILL)
    _has_the_item(d)
    phrases = ("watch out", "its commands are the ones that run")
    assert not d.missing(*phrases), d.missing(*phrases)


def test_says_so_and_lists_the_copy_when_it_cannot_tell(skill):
    d = skill(SKILL)
    _has_the_item(d)
    pattern = r"(could not|couldn't|can't|cannot|unable to) tell"
    assert re.search(pattern, d.flat), "no statement that it could not tell"
    assert not d.missing("lists the copy"), d.missing("lists the copy")
