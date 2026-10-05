"""README.md and src/pages/WORKFLOW.md state the agent types' model and effort (T080, II-17f).

Assertion style (II-0): literals through `Doc.missing`; absence on `d.flat`; the paragraph
helper lives here (tests/conftest.py is frozen). Red until T075 writes the paragraph.
"""

from __future__ import annotations

import re

# II-17f, exact.
AGENT_TYPE_SENTENCE = (
    "every agent type runs on Opus: packets at low, medium or high effort by tier, "
    "the strong-diff reviewer at high and the proxy verifier at medium"
)
README_LINK = "docs/models.md"
WORKFLOW_LINK = "https://github.com/GnetDan/s2tdd/blob/main/docs/models.md"
ABSENT = "sonnet"


def _flatten(s: str) -> str:
    return " ".join(s.lower().replace("`", "").replace("*", "").split())


def _paragraphs_with(body: str, phrase: str) -> list[str]:
    """Flattened blank-line-separated paragraphs of body that contain phrase (flattened)."""
    target = _flatten(phrase)
    paras = (_flatten(p) for p in re.split(r"\n\s*\n", body))
    return [p for p in paras if target in p]


def _check(d, link: str) -> None:
    assert not d.missing(AGENT_TYPE_SENTENCE)
    paras = _paragraphs_with(d.body, AGENT_TYPE_SENTENCE)
    assert any(_flatten(link) in p for p in paras), f"{link} not in the sentence's paragraph"
    assert _flatten(ABSENT) not in d.flat


def test_docs_readme_agent_types(doc):
    _check(doc("README.md"), README_LINK)


def test_docs_workflow_agent_types(doc):
    _check(doc("src/pages/WORKFLOW.md"), WORKFLOW_LINK)
