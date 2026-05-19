# Thesis TODO

Single living checklist of remaining work before submission. Merged from
the former `TODO.md` and the TODO sections of `discussion.md`. Grouped
by priority, not by chapter. `discussion.md` remains the working
scratchpad for the Discussion chapter (case studies, section outline,
prose ideas) — it no longer holds todos.

---

## Recently completed (last review passes)

- Citation sanity check — orphan bib entries (`liLegalAgentBenchEvaluatingLLM2025`,
  `zhouLawGPTKnowledgeGuidedData2025`) deleted; `\nocite` template entries
  (Sturm2012, Voss2010, Knappen2009, Mittelbach2005, Schlosser2014)
  removed from `main.tex` backmatter; all remaining `\cite{...}`
  resolve cleanly.
- Methodology — Mann--Whitney $U$ + Kruskal--Wallis reframed from
  "sensitivity check" to primary between-groups test family.
- Methodology — statistical-test definitions regrouped by usage (survey
  vs. document-quality vs. ranking) with a plain-language reading of
  each test value.
- Methodology — `\subsection*` headers converted to numbered
  `\subsection` for ROPAgen (3.1.1--3.1.3) and User Study
  (3.2.1--3.2.7).
- Methodology — Fig.\ 3.1 (project timeline) rotated to landscape via
  `sidewaysfigure`.
- Evaluation — chapter introduction now states the survey inferential
  family (Friedman + Wilcoxon) alongside the existing NLP/timing
  statement (Kruskal--Wallis + Mann--Whitney $U$) and the ranking
  chi-square goodness-of-fit.
- Evaluation — SUS composite reporting: non-significant Friedman omnibus
  now stated cleanly; pairwise post-hocs no longer claimed where the
  omnibus does not clear the threshold.
- Evaluation — ranking section now reports the chi-square result
  directly without hedging against a non-significant complementary
  Friedman.
- Tables — all full-distribution tables (4.1, 4.4, 4.6, 4.8, 4.10,
  4.11) standardized to column order Mean | SD | Q1 | Median | Q3 |
  Min | Max; SUS / AI per-item tables (4.4, 4.8) expanded with full
  item text and laid out landscape.
- Tables — `mean (SD)` format standardized across compact mean-by-mode
  tables (4.5, 4.21) to match the chapter-level NLP tables
  (4.12--4.18).
- Introduction — `\section{Thesis Structure}` added at the end of
  Chapter~1 with one-paragraph blurbs for each subsequent chapter,
  including the case studies.
- Introduction — original hypothesis (Chat $\succ$ Form $\succ$ Ask)
  recorded as a `\paragraph{Prior expectation.}` immediately after the
  RQs, framed as the prediction the study tests.
- Introduction — empty `\section{Objectives and Contributions}` stub
  removed.
- Appendix C — sample-size discrepancy fixed (was 70, should have been
  69, matching the canonical `python/output/sample_sizes.md`).
- Spelling — full thesis converted to American English (narrative
  text); verbatim prompts and German source artifacts preserved.
- Labels — `ch:background` and `ch:conclusion` added so all
  Thesis-Structure cross-references resolve.

---

## P0 — Content gaps (must close before defence)

### ROPAgen appendix (Appendix D)

- [ ] **Three mode screenshots.** Form/Ask/Chat UI captures on the same
      scenario step for visual comparability. Section frames and labels
      already exist in `appendix_ropagen.tex` (\S~D.2.1/2/3); only the
      PNGs themselves are missing. Emilija is supplying these.

### Discussion (currently a stub — extensive prep in `discussion.md`)

The case-study data, section outline, argumentative spine, related-work
hooks, and limitations list are all in `discussion.md`. The decisions
and drafting items below need to happen before/while turning the
scratchpad into LaTeX.

**Decisions to settle before drafting:**

- [ ] Include both case studies (AEB2451 + IAR1116) or just AEB2451 alone?
- [ ] Case studies inline in §4 (confidence-gap) or as their own §6?
- [ ] Lead claim: confidence-gap-first or Form-paradox-first?
- [ ] Target length — `discussion.md` proposes ~8--10 pages. Confirm.
- [ ] Design implications: inline per finding section, or collected as
      a dedicated §7?
- [ ] Hybrid-mode sketch (Form structure + Chat context, surfaced
      repeatedly in freeform comments): worth a paragraph in §5, a
      standalone subsection, or only in Conclusion future-work?

**Content to draft:**

- [ ] **RQ1 synthesis** — pull the Form-first ordering across SUS,
      R-TLX, ranking, and item-6 reuse into one coherent narrative.
      The interesting tension is item-3 transparency / item-5
      confidence *favoring* Ask/Chat against the broader Form-first
      pattern.
- [ ] **RQ2 + the confidence--quality gap** — heart of the thesis
      argument. Use the Spearman correlations
      (`tab:app-corr-primary`) and the Judge
      Form-Completeness/Hallucination co-occurrence
      ($83.8\,\%$ of Form documents combine Completeness $= 5$ with
      Hallucination(inv) $\leq 2$) as the empirical core. Frame:
      confidence is uncalibrated because input scaffolding does not
      scaffold output truth.
- [ ] **Surface the confidence--quality correlations in the body.**
      They live in Appendix~C.4 but no body chapter references them.
      Decide whether to surface in the judge synthesis (§4.3.2),
      only in Discussion, or both. Headline number: Chat-only
      positive correlation with Judge Overall
      ($\rho = +0.41$, $p = 0.012$).
- [ ] **Comparison with von Schwerin et al.** — Methodology cites their
      metric suite. Discussion should circle back: do the orderings
      observed here align with theirs? Where do they diverge?
- [ ] **Judge descriptive-only treatment.** Acknowledge that the judge
      section is intentionally descriptive (single judge, no
      inter-rater variance, framed as indicative). Explain why no
      Friedman/Wilcoxon is reported on the rubric dimensions.
- [ ] **Limitations** — single scenario, novice-only sample, single
      reference document for NLP metrics, single judge model. Tie
      each limitation to a specific affected claim. Full list in
      `discussion.md`.
- [ ] **Pull per-chapter NLP numbers** for §3 (Retention / T\&O lead) —
      both the chapter-level table values and the boxplot direction.
- [ ] **Decide chapter-level inferential citation style** — explicit
      Friedman/MW reference for §3 chapter-level points, or descriptive
      direction only.
- [ ] **One more pass on German free-text translations** — the IAR1116
      summary quote in `discussion.md` §6 is raw German with a draft
      gloss; verify both case studies' quotes for accuracy.

### Conclusion (stub)

- [ ] **Direct, declarative answers to RQ1 and RQ2.** Two short
      paragraphs. No new data. Just the answer and its consequence.
- [ ] **Future work** — hybrid mode (Form structure + Chat
      conversation) surfaced repeatedly in the freeform comments;
      multi-judge or legal-expert validation of the judge layer;
      longitudinal study of novice $\rightarrow$ expert transition;
      replication on a non-employment scenario.
- [ ] *(Optional)* **Implications for ROPAgen** — a sentence or two on
      what the team should change about the tool given these findings,
      since Magdalena is the supervisor. Keep academic.

---

## P1 — Polish (after content is settled)

- [ ] **Terminology consistency (continued).** Already applied:
      ROPA (was RoPA); "LLM support" (was "involvement"); AI
      questionnaire item wording reconciled. Still to do: Form/Ask/Chat
      capitalization across all chapters and tables; AI vs LLM where
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
      tokens (e.g.\ JSON field names, ALL-CAPS keywords) don't break.
      Cosmetic; can be tightened with a more aggressive breakindent
      or by switching to `listingsutf8`.
- [ ] **Typo / orphan / widow pass.** Last-mile read-through, ideally
      after a 24h cooling period.
- [ ] **Final formatting check** — page numbers, margins, font size,
      heading style match University of Ulm / DBIS thesis template.

---

## P2 — Structure overhaul (last)

- [ ] **Chapter-level structure pass.** Re-evaluate after all content
      is in. Likely candidates:
      - Background may need trimming if content drifts toward
        Methodology.
      - Discussion may grow large enough to warrant section
        subdivision (RQ1 / RQ2 / Implications / Limitations) — the
        current `discussion.md` outline already does this.
- [ ] **Front matter polish.** Title page, declaration, dedication.
