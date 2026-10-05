"""Unit tests of tools/check.py against small trees under tmp_path (II-3, II-10; T016).

Every test runs the tool with ``--root <tree>`` through the conftest ``tool`` fixture. The
constants below are transcribed from II-3 (the type home is tools/check.py); the tests never
import the tool.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

COMMANDS = ("epic", "specify", "clarify", "plan", "harden", "implement", "verify-done",
            "converge", "pr-review", "close", "next", "foundation-review", "constitution")
PLACEHOLDERS = ("$ARGUMENTS", "${CLAUDE_PLUGIN_ROOT}", "${CLAUDE_SKILL_DIR}",
                "__SPECKIT_COMMAND_", "{SCRIPT}", "{ARGS}")
OLD_NAME_SAMPLES = (".specify/scripts/run.sh", "docs/sdd-workflow.md", "/speckit-plan",
                    "skills/speckit-plan/SKILL.md")  # one per OLD_NAMES pattern (+ a path form)
MIGRATION_FENCE_FILES = ("skills/s2tdd-next/SKILL.md", "skills/s2tdd-implement/SKILL.md",
                         "skills/s2tdd-harden/SKILL.md")
CREDIT_LINE = "<!-- Adapted from github/spec-kit (MIT). -->"
RULES = ("frontmatter", "command-set", "placeholders", "old-names", "bundled-files", "credits",
         "manifests")
DESCRIPTION = "s2tdd: spec to test-driven development."

OPEN = "<!-- s2tdd:migration -->"
CLOSE = "<!-- /s2tdd:migration -->"

LINE = re.compile(r"^(?P<path>[^:]+):(?P<line>\d+): (?P<rule>[a-z-]+): (?P<detail>.+)$")


# ---------------------------------------------------------------- fixtures and helpers


@pytest.fixture
def check(repo_root, tool):
    """Run tools/check.py on a tree. Red while the tool does not exist."""

    def run(root: Path, *args: str):
        assert (repo_root / "tools" / "check.py").is_file(), "tools/check.py not found"
        return tool("check", "--root", str(root), *args)

    return run


def put(root: Path, rel: str, text: str = "") -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def skill_text(name: str, body: str = "Body.\n") -> str:
    return f"---\nname: {name}\ndescription: A command.\n---\n{body}"


def agent_text(name: str, extra: str = "model: sonnet\neffort: medium\n") -> str:
    return f"---\nname: {name}\ndescription: An agent.\n{extra}---\nBody.\n"


def put_skill(root: Path, command: str, body: str = "Body.\n") -> Path:
    return put(root, f"skills/s2tdd-{command}/SKILL.md", skill_text(f"s2tdd-{command}", body))


def put_manifests(root: Path) -> None:
    put(root, ".claude-plugin/plugin.json",
        json.dumps({"name": "s2tdd", "description": DESCRIPTION}))
    put(root, ".claude-plugin/marketplace.json", json.dumps({
        "name": "s2tdd",
        "owner": {"name": "acme"},
        "plugins": [{"name": "s2tdd", "source": "./", "description": DESCRIPTION}],
    }))


def put_license(root: Path, registry: tuple[str, ...] = ()) -> None:
    lines = ["MIT License", "", "These files are forked or derived from github/spec-kit, and",
             f"each carries the line {CREDIT_LINE}:", ""]
    lines += [f"- {path}" for path in registry]
    put(root, "LICENSE", "\n".join(lines) + "\n")


def clean_tree(root: Path) -> Path:
    """A tree on which every rule passes: 13 commands, an agent, a source, manifests, LICENSE."""
    for command in COMMANDS:
        put_skill(root, command)
    put(root, "skills/s2tdd-plan/plan-template.md", f"{CREDIT_LINE}\n# Plan\n")
    put(root, "agents/packet-cheap.md", agent_text("packet-cheap"))
    put(root, "src/shared/worktrees.md", "Use worktrees.\n")
    put_manifests(root)
    put_license(root, ("skills/s2tdd-plan/plan-template.md",))
    return root


def output(result) -> str:
    return result.stdout + result.stderr


def failures(result, rule: str | None = None) -> list[dict[str, str]]:
    """Parse every output line as `path:line: rule: detail`; fail if one does not parse."""
    parsed = []
    for line in output(result).splitlines():
        if not line.strip():
            continue
        match = LINE.match(line)
        assert match, f"not a `path:line: rule: detail` line: {line!r}"
        parsed.append(match.groupdict())
    if rule is not None:
        assert all(f["rule"] == rule for f in parsed), output(result)
    return parsed


def assert_fails(result, rule: str, path: str | None = None) -> list[dict[str, str]]:
    assert result.returncode == 1, output(result)
    found = failures(result, rule)
    assert found, "exit 1 with no failure line"
    if path is not None:
        assert any(f["path"] == path for f in found), output(result)
    return found


def assert_passes(result) -> None:
    assert result.returncode == 0, output(result)
    assert result.stdout == "" and result.stderr == "", output(result)


def paths(found: list[dict[str, str]]) -> set[str]:
    return {f["path"] for f in found}


# ---------------------------------------------------------------- output format, exit codes


def test_success_prints_nothing(tmp_path, check):
    assert_passes(check(clean_tree(tmp_path)))


def test_failure_line_has_relative_forward_slash_path_line_rule_detail(tmp_path, check):
    clean_tree(tmp_path)
    put(tmp_path, "skills/s2tdd-plan/pages/page.md", "one\ntwo\nthree uses $ARGUMENTS\n")
    result = check(tmp_path)
    found = assert_fails(result, "placeholders")
    assert len(found) == 1, output(result)
    assert found[0]["path"] == "skills/s2tdd-plan/pages/page.md"
    assert found[0]["line"] == "3"
    assert str(tmp_path) not in output(result)
    assert "\\" not in output(result)


def test_one_line_per_failure(tmp_path, check):
    clean_tree(tmp_path)
    put(tmp_path, "src/a.md", "$ARGUMENTS\n")
    put(tmp_path, "src/b.md", "ok\n{SCRIPT}\n")
    found = assert_fails(check(tmp_path, "--rule", "placeholders"), "placeholders")
    assert sorted((f["path"], f["line"]) for f in found) == [("src/a.md", "1"), ("src/b.md", "2")]


def test_missing_command_folder_reports_line_zero(tmp_path, check):
    clean_tree(tmp_path)
    (tmp_path / "skills" / "s2tdd-converge" / "SKILL.md").unlink()
    (tmp_path / "skills" / "s2tdd-converge").rmdir()
    found = assert_fails(check(tmp_path, "--rule", "command-set"), "command-set")
    assert all(f["line"] == "0" for f in found)


def test_missing_manifest_reports_line_zero(tmp_path, check):
    clean_tree(tmp_path)
    (tmp_path / ".claude-plugin" / "plugin.json").unlink()
    found = assert_fails(check(tmp_path, "--rule", "manifests"), "manifests")
    assert all(f["line"] == "0" for f in found)


# ---------------------------------------------------------------- --rule


def test_unknown_rule_exits_2(tmp_path, check):
    result = check(clean_tree(tmp_path), "--rule", "no-such-rule")
    assert result.returncode == 2
    assert result.stdout == ""


@pytest.mark.parametrize("rule", RULES)
def test_each_rule_name_is_accepted_and_passes_on_a_clean_tree(tmp_path, check, rule):
    assert_passes(check(clean_tree(tmp_path), "--rule", rule))


def test_no_rule_runs_all_seven(tmp_path, check):
    # one defect per rule: 12 commands plus an extra folder, and no manifests
    for command in COMMANDS[:-1]:
        put_skill(tmp_path, command)
    put(tmp_path, "skills/s2tdd-bogus/SKILL.md", "no frontmatter here\n")  # frontmatter
    put(tmp_path, "src/placeholder.md", "$ARGUMENTS\n")  # placeholders
    put(tmp_path, "src/old.md", "see .specify/ here\n")  # old-names
    put_skill(tmp_path, "close", "See ./missing.md\n")  # bundled-files
    put_license(tmp_path, ("skills/s2tdd-plan/plan-template.md",))  # credits: the file is absent
    result = check(tmp_path)
    assert result.returncode == 1
    assert {f["rule"] for f in failures(result)} == set(RULES)


def test_no_rule_reports_command_set_too(tmp_path, check):
    put_skill(tmp_path, "plan")
    put_manifests(tmp_path)
    put_license(tmp_path)
    found = assert_fails(check(tmp_path), "command-set")
    assert all(f["rule"] == "command-set" for f in found)


def test_rule_limits_which_rules_run(tmp_path, check):
    clean_tree(tmp_path)
    put(tmp_path, "src/bad.md", "$ARGUMENTS and .specify/\n")
    only_placeholders = check(tmp_path, "--rule", "placeholders")
    assert_fails(only_placeholders, "placeholders")
    only_old_names = check(tmp_path, "--rule", "old-names")
    assert_fails(only_old_names, "old-names")
    assert_passes(check(tmp_path, "--rule", "frontmatter"))


def test_rule_is_repeatable(tmp_path, check):
    clean_tree(tmp_path)
    put(tmp_path, "src/bad.md", "$ARGUMENTS and .specify/\n")
    result = check(tmp_path, "--rule", "placeholders", "--rule", "old-names")
    assert result.returncode == 1
    assert {f["rule"] for f in failures(result)} == {"placeholders", "old-names"}


# ---------------------------------------------------------------- --only


def test_only_limits_per_file_rules_to_the_named_paths(tmp_path, check):
    clean_tree(tmp_path)
    put(tmp_path, "skills/s2tdd-plan/pages/a.md", "$ARGUMENTS\n")
    put(tmp_path, "skills/s2tdd-next/pages/b.md", "$ARGUMENTS\n")
    result = check(tmp_path, "--only", "skills/s2tdd-plan")
    found = assert_fails(result, "placeholders")
    assert paths(found) == {"skills/s2tdd-plan/pages/a.md"}


def test_only_is_repeatable(tmp_path, check):
    clean_tree(tmp_path)
    put(tmp_path, "skills/s2tdd-plan/pages/a.md", "$ARGUMENTS\n")
    put(tmp_path, "skills/s2tdd-next/pages/b.md", "$ARGUMENTS\n")
    put(tmp_path, "skills/s2tdd-close/pages/c.md", "$ARGUMENTS\n")
    result = check(tmp_path, "--only", "skills/s2tdd-plan", "--only", "skills/s2tdd-next")
    found = assert_fails(result, "placeholders")
    assert paths(found) == {"skills/s2tdd-plan/pages/a.md", "skills/s2tdd-next/pages/b.md"}


@pytest.mark.parametrize("area, bad_path, other_path", [
    ("agents", "agents/packet-cheap.md", "src/other.md"),
    ("src", "src/bad.md", "agents/packet-medium.md"),
])
def test_only_accepts_agents_and_src(tmp_path, check, area, bad_path, other_path):
    clean_tree(tmp_path)
    stem = Path(bad_path).stem
    bad_text = agent_text(stem) if bad_path.startswith("agents/") else ""
    put(tmp_path, bad_path, bad_text + "$ARGUMENTS\n")
    put(tmp_path, other_path, "$ARGUMENTS\n")
    found = assert_fails(check(tmp_path, "--only", area), "placeholders")
    assert paths(found) == {bad_path}


def test_only_limits_frontmatter_to_the_named_skill(tmp_path, check):
    clean_tree(tmp_path)
    put(tmp_path, "skills/s2tdd-plan/SKILL.md", "no frontmatter\n")
    put(tmp_path, "skills/s2tdd-next/SKILL.md", "no frontmatter\n")
    found = assert_fails(check(tmp_path, "--only", "skills/s2tdd-next", "--rule", "frontmatter"),
                         "frontmatter")
    assert paths(found) == {"skills/s2tdd-next/SKILL.md"}


def test_only_skips_the_repository_wide_rules(tmp_path, check):
    # no 13 commands, no manifests, a LICENSE whose registry names a file that does not exist
    put_skill(tmp_path, "plan")
    put_license(tmp_path, ("skills/s2tdd-plan/plan-template.md",))
    broken = check(tmp_path)
    assert {f["rule"] for f in failures(broken)} >= {"command-set", "manifests", "credits"}
    assert_passes(check(tmp_path, "--only", "skills/s2tdd-plan"))


def test_only_with_rule_runs_only_that_rule_under_the_path(tmp_path, check):
    clean_tree(tmp_path)
    put(tmp_path, "src/bad.md", "$ARGUMENTS and .specify/\n")
    found = assert_fails(check(tmp_path, "--only", "src", "--rule", "old-names"), "old-names")
    assert paths(found) == {"src/bad.md"}


# ---------------------------------------------------------------- frontmatter


def test_frontmatter_passes_for_a_skill_and_an_agent(tmp_path, check):
    put_skill(tmp_path, "plan")
    put(tmp_path, "skills/s2tdd-next/SKILL.md",
        "---\nname: s2tdd-next\ndescription: A command.\nargument-hint: \"[x]\"\n---\nBody.\n")
    put(tmp_path, "agents/packet-cheap.md", agent_text("packet-cheap"))
    assert_passes(check(tmp_path, "--rule", "frontmatter"))


@pytest.mark.parametrize("text", [
    "# Plan\nno frontmatter at all\n",
    "\n---\nname: s2tdd-plan\ndescription: A command.\n---\nBody.\n",  # does not start with ---
    "---\nname: s2tdd-plan\ndescription: A command.\nBody never closes the block.\n",
    "---\nname: [unclosed\ndescription: A command.\n---\nBody.\n",  # YAML does not parse
    "---\ndescription: A command.\n---\nBody.\n",  # no name
    "---\nname: s2tdd-plan\n---\nBody.\n",  # no description
    "---\nname: s2tdd-plan\ndescription:\n---\nBody.\n",  # empty description
    "---\nname:\ndescription: A command.\n---\nBody.\n",  # empty name
    "---\nname: s2tdd-other\ndescription: A command.\n---\nBody.\n",  # name != folder
], ids=["none", "late-start", "unclosed", "bad-yaml", "no-name", "no-description",
        "empty-description", "empty-name", "name-not-folder"])
def test_frontmatter_fails_for_a_skill(tmp_path, check, text):
    put(tmp_path, "skills/s2tdd-plan/SKILL.md", text)
    assert_fails(check(tmp_path, "--rule", "frontmatter"), "frontmatter",
                 "skills/s2tdd-plan/SKILL.md")


@pytest.mark.parametrize("name, extra", [
    ("packet-cheap", "effort: medium\n"),  # no model
    ("packet-cheap", "model: sonnet\n"),  # no effort
    ("packet-cheap", "model:\neffort: medium\n"),  # empty model
    ("packet-medium", "model: sonnet\neffort: medium\n"),  # name != file stem
], ids=["no-model", "no-effort", "empty-model", "name-not-stem"])
def test_frontmatter_fails_for_an_agent(tmp_path, check, name, extra):
    put(tmp_path, "agents/packet-cheap.md", agent_text(name, extra))
    assert_fails(check(tmp_path, "--rule", "frontmatter"), "frontmatter",
                 "agents/packet-cheap.md")


def test_frontmatter_agent_without_frontmatter_fails(tmp_path, check):
    put(tmp_path, "agents/packet-cheap.md", "Just a body.\n")
    assert_fails(check(tmp_path, "--rule", "frontmatter"), "frontmatter",
                 "agents/packet-cheap.md")


def test_frontmatter_a_skill_needs_no_model_or_effort(tmp_path, check):
    put_skill(tmp_path, "plan")
    assert_passes(check(tmp_path, "--rule", "frontmatter"))


# ---------------------------------------------------------------- command-set


def test_command_set_passes_for_exactly_the_13(tmp_path, check):
    for command in COMMANDS:
        put_skill(tmp_path, command)
    assert_passes(check(tmp_path, "--rule", "command-set"))


def test_command_set_fails_naming_the_missing_command(tmp_path, check):
    for command in COMMANDS:
        if command != "verify-done":
            put_skill(tmp_path, command)
    found = assert_fails(check(tmp_path, "--rule", "command-set"), "command-set")
    assert any("s2tdd-verify-done" in f["detail"] for f in found)


def test_command_set_fails_naming_the_extra_folder(tmp_path, check):
    for command in COMMANDS:
        put_skill(tmp_path, command)
    put(tmp_path, "skills/s2tdd-bogus/SKILL.md", skill_text("s2tdd-bogus"))
    found = assert_fails(check(tmp_path, "--rule", "command-set"), "command-set")
    assert any("s2tdd-bogus" in f["detail"] for f in found)


def test_command_set_fails_for_a_folder_without_the_prefix(tmp_path, check):
    for command in COMMANDS:
        put_skill(tmp_path, command)
    put(tmp_path, "skills/plan/SKILL.md", skill_text("plan"))
    found = assert_fails(check(tmp_path, "--rule", "command-set"), "command-set")
    assert any("plan" in f["detail"] for f in found)


def test_command_set_names_missing_and_extra_together(tmp_path, check):
    for command in COMMANDS:
        if command != "epic":
            put_skill(tmp_path, command)
    put(tmp_path, "skills/s2tdd-bogus/SKILL.md", skill_text("s2tdd-bogus"))
    found = assert_fails(check(tmp_path, "--rule", "command-set"), "command-set")
    detail = " ".join(f["detail"] for f in found)
    assert "s2tdd-epic" in detail and "s2tdd-bogus" in detail


# ---------------------------------------------------------------- placeholders


PLACEHOLDER_FILES = ("skills/s2tdd-plan/SKILL.md", "skills/s2tdd-plan/pages/page.md",
                     "agents/packet-cheap.md", "src/shared/worktrees.md", "src/pages/README.md")


@pytest.mark.parametrize("rel", PLACEHOLDER_FILES)
@pytest.mark.parametrize("token", PLACEHOLDERS)
def test_placeholders_fail_for_each_token_in_each_scanned_tree(tmp_path, check, token, rel):
    put(tmp_path, rel, f"one\ntwo\nthree\nfour\nfive\nsix {token} here\n")
    found = assert_fails(check(tmp_path, "--rule", "placeholders"), "placeholders", rel)
    assert [f["line"] for f in found if f["path"] == rel] == ["6"]


def test_placeholders_pass_on_plain_text_and_near_misses(tmp_path, check):
    text = ("ARGUMENTS and CLAUDE_PLUGIN_ROOT are just words.\n"
            "$ARG, ${CLAUDE_PLUGIN}, SCRIPT, {ARG}, {SCRIPTS}, __SPECKIT_COMMAND.\n")
    for rel in PLACEHOLDER_FILES:
        put(tmp_path, rel, text)
    assert_passes(check(tmp_path, "--rule", "placeholders"))


def test_placeholders_and_old_names_ignore_files_outside_the_scanned_trees(tmp_path, check):
    clean_tree(tmp_path)
    text = "$ARGUMENTS {SCRIPT} .specify/ docs/sdd-workflow.md /speckit-plan\n"
    put(tmp_path, "README.md", text)
    put(tmp_path, "MIGRATING.md", text)
    put(tmp_path, "docs/coming-from-spec-kit.md", text)
    put(tmp_path, "tests/notes.md", text)
    assert_passes(check(tmp_path, "--rule", "placeholders", "--rule", "old-names"))


# ---------------------------------------------------------------- old-names: patterns


OLD_NAME_FILES = ("skills/s2tdd-plan/SKILL.md", "agents/packet-cheap.md", "src/shared/worktrees.md")


@pytest.mark.parametrize("rel", OLD_NAME_FILES)
@pytest.mark.parametrize("sample", OLD_NAME_SAMPLES)
def test_old_names_fail_outside_a_fence_for_each_pattern(tmp_path, check, sample, rel):
    put(tmp_path, rel, f"one\ntwo\nthree\nfour\nfive\nsix uses {sample} here\n")
    found = assert_fails(check(tmp_path, "--rule", "old-names"), "old-names", rel)
    assert "6" in [f["line"] for f in found if f["path"] == rel]


@pytest.mark.parametrize("text", [
    "/SPECKIT-plan and .SPECIFY/ and DOCS/SDD-WORKFLOW.MD",  # case-sensitive
    "Xspecify/ and docs/sdd-workflowXmd",  # the dots are literal
    "specify/ and /s2tdd-specify and skills/s2tdd-plan and sdd-workflow",
    "speckit and speckit-plan without a slash",
], ids=["uppercase", "dot-is-literal", "new-names", "bare-speckit"])
def test_old_names_pass_for_near_misses(tmp_path, check, text):
    for rel in OLD_NAME_FILES:
        put(tmp_path, rel, f"intro\n{text}\n")
    assert_passes(check(tmp_path, "--rule", "old-names"))


# ---------------------------------------------------------------- old-names: fences


def fenced(*inside: str, before: tuple[str, ...] = ("Intro.",), after: tuple[str, ...] = ()) -> str:
    lines = [*before, OPEN, *inside, CLOSE, *after]
    return "\n".join(lines) + "\n"


def put_fenced(root: Path, rel: str, body: str) -> None:
    name = rel.split("/")[1] if rel.startswith("skills/") else "agent"
    put(root, rel, f"---\nname: {name}\ndescription: A command.\n---\n{body}")


@pytest.mark.parametrize("rel", MIGRATION_FENCE_FILES)
def test_old_name_inside_a_fence_passes_in_each_allowed_file(tmp_path, check, rel):
    put_fenced(tmp_path, rel, fenced("Rewrite .specify/ to specs/.", "And /speckit-plan too."))
    assert_passes(check(tmp_path, "--rule", "old-names"))


def test_two_fences_in_one_allowed_file_pass(tmp_path, check):
    body = fenced("old .specify/") + "Between.\n" + fenced("old /speckit-plan", before=())
    put_fenced(tmp_path, MIGRATION_FENCE_FILES[0], body)
    assert_passes(check(tmp_path, "--rule", "old-names"))


def test_old_name_after_the_fence_closes_fails_on_its_line(tmp_path, check):
    rel = MIGRATION_FENCE_FILES[0]
    body = fenced("old .specify/", after=("Then a stray docs/sdd-workflow.md.",))
    put_fenced(tmp_path, rel, body)
    found = assert_fails(check(tmp_path, "--rule", "old-names"), "old-names", rel)
    # frontmatter is 4 lines; intro 5, open 6, inside 7, close 8, stray 9
    assert [f["line"] for f in found if f["path"] == rel] == ["9"]


def test_old_name_before_the_fence_opens_fails_on_its_line(tmp_path, check):
    rel = MIGRATION_FENCE_FILES[0]
    put_fenced(tmp_path, rel, fenced("old .specify/", before=("Stray /speckit-plan here.",)))
    found = assert_fails(check(tmp_path, "--rule", "old-names"), "old-names", rel)
    assert [f["line"] for f in found if f["path"] == rel] == ["5"]


@pytest.mark.parametrize("rel", ["skills/s2tdd-plan/SKILL.md", "src/shared/worktrees.md",
                                 "agents/packet-cheap.md", "skills/s2tdd-epic/pages/page.md"])
def test_fence_outside_next_implement_harden_fails(tmp_path, check, rel):
    put_fenced(tmp_path, rel, fenced("old .specify/ inside the fence"))
    assert_fails(check(tmp_path, "--rule", "old-names"), "old-names", rel)


def test_unclosed_fence_fails(tmp_path, check):
    rel = MIGRATION_FENCE_FILES[0]
    put_fenced(tmp_path, rel, f"Intro.\n{OPEN}\nold .specify/\nand more text\n")
    assert_fails(check(tmp_path, "--rule", "old-names"), "old-names", rel)


def test_unopened_fence_fails(tmp_path, check):
    rel = MIGRATION_FENCE_FILES[0]
    put_fenced(tmp_path, rel, f"Intro.\nold text without an old name\n{CLOSE}\nMore.\n")
    assert_fails(check(tmp_path, "--rule", "old-names"), "old-names", rel)


def test_unopened_fence_after_a_good_fence_fails(tmp_path, check):
    rel = MIGRATION_FENCE_FILES[0]
    put_fenced(tmp_path, rel, fenced("old .specify/") + f"{CLOSE}\n")
    assert_fails(check(tmp_path, "--rule", "old-names"), "old-names", rel)


def test_nested_fence_fails(tmp_path, check):
    rel = MIGRATION_FENCE_FILES[0]
    put_fenced(tmp_path, rel,
               f"Intro.\n{OPEN}\nold .specify/\n{OPEN}\nold /speckit-plan\n{CLOSE}\n{CLOSE}\n")
    assert_fails(check(tmp_path, "--rule", "old-names"), "old-names", rel)


def test_empty_fence_fails(tmp_path, check):
    rel = MIGRATION_FENCE_FILES[0]
    put_fenced(tmp_path, rel, fenced())
    assert_fails(check(tmp_path, "--rule", "old-names"), "old-names", rel)


def test_fence_holding_only_prose_fails(tmp_path, check):
    rel = MIGRATION_FENCE_FILES[1]
    put_fenced(tmp_path, rel, fenced("Just prose,", "", "no old name at all."))
    assert_fails(check(tmp_path, "--rule", "old-names"), "old-names", rel)


def test_one_empty_fence_among_good_ones_fails(tmp_path, check):
    rel = MIGRATION_FENCE_FILES[2]
    put_fenced(tmp_path, rel, fenced("old .specify/") + fenced("nothing here", before=()))
    assert_fails(check(tmp_path, "--rule", "old-names"), "old-names", rel)


# ---------------------------------------------------------------- bundled-files


def put_skill_lines(root: Path, command: str, line: str) -> None:
    put_skill(root, command, f"one\ntwo\nthree\n{line}\nfive\n")  # the line is file line 8


def test_bundled_files_pass_for_an_existing_file(tmp_path, check):
    put_skill_lines(tmp_path, "specify", "Read ./pages/README.md and ./spec-template.md.")
    put(tmp_path, "skills/s2tdd-specify/pages/README.md", "x\n")
    put(tmp_path, "skills/s2tdd-specify/spec-template.md", "x\n")
    assert_passes(check(tmp_path, "--rule", "bundled-files"))


def test_bundled_files_fail_for_a_missing_file_on_its_line(tmp_path, check):
    put_skill_lines(tmp_path, "specify", "Read ./pages/missing.md here.")
    found = assert_fails(check(tmp_path, "--rule", "bundled-files"), "bundled-files",
                         "skills/s2tdd-specify/SKILL.md")
    assert [f["line"] for f in found] == ["8"]


def test_bundled_files_fail_when_the_file_is_in_another_skill_folder(tmp_path, check):
    put_skill_lines(tmp_path, "specify", "Read ./pages/README.md here.")
    put(tmp_path, "skills/s2tdd-epic/pages/README.md", "x\n")
    assert_fails(check(tmp_path, "--rule", "bundled-files"), "bundled-files",
                 "skills/s2tdd-specify/SKILL.md")


@pytest.mark.parametrize("line", [
    "Read ../s2tdd-epic/SKILL.md here.",
    "Read ../shared/worktrees.md here.",
    "Go to ../.. and look.",
], ids=["sibling-skill", "shared", "bare-parent"])
def test_bundled_files_fail_for_a_parent_path(tmp_path, check, line):
    put_skill_lines(tmp_path, "specify", line)
    found = assert_fails(check(tmp_path, "--rule", "bundled-files"), "bundled-files",
                         "skills/s2tdd-specify/SKILL.md")
    assert "8" in [f["line"] for f in found]


@pytest.mark.parametrize("line", [
    "Look under ./specs for the feature.",
    "Look under ./specs/ for the feature.",
    "Look under ./specs/004-csv-export and ./specs/acme-notes",
    "Run it from ./ and see.",
], ids=["no-extension", "trailing-slash", "no-extension-nested", "bare-dot-slash"])
def test_bundled_files_ignore_a_path_without_an_extension(tmp_path, check, line):
    put_skill_lines(tmp_path, "specify", line)
    assert_passes(check(tmp_path, "--rule", "bundled-files"))


def test_bundled_files_only_scan_skill_md(tmp_path, check):
    put_skill(tmp_path, "specify")
    put(tmp_path, "skills/s2tdd-specify/pages/README.md", "See ./nothing.md and ../x.md\n")
    put(tmp_path, "skills/s2tdd-specify/spec-template.md", "See ./nothing.md and ../x.md\n")
    assert_passes(check(tmp_path, "--rule", "bundled-files"))


def test_bundled_files_pass_for_a_nested_existing_file(tmp_path, check):
    put_skill_lines(tmp_path, "constitution", "Use ./pages/deep/guide.md here.")
    put(tmp_path, "skills/s2tdd-constitution/pages/deep/guide.md", "x\n")
    assert_passes(check(tmp_path, "--rule", "bundled-files"))


# ---------------------------------------------------------------- credits


REGISTRY = ("skills/s2tdd-plan/SKILL.md", "skills/s2tdd-plan/plan-template.md")


def credited_tree(root: Path) -> None:
    put(root, "skills/s2tdd-plan/SKILL.md",
        f"---\nname: s2tdd-plan\ndescription: A command.\n---\n{CREDIT_LINE}\nBody.\n")
    put(root, "skills/s2tdd-plan/plan-template.md", f"{CREDIT_LINE}\n# Plan\n")
    put_license(root, REGISTRY)


def test_credits_pass_when_registry_and_credit_lines_agree(tmp_path, check):
    credited_tree(tmp_path)
    assert_passes(check(tmp_path, "--rule", "credits"))


def test_credits_pass_with_an_empty_registry_and_no_credited_file(tmp_path, check):
    put_skill(tmp_path, "plan")
    put_license(tmp_path)
    assert_passes(check(tmp_path, "--rule", "credits"))


def test_credits_fail_when_a_registry_path_does_not_exist(tmp_path, check):
    credited_tree(tmp_path)
    (tmp_path / "skills/s2tdd-plan/plan-template.md").unlink()
    result = check(tmp_path, "--rule", "credits")
    assert_fails(result, "credits")
    assert "skills/s2tdd-plan/plan-template.md" in output(result)


def test_credits_fail_when_a_registry_file_lacks_the_credit_line(tmp_path, check):
    credited_tree(tmp_path)
    put(tmp_path, "skills/s2tdd-plan/plan-template.md", "# Plan without a credit\n")
    result = check(tmp_path, "--rule", "credits")
    assert_fails(result, "credits")
    assert "skills/s2tdd-plan/plan-template.md" in output(result)


@pytest.mark.parametrize("rel", ["skills/s2tdd-clarify/SKILL.md", "skills/s2tdd-clarify/x.md",
                                 "agents/packet-cheap.md"])
def test_credits_fail_when_a_credited_file_is_not_in_the_registry(tmp_path, check, rel):
    credited_tree(tmp_path)
    put(tmp_path, rel, f"{CREDIT_LINE}\nBody.\n")
    result = check(tmp_path, "--rule", "credits")
    assert_fails(result, "credits")
    assert rel in output(result)


def test_credits_ignore_lines_that_are_not_registry_entries(tmp_path, check):
    credited_tree(tmp_path)
    license_text = (tmp_path / "LICENSE").read_text(encoding="utf-8")
    put(tmp_path, "LICENSE", license_text + "\n- README.md\n- docs/missing.md\n"
        "Some prose naming skills/s2tdd-gone/SKILL.md without a dash.\n")
    assert_passes(check(tmp_path, "--rule", "credits"))


def test_credits_count_the_license_only_for_its_registry(tmp_path, check):
    # the LICENSE itself quotes the credit line and is not a credited file
    credited_tree(tmp_path)
    assert CREDIT_LINE in (tmp_path / "LICENSE").read_text(encoding="utf-8")
    assert_passes(check(tmp_path, "--rule", "credits"))


# ---------------------------------------------------------------- manifests


def test_manifests_pass_for_a_matching_pair(tmp_path, check):
    put_manifests(tmp_path)
    assert_passes(check(tmp_path, "--rule", "manifests"))


@pytest.mark.parametrize("missing", ["plugin.json", "marketplace.json"])
def test_manifests_fail_for_a_missing_file(tmp_path, check, missing):
    put_manifests(tmp_path)
    (tmp_path / ".claude-plugin" / missing).unlink()
    assert_fails(check(tmp_path, "--rule", "manifests"), "manifests")


@pytest.mark.parametrize("name", ["plugin.json", "marketplace.json"])
def test_manifests_fail_for_a_file_that_is_not_json(tmp_path, check, name):
    put_manifests(tmp_path)
    put(tmp_path, f".claude-plugin/{name}", "{ not json")
    assert_fails(check(tmp_path, "--rule", "manifests"), "manifests")


def rewrite(root: Path, name: str, change) -> None:
    path = root / ".claude-plugin" / name
    data = json.loads(path.read_text(encoding="utf-8"))
    change(data)
    path.write_text(json.dumps(data), encoding="utf-8", newline="\n")


@pytest.mark.parametrize("manifest, change", [
    ("plugin.json", lambda d: d.update(name="other")),
    ("marketplace.json", lambda d: d.update(name="other")),
    ("marketplace.json", lambda d: d["plugins"][0].update(name="other")),
    ("marketplace.json", lambda d: d["plugins"][0].update(source="./plugin")),
    ("marketplace.json", lambda d: d["plugins"][0].update(source="s2tdd")),
    ("marketplace.json", lambda d: d["plugins"].append(
        {"name": "other", "source": "./other", "description": DESCRIPTION})),
    ("marketplace.json", lambda d: d.update(plugins=[])),
    ("plugin.json", lambda d: d.update(description="A different description.")),
    ("marketplace.json", lambda d: d["plugins"][0].update(description="A different one.")),
], ids=["plugin-name", "marketplace-name", "marketplace-plugin-name", "source-subfolder",
        "source-not-dot-slash", "two-plugins", "no-plugin", "plugin-description-differs",
        "marketplace-description-differs"])
def test_manifests_fail_for_each_mismatch(tmp_path, check, manifest, change):
    put_manifests(tmp_path)
    rewrite(tmp_path, manifest, change)
    assert_fails(check(tmp_path, "--rule", "manifests"), "manifests")
