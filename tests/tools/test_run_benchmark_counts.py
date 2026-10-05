"""The run benchmark's `user messages` count holds typed messages only (II-18 i; II-14).

Harness-injected user entries (compaction summaries, transcript-only entries, task
notifications, local command output, system reminders) are not human touches; a slash command
the user typed still is.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SCRIPT_PATH = "tools/run_benchmark_tokens.py"
SESSION_ID = "acme0001-0000-4000-8000-000000000001"


def _user(content, **flags):
    return {"type": "user", "message": {"role": "user", "content": content}, **flags}


def _text(s):
    return [{"type": "text", "text": s}]


def test_user_messages_count_typed_messages_only(repo_root: Path, tmp_path: Path):
    main = [
        _user("start the wave"),
        _user("<command-name>/s2tdd-next</command-name>\n<command-args></command-args>"),
        _user(_text("This session is being continued from a previous conversation..."),
              isCompactSummary=True),
        _user("Compacted. ctrl+o to see full summary", isVisibleInTranscriptOnly=True),
        _user(_text("<task-notification>\n<task-id>t1</task-id>\n</task-notification>")),
        _user("<local-command-stdout>done</local-command-stdout>"),
        _user(_text("<system-reminder>\nThe date has changed.\n</system-reminder>")),
    ]
    path = tmp_path / f"{SESSION_ID}.jsonl"
    path.write_text("\n".join(json.dumps(i) for i in main) + "\n", encoding="utf-8")
    out = subprocess.run(
        [sys.executable, "-X", "utf8", str(repo_root / SCRIPT_PATH), str(tmp_path), "session",
         "acme0001"],
        capture_output=True, text=True, encoding="utf-8", check=True, timeout=60,
    ).stdout.splitlines()
    line = "  dispatches 0 · subagent transcripts 0 · compactions 0 · user messages 2"
    assert line in out, f"missing {line!r} in {out!r}"
