---
name: python
description: Delegate a task to the Python/Statistics agent. Use when the task involves data analysis, NLP metrics, notebook edits, survey statistics, or visualisation work. Arguments become the task handed to the agent.
user-invocable: true
allowed-tools:
  - Agent
  - Read
  - Glob
  - Grep
---

# /python — Delegate to Python / Statistics Agent

Spawn a subagent to handle a data analysis or notebook task. The subagent has exclusive write access to the `/python` folder and acts as the statistics specialist for this thesis.

**Task from user:** $ARGUMENTS

---

## Instructions

1. Read `/mnt/c/Dev/ropagen-bert/python/CLAUDE.md` to load the agent's full context.
2. Spawn a **general-purpose** subagent with the following briefing:

> You are the Python / Statistics agent for Emilija's Master's thesis on ropagen and GDPR ROPA documentation. Your full role, conventions, and context are defined in `/mnt/c/Dev/ropagen-bert/python/CLAUDE.md` — read it before proceeding.
>
> You have **exclusive write access** to `/mnt/c/Dev/ropagen-bert/python/`. Do not edit files outside this folder.
>
> The two notebooks are:
> - `python/survey/ROPAgen_SURVEY.ipynb` — SUS, NASA-TLX, confidence, mode preferences
> - `python/metrics/ROPAgen_METRICS.ipynb` — BLEU, ROUGE, METEOR, BERTScore, SBERT
>
> Task: $ARGUMENTS

3. Return the subagent's full response to the user.
