# Thesis TODO

Living checklist of remaining work before submission. Grouped by priority,
not by chapter — chapter-level reorganisation is the very last step.

---

## P0 — Content gaps (must close before defence)

### Data integrity
- [ ] **Recheck all numeric data for correctness.** Re-run notebooks end-to-end;
      diff outputs against tables in `evaluation/*.tex`. Pay particular
      attention to: matched-triple n's (n=69 survey, n=26 NLP), per-mode
      counts (37/37/39), and the BERTScore Recall Form-vs-Ask r=+1.000
      (looks suspiciously perfect — verify it's not a tie-handling artefact).

### ROPAgen chapter (NEW, sits before Evaluation)
- [ ] **Dedicated ROPAgen chapter.** Sits between Methodology and
      Evaluation. Covers: who built the tool (DBIS / Uni Ulm), what
      it does, the LLM (Mistral Large 3) backing it, and a detailed
      walk-through of the three interaction modes
      (Form / Ask / Chat) with screenshots for each. This is where
      the reader builds the mental model of *the tool under study*
      that the rest of the thesis evaluates. Distinct from
      `methodology.tex`, which describes the *study*, not the *tool*.
- [ ] **Screenshots of the three modes.** Belong in the ROPAgen
      chapter above (one per mode, ideally captured on the same
      scenario step for visual comparability).
- [ ] **Example generated ROPA documents.** One per mode, same
      participant if possible. Either inside the ROPAgen chapter
      as illustrative figures, or in an appendix referenced from it.

### Methodology
- [ ] **User-study timeline / BPMN diagram.** A figure showing the
      participant journey: consent → demographics → mode 1 (instrument
      battery) → mode 2 → mode 3 → final ranking → free-text. Either
      a swimlane / BPMN diagram or a simple horizontal timeline. Place
      in `chapters/methodology.tex` near the procedure description.
- [ ] **Counterbalancing detail review.** Verify the Latin Square
      description in methodology matches the actual group assignments
      in `python/survey/`. Six groups → 6×k participants, where k = ?

### Evaluation gaps
- [ ] **Justify in body why confidence–quality correlations live
      appendix-only.** Decision: keep them in
      `appendix_inferential.tex` (`tab:app-corr-primary`), but add
      one short paragraph in the body — likely at the end of the
      Judge section or in `summary.tex` — that points at the table
      and notes the Chat-only positive correlation
      (ρ = +0.41, p = 0.012 vs Judge Overall) without re-tabulating.
      Detailed interpretation belongs in Discussion.
- [ ] **Brief mention of judge descriptive-only treatment in
      Discussion.** The Judge section is intentionally descriptive
      (single judge, no inter-rater variance to model, framed as
      indicative). Add a sentence in Discussion acknowledging this
      and explaining why no Friedman/Wilcoxon is reported on the
      rubric dimensions. No new analysis needed.

### Discussion (currently a stub)
- [ ] **RQ1 synthesis** — pull the Form-first ordering across SUS, R-TLX,
      ranking, ranking, and item-6 reuse into one coherent narrative.
      The interesting tension is item-3 transparency / item-5 confidence
      *favouring* Ask/Chat against the broader Form-first pattern.
- [ ] **RQ2 + the confidence–quality gap** — this is the heart of the
      thesis argument. Use the Spearman correlations + the Judge
      Form-Completeness/Hallucination co-occurrence (83.8% of Form
      documents combine Completeness=5 with Hallucination(inv) ≤ 2) as
      the empirical core. Frame: confidence is uncalibrated in Form
      because the form-fill scaffolds completeness without scaffolding
      faithfulness. (This was already pre-flagged in
      `project_thesis_framing.md`.)
- [ ] **Comparison with von Schwerin et al.** — the methodology chapter
      references their metric suite. Discussion should circle back: do
      the orderings observed here align with their findings? Where do
      they diverge?
- [ ] **Limitations** — single scenario, novice-only sample, single
      reference document for NLP metrics, single judge model. Keep
      honest; tie each limitation to a specific affected claim.

### Conclusion (stub)
- [ ] **Direct, declarative answers to RQ1 and RQ2.** Two short
      paragraphs. No new data. Just the answer and its consequence.
- [ ] **Future work** — hybrid mode (Form structure + Chat conversation)
      surfaced repeatedly in the freeform comments; multi-judge or
      legal-expert validation of judge layer; longitudinal study of
      novice → expert transition; replication on a non-employment
      scenario.
- [ ] *(Optional)* **Implications for ROPAgen** — a sentence or two
      on what the team should change about the tool given these
      findings, since Magdalena is the supervisor. Keep academic if
      it feels out of place.

### Appendices / supplementary
- [ ] **Backend prompt(s) sent to ROPAgen.** The prompt the *Mistral
      backend* receives on each user turn (per mode). Distinct from
      the LLM-as-Judge prompt already in `app:judge-prompt`.
      Retrievable from the ropagen repo on GitHub
      (`ganglem/ropagen`). Either a new appendix chapter, or rename
      "LLM-as-a-Judge Configuration" → "LLM Configuration" with
      sub-sections for backend (ropagen) vs judge.
- [ ] **Reference document** — the expert-authored ROPA used as the
      NLP reference. Currently described but not reproduced. Should
      be in an appendix; reproducibility-critical.

---

## P1 — Polish (after content is settled)

- [ ] **Citation sanity check.** Run a pass over `bibliography.bib` —
      every `\cite{...}` resolves, no orphans, fields complete
      (title/author/year/venue minimum). The biblatex warnings about
      Sturm2012, Voss2010, Knappen2009, Mittelbach2005, Schlosser2014
      are `\nocite` template entries — delete or fill.
- [ ] **Terminology consistency.** Pick canonical forms and apply
      throughout: ROPA vs RoPA vs Ropa; ropagen vs ROPAgen vs
      ROPAGen; Form/Ask/Chat capitalisation; *AI* vs *LLM*; *novice*
      vs *non-expert*.
- [ ] **English/German consistency.** Free-text comments are German
      with English glosses; check every quoted German phrase has its
      gloss; check chapter names (Verantwortliche Stelle… vs.
      Controller and Contact Details) are consistent across body
      and tables.
- [ ] **List of figures / list of tables.** Currently not in the
      front matter. Add via `\listoffigures` / `\listoftables` after
      `\tableofcontents` if required by the thesis template.
- [ ] **Abstract / Zusammenfassung.** University of Ulm typically
      requires both — verify with the DBIS template.
- [ ] *(Optional)* **Acknowledgements.** Conventional but not
      required.
- [ ] **Typo / orphan / widow pass.** Last-mile read-through, ideally
      after a 24h cooling period.
- [ ] **Cross-reference verification.** `latexmk` clean; no "??" in
      the PDF; every `\ref` resolves; all `\S` references point to
      live labels.
- [ ] **Final formatting check** — page numbers, margins, font size,
      heading style match University of Ulm / DBIS thesis template.

## P2 — Structure overhaul (last)

- [ ] **Chapter-level structure pass.** Re-evaluate after all content
      is in. Likely candidates:
      - Methodology may want subsection reordering once ROPAgen
        explanation and timeline figure are added.
      - Background may need trimming if content drifts toward
        Methodology.
      - Discussion may grow large enough to warrant section
        subdivision (RQ1 / RQ2 / Implications / Limitations).
- [ ] **Front matter polish.** Title page, declaration, dedication.

---

## Inferential coverage status (as of restructure)

For reference — what's currently *in the body* vs *appendix-only*:

| Test family               | Body | Appendix |
|---------------------------|:----:|:--------:|
| Shapiro–Wilk normality    |  —   |    ✓     |
| Friedman omnibus (survey) |  ✓   |    ✓     |
| Wilcoxon post-hoc (survey)|  ✓   |    ✓     |
| Mode-pref χ² + Friedman   |  ✓   |    ✓     |
| Friedman omnibus (NLP)    |  ✓   |    ✓     |
| Wilcoxon post-hoc (NLP)   |  ✓   |    ✓     |
| Kruskal–Wallis sens.      |  —   |    ✓     |
| Mann–Whitney sens.        |  —   |    ✓     |
| Spearman conf×quality     |  —   |    ✓     |
| Friedman / Wilcoxon (judge) |  —   |    —     |

The bottom three rows (sensitivity checks + correlations + judge
inferentials) are the visible gaps. Sensitivity checks are
appropriately appendix-only; correlations and judge tests should
move into the body or get explicit narrative coverage.
