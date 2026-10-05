# US6-AC6: refuse in a cloud session

The scenario needs `CLAUDE_CODE_REMOTE=true` in the run's environment (R2). A case cannot set
it: its `env` key takes `EVAL_*` names only (II-14, J-17), and this case sets none. So the
case's `prompt.md` and graders describe the check, and the run that records it under V5 is the
`claude -p` fallback from contracts/eval-suite.md, on the same fixture:

```bash
CLAUDE_CODE_REMOTE=true claude -p "/s2tdd-pr-review 1"
```

`run-fallback.sh` does all of it: it builds `scaffold.sh`'s fixture in a temporary directory,
runs the line above there with this repository as the plugin, and checks the reply for the
refusal text (II-8: "start it locally with `--cloud`"):

```bash
bash evals/cloud/US6-AC6-refuse-in-cloud/run-fallback.sh        # from the repository root
```

Needs Linux, macOS or WSL (the case grants `Bash`; II-14's Platform line) and a live model.
Record its output under `validation.md` `## V5`.

Without the variable, the plain `claude plugin eval` run of this case sees a local session and
does not refuse, so a failing score for this case there is expected and not a defect.
