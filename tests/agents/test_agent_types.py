"""T035: the seven agent types (II-9; research.md R10; 003 T007).

Exactly `agents/packet-cheap.md`, `packet-medium.md`, `packet-strong.md`,
`strong-diff-reviewer.md`, `proxy-verifier.md`, `converger.md` and `hardener.md`, each with
`name` (= file stem), a non-empty `description`, and `model` / `effort` as 003's II-1 table
(002 FR-004 supersedes 001 R10; 003 FR-003 adds the converger and the hardener).
"""

from __future__ import annotations

import pytest

# 002 FR-004 / II-1 (supersedes 001 research.md R10's models): file stem -> (model, effort).
AGENT_TYPES = {
    "packet-cheap": ("opus", "low"),
    "packet-medium": ("opus", "medium"),
    "packet-strong": ("opus", "high"),
    "strong-diff-reviewer": ("opus", "high"),
    "proxy-verifier": ("opus", "medium"),
    # 003 FR-003 / II-1: the converger and the hardener join the five.
    "converger": ("opus", "medium"),
    "hardener": ("opus", "high"),
}


def test_exactly_the_seven_agent_files_exist(repo_root):
    expected = sorted(f"{stem}.md" for stem in AGENT_TYPES)
    missing = [f"agents/{name}" for name in expected if not (repo_root / "agents" / name).is_file()]
    assert not missing, f"not found: {missing}"
    present = sorted(p.name for p in (repo_root / "agents").glob("*.md"))
    assert present == expected, present


@pytest.mark.parametrize("stem", sorted(AGENT_TYPES))
def test_frontmatter(doc, stem):
    d = doc(f"agents/{stem}.md")
    assert d.frontmatter.get("name") == stem, d.frontmatter
    description = d.frontmatter.get("description")
    assert isinstance(description, str) and description.strip(), d.frontmatter


@pytest.mark.parametrize("stem", sorted(AGENT_TYPES))
def test_model_and_effort(doc, stem):
    d = doc(f"agents/{stem}.md")
    model, effort = AGENT_TYPES[stem]
    actual_model = d.frontmatter.get("model")
    actual_effort = d.frontmatter.get("effort")
    assert actual_model == model, f"{stem} model {actual_model}, not {model}"
    assert actual_effort == effort, f"{stem} effort {actual_effort}, not {effort}"
