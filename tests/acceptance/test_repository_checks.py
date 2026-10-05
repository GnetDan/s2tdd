"""US5 acceptance tests for the build and the checker (T014; II-1, II-2, II-3, II-5).

Each test runs the tools against a copy of the repository (`repo_copy`), never the repository.
"""

from __future__ import annotations

import shutil
from pathlib import Path

CLOSING_STEP_FENCE = "<!-- s2tdd:shared closing-step -->"
MIGRATION_OPEN = "<!-- s2tdd:migration -->"
MIGRATION_CLOSE = "<!-- /s2tdd:migration -->"


def _require_tool(repo_root: Path, name: str) -> None:
    assert (repo_root / "tools" / f"{name}.py").is_file(), f"tools/{name}.py not found"


def _skills_holding(tree: Path, fence: str) -> list[str]:
    """Names of the skill folders whose SKILL.md holds `fence` as a whole line."""
    names = []
    for skill_md in sorted((tree / "skills").glob("*/SKILL.md")):
        if fence in skill_md.read_text(encoding="utf-8").split("\n"):
            names.append(skill_md.parent.name)
    return names


def _append(tree: Path, relpath: str, text: str) -> int:
    """Append `text` (a block of whole lines) to `relpath`, creating folders and file if
    missing. Returns the 1-based line number of the first appended line."""
    path = tree / relpath
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.is_file() else ""
    if existing and not existing.endswith("\n"):
        existing += "\n"
    first_line = existing.count("\n") + 1
    path.write_bytes((existing + text + "\n").encode("utf-8"))
    return first_line


def test_001_us5_ac1_stale_stamp_fails(repo_root, repo_copy, tool):
    """US5-AC1: **Given** an edit to the shared rules source with the stamped commands not
    rebuilt, **When** CI runs, **Then** it fails and names the commands whose stamped text is
    stale (T05, T08).

    Provenance: 001 spec.md
    """
    _require_tool(repo_root, "build")
    holders = _skills_holding(repo_copy, CLOSING_STEP_FENCE)
    assert holders, "no skill holds a closing-step fence"

    _append(repo_copy, "src/shared/closing-step.md", "An added rule, not yet rebuilt.")
    result = tool("build", "--root", str(repo_copy), "--check")

    assert result.returncode == 1, result.stdout + result.stderr
    lines = result.stdout.splitlines()
    for name in holders:
        expected = f"stale: skills/{name}/SKILL.md (block closing-step)"
        assert expected in lines, f"missing line: {expected}\n{result.stdout}"


def test_001_us5_ac2_bad_frontmatter_fails(repo_root, repo_copy, tool):
    """US5-AC2: **Given** a `SKILL.md` with missing or invalid frontmatter, **When** CI runs,
    **Then** it fails and names the file (T05).

    Provenance: 001 spec.md
    """
    _require_tool(repo_root, "check")
    relpath = "skills/s2tdd-next/SKILL.md"
    path = repo_copy / relpath
    assert path.is_file(), f"{relpath} not found"

    lines = path.read_text(encoding="utf-8").split("\n")
    body = lines
    if lines[0].rstrip() == "---":
        closing = next(i for i in range(1, len(lines)) if lines[i].rstrip() == "---")
        body = lines[closing + 1 :]
    path.write_bytes(("---\nname: [\n---\n" + "\n".join(body)).encode("utf-8"))

    result = tool("check", "--root", str(repo_copy), "--rule", "frontmatter")

    assert result.returncode == 1, result.stdout + result.stderr
    assert relpath in result.stdout, result.stdout


def test_001_ec010_old_names_only_in_marked_passages(repo_root, repo_copy, tool, tmp_path):
    """EC-010: **Given** `.specify/`, `docs/sdd-workflow.md` or a `/speckit-` name in a command,
    **When** CI checks for old names, **Then** it passes when the name sits in a marked passage of
    the migration material and fails, naming the file, anywhere else (FR-022).

    Provenance: 001 spec.md
    """
    _require_tool(repo_root, "check")
    fenced = f"{MIGRATION_OPEN}\n/speckit-x\n{MIGRATION_CLOSE}"
    next_md = "skills/s2tdd-next/SKILL.md"
    plan_md = "skills/s2tdd-plan/SKILL.md"

    def fresh(label: str) -> Path:
        tree = tmp_path / f"case-{label}"
        shutil.copytree(repo_copy, tree)
        return tree

    def old_names(tree: Path):
        return tool("check", "--root", str(tree), "--rule", "old-names")

    # 1. a name inside a migration fence in next passes
    tree = fresh("fenced")
    _append(tree, next_md, fenced)
    result = old_names(tree)
    assert result.returncode == 0, result.stdout + result.stderr

    # 2. the same line outside the fence fails, naming the file and line
    tree = fresh("outside")
    line = _append(tree, next_md, "/speckit-x")
    result = old_names(tree)
    assert result.returncode == 1, result.stdout + result.stderr
    assert f"{next_md}:{line}:" in result.stdout, result.stdout

    # 3. a migration fence in plan (not an allowed file) fails, naming the file
    tree = fresh("wrong-file")
    _append(tree, plan_md, fenced)
    result = old_names(tree)
    assert result.returncode == 1, result.stdout + result.stderr
    assert plan_md in result.stdout, result.stdout
