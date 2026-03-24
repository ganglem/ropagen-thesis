---
name: commit
description: Create focused git commits, always split by subfolder/domain. Never commit all changes at once.
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# /commit — Focused Git Commits

**Arguments:** $ARGUMENTS

---

## Rules

**Never commit all changes in a single commit.** Changes must always be split by subfolder or domain. Each logical unit of work gets its own commit. Subfolders can be split further if they contain unrelated changes.

## Instructions

1. Run `git status` and `git diff` to understand all staged and unstaged changes.

2. Group changes by subfolder/domain. Typical groups for this repo:
   - `python/` — notebooks, data, scripts, metrics
   - `thesis/` — LaTeX chapters, figures, bibliography
   - `.claude/` — agent config, skills, settings
   - Root-level files — `CLAUDE.md`, `README.md`, etc.

3. For each group (one at a time, never together):
   a. Review the diff for that group to understand what changed and why.
   b. If the group contains clearly unrelated changes, split it further into sub-commits.
   c. Stage only those files: `git add <specific files>` — never `git add .` or `git add -A`.
   d. Write a concise commit message: imperative mood, one line, no fluff. State *what* changed and *why* if not obvious.
   e. Commit.

4. After all commits, run `git log --oneline -10` to show the result.

5. Report back: list each commit made (hash + message), one line each.

## Commit message style

- Imperative mood: "add X", "fix Y", "update Z"
- Max ~60 characters
- No bullet lists in the message body unless truly necessary
- No "Co-Authored-By" lines unless the user asks

