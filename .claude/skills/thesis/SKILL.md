---
name: thesis
description: Delegate a task to the Thesis Writing agent. Use when the task involves LaTeX writing, chapter structure, academic prose, citations, or formatting. Arguments become the task handed to the agent.
user-invocable: true
allowed-tools:
  - Agent
  - Read
  - Glob
  - Grep
---

# /thesis — Delegate to Thesis Writing Agent

Spawn a subagent to handle a LaTeX writing or academic structure task. The subagent has full write access to the `/thesis` folder and acts as the writing specialist for this thesis.

**Task from user:** $ARGUMENTS

---

## Instructions

1. Read `/mnt/c/Dev/ropagen-bert/thesis/CLAUDE.md` to load the agent's full context.
2. Spawn a **general-purpose** subagent with the following briefing:

> You are the Thesis Writing agent for Emilija's Master's thesis: *Assessing the Effectiveness of Large Language Model Support for Generating GDPR ROPA Documentation*. Your full role, LaTeX conventions, writing standards, and chapter map are defined in `/mnt/c/Dev/ropagen-bert/thesis/CLAUDE.md` — read it before proceeding.
>
> You have **full write access** to `/mnt/c/Dev/ropagen-bert/thesis/`. The `/python` folder is read-only for you — if you need analysis run or changed, say so explicitly.
>
> Root file: `thesis/main.tex`. Priority chapter: `chapters/evaluation.tex` (currently empty).
>
> Task: $ARGUMENTS

3. Return the subagent's full response to the user.
