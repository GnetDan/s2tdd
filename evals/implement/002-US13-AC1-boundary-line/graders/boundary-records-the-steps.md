---
{type: llm, focus: trace, weight: 1}
---

After wave 2's commit the relay ran the boundary steps: it read usage once (or wrote `n/a` for
the windows, where no usage tool exists), checked for BRAKES (`.sdd-run/004/BRAKES`), and
appended the ledger's lines; then it wrote wave 2's report with `Boundary: context <x>% ·
five-hour <y>% · week <z>% · BRAKES <none|found> · ledger +<n> lines`, whose values are what
those steps found (BRAKES none: no BRAKES file exists; `<n>`: the lines it appended).
