# ROPAgen Thesis

[![Compile Thesis](https://github.com/ganglem/ropagen-thesis/actions/workflows/compile-thesis.yml/badge.svg)](https://github.com/ganglem/ropagen-thesis/actions/workflows/compile-thesis.yml)
&nbsp;[**Read the thesis (PDF)**](https://ganglem.github.io/ropagen-thesis/thesis.pdf)

[![Compile Presentation](https://github.com/ganglem/ropagen-thesis/actions/workflows/compile-presentation.yml/badge.svg)](https://github.com/ganglem/ropagen-thesis/actions/workflows/compile-presentation.yml)
&nbsp;[**View the defense slides (PDF)**](https://ganglem.github.io/ropagen-thesis/presentation.pdf)

---

Research repository for the Master's thesis:

> **Assessing the Effectiveness of Large Language Model Support for Generating GDPR ROPA Documentation**
> Emilija Kastratović — University of Ulm, 2025/2026

## What this is

[ropagen](https://ropagen.eu) is an LLM-powered tool (University of Ulm, DBIS) that helps users create GDPR Records of Processing Activities (ROPA) documents. This repo contains the study data, analysis notebooks, and thesis LaTeX source evaluating ropagen's three interaction modes — **Form**, **Ask**, and **Chat** — across 73 participants.

## Structure

```
python/                 # Data analysis — Jupyter notebooks, NLP metrics, survey statistics
thesis/                 # LaTeX thesis source
thesis/presentation/    # Defense slides — uulm Beamer deck (main.tex)
jester/                 # You don't need to worry about this one
```

The defense slides are built by the **Compile Presentation** workflow on every
push to `thesis/presentation/**`. Each run uploads `presentation.pdf` as a
downloadable artifact and publishes it to GitHub Pages (linked by the badge above).

## Setup

**Python environment** (requires Python 3.10+):

```bash
cd python
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**Notebooks:**

```
python/survey/ROPAgen_SURVEY.ipynb    — SUS, NASA-TLX, confidence, mode preferences
python/metrics/ROPAgen_METRICS.ipynb  — BLEU, ROUGE, METEOR, BERTScore, SBERT
```

Open with Jupyter Lab or VS Code.

**Thesis** (requires a LaTeX distribution, e.g. TeX Live or MiKTeX):

```bash
cd thesis
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```

## Claude agents

This project is developed with the assistance of [Claude Code](https://claude.ai/claude-code). Three specialised agents collaborate on the work:

| Agent | Responsibility |
|-------|---------------|
| Orchestrator | Thesis-wide strategy, academic framing, coordination |
| `/python` | Statistical analysis, notebooks, NLP metrics |
| `/thesis` | LaTeX writing, chapter structure, academic prose |

Agent instructions live in `CLAUDE.md` files throughout the repo (`./CLAUDE.md`, `python/CLAUDE.md`, `thesis/CLAUDE.md`).
