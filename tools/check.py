"""Repository checker for the s2tdd plugin tree (development and CI only).

    python tools/check.py [--root DIR] [--rule NAME ...] [--only PATH ...]

Runs the rules below over the tree (default: the repository holding ``tools/``). Prints nothing
and exits 0 when every rule passes; otherwise prints one line per failure,
``<path>:<line>: <rule>: <detail>`` (path relative to the root, forward slashes; line ``0``
when the failure is not on a line) and exits 1. An unknown rule name, or an ``--only`` path
that is missing, outside the root, typed in a case that differs from the disk, or not under
skills, agents or src, is a usage error (exit 2).

``--only PATH`` limits the per-file rules (frontmatter, placeholders, old-names, bundled-files)
to files under those paths and skips the repository-wide rules (command-set, credits,
manifests).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Callable, Iterable, Iterator

import yaml

COMMANDS = ("epic", "specify", "clarify", "plan", "harden", "implement", "verify-done",
            "converge", "pr-review", "close", "next", "foundation-review", "constitution")
PLACEHOLDERS = ("$ARGUMENTS", "${CLAUDE_PLUGIN_ROOT}", "${CLAUDE_SKILL_DIR}",
                "__SPECKIT_COMMAND_", "{SCRIPT}", "{ARGS}")
OLD_NAMES = (r"\.specify/", r"docs/sdd-workflow\.md", r"/speckit-", r"skills/speckit-")  # regex, case-sensitive
MIGRATION_FENCE_FILES = ("skills/s2tdd-next/SKILL.md", "skills/s2tdd-implement/SKILL.md",
                         "skills/s2tdd-harden/SKILL.md")
CREDIT_LINE = "<!-- Adapted from github/spec-kit (MIT). -->"

RULES = ("frontmatter", "command-set", "placeholders", "old-names", "bundled-files", "credits",
         "manifests")
PER_FILE_RULES = ("frontmatter", "placeholders", "old-names", "bundled-files")

PLUGIN_NAME = "s2tdd"
SKILL_PREFIX = "s2tdd-"
MIGRATION_OPEN = "<!-- s2tdd:migration -->"
MIGRATION_CLOSE = "<!-- /s2tdd:migration -->"
SCANNED_TREES = ("skills", "agents", "src")
CREDITED_TREES = ("skills", "agents")

OLD_NAME_RE = re.compile("|".join(f"(?:{pattern})" for pattern in OLD_NAMES))
BUNDLED_PATH_RE = re.compile(r"(?<![\w./])\./[\w./-]+\.\w+")
REGISTRY_RE = re.compile(r"^- ((skills|agents)/\S+)$")

Failure = tuple[str, int, str, str]  # path, line, rule, detail


# ---------------------------------------------------------------- tree access


class Tree:
    """The checked tree: the root, the --only scope, and cached text reads."""

    def __init__(self, root: Path, only: list[str]) -> None:
        self.root = root
        self.only = only
        self._lines: dict[Path, list[str] | None] = {}

    def rel(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()

    def in_scope(self, path: Path) -> bool:
        if not self.only:
            return True
        rel = self.rel(path)
        return any(rel == scope or rel.startswith(scope + "/") for scope in self.only)

    def lines(self, path: Path) -> list[str] | None:
        """The file's lines (CRLF tolerated, BOM dropped), or None for a binary file."""
        if path not in self._lines:
            self._lines[path] = read_lines(path)
        return self._lines[path]

    def files_under(self, *tops: str) -> Iterator[Path]:
        """Every file under the named top-level folders, sorted, within the --only scope."""
        for top in tops:
            base = self.root / top
            if not base.is_dir():
                continue
            for path in sorted(p for p in base.rglob("*") if p.is_file()):
                if self.in_scope(path):
                    yield path

    def text_files_under(self, *tops: str) -> Iterator[tuple[Path, list[str]]]:
        for path in self.files_under(*tops):
            lines = self.lines(path)
            if lines is not None:
                yield path, lines

    def skill_files(self) -> Iterator[Path]:
        base = self.root / "skills"
        if not base.is_dir():
            return
        for path in sorted(base.glob("*/SKILL.md")):
            if path.is_file() and self.in_scope(path):
                yield path

    def agent_files(self) -> Iterator[Path]:
        base = self.root / "agents"
        if not base.is_dir():
            return
        for path in sorted(base.glob("*.md")):
            if path.is_file() and self.in_scope(path):
                yield path


def read_lines(path: Path) -> list[str] | None:
    data = path.read_bytes()
    if b"\0" in data:
        return None
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return None
    if text.startswith("\ufeff"):
        text = text[1:]
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    return [line[:-1] if line.endswith("\r") else line for line in lines]


def exact_case(base: Path, parts: Iterable[str]) -> str:
    """'ok' when base/parts exists with exactly this spelling (case included, on every system),
    'case' when it exists only under a different case, else 'missing'."""
    current = base
    for part in parts:
        if part in ("", "."):
            continue
        try:
            names = os.listdir(current) if current.is_dir() else []
        except OSError:
            names = []
        if part not in names:
            return "case" if any(name.lower() == part.lower() for name in names) else "missing"
        current = current / part
    return "ok"


# ---------------------------------------------------------------- frontmatter


def parse_frontmatter(lines: list[str]) -> tuple[dict | None, str | None]:
    """Return (mapping, None) or (None, the reason the frontmatter is unusable)."""
    if not lines or lines[0] != "---":
        return None, "no frontmatter (the file does not start with a '---' line)"
    try:
        closing = lines.index("---", 1)
    except ValueError:
        return None, "frontmatter never closes (no second '---' line)"
    try:
        data = yaml.safe_load("\n".join(lines[1:closing]))
    except yaml.YAMLError as error:
        mark = getattr(error, "problem_mark", None)
        where = f" (frontmatter line {mark.line + 1})" if mark is not None else ""
        return None, f"frontmatter YAML does not parse{where}"
    if data is None:
        data = {}
    if not isinstance(data, dict):
        return None, "frontmatter is not a YAML mapping"
    return data, None


def blank(value: object) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def rule_frontmatter(tree: Tree) -> Iterator[Failure]:
    targets = [(path, path.parent.name, ("name", "description"), "folder")
               for path in tree.skill_files()]
    targets += [(path, path.stem, ("name", "description", "model", "effort"), "file stem")
                for path in tree.agent_files()]
    for path, expected_name, required, what in targets:
        rel = tree.rel(path)
        lines = tree.lines(path)
        if lines is None:
            yield rel, 0, "frontmatter", "not a UTF-8 text file"
            continue
        data, problem = parse_frontmatter(lines)
        if data is None:
            yield rel, 1, "frontmatter", problem
            continue
        for key in required:
            if blank(data.get(key)):
                yield rel, 1, "frontmatter", f"'{key}' missing or empty"
        name = data.get("name")
        if not blank(name) and str(name) != expected_name:
            yield rel, 1, "frontmatter", f"name '{name}' is not its {what} '{expected_name}'"


# ---------------------------------------------------------------- command-set


def rule_command_set(tree: Tree) -> Iterator[Failure]:
    expected = {SKILL_PREFIX + command for command in COMMANDS}
    base = tree.root / "skills"
    present = {p.name for p in base.iterdir() if p.is_dir()} if base.is_dir() else set()
    for name in sorted(expected - present, key=lambda n: COMMANDS.index(n[len(SKILL_PREFIX):])):
        yield "skills", 0, "command-set", f"missing skill folder {name}"
    for name in sorted(present - expected):
        yield "skills", 0, "command-set", f"extra skill folder {name}"


# ---------------------------------------------------------------- placeholders


def rule_placeholders(tree: Tree) -> Iterator[Failure]:
    for path, lines in tree.text_files_under(*SCANNED_TREES):
        for number, line in enumerate(lines, 1):
            found = [token for token in PLACEHOLDERS if token in line]
            if found:
                yield tree.rel(path), number, "placeholders", "placeholder " + ", ".join(found)


# ---------------------------------------------------------------- old-names


def migration_fences(rel: str, lines: list[str]) -> tuple[list[Failure], set[int]]:
    """Parse migration fences. Return the fence failures and the exempt line numbers.

    Lines inside a well-formed fence (opened and closed, not nested) are exempt from the old-name
    patterns, but only in MIGRATION_FENCE_FILES. A whitespace-padded marker is malformed.
    """
    failures: list[Failure] = []
    exempt: set[int] = set()
    allowed = rel in MIGRATION_FENCE_FILES
    open_at: int | None = None
    nested = False
    for number, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped in (MIGRATION_OPEN, MIGRATION_CLOSE) and line != stripped:
            failures.append((rel, number, "old-names",
                             "malformed migration fence (the marker must be the whole line)"))
            continue
        if line == MIGRATION_OPEN:
            if not allowed:
                failures.append((rel, number, "old-names",
                                 "migration fence outside next, implement and harden"))
            if open_at is not None:
                failures.append((rel, number, "old-names", "nested migration fence"))
                nested = True
                continue
            open_at, nested = number, False
        elif line == MIGRATION_CLOSE:
            if open_at is None:
                failures.append((rel, number, "old-names", "migration fence closed but never opened"))
                continue
            inside = range(open_at + 1, number)
            if not any(OLD_NAME_RE.search(lines[i - 1]) for i in inside):
                failures.append((rel, open_at, "old-names", "migration fence holds no old name"))
            if allowed and not nested:
                exempt.update(inside)
            open_at = None
    if open_at is not None:
        failures.append((rel, open_at, "old-names", "migration fence never closed"))
    return failures, exempt


def rule_old_names(tree: Tree) -> Iterator[Failure]:
    for path, lines in tree.text_files_under(*SCANNED_TREES):
        rel = tree.rel(path)
        fence_failures, exempt = migration_fences(rel, lines)
        failures = list(fence_failures)
        for number, line in enumerate(lines, 1):
            if number in exempt:
                continue
            found = sorted({match.group(0) for match in OLD_NAME_RE.finditer(line)})
            if found:
                failures.append((rel, number, "old-names",
                                 "old name outside a migration fence: " + ", ".join(found)))
        yield from sorted(failures, key=lambda f: f[1])


# ---------------------------------------------------------------- bundled-files


def rule_bundled_files(tree: Tree) -> Iterator[Failure]:
    for path in tree.skill_files():
        rel = tree.rel(path)
        lines = tree.lines(path)
        if lines is None:
            continue
        folder = path.parent
        for number, line in enumerate(lines, 1):
            if "../" in line:
                yield rel, number, "bundled-files", "parent path '../' (bundle the file instead)"
            for match in BUNDLED_PATH_RE.finditer(line):
                found = exact_case(folder, match.group(0)[2:].split("/"))
                if found != "ok":
                    how = "differs in case from the file in" if found == "case" else "not found in"
                    yield rel, number, "bundled-files", f"{match.group(0)} {how} {tree.rel(folder)}"


# ---------------------------------------------------------------- credits


def holds_credit(lines: list[str]) -> int:
    """The 1-based line holding CREDIT_LINE as a whole line, or 0."""
    for number, line in enumerate(lines, 1):
        if line.strip() == CREDIT_LINE:
            return number
    return 0


def rule_credits(tree: Tree) -> Iterator[Failure]:
    license_path = tree.root / "LICENSE"
    registry: dict[str, int] = {}
    if not license_path.is_file():
        yield "LICENSE", 0, "credits", "LICENSE missing"
    else:
        for number, line in enumerate(tree.lines(license_path) or [], 1):
            match = REGISTRY_RE.match(line)
            if match:
                registry.setdefault(match.group(1), number)
    for listed, number in registry.items():
        path = tree.root / listed
        if not path.is_file():
            yield "LICENSE", number, "credits", f"listed file {listed} does not exist"
            continue
        lines = tree.lines(path)
        if lines is None or not holds_credit(lines):
            yield listed, 0, "credits", "listed in LICENSE but lacks the credit line"
    for path, lines in tree.text_files_under(*CREDITED_TREES):
        rel = tree.rel(path)
        number = holds_credit(lines)
        if number and rel not in registry:
            yield rel, number, "credits", "carries the credit line but LICENSE does not list it"


# ---------------------------------------------------------------- manifests


def load_manifest(tree: Tree, rel: str) -> tuple[object, Failure | None]:
    path = tree.root / rel
    if not path.is_file():
        return None, (rel, 0, "manifests", "missing")
    try:
        return json.loads(path.read_text(encoding="utf-8-sig")), None
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        return None, (rel, 0, "manifests", f"not JSON ({error})")


def rule_manifests(tree: Tree) -> Iterator[Failure]:
    plugin_rel = ".claude-plugin/plugin.json"
    market_rel = ".claude-plugin/marketplace.json"
    plugin, problem = load_manifest(tree, plugin_rel)
    if problem:
        yield problem
    market, problem = load_manifest(tree, market_rel)
    if problem:
        yield problem

    plugin_description = None
    if problem is None and not isinstance(market, dict):
        yield market_rel, 0, "manifests", "not a JSON object"
    if plugin is not None:
        if not isinstance(plugin, dict):
            yield plugin_rel, 0, "manifests", "not a JSON object"
        else:
            if plugin.get("name") != PLUGIN_NAME:
                yield plugin_rel, 0, "manifests", f"name {plugin.get('name')!r} is not '{PLUGIN_NAME}'"
            plugin_description = plugin.get("description")
            if blank(plugin_description):
                yield plugin_rel, 0, "manifests", "description missing or empty"

    if not isinstance(market, dict):
        return
    if market.get("name") != PLUGIN_NAME:
        yield market_rel, 0, "manifests", f"name {market.get('name')!r} is not '{PLUGIN_NAME}'"
    entries = market.get("plugins")
    if not isinstance(entries, list) or len(entries) != 1 or not isinstance(entries[0], dict):
        count = len(entries) if isinstance(entries, list) else 0
        yield market_rel, 0, "manifests", f"must list exactly one plugin, lists {count}"
        return
    entry = entries[0]
    if entry.get("name") != PLUGIN_NAME or entry.get("source") != "./":
        yield (market_rel, 0, "manifests",
               f"the plugin must be {{name: {PLUGIN_NAME}, source: \"./\"}}, is "
               f"{{name: {entry.get('name')!r}, source: {entry.get('source')!r}}}")
    if isinstance(plugin, dict) and not blank(plugin_description):
        if entry.get("description") != plugin_description:
            yield (market_rel, 0, "manifests",
                   f"the plugin's description differs from {plugin_rel}'s")


# ---------------------------------------------------------------- driver


RULE_FUNCTIONS: dict[str, Callable[[Tree], Iterable[Failure]]] = {
    "frontmatter": rule_frontmatter,
    "command-set": rule_command_set,
    "placeholders": rule_placeholders,
    "old-names": rule_old_names,
    "bundled-files": rule_bundled_files,
    "credits": rule_credits,
    "manifests": rule_manifests,
}


def resolve_scope(root: Path, raw: str) -> tuple[str, str]:
    """Resolve an --only value (absolute, or relative to the root) to a root-relative POSIX path.

    Return (scope, "") or ("", the reason it is unusable): outside the root, missing, a case that
    differs from the files on disk, or not skills, agents or src (or a path under them), where no
    per-file rule looks and the scope would silently match nothing.
    """
    typed = Path(raw)
    full = os.path.normpath(os.path.abspath(typed if typed.is_absolute() else root / typed))
    root_text = os.path.normpath(str(root)).rstrip(os.sep)
    folded, folded_root = os.path.normcase(full), os.path.normcase(root_text)
    if folded == folded_root:
        rel = ""
    elif folded.startswith(folded_root + os.sep):
        rel = full[len(root_text) + 1:]
    else:
        return "", "lies outside the root"
    parts = [part for part in rel.replace(os.sep, "/").split("/") if part]
    found = exact_case(root, parts)
    if found == "case":
        return "", "differs in case from the files on disk"
    if found == "missing":
        return "", "no such path under the root"
    if not parts or parts[0] not in SCANNED_TREES:
        return "", "is not " + ", ".join(SCANNED_TREES) + " or a path under them"
    return "/".join(parts), ""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="check.py", description="Check the s2tdd plugin tree.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent,
                        help="the tree to check (default: this repository)")
    parser.add_argument("--rule", action="append", choices=RULES, metavar="NAME",
                        help="run only this rule (repeatable); one of: " + ", ".join(RULES))
    parser.add_argument("--only", action="append", metavar="PATH", default=[],
                        help="limit per-file rules to this path under skills, agents or src "
                             "(absolute, or relative to the root; repeatable); skips the "
                             "repository-wide rules")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"--root {args.root} is not a directory")
    only = []
    for raw in args.only:
        scope, problem = resolve_scope(root, raw)
        if problem:
            parser.error(f"--only {raw}: {problem}")
        only.append(scope)

    selected = args.rule or list(RULES)
    rules = [rule for rule in RULES if rule in selected]
    if only:
        rules = [rule for rule in rules if rule in PER_FILE_RULES]

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    tree = Tree(root, only)
    failed = False
    for rule in rules:
        for path, line, name, detail in RULE_FUNCTIONS[rule](tree):
            failed = True
            print(f"{path}:{line}: {name}: {detail}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
