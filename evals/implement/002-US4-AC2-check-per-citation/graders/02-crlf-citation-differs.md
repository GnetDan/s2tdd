---
type: regex
target: last_message
pattern: '(ends_every_row_with_crlf|CRLF|\\r\\n)[^\n]*\bdiffers\b|\bdiffers\b[^\n]*(CRLF|\\r\\n)'
flags: i
weight: 1
---

The verdict has a line for P0a's line-end citation saying it differs: the test asserts CRLF row
ends where §II-1 says LF on every platform.
