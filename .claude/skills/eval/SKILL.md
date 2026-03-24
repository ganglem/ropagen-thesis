---
name: eval
description: Coordinate work on the Evaluation chapter — the most urgent thesis gap. Routes analysis to the python agent and writing to the thesis agent. Use with a specific sub-task (e.g. "RQ1 usability results", "BERTScore comparison table") or no arguments for a full coordination plan.
user-invocable: true
allowed-tools:
  - Agent
  - Read
  - Glob
  - Grep
---

# /eval — Evaluation Chapter Coordinator

The Evaluation chapter (`thesis/chapters/evaluation.tex`) is currently empty and is the highest-priority gap in the thesis. This skill coordinates the pipeline: data → analysis → prose.

**Specific task (if any):** $ARGUMENTS

---

## Evaluation chapter structure

The chapter should follow this skeleton (from `thesis/CLAUDE.md`):

1. **Overview** — recap of analysis plan, what this chapter covers
2. **RQ1: User Experience**
   - Usability (SUS scores by mode)
   - Cognitive load (NASA R-TLX dimensions by mode)
   - Confidence (Likert items by mode)
   - Mode preferences and rankings
3. **RQ2: Document Quality**
   - Metric results by mode (BLEU, ROUGE, METEOR, BERTScore, SBERT)
   - Statistical significance (ANOVA / post-hoc results)
   - Confidence–quality gap analysis
4. **Summary** — one paragraph linking RQ1 and RQ2 findings, setting up Discussion

---

## Instructions

If `$ARGUMENTS` is empty or is "plan": produce a coordination plan — which sections need what analysis, what the python agent should run first, what the thesis agent should draft once results are ready. Be specific.

If `$ARGUMENTS` names a specific section or task:
1. Determine whether the task is primarily **analysis** (→ python agent) or **writing** (→ thesis agent) or **both**.
2. For analysis tasks: spawn a python agent subagent (as per `/python` skill pattern — read `python/CLAUDE.md`, delegate the specific analysis).
3. For writing tasks: spawn a thesis agent subagent (as per `/thesis` skill pattern — read `thesis/CLAUDE.md`, delegate with any relevant data already gathered).
4. For tasks requiring both: run analysis first, then pass results to the writing subagent.
5. Return a synthesised result.

Always reference specific metric values when available from `python/metrics/output/evaluation_results.csv`. Never invent numbers.
