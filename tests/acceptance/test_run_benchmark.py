"""US15 acceptance tests: a run benchmark for whoever maintains the workflow (T052; II-14)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SKILL_PATH = ".claude/skills/run-benchmark/SKILL.md"
SCRIPT_PATH = "tools/run_benchmark_tokens.py"
REPORT_PHRASES = (
    "Write the report to the analyzed project's specs repository: "
    "<project dir>/specs/benchmarks/<project>-<earlier>-vs-<later>.md",
    "Never write a report into this repository.",
)

SESSION_ID = "abcdef12-0000-4000-8000-000000000001"


def _flatten(s: str) -> str:
    return " ".join(s.lower().replace("`", "").replace("*", "").split())


def _assistant(msg_id, usage, content=(), sidechain=False):
    return {
        "type": "assistant",
        "isSidechain": sidechain,
        "message": {"id": msg_id, "usage": usage, "content": list(content)},
    }


def _usage(inp, read, write, out):
    return {
        "input_tokens": inp,
        "cache_read_input_tokens": read,
        "cache_creation_input_tokens": write,
        "output_tokens": out,
    }


def _write_jsonl(path: Path, items) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(i) for i in items) + "\n", encoding="utf-8")


def test_002_us15_ac1_maintainer_skill(repo_root, doc):
    """US15-AC1: **Given** a clone of the plugin repository, **When** a maintainer works in it,
    **Then** the run-benchmark skill is available to them, and the installed plugin offers no such
    command to users.

    Provenance: 002 spec.md
    """
    d = doc(SKILL_PATH)
    assert d.frontmatter.get("name") == "run-benchmark"
    assert not (repo_root / "skills" / "run-benchmark").exists()
    plugin_dir = repo_root / ".claude-plugin"
    naming = [
        p for p in plugin_dir.rglob("*")
        if p.is_file() and "run-benchmark" in p.read_text(encoding="utf-8", errors="replace")
    ]
    assert naming == []
    dev = doc("docs/developing.md")
    assert not dev.missing(SKILL_PATH, SCRIPT_PATH)


def test_002_us15_ac2_token_figures(repo_root, tmp_path):
    """US15-AC2: **Given** a session transcript with known context and token figures, **When** the
    token script reads it, **Then** it reports those figures, counting each dispatch and each
    message's final usage once.

    Provenance: 002 spec.md
    """
    script = repo_root / SCRIPT_PATH
    assert script.is_file(), f"{SCRIPT_PATH} not found"
    agent = {"type": "tool_use", "id": "tu_1", "name": "Agent", "input": {}}
    main = [
        {"type": "user", "message": {"role": "user", "content": "start the wave"}},
        _assistant("msg_1", _usage(100, 20000, 1000, 50)),
        _assistant("msg_2", _usage(10, 30000, 2000, 1), [agent]),
        _assistant("msg_2", _usage(10, 30000, 2000, 400), [agent]),
        _assistant(
            "msg_s", _usage(99999, 99999, 99999, 999),
            [{"type": "tool_use", "id": "tu_9", "name": "Agent", "input": {}}], sidechain=True,
        ),
        _assistant("msg_3", _usage(5, 40000, 500, 70)),
    ]
    _write_jsonl(tmp_path / f"{SESSION_ID}.jsonl", main)
    _write_jsonl(
        tmp_path / SESSION_ID / "subagents" / "agent-1.jsonl",
        [_assistant("sub_1", _usage(7, 1000, 200, 30))],
    )
    out = subprocess.run(
        [sys.executable, "-X", "utf8", str(script), str(tmp_path), "session", "abcdef"],
        capture_output=True, text=True, encoding="utf-8", check=True, timeout=60,
    ).stdout.splitlines()
    expected = [
        "session abcdef12",
        "  context: start 21k · first dispatch 32k · max 40k · end 40k · turns 3",
        "  dispatches 1 · subagent transcripts 1 · compactions 0 · user messages 1",
        "  main tokens: input 115 · cache read 90,000 · cache write 3,500 · output 520",
        "  subagents tokens: input 7 · cache read 1,000 · cache write 200 · output 30",
    ]
    for line in expected:
        assert line in out, f"missing {line!r} in {out!r}"


def test_002_us15_ac3_reports_in_project_specs(doc):
    """US15-AC3: **Given** a benchmark of a project's two features, **When** the report is
    written, **Then** it lands in that project's specs repository, never in the plugin repository.

    Provenance: 002 spec.md
    """
    d = doc(SKILL_PATH)
    assert not d.missing(*REPORT_PHRASES)
