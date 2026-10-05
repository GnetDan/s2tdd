"""Review fix E-3: close's preamble step 3 leaves a docs wave's uncommitted files to A0."""

import re
from pathlib import Path

SKILL = Path(__file__).resolve().parents[2] / "skills" / "s2tdd-close" / "SKILL.md"

PHRASE = (
    "When the only uncommitted files are exactly the docs wave's files run-ledger.md names, "
    "step 3 leaves them to A0 and asks nothing"
)


def _flat(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("`", ""))


def test_preamble_step_3_leaves_docs_wave_files_to_a0():
    text = _flat(SKILL.read_text(encoding="utf-8"))
    step3 = text.find("3. Record SHA")
    step4 = text.find("4. Read spec.md")
    a0 = text.find("A0. Docs wave")
    assert -1 not in (step3, step4, a0), "preamble step 3, step 4 or A0 not found"
    pos = text.find(PHRASE)
    assert pos != -1, f"missing phrase: {PHRASE!r}"
    assert step3 < pos < step4 < a0, "phrase must sit in preamble step 3, before A0. Docs wave"
