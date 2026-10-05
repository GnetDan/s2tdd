"""T005: the shared-rule sources, the project pages and the bundle manifest.

Checks `src/shared/*.md`, `src/pages/*.md` and `src/bundle.toml` against
contracts/shared-rules.md, asserting the phrases II-7 lists for each block (literals and listed
phrases through `Doc.missing`, II-5), plus the two repository-wide rules of II-3 that apply to
every source file here: no placeholder token and no R6 old name.
"""

from __future__ import annotations

import re

# II-3's constants (the type home is tools/check.py; tests transcribe them).
COMMANDS = (
    "epic", "specify", "clarify", "plan", "harden", "implement", "verify-done",
    "converge", "pr-review", "close", "next", "foundation-review", "constitution",
)
PLACEHOLDERS = (
    "$ARGUMENTS", "${CLAUDE_PLUGIN_ROOT}", "${CLAUDE_SKILL_DIR}",
    "__SPECKIT_COMMAND_", "{SCRIPT}", "{ARGS}",
)
OLD_NAMES = (r"\.specify/", r"docs/sdd-workflow\.md", r"/speckit-", r"skills/speckit-")

# II-4: exactly these two entries.
BUNDLE_ENTRIES = [
    {
        "source": "pages/README.md",
        "to": ["s2tdd-specify", "s2tdd-epic", "s2tdd-constitution"],
        "as": "pages/README.md",
    },
    {
        "source": "pages/WORKFLOW.md",
        "to": ["s2tdd-specify", "s2tdd-epic", "s2tdd-constitution"],
        "as": "pages/WORKFLOW.md",
    },
]

_COMMAND_REF = re.compile(r"(?<![\w.])/s2tdd-([a-z]+(?:-[a-z]+)*)")


def _assert_clean(d):
    """Every source file: no placeholder token and no R6 old name (raw text)."""
    found = [token for token in PLACEHOLDERS if token in d.text]
    assert not found, f"{d.path.name}: placeholder tokens {found}"
    old = [pattern for pattern in OLD_NAMES if re.search(pattern, d.text)]
    assert not old, f"{d.path.name}: old names matching {old}"


def _assert_in_order(d, *markers):
    """The markers all appear in the raw text, each after the one before it."""
    positions = [d.text.find(marker) for marker in markers]
    assert -1 not in positions, f"missing: {[m for m, p in zip(markers, positions) if p < 0]}"
    assert positions == sorted(set(positions)), f"out of order: {list(zip(markers, positions))}"


def test_feature_resolution(doc):
    d = doc("src/shared/feature-resolution.md")
    _assert_in_order(d, "1. **Named.**", "2. **Branch.**", "3. **Branch number.**", "4. **Ask.**")
    phrases = (
        "git branch --show-current",
        "prefix/",
        "if two directories share the number, ask",
        "never write a pointer file",
    )
    assert not d.missing(*phrases), d.missing(*phrases)
    _assert_clean(d)


def test_epic_resolution(doc):
    d = doc("src/shared/epic-resolution.md")
    _assert_in_order(d, "1. **Named.**", "2. **Single open epic.**", "3. **Ask.**")
    assert not d.missing("specs/epics/<slug>/"), d.missing("specs/epics/<slug>/")
    _assert_clean(d)


def test_worktrees(doc):
    d = doc("src/shared/worktrees.md")
    phrases = ("git worktree list --porcelain", "say so", "first worktree")
    assert not d.missing(*phrases), d.missing(*phrases)
    _assert_clean(d)


def test_closing_step(doc):
    d = doc("src/shared/closing-step.md")
    phrases = ("run /s2tdd-next", "no hook")
    assert not d.missing(*phrases), d.missing(*phrases)
    _assert_clean(d)


def test_first_run_setup(doc):
    d = doc("src/shared/first-run-setup.md")
    phrases = (
        "git remote get-url origin",
        "gh api user --jq .login",
        "git config --get github.user",
        "ask the user once",
        "declines to answer, treat it as foreign",
        "no remote at all",
        "gh repo create",
        "./pages/README.md",
        "./pages/WORKFLOW.md",
        "only when it is missing",
        "never delete or rewrite an existing file",
        "specs/",
        ".sdd-run/",
        "in a foreign repository only, .claude/skills/s2tdd-*/",
        "git status --porcelain",
        "say nothing about setup",
    )
    assert not d.missing(*phrases), d.missing(*phrases)
    assert "sdd-workflow" not in d.text, "the setup block must not name the old workflow page"
    _assert_clean(d)


def test_pages(doc):
    readme = doc("src/pages/README.md")
    workflow = doc("src/pages/WORKFLOW.md")
    for page in (readme, workflow):
        _assert_clean(page)
        named = set(_COMMAND_REF.findall(page.text))
        unknown = sorted(named - set(COMMANDS))
        assert not unknown, f"{page.path.name}: /s2tdd- names that are not commands: {unknown}"
    assert not workflow.missing("specs/constitution.md"), workflow.missing("specs/constitution.md")


def test_bundle(doc):
    import tomllib

    d = doc("src/bundle.toml")
    assert tomllib.loads(d.text) == {"file": BUNDLE_ENTRIES}
