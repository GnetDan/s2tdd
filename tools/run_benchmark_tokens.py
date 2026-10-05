"""Token and time figures for Claude Code sessions, from their JSONL transcripts.

Usage:
  python tools/run_benchmark_tokens.py <transcripts dir> find <text> [<text> ...]
      List sessions whose user messages mention every <text> (e.g. "003" "wave"),
      with first/last timestamp and size, to pick out a feature's sessions.
  python tools/run_benchmark_tokens.py <transcripts dir> session <id-prefix> [<id-prefix> ...]
      Per session: orchestrator context curve (start, first dispatch, max, end),
      dispatches, compactions, wall time, idle gaps over 15 min, user messages,
      and summed token usage of the session and of its subagents.

<transcripts dir> is ~/.claude/projects/<project slug>, e.g. C--Git-acme. Context at a
turn = input + cache_read + cache_creation tokens of the main thread's assistant entry
(sidechains skipped, duplicate message ids counted once). Read-only.
"""

from __future__ import annotations

import glob
import json
import os
import sys
from datetime import datetime

DISPATCH = {"Agent", "Task"}
INJECTED = ("<task-notification>", "<local-command-", "<system-reminder>")  # harness, not typed


def entries(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                yield json.loads(line)
            except ValueError:
                continue


def ts(e):
    t = e.get("timestamp")
    return datetime.fromisoformat(t.replace("Z", "+00:00")) if t else None


def usage_sum(path, main_only):
    tot = dict(input=0, cache_read=0, cache_creation=0, output=0)
    last = {}  # message id -> its last usage (later entries carry the final output count)
    for e in entries(path):
        m = e.get("message")
        if e.get("type") != "assistant" or not isinstance(m, dict) or not m.get("usage"):
            continue
        if main_only and e.get("isSidechain"):
            continue
        last[m.get("id")] = m["usage"]
    for u in last.values():
        tot["input"] += u.get("input_tokens", 0)
        tot["cache_read"] += u.get("cache_read_input_tokens", 0)
        tot["cache_creation"] += u.get("cache_creation_input_tokens", 0)
        tot["output"] += u.get("output_tokens", 0)
    return tot


def user_text(e):
    m = e.get("message")
    if e.get("type") != "user" or not isinstance(m, dict) or e.get("isSidechain"):
        return None
    c = m.get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        parts = [x.get("text", "") for x in c if isinstance(x, dict) and x.get("type") == "text"]
        return "\n".join(parts) if parts else None
    return None


def typed(e):
    """A user message the human typed: not meta, compact summary, transcript-only or injected."""
    u = user_text(e)
    if not u or e.get("isMeta") or e.get("isCompactSummary") or e.get("isVisibleInTranscriptOnly"):
        return False
    return not u.lstrip().startswith(INJECTED)


def find(base, needles):
    for path in sorted(glob.glob(os.path.join(base, "*.jsonl"))):
        texts, times = [], []
        for e in entries(path):
            t = ts(e)
            if t:
                times.append(t)
            u = user_text(e)
            if u:
                texts.append(u)
        blob = "\n".join(texts)
        if times and all(n in blob for n in needles):
            first = next((t for t in texts if t.strip()), "")[:80].replace("\n", " ")
            print(f"{os.path.basename(path)[:8]}  {times[0]:%m-%d %H:%M} → {times[-1]:%m-%d %H:%M}"
                  f"  {os.path.getsize(path) // 1024}KB  {first!r}")


def session(base, prefix):
    path = glob.glob(os.path.join(base, prefix + "*.jsonl"))[0]
    sid = os.path.basename(path)[:-6]
    pts, seen, tool_ids, comp, dispatches, users, times = [], set(), set(), 0, 0, 0, []
    first_dispatch = None
    for e in entries(path):
        t = ts(e)
        if t and not e.get("isSidechain"):
            times.append(t)
        if e.get("type") == "system" and e.get("subtype") == "compact_boundary":
            comp += 1
        if typed(e):
            users += 1
        m = e.get("message")
        if e.get("type") != "assistant" or not isinstance(m, dict) or not m.get("usage"):
            continue
        if e.get("isSidechain"):
            continue
        u = m["usage"]
        ctx = (u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0)
               + u.get("cache_creation_input_tokens", 0))
        if m.get("id") not in seen:  # one message can span several entries
            seen.add(m.get("id"))
            pts.append(ctx)
        for x in m.get("content") or []:
            if (isinstance(x, dict) and x.get("name") in DISPATCH
                    and x.get("id") not in tool_ids):
                tool_ids.add(x.get("id"))
                dispatches += 1
                if first_dispatch is None:
                    first_dispatch = ctx
    times.sort()
    gaps = [(a, b) for a, b in zip(times, times[1:]) if (b - a).total_seconds() > 900]
    main = usage_sum(path, main_only=True)
    sub = dict(input=0, cache_read=0, cache_creation=0, output=0)
    subs = glob.glob(os.path.join(base, sid, "subagents", "*.jsonl"))
    for sp in subs:
        for k, v in usage_sum(sp, main_only=False).items():
            sub[k] += v
    print(f"session {sid[:8]}")
    if pts:
        print(f"  context: start {pts[0] // 1000}k · first dispatch "
              f"{(first_dispatch or 0) // 1000}k · max {max(pts) // 1000}k · end {pts[-1] // 1000}k"
              f" · turns {len(pts)}")
    print(f"  dispatches {dispatches} · subagent transcripts {len(subs)} · compactions {comp}"
          f" · user messages {users}")
    if times:
        print(f"  wall {times[0]:%m-%d %H:%M} → {times[-1]:%m-%d %H:%M}"
              f" ({(times[-1] - times[0]).total_seconds() / 3600:.1f} h)")
    for a, b in gaps:
        print(f"  idle {a:%H:%M} → {b:%H:%M} ({(b - a).total_seconds() / 60:.0f} min)")
    for name, tot in (("main", main), ("subagents", sub)):
        print(f"  {name} tokens: input {tot['input']:,} · cache read {tot['cache_read']:,}"
              f" · cache write {tot['cache_creation']:,} · output {tot['output']:,}")


if __name__ == "__main__":
    base, mode, *args = sys.argv[1:]
    if mode == "find":
        find(base, args)
    else:
        for a in args:
            session(base, a)
