---
description: "US8-AC2: Given an existing constitution at version 1.1.0, When the user amends a principle with `/s2tdd-constitution`, Then the file's version is bumped and a dated change note is added in the file (T11)."
max_turns: 40
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Bash, Write, Edit]
---

/s2tdd-constitution Amend principle II (Small changes): a pull request may change at most 400 lines. Take the recommended answer to any question.

The project is the git repository in ./acme-notes: work there.
