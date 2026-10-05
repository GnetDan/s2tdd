"""US4 acceptance test for portability: CI enforces that the commands carry no Claude Code
placeholder and read only their own bundled files (T061; II-3, II-6, contracts/build-and-check.md).
"""

from __future__ import annotations

import yaml

CI_PATH = ".github/workflows/ci.yml"
INPUT_SENTENCE = "the text the user typed after the command"


def _triggers(workflow: dict) -> set[str]:
    """The event names in the workflow's `on` key (YAML 1.1 reads a bare `on` as True)."""
    value = workflow.get("on", workflow.get(True))
    if isinstance(value, str):
        return {value}
    if isinstance(value, list):
        return {str(item) for item in value}
    if isinstance(value, dict):
        return {str(key) for key in value}
    return set()


def _run_lines(workflow: dict) -> list[str]:
    """Every line of every step's `run` in every job, stripped."""
    lines: list[str] = []
    for job in (workflow.get("jobs") or {}).values():
        for step in job.get("steps") or []:
            run = step.get("run")
            if isinstance(run, str):
                lines.extend(line.strip() for line in run.splitlines() if line.strip())
    return lines


def test_001_us4_ac3_ci_checks_placeholders_and_bundled_files(repo_root, tool, skill):
    """US4-AC3: **Given** the plugin's commands, **When** CI checks them, **Then** none contains a
    Claude Code placeholder (`$ARGUMENTS`, `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_SKILL_DIR}`), and
    every file a command reads lives in its own skill folder (T12).

    Provenance: 001 spec.md
    """
    # CI runs the checker with no --rule filter, on push and pull request
    ci_file = repo_root / CI_PATH
    assert ci_file.is_file(), f"{CI_PATH} not found"
    workflow = yaml.safe_load(ci_file.read_text(encoding="utf-8"))
    assert isinstance(workflow, dict), f"{CI_PATH} is not a YAML mapping"

    triggers = _triggers(workflow)
    assert {"push", "pull_request"} <= triggers, (
        f"{CI_PATH} runs on {sorted(triggers)}, not on push and pull_request"
    )

    check_lines = [line for line in _run_lines(workflow) if line.startswith("python tools/check.py")]
    assert check_lines, f"{CI_PATH} has no step running python tools/check.py"
    unfiltered = [line for line in check_lines if "--rule" not in line and "--only" not in line]
    assert unfiltered, (
        f"{CI_PATH} runs python tools/check.py only with a filter: {check_lines}"
    )

    # the placeholders and bundled-files rules hold on the repository today
    result = tool(
        "check", "--root", str(repo_root), "--rule", "placeholders", "--rule", "bundled-files"
    )
    assert result.returncode == 0, (
        f"check.py --rule placeholders --rule bundled-files exited {result.returncode}: "
        f"{result.stdout}{result.stderr}"
    )

    # every SKILL.md's input section says the literal II-6 sentence
    skill_files = sorted((repo_root / "skills").glob("*/SKILL.md"))
    assert skill_files, "no skills/*/SKILL.md found"
    lacking = [
        path.parent.name
        for path in skill_files
        if skill(path.parent.name).missing(INPUT_SENTENCE)
    ]
    assert not lacking, f"no input sentence {INPUT_SENTENCE!r} in {lacking}"
