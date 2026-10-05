"""US5 acceptance tests for the release package: LICENSE registry and product name
(T014; II-3, II-10, II-16).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

CREDIT_LINE = "<!-- Adapted from github/spec-kit (MIT). -->"
DESCRIPTION = (
    "s2tdd: spec to test-driven development — a spec drives the build, "
    "and the tests it leaves are the spec that survives."
)
REGISTRY_LINE = re.compile(r"^- ((skills|agents)/\S+)$")
OLD_PRODUCT_NAME = re.compile(r"(?<!sdd-)tests-as-spec")
REQUIRED_REGISTRY = (
    "skills/s2tdd-specify/SKILL.md",
    "skills/s2tdd-specify/spec-template.md",
    "skills/s2tdd-clarify/SKILL.md",
    "skills/s2tdd-plan/SKILL.md",
    "skills/s2tdd-plan/plan-template.md",
    "skills/s2tdd-harden/SKILL.md",
    "skills/s2tdd-harden/tasks-template.md",
    "skills/s2tdd-implement/SKILL.md",
    "skills/s2tdd-converge/SKILL.md",
    "skills/s2tdd-constitution/SKILL.md",
    "skills/s2tdd-constitution/constitution-template.md",
)
IMPLIED_ENDORSEMENT = ("endorsed by GitHub", "official GitHub", "by GitHub")


def _text_files(root: Path, *relpaths: str) -> list[Path]:
    """Every regular file under the given files or folders of `root`, sorted."""
    found: list[Path] = []
    for rel in relpaths:
        target = root / rel
        if target.is_file():
            found.append(target)
        elif target.is_dir():
            found.extend(p for p in target.rglob("*") if p.is_file())
    return sorted(found)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def test_001_us5_ac6_license_and_credits(repo_root, doc):
    """US5-AC6: **Given** the released plugin, **When** someone inspects it, **Then** the LICENSE
    ships inside it and lists every forked file, each forked file carries its one-line credit, and
    nothing implies GitHub made or endorses s2tdd (T04).

    Provenance: 001 spec.md
    """
    license_path = repo_root / "LICENSE"
    assert license_path.is_file(), "LICENSE not found at the repository root"
    license_text = _read(license_path)

    registry = [m.group(1) for m in map(REGISTRY_LINE.match, license_text.split("\n")) if m]
    absent = [p for p in REQUIRED_REGISTRY if p not in registry]
    assert not absent, f"the registry lacks {absent}"

    # every registry path exists and carries the credit line
    for relpath in registry:
        assert (repo_root / relpath).is_file(), f"registry path not found: {relpath}"
        assert doc(relpath).first_body_line == CREDIT_LINE, (
            f"{relpath} lacks the credit line after its frontmatter"
        )

    # every skills/** or agents/** file carrying the credit line is in the registry
    for path in _text_files(repo_root, "skills", "agents"):
        rel = path.relative_to(repo_root).as_posix()
        if CREDIT_LINE in _read(path):
            assert rel in registry, f"{rel} carries the credit line but is not in the registry"

    # the LICENSE keeps the spec-kit and mattpocock/skills MIT notices
    assert "github/spec-kit" in license_text, "LICENSE lost the spec-kit notice"
    assert "Copyright GitHub, Inc." in license_text, "LICENSE lost the spec-kit copyright line"
    assert "mattpocock/skills" in license_text, "LICENSE lost the mattpocock/skills notice"
    assert license_text.count("MIT License") >= 3, "LICENSE lacks its three MIT notices"

    # nothing implies that GitHub made or endorses s2tdd
    scanned = _text_files(repo_root, "skills", "README.md", ".claude-plugin")
    for path in scanned:
        text = _read(path)
        for phrase in IMPLIED_ENDORSEMENT:
            assert phrase not in text, (
                f"{path.relative_to(repo_root).as_posix()} contains {phrase!r}"
            )


def test_001_us5_ac7_product_name(repo_root):
    """US5-AC7: **Given** the README and marketplace listing, **When** a reader sees the product
    name, **Then** it appears as s2tdd with T13's description line, and "tests as spec" appears
    only as the principle (T13).

    Provenance: 001 spec.md
    """
    plugin = json.loads(_read(repo_root / ".claude-plugin" / "plugin.json"))
    marketplace = json.loads(_read(repo_root / ".claude-plugin" / "marketplace.json"))
    assert plugin["description"] == DESCRIPTION, "plugin.json description differs from II-16"
    assert marketplace["plugins"][0]["description"] == DESCRIPTION, (
        "marketplace.json description differs from II-16"
    )

    readme_lines = _read(repo_root / "README.md").split("\n")
    heading = next((line for line in readme_lines if line.startswith("#")), "")
    assert heading == "# s2tdd", f"README.md heading is {heading}"
    assert DESCRIPTION in "\n".join(readme_lines[:5]), (
        "README.md's first five lines lack the description line"
    )

    for path in _text_files(repo_root, "README.md", ".claude-plugin", "skills"):
        if path.parent.name == ".claude-plugin" and path.suffix != ".json":
            continue
        for number, line in enumerate(_read(path).split("\n"), start=1):
            assert not OLD_PRODUCT_NAME.search(line), (
                f"{path.relative_to(repo_root).as_posix()}:{number}: tests-as-spec"
            )
