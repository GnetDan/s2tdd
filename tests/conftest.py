"""Shared test fixtures (II-5): repo_root, repo_copy, tool, doc, skill, and the Doc type.

Frozen after wave 0 (orchestration F5): a test that needs another fixture defines it in its
own test file.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import pytest
import yaml

_SKIPPED_PREFIXES = (".claude/", ".specify/", ".venv/")
_SHARED_OPEN = re.compile(r"^<!-- s2tdd:shared ([a-z][a-z-]*) -->$")
_SHARED_CLOSE = "<!-- /s2tdd:shared -->"
_MIGRATION_OPEN = "<!-- s2tdd:migration -->"
_MIGRATION_CLOSE = "<!-- /s2tdd:migration -->"


def _flatten(text: str) -> str:
    """Lowercase, drop backticks and asterisks, collapse whitespace runs to one space."""
    text = text.lower().replace("`", "").replace("*", "")
    return re.sub(r"\s+", " ", text).strip()


@dataclass
class Doc:
    path: Path
    text: str  # the file's text
    frontmatter: dict  # parsed YAML between leading '---' lines, else {}
    body: str  # text after the frontmatter
    first_body_line: str  # the line right after the closing '---' (or line 1)
    shared_blocks: list[str]  # block names of shared fences, in order
    migration_passages: list[str]  # text inside each migration fence, in order
    flat: str  # body lowercased, '`' and '*' removed, whitespace runs -> ' '

    def missing(self, *phrases: str) -> list[str]:
        """The phrases whose flattened form (same flattening) is not in self.flat."""
        return [p for p in phrases if _flatten(p) not in self.flat]


def _split_frontmatter(text: str) -> tuple[dict, str]:
    lines = text.split("\n")
    if lines[0].rstrip() != "---":
        return {}, text
    for i in range(1, len(lines)):
        if lines[i].rstrip() == "---":
            loaded = yaml.safe_load("\n".join(lines[1:i]))
            frontmatter = loaded if isinstance(loaded, dict) else {}
            return frontmatter, "\n".join(lines[i + 1 :])
    return {}, text


def _fences(body: str) -> tuple[list[str], list[str]]:
    shared: list[str] = []
    passages: list[str] = []
    in_migration: list[str] | None = None
    for line in body.split("\n"):
        if in_migration is not None:
            if line == _MIGRATION_CLOSE:
                passages.append("\n".join(in_migration))
                in_migration = None
            else:
                in_migration.append(line)
            continue
        if line == _MIGRATION_OPEN:
            in_migration = []
            continue
        match = _SHARED_OPEN.match(line)
        if match:
            shared.append(match.group(1))
    return shared, passages


def _load_doc(repo_root: Path, relpath: str) -> Doc:
    path = repo_root / relpath
    if not path.is_file():
        raise FileNotFoundError(f"no such file: {path}")
    text = path.read_text(encoding="utf-8")
    frontmatter, body = _split_frontmatter(text)
    shared_blocks, migration_passages = _fences(body)
    return Doc(
        path=path,
        text=text,
        frontmatter=frontmatter,
        body=body,
        first_body_line=body.split("\n", 1)[0],
        shared_blocks=shared_blocks,
        migration_passages=migration_passages,
        flat=_flatten(body),
    )


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


@pytest.fixture
def repo_copy(repo_root: Path, tmp_path: Path) -> Path:
    listing = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=repo_root,
        capture_output=True,
        check=True,
    ).stdout.decode("utf-8")
    dest_root = tmp_path / "repo"
    dest_root.mkdir()
    for rel in dict.fromkeys(p for p in listing.split("\0") if p):
        if rel.startswith(_SKIPPED_PREFIXES):
            continue
        src = repo_root / rel
        if not src.is_file():  # deleted in the work tree, a directory or a submodule
            continue
        dest = dest_root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
    return dest_root


@pytest.fixture(scope="session")
def tool(repo_root: Path) -> Callable[..., subprocess.CompletedProcess[str]]:
    def run(name: str, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(repo_root / "tools" / f"{name}.py"), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    return run


@pytest.fixture(scope="session")
def doc(repo_root: Path) -> Callable[[str], Doc]:
    def load(relpath: str) -> Doc:
        return _load_doc(repo_root, relpath)

    return load


@pytest.fixture(scope="session")
def skill(doc: Callable[[str], Doc]) -> Callable[[str], Doc]:
    def load(name: str) -> Doc:
        return doc(f"skills/{name}/SKILL.md")

    return load
