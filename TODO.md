# Thesis TODO

Living checklist of remaining work before submission. Grouped by priority,
not by chapter — chapter-level reorganisation is the very last step.

---

## P0 — Content gaps (must close before defence)

### ROPAgen appendix (Appendix D)

- [ ] **Three mode screenshots.** Form/Ask/Chat UI captures on the same
      scenario step for visual comparability. Section frames and labels
      already exist in `appendix_ropagen.tex` (\S~D.2.1/2/3); only the
      PNGs themselves are missing. Emilija is supplying these.

---

## P0 — Missing chapters (Discussion + Conclusion)

*These are out of scope for the current polish pass; listed here so they
are not lost.*

### Discussion (currently a stub)

- [ ] **RQ1 synthesis** — pull the Form-first ordering across SUS,
      R-TLX, ranking, and item-6 reuse into one coherent narrative.
      The interesting tension is item-3 transparency / item-5
      confidence *favouring* Ask/Chat against the broader Form-first
      pattern.
- [ ] **RQ2 + the confidence–quality gap** — heart of the thesis
      argument. Use the Spearman correlations + the Judge
      Form-Completeness/Hallucination co-occurrence
      (83.8% of Form documents combine Completeness=5 with
      Hallucination(inv) ≤ 2) as the empirical core. Frame: confidence
      is uncalibrated in Form because the form-fill scaffolds
      completeness without scaffolding faithfulness.
- [ ] **Confidence–quality body pointer (moved from Evaluation gaps).**
      The correlation results live in `tab:app-corr-primary`
      (Appendix~C.4) but the body currently has no reference to
      them. Decide as part of Discussion drafting whether to surface
      them in the judge Synthesis subsection (§4.3.2), only in
      Discussion, or both. Headline number: Chat-only positive
      correlation with Judge Overall (ρ = +0.41, p = 0.012).
- [ ] **Comparison with von Schwerin et al.** — the methodology
      chapter references their metric suite. Discussion should circle
      back: do the orderings observed here align with their findings?
      Where do they diverge?
- [ ] **Judge descriptive-only treatment.** Acknowledge that the judge
      section is intentionally descriptive (single judge, no
      inter-rater variance, framed as indicative). Explain why no
      Friedman/Wilcoxon is reported on the rubric dimensions.
- [ ] **Limitations** — single scenario, novice-only sample, single
      reference document for NLP metrics, single judge model. Tie each
      limitation to a specific affected claim.

### Conclusion (stub)

- [ ] **Direct, declarative answers to RQ1 and RQ2.** Two short
      paragraphs. No new data. Just the answer and its consequence.
- [ ] **Future work** — hybrid mode (Form structure + Chat
      conversation) surfaced repeatedly in the freeform comments;
      multi-judge or legal-expert validation of the judge layer;
      longitudinal study of novice → expert transition; replication on
      a non-employment scenario.
- [ ] *(Optional)* **Implications for ROPAgen** — a sentence or two
      on what the team should change about the tool given these
      findings, since Magdalena is the supervisor. Keep academic.

---

## P1 — Polish (after content is settled)

- [ ] **Citation sanity check.** Run a pass over `bibliography.bib` —
      every `\cite{...}` resolves, no orphans, fields complete
      (title/author/year/venue minimum). The biblatex warnings about
      Sturm2012, Voss2010, Knappen2009, Mittelbach2005, Schlosser2014
      are `\nocite` template entries in `main.tex` backmatter — delete
      or fill.
- [ ] **Terminology consistency (continued).** Already applied this
      pass: ROPA (was RoPA), "LLM support" (was "involvement"), AI
      questionnaire item wording reconciled. Still to do: Form/Ask/Chat
      capitalisation across all chapters and tables; AI vs LLM where
      the distinction matters; novice vs non-expert.
- [ ] **English/German consistency.** Free-text comments are German
      with English glosses; check every quoted German phrase has its
      gloss. Check chapter names (Verantwortliche Stelle… vs.
      Controller and Contact Details) are consistent across body and
      tables.
- [ ] **List of figures / list of tables.** Currently not in the
      front matter. Add via `\listoffigures` / `\listoftables` after
      `\tableofcontents` if required by the thesis template.
- [ ] **Abstract / Zusammenfassung.** University of Ulm typically
      requires both — verify with the DBIS template.
- [ ] *(Optional)* **Acknowledgements.** Conventional but not
      required.
- [ ] **Overfull-hbox cleanup in Appendix D.** ~113 overfull hbox
      warnings, all inside `lstlisting` blocks where long unbroken
      tokens (e.g. JSON field names, ALL-CAPS keywords) don't break.
      Cosmetic; can be tightened with a more aggressive breakindent
      or by switching to `listingsutf8`.
- [ ] **Typo / orphan / widow pass.** Last-mile read-through, ideally
      after a 24h cooling period.
- [ ] **Cross-reference verification.** `latexmk` clean; no "??" in
      the PDF; every `\ref` resolves; all `\S` references point to
      live labels. Verified clean as of this commit (only screenshots
      P0 item left, which is image inclusion not LaTeX).
- [ ] **Final formatting check** — page numbers, margins, font size,
      heading style match University of Ulm / DBIS thesis template.

## P2 — Structure overhaul (last)

- [ ] **Chapter-level structure pass.** Re-evaluate after all content
      is in. Likely candidates:
      - Methodology may want subsection reordering once the timeline
        figure is added.
      - Background may need trimming if content drifts toward
        Methodology.
      - Discussion may grow large enough to warrant section
        subdivision (RQ1 / RQ2 / Implications / Limitations).
- [ ] **Front matter polish.** Title page, declaration, dedication.

---

