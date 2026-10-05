---
type: regex
target: last_message
pattern: 'Red first at W2\W{0,4}\(\W{0,2}[0-9a-f]{7,}\W{0,2}\)\W{0,4}:?[^\n]*large_notebook_exports_one_row_per_note[^\n]*green at W1\W{0,4}\(\W{0,2}[0-9a-f]{7,}'
match: contains
weight: 1
---

The report names the red test and the first wave commit of the slice where it alone goes red,
in RR-7's line: `Red first at W2 (<sha>): test_export_rows.py::test_a_large_notebook_exports_one_row_per_note — green at W1 (<sha>)`.
