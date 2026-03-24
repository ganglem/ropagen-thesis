---
name: status
description: Show the current state of the thesis — which chapters are complete, what data/notebooks exist, and what the most urgent next steps are.
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# /status — Thesis Status Check

Give a concise, accurate snapshot of where the thesis stands right now.

---

## Instructions

Run the following checks in parallel, then synthesise:

### 1. Chapter status
Read each of these files and report word count / content state (empty, stub, partial, complete):
- `thesis/chapters/introduction.tex`
- `thesis/chapters/background.tex`
- `thesis/chapters/methodology.tex`
- `thesis/chapters/evaluation.tex`
- `thesis/chapters/discussion.tex`
- `thesis/chapters/conclusion.tex`
- `thesis/chapters/sources.tex`

### 2. Notebook outputs
Check whether the notebooks have outputs (i.e. have been run):
- `python/survey/ROPAgen_SURVEY.ipynb`
- `python/metrics/ROPAgen_METRICS.ipynb`

Check if output artefacts exist:
- `python/metrics/output/` — list any CSVs or PNGs
- `python/survey/output/` — list any files

### 3. Metrics data
Check `python/metrics/output/evaluation_results.csv` — does it exist, how many rows?

---

## Output format

```
## Thesis Status — [today's date]

### Chapters
| Chapter        | Status   | Notes |
|---------------|----------|-------|
| Introduction   | ...      | ...   |
...

### Data & Notebooks
- survey notebook: [run / not run]
- metrics notebook: [run / not run]
- evaluation_results.csv: [exists, N rows / missing]
- output figures: [list or none]

### Most urgent next steps
1. ...
2. ...
3. ...
```

Be specific. If evaluation.tex is empty, say so. If the notebooks have no outputs, flag it.
