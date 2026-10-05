#!/usr/bin/env python3
"""Stamp shared blocks into skills and copy bundled files (development and CI only).

    python tools/build.py [--root DIR] [--only SKILL ...] [--check]

Shapes: specs/001-s2tdd-standalone-plugin/contracts/internal-interfaces.md II-1, II-2, II-4.

- A shared fence pair in ``skills/*/SKILL.md`` holds, between its markers, exactly the bytes of
  ``src/shared/<block>.md`` (LF, one final newline).
- Each ``[[file]]`` of ``src/bundle.toml`` is copied to ``skills/<to>/<as>`` for every ``to``.
- ``--check`` builds into a temporary copy, modifies nothing, and lists what is stale.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

if sys.version_info < (3, 11):  # pragma: no cover - guard for the machine's old default python
    sys.stderr.write("tools/build.py needs Python 3.11 or newer (tomllib)\n")
    raise SystemExit(2)

import tomllib  # noqa: E402

SHARED_OPEN = re.compile(r"<!-- s2tdd:shared (.+) -->")
SHARED_CLOSE = "<!-- /s2tdd:shared -->"
MIGRATION_OPEN = "<!-- s2tdd:migration -->"
MIGRATION_CLOSE = "<!-- /s2tdd:migration -->"
BLOCK_NAME = re.compile(r"[a-z][a-z-]*")

SKILL_FILE = "SKILL.md"


class FenceError(Exception):
    """A structural fence error; carries the 1-based line it is reported on."""

    def __init__(self, line: int, message: str) -> None:
        super().__init__(message)
        self.line = line
        self.message = message


@dataclass
class Plan:
    """What a build would do: files to write, notes to print, errors to report."""

    # relative posix path -> new bytes, in processing order
    outputs: dict[str, bytes] = field(default_factory=dict)
    # relative posix path of a SKILL.md -> block names whose fenced content differs
    stale_blocks: dict[str, set[str]] = field(default_factory=dict)
    skipped: set[str] = field(default_factory=set)
    errors: list[str] = field(default_factory=list)


def to_lf(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def load_block(root: Path, name: str, cache: dict[str, list[str] | None]) -> list[str] | None:
    """The lines of src/shared/<name>.md, or None when no such block exists."""
    if name in cache:
        return cache[name]
    lines: list[str] | None = None
    if BLOCK_NAME.fullmatch(name):
        path = root / "src" / "shared" / f"{name}.md"
        if path.is_file():
            text = to_lf(path.read_bytes()).decode("utf-8")
            if not text.endswith("\n"):
                text += "\n"
            lines = text[:-1].split("\n")
    cache[name] = lines
    return lines


def stamp(text: str, root: Path, cache: dict[str, list[str] | None]) -> tuple[str, set[str], list[tuple[int, str]]]:
    """Return the stamped text, the blocks that were stale, and (line, message) errors."""
    lines = text.split("\n")
    count = len(lines)
    out: list[str] = []
    stale: set[str] = set()
    errors: list[tuple[int, str]] = []
    in_migration = False
    i = 0
    try:
        while i < count:
            line = lines[i]
            opened = SHARED_OPEN.fullmatch(line)
            if opened:
                if in_migration:
                    raise FenceError(i + 1, "nested fence")
                name = opened.group(1)
                end = i + 1
                while end < count and lines[end] != SHARED_CLOSE:
                    other = lines[end]
                    if SHARED_OPEN.fullmatch(other) or other in (MIGRATION_OPEN, MIGRATION_CLOSE):
                        raise FenceError(end + 1, "nested fence")
                    end += 1
                if end >= count:
                    raise FenceError(i + 1, "unclosed fence")
                source = load_block(root, name, cache)
                if source is None:
                    errors.append((i + 1, f"unknown block '{name}'"))
                    out.extend(lines[i : end + 1])
                else:
                    if lines[i + 1 : end] != source:
                        stale.add(name)
                    out.append(line)
                    out.extend(source)
                    out.append(SHARED_CLOSE)
                i = end + 1
                continue
            if line == SHARED_CLOSE:
                raise FenceError(i + 1, "unopened fence")
            if line == MIGRATION_OPEN:
                in_migration = True
            elif line == MIGRATION_CLOSE:
                in_migration = False
            out.append(line)
            i += 1
    except FenceError as err:
        errors.append((err.line, err.message))
        return text, set(), errors
    return "\n".join(out), stale, errors


def safe_relative(value: str, *, forbid: str | None = None) -> bool:
    """A relative path inside its folder: no drive, no leading slash, no '..', not empty."""
    if not value or "\\" in value or "\0" in value:
        return False
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "." in path.parts or re.match(r"^[A-Za-z]:", value):
        return False
    return forbid is None or value != forbid


def read_bundle(root: Path, plan: Plan) -> list[dict]:
    """The validated [[file]] entries; problems go to plan.errors. No file means no entries."""
    path = root / "src" / "bundle.toml"
    if not path.is_file():
        return []
    try:
        data = tomllib.loads(path.read_bytes().decode("utf-8"))
    except (tomllib.TOMLDecodeError, UnicodeDecodeError) as err:
        plan.errors.append(f"src/bundle.toml:0: invalid TOML: {err}")
        return []
    entries: list[dict] = []
    for number, entry in enumerate(data.get("file", []), start=1):
        source, to, as_ = (entry.get("source"), entry.get("to"), entry.get("as")) if isinstance(entry, dict) else (None, None, None)
        valid = (
            isinstance(source, str)
            and isinstance(as_, str)
            and isinstance(to, list)
            and to
            and all(isinstance(t, str) for t in to)
        )
        if not valid:
            plan.errors.append(f"src/bundle.toml:0: entry {number} needs source (string), to (list of skills) and as (string)")
            continue
        if not safe_relative(source):
            plan.errors.append(f"src/bundle.toml:0: unsafe source '{source}'")
            continue
        if not safe_relative(as_, forbid=SKILL_FILE):
            plan.errors.append(f"src/bundle.toml:0: unsafe destination '{as_}'")
            continue
        if not all(safe_relative(t) and "/" not in t for t in to):
            plan.errors.append(f"src/bundle.toml:0: unsafe skill name in entry {number}")
            continue
        entries.append({"source": source, "to": to, "as": as_})
    return entries


def make_plan(root: Path, only: list[str] | None) -> Plan:
    """Work out every output without touching the tree."""
    plan = Plan()
    skills_dir = root / "skills"
    selected = set(only) if only else None
    cache: dict[str, list[str] | None] = {}

    # 1. stamp the SKILL.md files, in folder order
    if skills_dir.is_dir():
        for folder in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
            if selected is not None and folder.name not in selected:
                continue
            skill_path = folder / SKILL_FILE
            if not skill_path.is_file():
                continue
            rel = f"skills/{folder.name}/{SKILL_FILE}"
            original = skill_path.read_bytes()
            text = to_lf(original).decode("utf-8")
            new_text, stale, errors = stamp(text, root, cache)
            for line, message in errors:
                plan.errors.append(f"{rel}:{line}: {message}")
            if errors:
                continue
            new = new_text.encode("utf-8")
            if new != original:
                plan.outputs[rel] = new
                plan.stale_blocks[rel] = stale

    # 2. the bundle copies
    destinations: dict[str, str] = {}
    for entry in read_bundle(root, plan):
        targets = [t for t in entry["to"] if selected is None or t in selected]
        if not targets:
            continue
        source_path = root / "src" / entry["source"]
        if not source_path.is_file():
            plan.errors.append(f"src/bundle.toml:0: missing source '{entry['source']}'")
            continue
        content = to_lf(source_path.read_bytes())
        for target in targets:
            if not (skills_dir / target).is_dir():
                plan.skipped.add(target)
                continue
            rel = f"skills/{target}/{entry['as']}"
            if rel in destinations:
                plan.errors.append(f"src/bundle.toml:0: duplicate destination '{rel}'")
                continue
            destinations[rel] = entry["source"]
            dest_path = root / rel
            if dest_path.is_file() and dest_path.read_bytes() == content:
                continue
            plan.outputs[rel] = content

    # 3. an --only skill that has no folder at all is skipped, like a bundle target
    if selected is not None:
        for name in selected:
            if not (skills_dir / name).is_dir():
                plan.skipped.add(name)
    return plan


def apply(root: Path, plan: Plan) -> list[str]:
    """Write the plan's outputs; return the relative paths written."""
    written: list[str] = []
    for rel, content in plan.outputs.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        written.append(rel)
    return written


def emit(stream, lines: list[str]) -> None:
    for line in lines:
        stream.write(line + "\n")
    stream.flush()


def run_build(root: Path, only: list[str] | None) -> int:
    plan = make_plan(root, only)
    emit(sys.stderr, plan.errors)
    if plan.errors:
        return 1
    written = apply(root, plan)
    emit(sys.stdout, [f"wrote: {rel}" for rel in written])
    emit(sys.stdout, [f"skip: {name} (no skill folder)" for name in sorted(plan.skipped)])
    return 0


def run_check(root: Path, only: list[str] | None) -> int:
    with tempfile.TemporaryDirectory(prefix="s2tdd-build-") as tmp:
        copy = Path(tmp) / "tree"
        copy.mkdir()
        for folder in ("src", "skills"):
            if (root / folder).is_dir():
                shutil.copytree(root / folder, copy / folder)
        plan = make_plan(copy, only)
        emit(sys.stderr, plan.errors)
        if plan.errors:
            return 1
        written = apply(copy, plan)
        stale: set[str] = set()
        for rel in written:
            blocks = plan.stale_blocks.get(rel)
            if blocks is None:
                stale.add(f"stale: {rel}")
            elif blocks:
                stale.update(f"stale: {rel} (block {block})" for block in blocks)
            else:
                stale.add(f"stale: {rel}")
    emit(sys.stdout, sorted(stale))
    emit(sys.stdout, [f"skip: {name} (no skill folder)" for name in sorted(plan.skipped)])
    return 1 if stale else 0


def skill_name(value: str) -> str:
    if not value or "/" in value or "\\" in value or value in (".", ".."):
        raise argparse.ArgumentTypeError(f"not a skill folder name: {value!r}")
    return value


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", newline="\n")
    parser = argparse.ArgumentParser(
        prog="build.py",
        description="Stamp shared blocks into skills and copy bundled files.",
    )
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent,
                        help="the tree to build (default: the repository holding tools/)")
    parser.add_argument("--only", action="append", type=skill_name, metavar="SKILL",
                        help="build only this skill folder (repeatable)")
    parser.add_argument("--check", action="store_true",
                        help="build into a temporary copy and list what is stale; change nothing")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"--root is not a directory: {args.root}")
    return run_check(root, args.only) if args.check else run_build(root, args.only)


if __name__ == "__main__":
    sys.exit(main())
