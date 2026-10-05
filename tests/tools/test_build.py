"""Tests for tools/build.py: shared-fence stamping, bundle copies, --check, --only, --root.

Shapes: specs/001-s2tdd-standalone-plugin/contracts/internal-interfaces.md II-1, II-2, II-4 and
contracts/build-and-check.md. Every test builds a small tree under tmp_path and runs the tool
with --root; the repository itself is never built here.
"""

from __future__ import annotations

import re
import subprocess
from collections.abc import Callable
from pathlib import Path

import pytest

OPEN_WORKTREES = "<!-- s2tdd:shared worktrees -->"
OPEN_CLOSING = "<!-- s2tdd:shared closing-step -->"
CLOSE = "<!-- /s2tdd:shared -->"

# Source texts: characters a naive regex replacement or a text-mode write would damage.
WORKTREES_SRC = "Worktree rule one.\n\nA line with $1 and \\1 and \\g<0>.\nTrailing spaces  \nUnicode: caf\u00e9 \u2014 ok\n"
CLOSING_SRC = "Closing step text.\n"
README_SRC = "# Pages README\n\nLine two.\n"
WORKFLOW_SRC = "# Pages WORKFLOW\n\nA table | with | pipes\n"

BUNDLE_TOML = """\
[[file]]
source = "pages/README.md"
to = ["s2tdd-a", "s2tdd-b"]
as = "pages/README.md"

[[file]]
source = "pages/WORKFLOW.md"
to = ["s2tdd-a", "s2tdd-b"]
as = "pages/WORKFLOW.md"
"""

Tool = Callable[..., "subprocess.CompletedProcess[str]"]


def put(path: Path, text: str) -> None:
    """Write text as UTF-8 bytes, never translating newlines."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


def skill_template(name: str, worktrees: str = "", closing: str = "") -> str:
    """A SKILL.md holding both shared fences, with the given text between each pair."""
    return (
        f"---\nname: {name}\ndescription: test skill\n---\n\n"
        f"# {name}\n\nbefore\n\n"
        f"{OPEN_WORKTREES}\n{worktrees}{CLOSE}\n\n"
        f"middle\n\n"
        f"{OPEN_CLOSING}\n{closing}{CLOSE}\n\n"
        f"after\n"
    )


def built_skill(name: str) -> str:
    return skill_template(name, WORKTREES_SRC, CLOSING_SRC)


def make_tree(root: Path, skills: tuple[str, ...] = ("s2tdd-a", "s2tdd-b"), bundle: str = BUNDLE_TOML) -> Path:
    """An unbuilt tree: sources, a bundle, and one skill per name with empty fence pairs."""
    put(root / "src" / "shared" / "worktrees.md", WORKTREES_SRC)
    put(root / "src" / "shared" / "closing-step.md", CLOSING_SRC)
    put(root / "src" / "pages" / "README.md", README_SRC)
    put(root / "src" / "pages" / "WORKFLOW.md", WORKFLOW_SRC)
    put(root / "src" / "bundle.toml", bundle)
    for name in skills:
        put(root / "skills" / name / "SKILL.md", skill_template(name))
    return root


@pytest.fixture
def tree(tmp_path: Path) -> Path:
    return make_tree(tmp_path / "tree")


def build(tool: Tool, root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return tool("build", "--root", str(root), *args)


def output_lines(result: subprocess.CompletedProcess[str]) -> list[str]:
    """stdout and stderr together (the contract does not say which stream carries what)."""
    text = (result.stdout or "") + "\n" + (result.stderr or "")
    return [line.strip().replace("\\", "/") for line in text.splitlines() if line.strip()]


def assert_exit(result: subprocess.CompletedProcess[str], code: int) -> None:
    assert result.returncode == code, (
        f"expected exit {code}, got {result.returncode}\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )


def snapshot(root: Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in sorted(root.rglob("*")) if p.is_file()}


def read(root: Path, rel: str) -> bytes:
    return (root / rel).read_bytes()


def wrote_lines(result: subprocess.CompletedProcess[str]) -> list[str]:
    return [line for line in output_lines(result) if line.startswith("wrote:")]


def stale_lines(result: subprocess.CompletedProcess[str]) -> list[str]:
    return [line for line in output_lines(result) if line.startswith("stale:")]


def has_line(result: subprocess.CompletedProcess[str], pattern: str) -> bool:
    return any(re.fullmatch(pattern, line) for line in output_lines(result))


# --- stamping --------------------------------------------------------------------------------


def test_stamping_replaces_fenced_content_verbatim(tool: Tool, tree: Path) -> None:
    result = build(tool, tree)
    assert_exit(result, 0)
    for name in ("s2tdd-a", "s2tdd-b"):
        assert read(tree, f"skills/{name}/SKILL.md") == built_skill(name).encode("utf-8")


def test_stamping_prints_wrote_for_each_changed_skill(tool: Tool, tree: Path) -> None:
    result = build(tool, tree)
    assert_exit(result, 0)
    wrote = wrote_lines(result)
    for name in ("s2tdd-a", "s2tdd-b"):
        assert any(f"skills/{name}/SKILL.md" in line for line in wrote), wrote


def test_stamping_replaces_stale_content_between_the_markers(tool: Tool, tree: Path) -> None:
    put(tree / "skills/s2tdd-a/SKILL.md", skill_template("s2tdd-a", "old stale text\nmore stale\n", "stale too\n"))
    assert_exit(build(tool, tree), 0)
    assert read(tree, "skills/s2tdd-a/SKILL.md") == built_skill("s2tdd-a").encode("utf-8")


def test_source_missing_its_final_newline_gets_one(tool: Tool, tree: Path) -> None:
    put(tree / "src/shared/closing-step.md", "No final newline")
    assert_exit(build(tool, tree), 0)
    expected = skill_template("s2tdd-a", WORKTREES_SRC, "No final newline\n")
    assert read(tree, "skills/s2tdd-a/SKILL.md") == expected.encode("utf-8")


def test_the_same_block_is_stamped_into_every_skill_that_holds_it(tool: Tool, tmp_path: Path) -> None:
    root = make_tree(tmp_path / "three", skills=("s2tdd-a", "s2tdd-b", "s2tdd-c"))
    assert_exit(build(tool, root), 0)
    for name in ("s2tdd-a", "s2tdd-b", "s2tdd-c"):
        assert read(root, f"skills/{name}/SKILL.md") == built_skill(name).encode("utf-8")


# --- idempotence and line endings ------------------------------------------------------------


def test_a_second_run_changes_nothing(tool: Tool, tree: Path) -> None:
    assert_exit(build(tool, tree), 0)
    before = snapshot(tree)
    second = build(tool, tree)
    assert_exit(second, 0)
    assert snapshot(tree) == before
    assert wrote_lines(second) == []


def test_output_files_are_lf(tool: Tool, tree: Path) -> None:
    assert_exit(build(tool, tree), 0)
    for rel in (
        "skills/s2tdd-a/SKILL.md",
        "skills/s2tdd-b/SKILL.md",
        "skills/s2tdd-a/pages/README.md",
        "skills/s2tdd-a/pages/WORKFLOW.md",
    ):
        assert b"\r" not in read(tree, rel), rel


# --- errors: file:line: ----------------------------------------------------------------------


def test_unknown_block_exits_1_with_file_and_line(tool: Tool, tree: Path) -> None:
    text = skill_template("s2tdd-a").replace("worktrees", "nonesuch", 1)
    put(tree / "skills/s2tdd-a/SKILL.md", text)
    result = build(tool, tree)
    assert_exit(result, 1)
    assert has_line(result, r"skills/s2tdd-a/SKILL\.md:\d+: unknown block 'nonesuch'"), output_lines(result)


def test_unclosed_fence_exits_1_with_file_and_line(tool: Tool, tree: Path) -> None:
    text = f"---\nname: s2tdd-a\ndescription: test skill\n---\n\n# s2tdd-a\n\n{OPEN_WORKTREES}\nsome text\n"
    put(tree / "skills/s2tdd-a/SKILL.md", text)
    result = build(tool, tree)
    assert_exit(result, 1)
    assert has_line(result, r"skills/s2tdd-a/SKILL\.md:\d+: unclosed fence"), output_lines(result)


def test_nested_fence_exits_1_with_file_and_line(tool: Tool, tree: Path) -> None:
    text = (
        "---\nname: s2tdd-a\ndescription: test skill\n---\n\n# s2tdd-a\n\n"
        f"{OPEN_WORKTREES}\n{OPEN_CLOSING}\n{CLOSE}\n{CLOSE}\n"
    )
    put(tree / "skills/s2tdd-a/SKILL.md", text)
    result = build(tool, tree)
    assert_exit(result, 1)
    assert has_line(result, r"skills/s2tdd-a/SKILL\.md:\d+: nested fence"), output_lines(result)


# --- the bundle ------------------------------------------------------------------------------


def test_a_bundle_entry_with_a_missing_source_exits_1(tool: Tool, tree: Path) -> None:
    put(
        tree / "src/bundle.toml",
        '[[file]]\nsource = "pages/absent.md"\nto = ["s2tdd-a"]\nas = "pages/absent.md"\n',
    )
    result = build(tool, tree)
    assert_exit(result, 1)
    assert has_line(result, r"src/bundle\.toml:0: missing source 'pages/absent\.md'"), output_lines(result)


def test_a_to_naming_a_missing_skill_folder_is_skipped_with_exit_0(tool: Tool, tmp_path: Path) -> None:
    bundle = (
        '[[file]]\nsource = "pages/README.md"\n'
        'to = ["s2tdd-a", "s2tdd-constitution"]\nas = "pages/README.md"\n'
    )
    root = make_tree(tmp_path / "skip", skills=("s2tdd-a",), bundle=bundle)
    result = build(tool, root)
    assert_exit(result, 0)
    assert has_line(result, r"skip: s2tdd-constitution \(no skill folder\)"), output_lines(result)
    assert read(root, "skills/s2tdd-a/pages/README.md") == README_SRC.encode("utf-8")
    assert not (root / "skills" / "s2tdd-constitution").exists()


def test_copies_land_at_as_in_each_to_skill(tool: Tool, tmp_path: Path) -> None:
    bundle = (
        '[[file]]\nsource = "pages/README.md"\nto = ["s2tdd-a", "s2tdd-b"]\nas = "pages/README.md"\n\n'
        '[[file]]\nsource = "pages/WORKFLOW.md"\nto = ["s2tdd-a"]\nas = "elsewhere/notes.md"\n'
    )
    root = make_tree(tmp_path / "copies", bundle=bundle)
    result = build(tool, root)
    assert_exit(result, 0)
    assert read(root, "skills/s2tdd-a/pages/README.md") == README_SRC.encode("utf-8")
    assert read(root, "skills/s2tdd-b/pages/README.md") == README_SRC.encode("utf-8")
    assert read(root, "skills/s2tdd-a/elsewhere/notes.md") == WORKFLOW_SRC.encode("utf-8")
    assert not (root / "skills/s2tdd-b/elsewhere/notes.md").exists()
    assert not (root / "skills/s2tdd-a/pages/WORKFLOW.md").exists()
    wrote = wrote_lines(result)
    assert any("skills/s2tdd-a/pages/README.md" in line for line in wrote), wrote


def test_a_changed_source_updates_an_existing_copy(tool: Tool, tree: Path) -> None:
    assert_exit(build(tool, tree), 0)
    put(tree / "src/pages/README.md", "# New README\n")
    assert_exit(build(tool, tree), 0)
    assert read(tree, "skills/s2tdd-a/pages/README.md") == b"# New README\n"
    assert read(tree, "skills/s2tdd-b/pages/README.md") == b"# New README\n"


# --- --check ---------------------------------------------------------------------------------


def test_check_exits_0_on_a_built_tree_and_modifies_nothing(tool: Tool, tree: Path) -> None:
    assert_exit(build(tool, tree), 0)
    before = snapshot(tree)
    result = build(tool, tree, "--check")
    assert_exit(result, 0)
    assert stale_lines(result) == []
    assert snapshot(tree) == before


def test_check_exits_0_on_a_built_tree_with_a_skipped_to(tool: Tool, tmp_path: Path) -> None:
    bundle = (
        '[[file]]\nsource = "pages/README.md"\n'
        'to = ["s2tdd-a", "s2tdd-constitution"]\nas = "pages/README.md"\n'
    )
    root = make_tree(tmp_path / "skipcheck", skills=("s2tdd-a",), bundle=bundle)
    assert_exit(build(tool, root), 0)
    assert_exit(build(tool, root, "--check"), 0)


def test_check_lists_a_stale_block_without_modifying_the_tree(tool: Tool, tree: Path) -> None:
    assert_exit(build(tool, tree), 0)
    put(tree / "skills/s2tdd-a/SKILL.md", skill_template("s2tdd-a", "hand-edited\n", CLOSING_SRC))
    before = snapshot(tree)
    result = build(tool, tree, "--check")
    assert_exit(result, 1)
    assert stale_lines(result) == ["stale: skills/s2tdd-a/SKILL.md (block worktrees)"]
    assert snapshot(tree) == before


def test_check_lists_one_line_per_stale_block_sorted(tool: Tool, tree: Path) -> None:
    # nothing is built yet: both blocks of both skills are stale, and so are the four copies
    before = snapshot(tree)
    result = build(tool, tree, "--check")
    assert_exit(result, 1)
    lines = stale_lines(result)
    for name in ("s2tdd-a", "s2tdd-b"):
        assert f"stale: skills/{name}/SKILL.md (block worktrees)" in lines, lines
        assert f"stale: skills/{name}/SKILL.md (block closing-step)" in lines, lines
    assert len(lines) == len(set(lines))
    assert lines == sorted(lines)
    assert snapshot(tree) == before


def test_check_lists_a_different_copy_and_a_missing_copy(tool: Tool, tree: Path) -> None:
    assert_exit(build(tool, tree), 0)
    put(tree / "skills/s2tdd-a/pages/README.md", "tampered\n")
    (tree / "skills/s2tdd-b/pages/WORKFLOW.md").unlink()
    before = snapshot(tree)
    result = build(tool, tree, "--check")
    assert_exit(result, 1)
    lines = stale_lines(result)
    assert lines == [
        "stale: skills/s2tdd-a/pages/README.md",
        "stale: skills/s2tdd-b/pages/WORKFLOW.md",
    ]
    assert snapshot(tree) == before


def test_check_lists_stale_block_and_stale_copy_together(tool: Tool, tree: Path) -> None:
    assert_exit(build(tool, tree), 0)
    put(tree / "skills/s2tdd-b/SKILL.md", skill_template("s2tdd-b", WORKTREES_SRC, "edited\n"))
    put(tree / "skills/s2tdd-a/pages/WORKFLOW.md", "tampered\n")
    result = build(tool, tree, "--check")
    assert_exit(result, 1)
    assert stale_lines(result) == [
        "stale: skills/s2tdd-a/pages/WORKFLOW.md",
        "stale: skills/s2tdd-b/SKILL.md (block closing-step)",
    ]


# --- --only ----------------------------------------------------------------------------------


def test_only_stamps_and_copies_just_that_skill(tool: Tool, tree: Path) -> None:
    unbuilt_b = read(tree, "skills/s2tdd-b/SKILL.md")
    result = build(tool, tree, "--only", "s2tdd-a")
    assert_exit(result, 0)
    assert read(tree, "skills/s2tdd-a/SKILL.md") == built_skill("s2tdd-a").encode("utf-8")
    assert read(tree, "skills/s2tdd-a/pages/README.md") == README_SRC.encode("utf-8")
    assert read(tree, "skills/s2tdd-b/SKILL.md") == unbuilt_b
    assert not (tree / "skills/s2tdd-b/pages").exists()
    assert not any("s2tdd-b" in line for line in wrote_lines(result))


def test_only_is_repeatable(tool: Tool, tmp_path: Path) -> None:
    root = make_tree(tmp_path / "rep", skills=("s2tdd-a", "s2tdd-b", "s2tdd-c"))
    unbuilt_c = read(root, "skills/s2tdd-c/SKILL.md")
    assert_exit(build(tool, root, "--only", "s2tdd-a", "--only", "s2tdd-b"), 0)
    assert read(root, "skills/s2tdd-a/SKILL.md") == built_skill("s2tdd-a").encode("utf-8")
    assert read(root, "skills/s2tdd-b/SKILL.md") == built_skill("s2tdd-b").encode("utf-8")
    assert read(root, "skills/s2tdd-c/SKILL.md") == unbuilt_c


def test_check_only_reports_just_that_skill(tool: Tool, tree: Path) -> None:
    # both skills are unbuilt
    result = build(tool, tree, "--check", "--only", "s2tdd-a")
    assert_exit(result, 1)
    lines = stale_lines(result)
    assert "stale: skills/s2tdd-a/SKILL.md (block worktrees)" in lines, lines
    assert "stale: skills/s2tdd-a/pages/README.md" in lines, lines
    assert not any("s2tdd-b" in line for line in lines), lines


def test_check_only_leaves_another_skills_staleness_unreported(tool: Tool, tree: Path) -> None:
    assert_exit(build(tool, tree, "--only", "s2tdd-a"), 0)
    before = snapshot(tree)
    only_a = build(tool, tree, "--check", "--only", "s2tdd-a")
    assert_exit(only_a, 0)
    assert stale_lines(only_a) == []
    everything = build(tool, tree, "--check")
    assert_exit(everything, 1)
    lines = stale_lines(everything)
    assert lines and all("s2tdd-b" in line for line in lines), lines
    assert snapshot(tree) == before
