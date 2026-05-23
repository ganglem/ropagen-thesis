# Statistical Test Results — NLP Metrics

Source: `python/metrics/ROPAgen_METRICS.ipynb` (markdown interpretation cells 28
and 33). Sample sizes: see `python/output/sample_sizes.md` (canonical).

---

## Dataset

- **N = 113 documents total**: Form n=37, Ask n=37, Chat n=39
- **Within-subjects subset**: **n = 26** participants with exactly one document
  per mode — used for Friedman test and Wilcoxon signed-rank post-hoc.
- 47 unique participants are represented in total; 28 have at least one
  document in each mode but three of them have duplicates in some mode and
  are excluded from the strict matched set.

---

## Normality Testing (Shapiro-Wilk)

Non-normal distributions detected in:
- BLEU (multiple modes)
- BERTScore Recall (Ask, Chat)
- SBERT (Form, Ask)

Non-parametric tests used throughout.

---

## Kruskal-Wallis H Test (full dataset, n = 113, unbalanced)

Tests whether at least one mode distribution differs from the others. Reported
as a **between-groups sensitivity check** on the unbalanced full sample; not the
primary post-hoc family.

| Metric | H | p-value | Significant (α=0.05) | ε² (effect size) |
|---|---|---|---|---|
| BLEU | 4.48 | 0.107 | No | — |
| ROUGE-1 | 5.57 | 0.062 | No | — |
| ROUGE-2 | 9.56 | 0.008 | Yes | 0.069 (moderate) |
| ROUGE-L | 7.79 | 0.020 | Yes | — |
| METEOR | 9.80 | 0.007 | Yes | 0.071 (moderate) |
| BERTScore Precision | 9.11 | 0.011 | Yes | — |
| BERTScore Recall | 32.38 | <0.001 | Yes | 0.276 (large) |
| BERTScore F1 | 9.75 | 0.008 | Yes | 0.071 (moderate) |
| SBERT | 17.43 | <0.001 | Yes | 0.140 (large) |

**ε² interpretation**: 0–0.01 = negligible, 0.01–0.06 = small, 0.06–0.14 = moderate, >0.14 = large

---

## Friedman Test (within-subjects, n = 26 paired users)

Non-parametric repeated-measures test — primary omnibus for mode effects.

| Metric | χ² | p-value | Significant | W (Kendall's) |
|---|---|---|---|---|
| BLEU | 6.23 | 0.044 | Yes | 0.083 (weak) |
| ROUGE-1 | 10.69 | 0.005 | Yes | ~0.18 (moderate) |
| ROUGE-2 | 13.46 | 0.001 | Yes | ~0.22 (moderate) |
| ROUGE-L | 11.31 | 0.004 | Yes | ~0.19 (moderate) |
| METEOR | 9.92 | 0.007 | Yes | ~0.17 (moderate) |
| BERTScore Precision | 18.54 | <0.001 | Yes | ~0.30 (strong) |
| BERTScore Recall | 30.77 | <0.001 | Yes | 0.410 (strong) |
| BERTScore F1 | 13.00 | 0.002 | Yes | ~0.21 (moderate) |
| SBERT | 16.69 | <0.001 | Yes | ~0.27 (moderate) |

**Kendall's W interpretation**: 0–0.1 = weak, 0.1–0.3 = moderate, 0.3–0.5 = strong

---

## Post-hoc Pairwise Wilcoxon Signed-Rank Tests (n = 26, primary)

The Friedman test is a **within-subjects** omnibus, so its matched post-hoc is
the Wilcoxon signed-rank test, not Mann-Whitney U. Bonferroni-corrected
α = 0.0167 (3 comparisons). Effect size: matched-pairs rank-biserial r
(positive when the first-named mode in the pair scores higher).

| Metric | Pair | W | p | r (rank-biserial) | Direction | Sig (Bonf) |
|---|---|---|---|---|---|---|
| BLEU | Form vs Ask | 108 | 0.089 | +0.385 (medium) | Form > Ask | No |
| BLEU | Form vs Chat | 133 | 0.291 | −0.242 (small) | Chat > Form | No |
| BLEU | Ask vs Chat | 74 | 0.009 | −0.578 (large) | Chat > Ask | **Yes** |
| ROUGE-1 | Form vs Ask | 77 | 0.011 | +0.561 (large) | Form > Ask | **Yes** |
| ROUGE-1 | Form vs Chat | 147 | 0.483 | −0.162 (small) | Chat > Form | No |
| ROUGE-1 | Ask vs Chat | 63 | 0.003 | −0.641 (large) | Chat > Ask | **Yes** |
| ROUGE-2 | Form vs Ask | 30 | <0.001 | +0.829 (large) | Form > Ask | **Yes** |
| ROUGE-2 | Form vs Chat | 136 | 0.328 | +0.225 (small) | Form > Chat | No |
| ROUGE-2 | Ask vs Chat | 71 | 0.007 | −0.595 (large) | Chat > Ask | **Yes** |
| ROUGE-L | Form vs Ask | 44 | <0.001 | +0.749 (large) | Form > Ask | **Yes** |
| ROUGE-L | Form vs Chat | 161 | 0.727 | +0.083 (negligible) | Form > Chat | No |
| ROUGE-L | Ask vs Chat | 66 | 0.004 | −0.624 (large) | Chat > Ask | **Yes** |
| METEOR | Form vs Ask | 33 | <0.001 | +0.812 (large) | Form > Ask | **Yes** |
| METEOR | Form vs Chat | 137 | 0.340 | +0.219 (small) | Form > Chat | No |
| METEOR | Ask vs Chat | 84 | 0.019 | −0.521 (large) | Chat > Ask | No (above Bonf) |
| BERTScore Precision | Form vs Ask | 63 | 0.003 | +0.641 (large) | Form > Ask | **Yes** |
| BERTScore Precision | Form vs Chat | 106 | 0.080 | −0.396 (medium) | Chat > Form | No |
| BERTScore Precision | Ask vs Chat | 40 | <0.001 | −0.772 (large) | Chat > Ask | **Yes** |
| BERTScore Recall | Form vs Ask | 0 | <0.001 | +1.000 (large) | Form > Ask | **Yes** |
| BERTScore Recall | Form vs Chat | 55 | 0.001 | +0.687 (large) | Form > Chat | **Yes** |
| BERTScore Recall | Ask vs Chat | 99 | 0.053 | −0.436 (medium) | Chat > Ask | No |
| BERTScore F1 | Form vs Ask | 24 | <0.001 | +0.863 (large) | Form > Ask | **Yes** |
| BERTScore F1 | Form vs Chat | 172 | 0.940 | +0.020 (negligible) | Form > Chat | No |
| BERTScore F1 | Ask vs Chat | 59 | 0.002 | −0.664 (large) | Chat > Ask | **Yes** |
| SBERT | Form vs Ask | 110 | 0.099 | +0.373 (medium) | Form > Ask | No |
| SBERT | Form vs Chat | 56 | 0.002 | −0.681 (large) | Chat > Form | **Yes** |
| SBERT | Ask vs Chat | 26 | <0.001 | −0.852 (large) | Chat > Ask | **Yes** |

**Key pattern (matched n = 26):** Ask consistently underperforms relative to
both Form and Chat across the board — Ask vs Chat is significant on every
metric except METEOR (just above Bonferroni) and BERTScore Recall, and Form vs
Ask is significant on every metric except BLEU and SBERT. Form and Chat are
not significantly different on most metrics; the two exceptions are BERTScore
Recall (Form > Chat, large effect) and SBERT (Chat > Form, large effect),
which is consistent with Form producing more reference-coverage and Chat
producing more semantic-document-level fluency.

---

## Sensitivity Check — Mann-Whitney U (full unbalanced sample, n = 113)

Reported as a between-groups sensitivity check; **not** the primary post-hoc
family for the within-subjects design. Bonferroni-corrected α = 0.0167.

| Metric | Comparison | p-value | r (effect) | Significant |
|---|---|---|---|---|
| BERTScore Recall | Form > Ask | <0.001 | 0.756 (large) | Yes |
| BERTScore Recall | Form > Chat | <0.001 | 0.512 (large) | Yes |
| BERTScore Recall | Ask vs Chat | ns | — | No |
| BERTScore F1 | Form > Ask | 0.004 | 0.386 (medium) | Yes |
| BERTScore F1 | Chat > Ask | 0.011 | 0.340 (medium) | Yes |
| BERTScore F1 | Form vs Chat | ns | — | No |
| SBERT | Chat > Form | <0.001 | 0.505 (large) | Yes |
| SBERT | Chat > Ask | <0.001 | 0.453 (large) | Yes |
| SBERT | Form vs Ask | ns | — | No |
| ROUGE-2 | Form > Ask | 0.006 | 0.369 (medium) | Yes |
| ROUGE-2 | Chat > Ask | 0.011 | 0.342 (medium) | Yes |
| ROUGE-2 | Form vs Chat | ns | — | No |
| METEOR | Form > Ask | 0.003 | 0.407 (medium) | Yes |
| METEOR | Form vs Chat | ns | — | No |
| METEOR | Ask vs Chat | 0.043 | — | No (above Bonf) |

The sensitivity check broadly agrees with the matched-pairs result on
direction (Ask < Form, Ask < Chat on most metrics), with the matched analysis
producing larger and more consistent effect sizes — as expected for a
within-subjects design.

---

## Descriptive Statistics by Mode (full dataset, n = 113)

| Metric | Form | Ask | Chat |
|---|---|---|---|
| BERTScore F1 (mean) | 0.905 | 0.897 | 0.904 |
| BERTScore Recall (mean) | 0.923 | 0.908 | 0.913 |
| BERTScore Precision (mean) | 0.889 | 0.886 | 0.895 |
| ROUGE-1 (mean) | 0.488 | 0.465 | 0.511 |
| METEOR (mean) | 0.412 | 0.365 | 0.390 |
| SBERT (mean) | 0.986 | 0.986 | 0.990 |
| BLEU (mean) | 0.129 | 0.127 | 0.143 |

---

## Confidence vs. Quality (RQ2)

**Operationalisation note (changed):** The survey exposes two related
constructs that were previously both called "confidence":

- **Perceived AI Support** (`AI_support`) — mean of the six AI items
  (helpfulness, efficiency, transparency, trust, legal-basis confidence,
  re-use intent). This is a **support / acceptance** composite, not a
  confidence construct. Reported as a secondary perceived-support measure.
- **AI Confidence** (`AI_confidence`) — single item `5_ai`, "I am confident
  the AI identified the correct legal basis." This is the **primary** RQ2
  confidence measure.

(`survey_summary.csv` previously labelled item `6_ai`, "I would use this mode
again," as `AI_confidence`. That was a mislabelling — `6_ai` is intent-to-use,
not confidence. It is now exported separately as `AI_reuse`.)

### Primary: item 5_ai (legal-basis confidence) vs document quality

Per-mode means in the survey × NLP joined sample (n = 106 documents,
44 unique participants; per-mode n: Form 34, Ask 34, Chat 38).

| Mode | AI_confidence (5_ai) | BERTScore F1 | Judge Overall | Rank (confidence) | Rank (BERTScore F1) | Rank (Judge Overall) |
|---|---|---|---|---|---|---|
| Form | 3.38 | 0.906 | 2.38 | 3 | 1 | 3 |
| Ask | 3.68 | 0.896 | 2.56 | 2 | 3 | 2 |
| Chat | 3.76 | 0.904 | 2.63 | 1 | 2 | 1 |

**Rank inversion (RQ2 primary):** Form users feel **least** confident the AI
identified the correct legal basis but produce the **highest**-quality
documents by BERTScore F1; Chat and Ask users feel more confident but their
output quality is at best comparable. The strongest mismatch is at the
extremes: Form (rank 3 confidence, rank 1 BERTScore F1) and Ask
(rank 2 confidence, rank 3 BERTScore F1). On the judge's Overall rating the
ordering tracks confidence more closely (Chat highest on both), so the
inversion is sharpest under reference-based NLP scoring.

### Secondary: 6-item Perceived AI Support composite

| Mode | AI_support (6-item) | BERTScore F1 | Rank (support) | Rank (BERTScore F1) |
|---|---|---|---|---|
| Form | 3.93 | 0.906 | 2 | 1 |
| Ask | 3.96 | 0.896 | 1 | 3 |
| Chat | 3.89 | 0.904 | 3 | 2 |

The composite produces a different (and weaker) inversion: Ask users rate
overall support highest but their documents score worst. This is the result
previously reported as the headline "confidence-quality gap"; it remains
suggestive but is now framed as a **perceived support** finding, separate
from confidence in correctness.

### Spearman correlations (item 5_ai vs document quality)

| Mode | n | ρ (5_ai vs BERTScore F1) | p | ρ (5_ai vs Judge Overall) | p |
|---|---|---|---|---|---|
| Form | 34 | −0.22 | 0.22 | +0.07 | 0.70 |
| Ask | 34 | −0.23 | 0.19 | −0.21 | 0.24 |
| Chat | 38 | +0.28 | 0.09 | **+0.41** | **0.012** |
| Pooled | 106 | −0.02 | 0.88 | +0.14 | 0.14 |

Within-mode correlations are non-significant for Form and Ask but trend
**negative** (more confident users produce lower-quality documents), and
**significantly positive** for Chat (more confident Chat users produce better
documents by judge Overall). The mode-specific direction reversal — negative
in Form/Ask, positive in Chat — is the clearest signal in the data and
supports the Discussion argument that *confidence calibration depends on the
interaction paradigm*.

For comparison, the 6-item composite produces weaker mode-specific
correlations (Form ρ = −0.22, Ask ρ = −0.04, Chat ρ = +0.20 vs BERTScore F1)
and a small but significant pooled correlation with Judge Overall
(ρ = +0.21, p = 0.033, n = 106) — evidence that *perceived support* tracks
quality slightly, while *confidence in correctness* does not.

---

## Limitations

- Full dataset unbalanced (n=37/37/39) due to parsing failures — between-mode
  comparisons on the full sample are reported as a sensitivity check only.
- Within-subjects subset (n = 26) is substantially smaller than full study
  (N = 73). Effect sizes are reported alongside p-values to mitigate this.
- Triangulated confidence–quality analyses (survey × NLP, all three modes per
  participant) are limited to n = 27 participants; per-mode joined n = 34/34/38.
- Chapter-level metrics macro-averaged across 6 chapters per document.
- BLEU and ROUGE unreliable for chapters with structured legal content
  (Ch2, Ch3).

---
---
---
---
---

## Per-Chapter Inferential Tests

Per-(metric, chapter) significance layer for the chapter-level NLP metrics, mirroring the doc-level Kruskal-Wallis → Friedman → Wilcoxon → Mann-Whitney U pipeline. Each cell is one of the 10 metrics applied to one of the six ROPA chapters (ch1–ch6); 60 (metric × chapter) combinations per test family.

Chapter labels: **ch1** = Verantwortliche Stelle und Kontaktdaten · **ch2** = Zwecke und Rechtsgrundlagen der Verarbeitung · **ch3** = Kategorien personenbezogener Daten und Datenquellen · **ch4** = Betroffene Personen und Empfänger · **ch5** = Aufbewahrungsfristen und Löschung · **ch6** = Technische und organisatorische Maßnahmen.

Sample sizes match the doc-level NLP analysis: full unbalanced n = 113 (Form 37 / Ask 37 / Chat 39) for Kruskal-Wallis and Mann-Whitney U; strict matched-triple within-subjects n = 26 for Friedman and Wilcoxon (identical participant list to the doc-level analysis, derived as the 26 users with exactly one document per mode in `chapter_results.csv`).

Significance thresholds and effect-size labels are identical to the doc-level pipeline: Kruskal-Wallis / Friedman use α = 0.05; Wilcoxon and Mann-Whitney are Bonferroni-corrected to α = 0.0167 (3 comparisons within each cell). Effect-size labels for rank-biserial r: |r| < 0.1 negligible, < 0.3 small, < 0.5 medium, ≥ 0.5 large. Kendall's W: < 0.1 weak, < 0.3 moderate, ≥ 0.3 strong. ε² for Kruskal-Wallis: < 0.01 negligible, < 0.06 small, < 0.14 moderate, ≥ 0.14 large.

Degenerate cells — typically the lexical metrics (BLEU, ROUGE-2) on Purposes (ch2) and Categories (ch3), where reference-overlap collapses to zero across every document — are reported as NaN with a footnote flag. `scipy.stats.friedmanchisquare` returns NaN χ² and p when every subject's values are tied across all three conditions, and `scipy.stats.kruskal` raises on fully constant input (caught and reported as NaN).

### Kruskal-Wallis Omnibus (full unbalanced n = 113)

| Metric | Chapter | H | p | ε² | ε² label | Significant (α=0.05) |
|---|---|---|---|---|---|---|
| BLEU | ch1 | 5.202 | 0.074 | 0.046 | small | No |
| BLEU | ch2 | 12.534 | 0.002 | 0.112 | moderate | **Yes** |
| BLEU | ch3 | 20.735 | <0.001 | 0.185 | large | **Yes** |
| BLEU | ch4 | 5.847 | 0.054 | 0.052 | small | No |
| BLEU | ch5 | 19.797 | <0.001 | 0.177 | large | **Yes** |
| BLEU | ch6 | 7.675 | 0.022 | 0.069 | moderate | **Yes** |
| ROUGE-1 | ch1 | 9.693 | 0.008 | 0.087 | moderate | **Yes** |
| ROUGE-1 | ch2 | 9.672 | 0.008 | 0.086 | moderate | **Yes** |
| ROUGE-1 | ch3 | 46.038 | <0.001 | 0.411 | large | **Yes** |
| ROUGE-1 | ch4 | 11.159 | 0.004 | 0.100 | moderate | **Yes** |
| ROUGE-1 | ch5 | 15.637 | <0.001 | 0.140 | moderate | **Yes** |
| ROUGE-1 | ch6 | 4.286 | 0.117 | 0.038 | small | No |
| ROUGE-2 | ch1 | 6.444 | 0.040 | 0.058 | small | **Yes** |
| ROUGE-2 | ch2 | 22.942 | <0.001 | 0.205 | large | **Yes** |
| ROUGE-2 | ch3 | 46.562 | <0.001 | 0.416 | large | **Yes** |
| ROUGE-2 | ch4 | 17.905 | <0.001 | 0.160 | large | **Yes** |
| ROUGE-2 | ch5 | 15.044 | <0.001 | 0.134 | moderate | **Yes** |
| ROUGE-2 | ch6 | 6.838 | 0.033 | 0.061 | moderate | **Yes** |
| ROUGE-L | ch1 | 8.833 | 0.012 | 0.079 | moderate | **Yes** |
| ROUGE-L | ch2 | 16.837 | <0.001 | 0.150 | large | **Yes** |
| ROUGE-L | ch3 | 46.626 | <0.001 | 0.416 | large | **Yes** |
| ROUGE-L | ch4 | 12.223 | 0.002 | 0.109 | moderate | **Yes** |
| ROUGE-L | ch5 | 14.440 | <0.001 | 0.129 | moderate | **Yes** |
| ROUGE-L | ch6 | 7.487 | 0.024 | 0.067 | moderate | **Yes** |
| METEOR | ch1 | 4.430 | 0.109 | 0.040 | small | No |
| METEOR | ch2 | 15.407 | <0.001 | 0.138 | moderate | **Yes** |
| METEOR | ch3 | 45.753 | <0.001 | 0.409 | large | **Yes** |
| METEOR | ch4 | 33.445 | <0.001 | 0.299 | large | **Yes** |
| METEOR | ch5 | 15.071 | <0.001 | 0.135 | moderate | **Yes** |
| METEOR | ch6 | 3.887 | 0.143 | 0.035 | small | No |
| BERTScore_Precision | ch1 | 4.359 | 0.113 | 0.039 | small | No |
| BERTScore_Precision | ch2 | 3.261 | 0.196 | 0.029 | small | No |
| BERTScore_Precision | ch3 | 32.992 | <0.001 | 0.295 | large | **Yes** |
| BERTScore_Precision | ch4 | 2.546 | 0.280 | 0.023 | small | No |
| BERTScore_Precision | ch5 | 10.437 | 0.005 | 0.093 | moderate | **Yes** |
| BERTScore_Precision | ch6 | 11.071 | 0.004 | 0.099 | moderate | **Yes** |
| BERTScore_Recall | ch1 | 4.665 | 0.097 | 0.042 | small | No |
| BERTScore_Recall | ch2 | 9.419 | 0.009 | 0.084 | moderate | **Yes** |
| BERTScore_Recall | ch3 | 51.198 | <0.001 | 0.457 | large | **Yes** |
| BERTScore_Recall | ch4 | 56.718 | <0.001 | 0.506 | large | **Yes** |
| BERTScore_Recall | ch5 | 10.230 | 0.006 | 0.091 | moderate | **Yes** |
| BERTScore_Recall | ch6 | 4.370 | 0.112 | 0.039 | small | No |
| BERTScore_F1 | ch1 | 6.152 | 0.046 | 0.055 | small | **Yes** |
| BERTScore_F1 | ch2 | 7.173 | 0.028 | 0.064 | moderate | **Yes** |
| BERTScore_F1 | ch3 | 51.917 | <0.001 | 0.464 | large | **Yes** |
| BERTScore_F1 | ch4 | 14.378 | <0.001 | 0.128 | moderate | **Yes** |
| BERTScore_F1 | ch5 | 10.731 | 0.005 | 0.096 | moderate | **Yes** |
| BERTScore_F1 | ch6 | 8.412 | 0.015 | 0.075 | moderate | **Yes** |
| SBERT_ModernBERT | ch1 | 4.478 | 0.107 | 0.040 | small | No |
| SBERT_ModernBERT | ch2 | 6.812 | 0.033 | 0.061 | moderate | **Yes** |
| SBERT_ModernBERT | ch3 | 36.690 | <0.001 | 0.328 | large | **Yes** |
| SBERT_ModernBERT | ch4 | 2.357 | 0.308 | 0.021 | small | No |
| SBERT_ModernBERT | ch5 | 8.983 | 0.011 | 0.080 | moderate | **Yes** |
| SBERT_ModernBERT | ch6 | 9.595 | 0.008 | 0.086 | moderate | **Yes** |
| SBERT_MiniLM | ch1 | 8.009 | 0.018 | 0.072 | moderate | **Yes** |
| SBERT_MiniLM | ch2 | 5.338 | 0.069 | 0.048 | small | No |
| SBERT_MiniLM | ch3 | 13.933 | <0.001 | 0.124 | moderate | **Yes** |
| SBERT_MiniLM | ch4 | 5.686 | 0.058 | 0.051 | small | No |
| SBERT_MiniLM | ch5 | 9.285 | 0.010 | 0.083 | moderate | **Yes** |
| SBERT_MiniLM | ch6 | 1.314 | 0.518 | 0.012 | small | No |

### Friedman Omnibus (matched within-subjects n = 26)

| Metric | Chapter | χ² | df | p | Kendall's W | W label | Significant (α=0.05) |
|---|---|---|---|---|---|---|---|
| BLEU | ch1 | 9.920 | 2 | 0.007 | 0.183 | moderate | **Yes** |
| BLEU | ch2 | 15.308 | 2 | <0.001 | 0.294 | moderate | **Yes** |
| BLEU | ch3 | 10.231 | 2 | 0.006 | 0.197 | moderate | **Yes** |
| BLEU | ch4 | 9.107 | 2 | 0.011 | 0.173 | moderate | **Yes** |
| BLEU | ch5 | 14.519 | 2 | <0.001 | 0.207 | moderate | **Yes** |
| BLEU | ch6 | 18.932 | 2 | <0.001 | 0.361 | strong | **Yes** |
| ROUGE-1 | ch1 | 9.961 | 2 | 0.007 | 0.188 | moderate | **Yes** |
| ROUGE-1 | ch2 | 7.923 | 2 | 0.019 | 0.152 | moderate | **Yes** |
| ROUGE-1 | ch3 | 21.462 | 2 | <0.001 | 0.413 | strong | **Yes** |
| ROUGE-1 | ch4 | 15.462 | 2 | <0.001 | 0.297 | moderate | **Yes** |
| ROUGE-1 | ch5 | 13.000 | 2 | 0.002 | 0.250 | moderate | **Yes** |
| ROUGE-1 | ch6 | 5.615 | 2 | 0.060 | 0.108 | moderate | No |
| ROUGE-2 | ch1 | 5.846 | 2 | 0.054 | 0.112 | moderate | No |
| ROUGE-2 | ch2 | 17.308 | 2 | <0.001 | 0.333 | strong | **Yes** |
| ROUGE-2 | ch3 | 24.077 | 2 | <0.001 | 0.463 | strong | **Yes** |
| ROUGE-2 | ch4 | 17.154 | 2 | <0.001 | 0.330 | strong | **Yes** |
| ROUGE-2 | ch5 | 11.615 | 2 | 0.003 | 0.223 | moderate | **Yes** |
| ROUGE-2 | ch6 | 14.077 | 2 | <0.001 | 0.271 | moderate | **Yes** |
| ROUGE-L | ch1 | 8.175 | 2 | 0.017 | 0.156 | moderate | **Yes** |
| ROUGE-L | ch2 | 7.692 | 2 | 0.021 | 0.148 | moderate | **Yes** |
| ROUGE-L | ch3 | 19.923 | 2 | <0.001 | 0.383 | strong | **Yes** |
| ROUGE-L | ch4 | 17.615 | 2 | <0.001 | 0.339 | strong | **Yes** |
| ROUGE-L | ch5 | 13.462 | 2 | 0.001 | 0.259 | moderate | **Yes** |
| ROUGE-L | ch6 | 10.231 | 2 | 0.006 | 0.197 | moderate | **Yes** |
| METEOR | ch1 | 4.385 | 2 | 0.112 | 0.084 | weak | No |
| METEOR | ch2 | 7.000 | 2 | 0.030 | 0.135 | moderate | **Yes** |
| METEOR | ch3 | 25.923 | 2 | <0.001 | 0.499 | strong | **Yes** |
| METEOR | ch4 | 23.154 | 2 | <0.001 | 0.445 | strong | **Yes** |
| METEOR | ch5 | 16.692 | 2 | <0.001 | 0.321 | strong | **Yes** |
| METEOR | ch6 | 6.462 | 2 | 0.040 | 0.124 | moderate | **Yes** |
| BERTScore_Precision | ch1 | 2.154 | 2 | 0.341 | 0.041 | weak | No |
| BERTScore_Precision | ch2 | 3.692 | 2 | 0.158 | 0.071 | weak | No |
| BERTScore_Precision | ch3 | 17.538 | 2 | <0.001 | 0.337 | strong | **Yes** |
| BERTScore_Precision | ch4 | 7.000 | 2 | 0.030 | 0.135 | moderate | **Yes** |
| BERTScore_Precision | ch5 | 9.538 | 2 | 0.008 | 0.183 | moderate | **Yes** |
| BERTScore_Precision | ch6 | 9.308 | 2 | 0.010 | 0.179 | moderate | **Yes** |
| BERTScore_Recall | ch1 | 4.923 | 2 | 0.085 | 0.095 | weak | No |
| BERTScore_Recall | ch2 | 5.615 | 2 | 0.060 | 0.108 | moderate | No |
| BERTScore_Recall | ch3 | 34.462 | 2 | <0.001 | 0.663 | strong | **Yes** |
| BERTScore_Recall | ch4 | 29.154 | 2 | <0.001 | 0.561 | strong | **Yes** |
| BERTScore_Recall | ch5 | 18.769 | 2 | <0.001 | 0.361 | strong | **Yes** |
| BERTScore_Recall | ch6 | 5.615 | 2 | 0.060 | 0.108 | moderate | No |
| BERTScore_F1 | ch1 | 6.231 | 2 | 0.044 | 0.120 | moderate | **Yes** |
| BERTScore_F1 | ch2 | 7.000 | 2 | 0.030 | 0.135 | moderate | **Yes** |
| BERTScore_F1 | ch3 | 31.000 | 2 | <0.001 | 0.596 | strong | **Yes** |
| BERTScore_F1 | ch4 | 10.231 | 2 | 0.006 | 0.197 | moderate | **Yes** |
| BERTScore_F1 | ch5 | 12.077 | 2 | 0.002 | 0.232 | moderate | **Yes** |
| BERTScore_F1 | ch6 | 5.769 | 2 | 0.056 | 0.111 | moderate | No |
| SBERT_ModernBERT | ch1 | 4.000 | 2 | 0.135 | 0.077 | weak | No |
| SBERT_ModernBERT | ch2 | 5.154 | 2 | 0.076 | 0.099 | weak | No |
| SBERT_ModernBERT | ch3 | 13.154 | 2 | 0.001 | 0.253 | moderate | **Yes** |
| SBERT_ModernBERT | ch4 | 2.385 | 2 | 0.304 | 0.046 | weak | No |
| SBERT_ModernBERT | ch5 | 6.231 | 2 | 0.044 | 0.120 | moderate | **Yes** |
| SBERT_ModernBERT | ch6 | 7.000 | 2 | 0.030 | 0.135 | moderate | **Yes** |
| SBERT_MiniLM | ch1 | 3.769 | 2 | 0.152 | 0.072 | weak | No |
| SBERT_MiniLM | ch2 | 5.615 | 2 | 0.060 | 0.108 | moderate | No |
| SBERT_MiniLM | ch3 | 14.846 | 2 | <0.001 | 0.286 | moderate | **Yes** |
| SBERT_MiniLM | ch4 | 6.077 | 2 | 0.048 | 0.117 | moderate | **Yes** |
| SBERT_MiniLM | ch5 | 9.308 | 2 | 0.010 | 0.179 | moderate | **Yes** |
| SBERT_MiniLM | ch6 | 1.462 | 2 | 0.482 | 0.028 | weak | No |

### Pairwise Wilcoxon Signed-Rank Post-hoc (matched n = 26, Bonferroni α = 0.0167)

Effect size: matched-pairs rank-biserial r (positive when the first-named mode in the pair scores higher).

| Metric | Chapter | Pair | W | p | r | r label | Direction | Sig (Bonf) |
|---|---|---|---|---|---|---|---|---|
| BLEU | ch1 | Form vs Ask | 110.0 | 0.158 | -0.323 | medium | Ask > Form | No |
| BLEU | ch1 | Form vs Chat | 101.0 | 0.098 | 0.378 | medium | Form > Chat | No |
| BLEU | ch1 | Ask vs Chat | 60.0 | 0.006 | 0.631 | large | Ask > Chat | **Yes** |
| BLEU | ch2 | Form vs Ask | 37.0 | <0.001 | 0.789 | large | Form > Ask | **Yes** |
| BLEU | ch2 | Form vs Chat | 74.0 | 0.009 | 0.578 | large | Form > Chat | **Yes** |
| BLEU | ch2 | Ask vs Chat | 126.0 | 0.217 | -0.282 | small | Chat > Ask | No |
| BLEU | ch3 | Form vs Ask | 81.0 | 0.015 | 0.538 | large | Form > Ask | **Yes** |
| BLEU | ch3 | Form vs Chat | 39.0 | <0.001 | 0.778 | large | Form > Chat | **Yes** |
| BLEU | ch3 | Ask vs Chat | 130.0 | 0.258 | 0.259 | small | Ask > Chat | No |
| BLEU | ch4 | Form vs Ask | 56.0 | 0.002 | 0.681 | large | Form > Ask | **Yes** |
| BLEU | ch4 | Form vs Chat | 132.0 | 0.280 | 0.248 | small | Form > Chat | No |
| BLEU | ch4 | Ask vs Chat | 109.0 | 0.150 | -0.329 | medium | Chat > Ask | No |
| BLEU | ch5 | Form vs Ask | 16.0 | 0.002 | 0.813 | large | Form > Ask | **Yes** |
| BLEU | ch5 | Form vs Chat | 125.0 | 0.693 | -0.094 | negligible | Chat > Form | No |
| BLEU | ch5 | Ask vs Chat | 11.0 | 0.016 | -0.758 | large | Chat > Ask | **Yes** |
| BLEU | ch6 | Form vs Ask | 68.0 | 0.005 | 0.613 | large | Form > Ask | **Yes** |
| BLEU | ch6 | Form vs Chat | 149.0 | 0.515 | -0.151 | small | Chat > Form | No |
| BLEU | ch6 | Ask vs Chat | 48.0 | 0.002 | -0.705 | large | Chat > Ask | **Yes** |
| ROUGE-1 | ch1 | Form vs Ask | 102.0 | 0.063 | -0.419 | medium | Ask > Form | No |
| ROUGE-1 | ch1 | Form vs Chat | 149.0 | 0.515 | 0.151 | small | Form > Chat | No |
| ROUGE-1 | ch1 | Ask vs Chat | 72.0 | 0.026 | 0.520 | large | Ask > Chat | No |
| ROUGE-1 | ch2 | Form vs Ask | 61.0 | 0.003 | 0.652 | large | Form > Ask | **Yes** |
| ROUGE-1 | ch2 | Form vs Chat | 89.0 | 0.027 | 0.493 | medium | Form > Chat | No |
| ROUGE-1 | ch2 | Ask vs Chat | 127.0 | 0.227 | -0.276 | small | Chat > Ask | No |
| ROUGE-1 | ch3 | Form vs Ask | 3.0 | <0.001 | 0.983 | large | Form > Ask | **Yes** |
| ROUGE-1 | ch3 | Form vs Chat | 43.0 | <0.001 | 0.755 | large | Form > Chat | **Yes** |
| ROUGE-1 | ch3 | Ask vs Chat | 100.0 | 0.056 | -0.430 | medium | Chat > Ask | No |
| ROUGE-1 | ch4 | Form vs Ask | 34.0 | <0.001 | 0.806 | large | Form > Ask | **Yes** |
| ROUGE-1 | ch4 | Form vs Chat | 64.0 | 0.004 | 0.635 | large | Form > Chat | **Yes** |
| ROUGE-1 | ch4 | Ask vs Chat | 96.0 | 0.043 | -0.453 | medium | Chat > Ask | No |
| ROUGE-1 | ch5 | Form vs Ask | 27.0 | <0.001 | 0.846 | large | Form > Ask | **Yes** |
| ROUGE-1 | ch5 | Form vs Chat | 120.0 | 0.165 | -0.316 | medium | Chat > Form | No |
| ROUGE-1 | ch5 | Ask vs Chat | 51.0 | <0.001 | -0.709 | large | Chat > Ask | **Yes** |
| ROUGE-1 | ch6 | Form vs Ask | 145.0 | 0.452 | 0.174 | small | Form > Ask | No |
| ROUGE-1 | ch6 | Form vs Chat | 114.0 | 0.123 | -0.350 | medium | Chat > Form | No |
| ROUGE-1 | ch6 | Ask vs Chat | 103.0 | 0.067 | -0.413 | medium | Chat > Ask | No |
| ROUGE-2 | ch1 | Form vs Ask | 108.0 | 0.089 | -0.385 | medium | Ask > Form | No |
| ROUGE-2 | ch1 | Form vs Chat | 136.0 | 0.328 | 0.225 | small | Form > Chat | No |
| ROUGE-2 | ch1 | Ask vs Chat | 85.0 | 0.020 | 0.516 | large | Ask > Chat | No |
| ROUGE-2 | ch2 | Form vs Ask | 21.0 | <0.001 | 0.880 | large | Form > Ask | **Yes** |
| ROUGE-2 | ch2 | Form vs Chat | 65.0 | 0.004 | 0.630 | large | Form > Chat | **Yes** |
| ROUGE-2 | ch2 | Ask vs Chat | 119.0 | 0.157 | -0.322 | medium | Chat > Ask | No |
| ROUGE-2 | ch3 | Form vs Ask | 0.0 | <0.001 | 1.000 | large | Form > Ask | **Yes** |
| ROUGE-2 | ch3 | Form vs Chat | 41.0 | <0.001 | 0.766 | large | Form > Chat | **Yes** |
| ROUGE-2 | ch3 | Ask vs Chat | 90.0 | 0.029 | -0.487 | medium | Chat > Ask | No |
| ROUGE-2 | ch4 | Form vs Ask | 32.0 | <0.001 | 0.818 | large | Form > Ask | **Yes** |
| ROUGE-2 | ch4 | Form vs Chat | 33.0 | <0.001 | 0.812 | large | Form > Chat | **Yes** |
| ROUGE-2 | ch4 | Ask vs Chat | 137.0 | 0.340 | -0.219 | small | Chat > Ask | No |
| ROUGE-2 | ch5 | Form vs Ask | 50.0 | <0.001 | 0.715 | large | Form > Ask | **Yes** |
| ROUGE-2 | ch5 | Form vs Chat | 174.0 | 0.980 | 0.009 | negligible | Form > Chat | No |
| ROUGE-2 | ch5 | Ask vs Chat | 67.0 | 0.005 | -0.618 | large | Chat > Ask | **Yes** |
| ROUGE-2 | ch6 | Form vs Ask | 84.0 | 0.019 | 0.521 | large | Form > Ask | No |
| ROUGE-2 | ch6 | Form vs Chat | 123.0 | 0.190 | -0.299 | small | Chat > Form | No |
| ROUGE-2 | ch6 | Ask vs Chat | 62.0 | 0.003 | -0.647 | large | Chat > Ask | **Yes** |
| ROUGE-L | ch1 | Form vs Ask | 106.0 | 0.128 | -0.348 | medium | Ask > Form | No |
| ROUGE-L | ch1 | Form vs Chat | 103.0 | 0.067 | 0.413 | medium | Form > Chat | No |
| ROUGE-L | ch1 | Ask vs Chat | 76.0 | 0.010 | 0.567 | large | Ask > Chat | **Yes** |
| ROUGE-L | ch2 | Form vs Ask | 38.0 | <0.001 | 0.783 | large | Form > Ask | **Yes** |
| ROUGE-L | ch2 | Form vs Chat | 88.0 | 0.025 | 0.499 | medium | Form > Chat | No |
| ROUGE-L | ch2 | Ask vs Chat | 103.0 | 0.067 | -0.413 | medium | Chat > Ask | No |
| ROUGE-L | ch3 | Form vs Ask | 1.0 | <0.001 | 0.994 | large | Form > Ask | **Yes** |
| ROUGE-L | ch3 | Form vs Chat | 50.0 | <0.001 | 0.715 | large | Form > Chat | **Yes** |
| ROUGE-L | ch3 | Ask vs Chat | 79.0 | 0.013 | -0.550 | large | Chat > Ask | **Yes** |
| ROUGE-L | ch4 | Form vs Ask | 38.0 | <0.001 | 0.783 | large | Form > Ask | **Yes** |
| ROUGE-L | ch4 | Form vs Chat | 62.0 | 0.003 | 0.647 | large | Form > Chat | **Yes** |
| ROUGE-L | ch4 | Ask vs Chat | 122.0 | 0.181 | -0.305 | medium | Chat > Ask | No |
| ROUGE-L | ch5 | Form vs Ask | 33.0 | <0.001 | 0.812 | large | Form > Ask | **Yes** |
| ROUGE-L | ch5 | Form vs Chat | 123.0 | 0.190 | -0.299 | small | Chat > Form | No |
| ROUGE-L | ch5 | Ask vs Chat | 55.0 | 0.001 | -0.687 | large | Chat > Ask | **Yes** |
| ROUGE-L | ch6 | Form vs Ask | 127.0 | 0.227 | 0.276 | small | Form > Ask | No |
| ROUGE-L | ch6 | Form vs Chat | 114.0 | 0.123 | -0.350 | medium | Chat > Form | No |
| ROUGE-L | ch6 | Ask vs Chat | 66.0 | 0.004 | -0.624 | large | Chat > Ask | **Yes** |
| METEOR | ch1 | Form vs Ask | 121.0 | 0.173 | -0.311 | medium | Ask > Form | No |
| METEOR | ch1 | Form vs Chat | 131.0 | 0.269 | 0.254 | small | Form > Chat | No |
| METEOR | ch1 | Ask vs Chat | 89.0 | 0.027 | 0.493 | medium | Ask > Chat | No |
| METEOR | ch2 | Form vs Ask | 41.0 | <0.001 | 0.766 | large | Form > Ask | **Yes** |
| METEOR | ch2 | Form vs Chat | 127.0 | 0.227 | 0.276 | small | Form > Chat | No |
| METEOR | ch2 | Ask vs Chat | 93.0 | 0.036 | -0.470 | medium | Chat > Ask | No |
| METEOR | ch3 | Form vs Ask | 7.0 | <0.001 | 0.960 | large | Form > Ask | **Yes** |
| METEOR | ch3 | Form vs Chat | 8.0 | <0.001 | 0.954 | large | Form > Chat | **Yes** |
| METEOR | ch3 | Ask vs Chat | 133.0 | 0.291 | 0.242 | small | Ask > Chat | No |
| METEOR | ch4 | Form vs Ask | 14.0 | <0.001 | 0.920 | large | Form > Ask | **Yes** |
| METEOR | ch4 | Form vs Chat | 31.0 | <0.001 | 0.823 | large | Form > Chat | **Yes** |
| METEOR | ch4 | Ask vs Chat | 143.0 | 0.423 | -0.185 | small | Chat > Ask | No |
| METEOR | ch5 | Form vs Ask | 34.0 | <0.001 | 0.806 | large | Form > Ask | **Yes** |
| METEOR | ch5 | Form vs Chat | 157.0 | 0.653 | -0.105 | small | Chat > Form | No |
| METEOR | ch5 | Ask vs Chat | 55.0 | 0.001 | -0.687 | large | Chat > Ask | **Yes** |
| METEOR | ch6 | Form vs Ask | 76.0 | 0.010 | 0.567 | large | Form > Ask | **Yes** |
| METEOR | ch6 | Form vs Chat | 131.0 | 0.269 | -0.254 | small | Chat > Form | No |
| METEOR | ch6 | Ask vs Chat | 88.0 | 0.025 | -0.499 | medium | Chat > Ask | No |
| BERTScore_Precision | ch1 | Form vs Ask | 132.0 | 0.280 | -0.248 | small | Ask > Form | No |
| BERTScore_Precision | ch1 | Form vs Chat | 110.0 | 0.099 | 0.373 | medium | Form > Chat | No |
| BERTScore_Precision | ch1 | Ask vs Chat | 93.0 | 0.036 | 0.470 | medium | Ask > Chat | No |
| BERTScore_Precision | ch2 | Form vs Ask | 119.0 | 0.157 | 0.322 | medium | Form > Ask | No |
| BERTScore_Precision | ch2 | Form vs Chat | 169.0 | 0.881 | -0.037 | negligible | Chat > Form | No |
| BERTScore_Precision | ch2 | Ask vs Chat | 92.0 | 0.033 | -0.476 | medium | Chat > Ask | No |
| BERTScore_Precision | ch3 | Form vs Ask | 8.0 | <0.001 | 0.954 | large | Form > Ask | **Yes** |
| BERTScore_Precision | ch3 | Form vs Chat | 100.0 | 0.056 | 0.430 | medium | Form > Chat | No |
| BERTScore_Precision | ch3 | Ask vs Chat | 54.0 | 0.001 | -0.692 | large | Chat > Ask | **Yes** |
| BERTScore_Precision | ch4 | Form vs Ask | 87.0 | 0.024 | 0.504 | large | Form > Ask | No |
| BERTScore_Precision | ch4 | Form vs Chat | 133.0 | 0.291 | -0.242 | small | Chat > Form | No |
| BERTScore_Precision | ch4 | Ask vs Chat | 71.0 | 0.007 | -0.595 | large | Chat > Ask | **Yes** |
| BERTScore_Precision | ch5 | Form vs Ask | 128.0 | 0.237 | 0.271 | small | Form > Ask | No |
| BERTScore_Precision | ch5 | Form vs Chat | 88.0 | 0.025 | -0.499 | medium | Chat > Form | No |
| BERTScore_Precision | ch5 | Ask vs Chat | 73.0 | 0.008 | -0.584 | large | Chat > Ask | **Yes** |
| BERTScore_Precision | ch6 | Form vs Ask | 123.0 | 0.190 | -0.299 | small | Ask > Form | No |
| BERTScore_Precision | ch6 | Form vs Chat | 101.0 | 0.059 | -0.425 | medium | Chat > Form | No |
| BERTScore_Precision | ch6 | Ask vs Chat | 112.0 | 0.111 | -0.362 | medium | Chat > Ask | No |
| BERTScore_Recall | ch1 | Form vs Ask | 114.0 | 0.123 | -0.350 | medium | Ask > Form | No |
| BERTScore_Recall | ch1 | Form vs Chat | 114.0 | 0.123 | 0.350 | medium | Form > Chat | No |
| BERTScore_Recall | ch1 | Ask vs Chat | 89.0 | 0.027 | 0.493 | medium | Ask > Chat | No |
| BERTScore_Recall | ch2 | Form vs Ask | 96.0 | 0.043 | 0.453 | medium | Form > Ask | No |
| BERTScore_Recall | ch2 | Form vs Chat | 166.0 | 0.822 | 0.054 | negligible | Form > Chat | No |
| BERTScore_Recall | ch2 | Ask vs Chat | 103.0 | 0.067 | -0.413 | medium | Chat > Ask | No |
| BERTScore_Recall | ch3 | Form vs Ask | 9.0 | <0.001 | 0.949 | large | Form > Ask | **Yes** |
| BERTScore_Recall | ch3 | Form vs Chat | 5.0 | <0.001 | 0.972 | large | Form > Chat | **Yes** |
| BERTScore_Recall | ch3 | Ask vs Chat | 135.0 | 0.315 | 0.231 | small | Ask > Chat | No |
| BERTScore_Recall | ch4 | Form vs Ask | 13.0 | <0.001 | 0.926 | large | Form > Ask | **Yes** |
| BERTScore_Recall | ch4 | Form vs Chat | 2.0 | <0.001 | 0.989 | large | Form > Chat | **Yes** |
| BERTScore_Recall | ch4 | Ask vs Chat | 109.0 | 0.094 | 0.379 | medium | Ask > Chat | No |
| BERTScore_Recall | ch5 | Form vs Ask | 36.0 | <0.001 | 0.795 | large | Form > Ask | **Yes** |
| BERTScore_Recall | ch5 | Form vs Chat | 142.0 | 0.408 | -0.191 | small | Chat > Form | No |
| BERTScore_Recall | ch5 | Ask vs Chat | 51.0 | <0.001 | -0.709 | large | Chat > Ask | **Yes** |
| BERTScore_Recall | ch6 | Form vs Ask | 123.0 | 0.190 | 0.299 | small | Form > Ask | No |
| BERTScore_Recall | ch6 | Form vs Chat | 119.0 | 0.157 | -0.322 | medium | Chat > Form | No |
| BERTScore_Recall | ch6 | Ask vs Chat | 85.0 | 0.020 | -0.516 | large | Chat > Ask | No |
| BERTScore_F1 | ch1 | Form vs Ask | 117.0 | 0.143 | -0.333 | medium | Ask > Form | No |
| BERTScore_F1 | ch1 | Form vs Chat | 104.0 | 0.071 | 0.407 | medium | Form > Chat | No |
| BERTScore_F1 | ch1 | Ask vs Chat | 87.0 | 0.024 | 0.504 | large | Ask > Chat | No |
| BERTScore_F1 | ch2 | Form vs Ask | 85.0 | 0.020 | 0.516 | large | Form > Ask | No |
| BERTScore_F1 | ch2 | Form vs Chat | 172.0 | 0.940 | 0.020 | negligible | Form > Chat | No |
| BERTScore_F1 | ch2 | Ask vs Chat | 83.0 | 0.018 | -0.527 | large | Chat > Ask | No |
| BERTScore_F1 | ch3 | Form vs Ask | 2.0 | <0.001 | 0.989 | large | Form > Ask | **Yes** |
| BERTScore_F1 | ch3 | Form vs Chat | 10.0 | <0.001 | 0.943 | large | Form > Chat | **Yes** |
| BERTScore_F1 | ch3 | Ask vs Chat | 140.0 | 0.380 | -0.202 | small | Chat > Ask | No |
| BERTScore_F1 | ch4 | Form vs Ask | 31.0 | <0.001 | 0.823 | large | Form > Ask | **Yes** |
| BERTScore_F1 | ch4 | Form vs Chat | 68.0 | 0.005 | 0.613 | large | Form > Chat | **Yes** |
| BERTScore_F1 | ch4 | Ask vs Chat | 117.0 | 0.143 | -0.333 | medium | Chat > Ask | No |
| BERTScore_F1 | ch5 | Form vs Ask | 93.0 | 0.036 | 0.470 | medium | Form > Ask | No |
| BERTScore_F1 | ch5 | Form vs Chat | 98.0 | 0.049 | -0.442 | medium | Chat > Form | No |
| BERTScore_F1 | ch5 | Ask vs Chat | 65.0 | 0.004 | -0.630 | large | Chat > Ask | **Yes** |
| BERTScore_F1 | ch6 | Form vs Ask | 170.0 | 0.901 | -0.031 | negligible | Ask > Form | No |
| BERTScore_F1 | ch6 | Form vs Chat | 94.0 | 0.038 | -0.464 | medium | Chat > Form | No |
| BERTScore_F1 | ch6 | Ask vs Chat | 84.0 | 0.019 | -0.521 | large | Chat > Ask | No |
| SBERT_ModernBERT | ch1 | Form vs Ask | 109.0 | 0.094 | -0.379 | medium | Ask > Form | No |
| SBERT_ModernBERT | ch1 | Form vs Chat | 115.0 | 0.129 | 0.345 | medium | Form > Chat | No |
| SBERT_ModernBERT | ch1 | Ask vs Chat | 85.0 | 0.020 | 0.516 | large | Ask > Chat | No |
| SBERT_ModernBERT | ch2 | Form vs Ask | 86.0 | 0.022 | 0.510 | large | Form > Ask | No |
| SBERT_ModernBERT | ch2 | Form vs Chat | 152.0 | 0.565 | -0.134 | small | Chat > Form | No |
| SBERT_ModernBERT | ch2 | Ask vs Chat | 93.0 | 0.036 | -0.470 | medium | Chat > Ask | No |
| SBERT_ModernBERT | ch3 | Form vs Ask | 35.0 | <0.001 | 0.801 | large | Form > Ask | **Yes** |
| SBERT_ModernBERT | ch3 | Form vs Chat | 30.0 | <0.001 | 0.829 | large | Form > Chat | **Yes** |
| SBERT_ModernBERT | ch3 | Ask vs Chat | 168.0 | 0.861 | 0.043 | negligible | Ask > Chat | No |
| SBERT_ModernBERT | ch4 | Form vs Ask | 105.0 | 0.075 | 0.402 | medium | Form > Ask | No |
| SBERT_ModernBERT | ch4 | Form vs Chat | 157.0 | 0.653 | 0.105 | small | Form > Chat | No |
| SBERT_ModernBERT | ch4 | Ask vs Chat | 133.0 | 0.291 | -0.242 | small | Chat > Ask | No |
| SBERT_ModernBERT | ch5 | Form vs Ask | 114.0 | 0.123 | 0.350 | medium | Form > Ask | No |
| SBERT_ModernBERT | ch5 | Form vs Chat | 92.0 | 0.033 | -0.476 | medium | Chat > Form | No |
| SBERT_ModernBERT | ch5 | Ask vs Chat | 66.0 | 0.004 | -0.624 | large | Chat > Ask | **Yes** |
| SBERT_ModernBERT | ch6 | Form vs Ask | 128.0 | 0.237 | -0.271 | small | Ask > Form | No |
| SBERT_ModernBERT | ch6 | Form vs Chat | 67.0 | 0.005 | -0.618 | large | Chat > Form | **Yes** |
| SBERT_ModernBERT | ch6 | Ask vs Chat | 93.0 | 0.036 | -0.470 | medium | Chat > Ask | No |
| SBERT_MiniLM | ch1 | Form vs Ask | 98.0 | 0.049 | -0.442 | medium | Ask > Form | No |
| SBERT_MiniLM | ch1 | Form vs Chat | 175.0 | 1.000 | 0.003 | negligible | Form > Chat | No |
| SBERT_MiniLM | ch1 | Ask vs Chat | 85.0 | 0.020 | 0.516 | large | Ask > Chat | No |
| SBERT_MiniLM | ch2 | Form vs Ask | 122.0 | 0.181 | 0.305 | medium | Form > Ask | No |
| SBERT_MiniLM | ch2 | Form vs Chat | 72.0 | 0.007 | 0.590 | large | Form > Chat | **Yes** |
| SBERT_MiniLM | ch2 | Ask vs Chat | 114.0 | 0.123 | 0.350 | medium | Ask > Chat | No |
| SBERT_MiniLM | ch3 | Form vs Ask | 146.0 | 0.468 | 0.168 | small | Form > Ask | No |
| SBERT_MiniLM | ch3 | Form vs Chat | 49.0 | <0.001 | 0.721 | large | Form > Chat | **Yes** |
| SBERT_MiniLM | ch3 | Ask vs Chat | 82.0 | 0.016 | 0.533 | large | Ask > Chat | **Yes** |
| SBERT_MiniLM | ch4 | Form vs Ask | 104.0 | 0.071 | 0.407 | medium | Form > Ask | No |
| SBERT_MiniLM | ch4 | Form vs Chat | 117.0 | 0.143 | -0.333 | medium | Chat > Form | No |
| SBERT_MiniLM | ch4 | Ask vs Chat | 57.0 | 0.002 | -0.675 | large | Chat > Ask | **Yes** |
| SBERT_MiniLM | ch5 | Form vs Ask | 85.0 | 0.020 | 0.516 | large | Form > Ask | No |
| SBERT_MiniLM | ch5 | Form vs Chat | 123.0 | 0.190 | -0.299 | small | Chat > Form | No |
| SBERT_MiniLM | ch5 | Ask vs Chat | 57.0 | 0.002 | -0.675 | large | Chat > Ask | **Yes** |
| SBERT_MiniLM | ch6 | Form vs Ask | 143.0 | 0.423 | 0.185 | small | Form > Ask | No |
| SBERT_MiniLM | ch6 | Form vs Chat | 153.0 | 0.582 | -0.128 | small | Chat > Form | No |
| SBERT_MiniLM | ch6 | Ask vs Chat | 142.0 | 0.408 | -0.191 | small | Chat > Ask | No |

### Pairwise Mann-Whitney U Sensitivity (full unbalanced n = 113, Bonferroni α = 0.0167)

Reported as a between-groups sensitivity check on the unbalanced full sample; the matched-pairs Wilcoxon family above is the primary inferential result. Effect size: rank-biserial r (positive when the first-named mode scores higher).

| Metric | Chapter | Pair | U | p | r | r label | Direction | Median A | Median B | Sig (Bonf) |
|---|---|---|---|---|---|---|---|---|---|---|
| BLEU | ch1 | Form vs Ask | 567.0 | 0.206 | -0.172 | small | Ask > Form | 0.1645 | 0.2047 | No |
| BLEU | ch1 | Form vs Chat | 804.5 | 0.391 | 0.115 | small | Form > Chat | 0.1645 | 0.1477 | No |
| BLEU | ch1 | Ask vs Chat | 945.0 | 0.020 | 0.310 | medium | Ask > Chat | 0.2047 | 0.1477 | No |
| BLEU | ch2 | Form vs Ask | 1028.0 | <0.001 | 0.502 | large | Form > Ask | 0.1307 | 0.1001 | **Yes** |
| BLEU | ch2 | Form vs Chat | 918.0 | 0.042 | 0.272 | small | Form > Chat | 0.1307 | 0.1194 | No |
| BLEU | ch2 | Ask vs Chat | 620.5 | 0.296 | -0.140 | small | Chat > Ask | 0.1001 | 0.1194 | No |
| BLEU | ch3 | Form vs Ask | 976.0 | 0.002 | 0.426 | medium | Form > Ask | 0.1043 | 0.0714 | **Yes** |
| BLEU | ch3 | Form vs Chat | 1145.0 | <0.001 | 0.587 | large | Form > Chat | 0.1043 | 0.0638 | **Yes** |
| BLEU | ch3 | Ask vs Chat | 842.0 | 0.210 | 0.167 | small | Ask > Chat | 0.0714 | 0.0638 | No |
| BLEU | ch4 | Form vs Ask | 935.0 | 0.007 | 0.366 | medium | Form > Ask | 0.1066 | 0.0508 | **Yes** |
| BLEU | ch4 | Form vs Chat | 840.0 | 0.220 | 0.164 | small | Form > Chat | 0.1066 | 0.0973 | No |
| BLEU | ch4 | Ask vs Chat | 671.0 | 0.600 | -0.070 | negligible | Chat > Ask | 0.0508 | 0.0973 | No |
| BLEU | ch5 | Form vs Ask | 1027.0 | <0.001 | 0.500 | large | Form > Ask | 0.0315 | 0.0000 | **Yes** |
| BLEU | ch5 | Form vs Chat | 663.0 | 0.536 | -0.081 | negligible | Chat > Form | 0.0315 | 0.0441 | No |
| BLEU | ch5 | Ask vs Chat | 398.0 | <0.001 | -0.448 | medium | Chat > Ask | 0.0000 | 0.0441 | **Yes** |
| BLEU | ch6 | Form vs Ask | 803.0 | 0.201 | 0.173 | small | Form > Ask | 0.0507 | 0.0477 | No |
| BLEU | ch6 | Form vs Chat | 514.0 | 0.031 | -0.288 | small | Chat > Form | 0.0507 | 0.0854 | No |
| BLEU | ch6 | Ask vs Chat | 496.0 | 0.019 | -0.313 | medium | Chat > Ask | 0.0477 | 0.0854 | No |
| ROUGE-1 | ch1 | Form vs Ask | 431.0 | 0.006 | -0.370 | medium | Ask > Form | 0.5306 | 0.6034 | **Yes** |
| ROUGE-1 | ch1 | Form vs Chat | 629.5 | 0.342 | -0.128 | small | Chat > Form | 0.5306 | 0.5574 | No |
| ROUGE-1 | ch1 | Ask vs Chat | 962.5 | 0.012 | 0.334 | medium | Ask > Chat | 0.6034 | 0.5574 | **Yes** |
| ROUGE-1 | ch2 | Form vs Ask | 986.0 | 0.001 | 0.440 | medium | Form > Ask | 0.4492 | 0.3857 | **Yes** |
| ROUGE-1 | ch2 | Form vs Chat | 860.5 | 0.150 | 0.193 | small | Form > Chat | 0.4492 | 0.4110 | No |
| ROUGE-1 | ch2 | Ask vs Chat | 587.0 | 0.164 | -0.186 | small | Chat > Ask | 0.3857 | 0.4110 | No |
| ROUGE-1 | ch3 | Form vs Ask | 1336.5 | <0.001 | 0.953 | large | Form > Ask | 0.6038 | 0.3906 | **Yes** |
| ROUGE-1 | ch3 | Form vs Chat | 1114.5 | <0.001 | 0.545 | large | Form > Chat | 0.6038 | 0.4469 | **Yes** |
| ROUGE-1 | ch3 | Ask vs Chat | 540.5 | 0.061 | -0.251 | small | Chat > Ask | 0.3906 | 0.4469 | No |
| ROUGE-1 | ch4 | Form vs Ask | 972.0 | 0.002 | 0.420 | medium | Form > Ask | 0.4921 | 0.3864 | **Yes** |
| ROUGE-1 | ch4 | Form vs Chat | 951.0 | 0.017 | 0.318 | medium | Form > Chat | 0.4921 | 0.4409 | No |
| ROUGE-1 | ch4 | Ask vs Chat | 604.0 | 0.224 | -0.163 | small | Chat > Ask | 0.3864 | 0.4409 | No |
| ROUGE-1 | ch5 | Form vs Ask | 931.0 | 0.008 | 0.360 | medium | Form > Ask | 0.2479 | 0.1833 | **Yes** |
| ROUGE-1 | ch5 | Form vs Chat | 535.5 | 0.054 | -0.258 | small | Chat > Form | 0.2479 | 0.3175 | No |
| ROUGE-1 | ch5 | Ask vs Chat | 376.5 | <0.001 | -0.478 | medium | Chat > Ask | 0.1833 | 0.3175 | **Yes** |
| ROUGE-1 | ch6 | Form vs Ask | 624.0 | 0.517 | -0.088 | negligible | Ask > Form | 0.2532 | 0.2831 | No |
| ROUGE-1 | ch6 | Form vs Chat | 516.5 | 0.034 | -0.284 | small | Chat > Form | 0.2532 | 0.3364 | No |
| ROUGE-1 | ch6 | Ask vs Chat | 607.0 | 0.236 | -0.159 | small | Chat > Ask | 0.2831 | 0.3364 | No |
| ROUGE-2 | ch1 | Form vs Ask | 483.5 | 0.030 | -0.294 | small | Ask > Form | 0.3459 | 0.4333 | No |
| ROUGE-2 | ch1 | Form vs Chat | 691.5 | 0.759 | -0.042 | negligible | Chat > Form | 0.3459 | 0.3659 | No |
| ROUGE-2 | ch1 | Ask vs Chat | 934.0 | 0.028 | 0.295 | small | Ask > Chat | 0.4333 | 0.3659 | No |
| ROUGE-2 | ch2 | Form vs Ask | 1164.0 | <0.001 | 0.701 | large | Form > Ask | 0.3034 | 0.2165 | **Yes** |
| ROUGE-2 | ch2 | Form vs Chat | 962.0 | 0.013 | 0.333 | medium | Form > Chat | 0.3034 | 0.2738 | **Yes** |
| ROUGE-2 | ch2 | Ask vs Chat | 582.0 | 0.149 | -0.193 | small | Chat > Ask | 0.2165 | 0.2738 | No |
| ROUGE-2 | ch3 | Form vs Ask | 1321.0 | <0.001 | 0.930 | large | Form > Ask | 0.4153 | 0.2018 | **Yes** |
| ROUGE-2 | ch3 | Form vs Chat | 1134.0 | <0.001 | 0.572 | large | Form > Chat | 0.4153 | 0.2297 | **Yes** |
| ROUGE-2 | ch3 | Ask vs Chat | 516.5 | 0.034 | -0.284 | small | Chat > Ask | 0.2018 | 0.2297 | No |
| ROUGE-2 | ch4 | Form vs Ask | 1010.0 | <0.001 | 0.476 | medium | Form > Ask | 0.2979 | 0.1749 | **Yes** |
| ROUGE-2 | ch4 | Form vs Chat | 1087.0 | <0.001 | 0.507 | large | Form > Chat | 0.2979 | 0.2364 | **Yes** |
| ROUGE-2 | ch4 | Ask vs Chat | 685.5 | 0.712 | -0.050 | negligible | Chat > Ask | 0.1749 | 0.2364 | No |
| ROUGE-2 | ch5 | Form vs Ask | 1004.0 | <0.001 | 0.467 | medium | Form > Ask | 0.1277 | 0.0508 | **Yes** |
| ROUGE-2 | ch5 | Form vs Chat | 669.0 | 0.589 | -0.073 | negligible | Chat > Form | 0.1277 | 0.1481 | No |
| ROUGE-2 | ch5 | Ask vs Chat | 409.0 | 0.001 | -0.433 | medium | Chat > Ask | 0.0508 | 0.1481 | **Yes** |
| ROUGE-2 | ch6 | Form vs Ask | 753.0 | 0.462 | 0.100 | small | Form > Ask | 0.1167 | 0.1146 | No |
| ROUGE-2 | ch6 | Form vs Chat | 511.0 | 0.029 | -0.292 | small | Chat > Form | 0.1167 | 0.1831 | No |
| ROUGE-2 | ch6 | Ask vs Chat | 507.0 | 0.026 | -0.297 | small | Chat > Ask | 0.1146 | 0.1831 | No |
| ROUGE-L | ch1 | Form vs Ask | 464.0 | 0.017 | -0.322 | medium | Ask > Form | 0.4941 | 0.5862 | No |
| ROUGE-L | ch1 | Form vs Chat | 729.5 | 0.938 | 0.011 | negligible | Form > Chat | 0.4941 | 0.5082 | No |
| ROUGE-L | ch1 | Ask vs Chat | 986.0 | 0.006 | 0.367 | medium | Ask > Chat | 0.5862 | 0.5082 | **Yes** |
| ROUGE-L | ch2 | Form vs Ask | 1097.0 | <0.001 | 0.603 | large | Form > Ask | 0.3853 | 0.3071 | **Yes** |
| ROUGE-L | ch2 | Form vs Chat | 886.5 | 0.087 | 0.229 | small | Form > Chat | 0.3853 | 0.3547 | No |
| ROUGE-L | ch2 | Ask vs Chat | 555.0 | 0.084 | -0.231 | small | Chat > Ask | 0.3071 | 0.3547 | No |
| ROUGE-L | ch3 | Form vs Ask | 1351.0 | <0.001 | 0.974 | large | Form > Ask | 0.5691 | 0.3273 | **Yes** |
| ROUGE-L | ch3 | Form vs Chat | 1095.0 | <0.001 | 0.518 | large | Form > Chat | 0.5691 | 0.3911 | **Yes** |
| ROUGE-L | ch3 | Ask vs Chat | 528.0 | 0.045 | -0.268 | small | Chat > Ask | 0.3273 | 0.3911 | No |
| ROUGE-L | ch4 | Form vs Ask | 984.0 | 0.001 | 0.438 | medium | Form > Ask | 0.4161 | 0.2956 | **Yes** |
| ROUGE-L | ch4 | Form vs Chat | 973.0 | 0.009 | 0.349 | medium | Form > Chat | 0.4161 | 0.3649 | **Yes** |
| ROUGE-L | ch4 | Ask vs Chat | 620.5 | 0.296 | -0.140 | small | Chat > Ask | 0.2956 | 0.3649 | No |
| ROUGE-L | ch5 | Form vs Ask | 933.5 | 0.007 | 0.364 | medium | Form > Ask | 0.2178 | 0.1471 | **Yes** |
| ROUGE-L | ch5 | Form vs Chat | 543.5 | 0.065 | -0.247 | small | Chat > Form | 0.2178 | 0.2540 | No |
| ROUGE-L | ch5 | Ask vs Chat | 397.0 | <0.001 | -0.450 | medium | Chat > Ask | 0.1471 | 0.2540 | **Yes** |
| ROUGE-L | ch6 | Form vs Ask | 701.5 | 0.858 | 0.025 | negligible | Form > Ask | 0.1659 | 0.1940 | No |
| ROUGE-L | ch6 | Form vs Chat | 471.5 | 0.010 | -0.347 | medium | Chat > Form | 0.1659 | 0.2685 | **Yes** |
| ROUGE-L | ch6 | Ask vs Chat | 518.5 | 0.035 | -0.281 | small | Chat > Ask | 0.1940 | 0.2685 | No |
| METEOR | ch1 | Form vs Ask | 518.0 | 0.073 | -0.243 | small | Ask > Form | 0.4489 | 0.5021 | No |
| METEOR | ch1 | Form vs Chat | 718.5 | 0.979 | -0.004 | negligible | Chat > Form | 0.4489 | 0.4451 | No |
| METEOR | ch1 | Ask vs Chat | 899.0 | 0.066 | 0.246 | small | Ask > Chat | 0.5021 | 0.4451 | No |
| METEOR | ch2 | Form vs Ask | 1062.0 | <0.001 | 0.551 | large | Form > Ask | 0.4361 | 0.3762 | **Yes** |
| METEOR | ch2 | Form vs Chat | 875.0 | 0.112 | 0.213 | small | Form > Chat | 0.4361 | 0.4193 | No |
| METEOR | ch2 | Ask vs Chat | 526.0 | 0.043 | -0.271 | small | Chat > Ask | 0.3762 | 0.4193 | No |
| METEOR | ch3 | Form vs Ask | 1202.0 | <0.001 | 0.756 | large | Form > Ask | 0.4155 | 0.3131 | **Yes** |
| METEOR | ch3 | Form vs Chat | 1295.0 | <0.001 | 0.795 | large | Form > Chat | 0.4155 | 0.2709 | **Yes** |
| METEOR | ch3 | Ask vs Chat | 864.0 | 0.140 | 0.198 | small | Ask > Chat | 0.3131 | 0.2709 | No |
| METEOR | ch4 | Form vs Ask | 1123.0 | <0.001 | 0.641 | large | Form > Ask | 0.4191 | 0.2998 | **Yes** |
| METEOR | ch4 | Form vs Chat | 1228.0 | <0.001 | 0.702 | large | Form > Chat | 0.4191 | 0.3287 | **Yes** |
| METEOR | ch4 | Ask vs Chat | 682.0 | 0.685 | -0.055 | negligible | Chat > Ask | 0.2998 | 0.3287 | No |
| METEOR | ch5 | Form vs Ask | 998.0 | <0.001 | 0.458 | medium | Form > Ask | 0.3314 | 0.2090 | **Yes** |
| METEOR | ch5 | Form vs Chat | 715.0 | 0.950 | -0.009 | negligible | Chat > Form | 0.3314 | 0.3252 | No |
| METEOR | ch5 | Ask vs Chat | 400.5 | <0.001 | -0.445 | medium | Chat > Ask | 0.2090 | 0.3252 | **Yes** |
| METEOR | ch6 | Form vs Ask | 753.0 | 0.462 | 0.100 | small | Form > Ask | 0.2603 | 0.2436 | No |
| METEOR | ch6 | Form vs Chat | 594.0 | 0.187 | -0.177 | small | Chat > Form | 0.2603 | 0.3155 | No |
| METEOR | ch6 | Ask vs Chat | 542.0 | 0.063 | -0.249 | small | Chat > Ask | 0.2436 | 0.3155 | No |
| BERTScore_Precision | ch1 | Form vs Ask | 538.0 | 0.114 | -0.214 | small | Ask > Form | 0.8525 | 0.8627 | No |
| BERTScore_Precision | ch1 | Form vs Chat | 766.5 | 0.644 | 0.062 | negligible | Form > Chat | 0.8525 | 0.8512 | No |
| BERTScore_Precision | ch1 | Ask vs Chat | 909.0 | 0.052 | 0.260 | small | Ask > Chat | 0.8627 | 0.8512 | No |
| BERTScore_Precision | ch2 | Form vs Ask | 739.0 | 0.559 | 0.080 | negligible | Form > Ask | 0.8713 | 0.8638 | No |
| BERTScore_Precision | ch2 | Form vs Chat | 619.0 | 0.289 | -0.142 | small | Chat > Form | 0.8713 | 0.8755 | No |
| BERTScore_Precision | ch2 | Ask vs Chat | 545.0 | 0.067 | -0.245 | small | Chat > Ask | 0.8638 | 0.8755 | No |
| BERTScore_Precision | ch3 | Form vs Ask | 1209.0 | <0.001 | 0.766 | large | Form > Ask | 0.8928 | 0.8672 | **Yes** |
| BERTScore_Precision | ch3 | Form vs Chat | 949.0 | 0.018 | 0.315 | medium | Form > Chat | 0.8928 | 0.8876 | No |
| BERTScore_Precision | ch3 | Ask vs Chat | 389.0 | <0.001 | -0.461 | medium | Chat > Ask | 0.8672 | 0.8876 | **Yes** |
| BERTScore_Precision | ch4 | Form vs Ask | 711.0 | 0.779 | 0.039 | negligible | Form > Ask | 0.8555 | 0.8517 | No |
| BERTScore_Precision | ch4 | Form vs Chat | 585.0 | 0.158 | -0.189 | small | Chat > Form | 0.8555 | 0.8687 | No |
| BERTScore_Precision | ch4 | Ask vs Chat | 595.0 | 0.190 | -0.175 | small | Chat > Ask | 0.8517 | 0.8687 | No |
| BERTScore_Precision | ch5 | Form vs Ask | 698.0 | 0.888 | 0.020 | negligible | Form > Ask | 0.8119 | 0.8023 | No |
| BERTScore_Precision | ch5 | Form vs Chat | 403.0 | <0.001 | -0.441 | medium | Chat > Form | 0.8119 | 0.8381 | **Yes** |
| BERTScore_Precision | ch5 | Ask vs Chat | 507.0 | 0.026 | -0.297 | small | Chat > Ask | 0.8023 | 0.8381 | No |
| BERTScore_Precision | ch6 | Form vs Ask | 460.0 | 0.015 | -0.328 | medium | Ask > Form | 0.8225 | 0.8603 | **Yes** |
| BERTScore_Precision | ch6 | Form vs Chat | 415.0 | 0.001 | -0.425 | medium | Chat > Form | 0.8225 | 0.8610 | **Yes** |
| BERTScore_Precision | ch6 | Ask vs Chat | 653.0 | 0.480 | -0.095 | negligible | Chat > Ask | 0.8603 | 0.8610 | No |
| BERTScore_Recall | ch1 | Form vs Ask | 510.0 | 0.060 | -0.255 | small | Ask > Form | 0.8777 | 0.8887 | No |
| BERTScore_Recall | ch1 | Form vs Chat | 721.5 | 1.000 | 0.000 | negligible | tie | 0.8777 | 0.8807 | No |
| BERTScore_Recall | ch1 | Ask vs Chat | 900.0 | 0.064 | 0.247 | small | Ask > Chat | 0.8887 | 0.8807 | No |
| BERTScore_Recall | ch2 | Form vs Ask | 952.0 | 0.004 | 0.391 | medium | Form > Ask | 0.9088 | 0.9025 | **Yes** |
| BERTScore_Recall | ch2 | Form vs Chat | 749.0 | 0.779 | 0.038 | negligible | Form > Chat | 0.9088 | 0.9101 | No |
| BERTScore_Recall | ch2 | Ask vs Chat | 491.0 | 0.017 | -0.319 | medium | Chat > Ask | 0.9025 | 0.9101 | No |
| BERTScore_Recall | ch3 | Form vs Ask | 1260.0 | <0.001 | 0.841 | large | Form > Ask | 0.9143 | 0.8802 | **Yes** |
| BERTScore_Recall | ch3 | Form vs Chat | 1315.0 | <0.001 | 0.823 | large | Form > Chat | 0.9143 | 0.8676 | **Yes** |
| BERTScore_Recall | ch3 | Ask vs Chat | 757.0 | 0.716 | 0.049 | negligible | Ask > Chat | 0.8802 | 0.8676 | No |
| BERTScore_Recall | ch4 | Form vs Ask | 1214.0 | <0.001 | 0.774 | large | Form > Ask | 0.9025 | 0.8811 | **Yes** |
| BERTScore_Recall | ch4 | Form vs Chat | 1385.0 | <0.001 | 0.920 | large | Form > Chat | 0.9025 | 0.8675 | **Yes** |
| BERTScore_Recall | ch4 | Ask vs Chat | 935.0 | 0.027 | 0.296 | small | Ask > Chat | 0.8811 | 0.8675 | No |
| BERTScore_Recall | ch5 | Form vs Ask | 903.0 | 0.018 | 0.319 | medium | Form > Ask | 0.8896 | 0.8784 | No |
| BERTScore_Recall | ch5 | Form vs Chat | 620.0 | 0.294 | -0.141 | small | Chat > Form | 0.8896 | 0.8910 | No |
| BERTScore_Recall | ch5 | Ask vs Chat | 438.0 | 0.003 | -0.393 | medium | Chat > Ask | 0.8784 | 0.8910 | **Yes** |
| BERTScore_Recall | ch6 | Form vs Ask | 725.0 | 0.665 | 0.059 | negligible | Form > Ask | 0.8836 | 0.8847 | No |
| BERTScore_Recall | ch6 | Form vs Chat | 561.0 | 0.096 | -0.222 | small | Chat > Form | 0.8836 | 0.9007 | No |
| BERTScore_Recall | ch6 | Ask vs Chat | 541.0 | 0.061 | -0.250 | small | Chat > Ask | 0.8847 | 0.9007 | No |
| BERTScore_F1 | ch1 | Form vs Ask | 509.0 | 0.059 | -0.256 | small | Ask > Form | 0.8629 | 0.8748 | No |
| BERTScore_F1 | ch1 | Form vs Chat | 715.5 | 0.954 | -0.008 | negligible | Chat > Form | 0.8629 | 0.8647 | No |
| BERTScore_F1 | ch1 | Ask vs Chat | 951.0 | 0.017 | 0.318 | medium | Ask > Chat | 0.8748 | 0.8647 | No |
| BERTScore_F1 | ch2 | Form vs Ask | 881.0 | 0.034 | 0.287 | small | Form > Ask | 0.8918 | 0.8812 | No |
| BERTScore_F1 | ch2 | Form vs Chat | 668.0 | 0.582 | -0.074 | negligible | Chat > Form | 0.8918 | 0.8959 | No |
| BERTScore_F1 | ch2 | Ask vs Chat | 487.0 | 0.015 | -0.325 | medium | Chat > Ask | 0.8812 | 0.8959 | **Yes** |
| BERTScore_F1 | ch3 | Form vs Ask | 1323.0 | <0.001 | 0.933 | large | Form > Ask | 0.9052 | 0.8740 | **Yes** |
| BERTScore_F1 | ch3 | Form vs Chat | 1228.0 | <0.001 | 0.702 | large | Form > Chat | 0.9052 | 0.8791 | **Yes** |
| BERTScore_F1 | ch3 | Ask vs Chat | 562.0 | 0.098 | -0.221 | small | Chat > Ask | 0.8740 | 0.8791 | No |
| BERTScore_F1 | ch4 | Form vs Ask | 977.0 | 0.002 | 0.427 | medium | Form > Ask | 0.8764 | 0.8589 | **Yes** |
| BERTScore_F1 | ch4 | Form vs Chat | 1048.0 | <0.001 | 0.453 | medium | Form > Chat | 0.8764 | 0.8686 | **Yes** |
| BERTScore_F1 | ch4 | Ask vs Chat | 686.0 | 0.716 | -0.049 | negligible | Chat > Ask | 0.8589 | 0.8686 | No |
| BERTScore_F1 | ch5 | Form vs Ask | 755.0 | 0.449 | 0.103 | small | Form > Ask | 0.8507 | 0.8383 | No |
| BERTScore_F1 | ch5 | Form vs Chat | 465.0 | 0.008 | -0.356 | medium | Chat > Form | 0.8507 | 0.8622 | **Yes** |
| BERTScore_F1 | ch5 | Ask vs Chat | 444.0 | 0.004 | -0.385 | medium | Chat > Ask | 0.8383 | 0.8622 | **Yes** |
| BERTScore_F1 | ch6 | Form vs Ask | 574.0 | 0.234 | -0.161 | small | Ask > Form | 0.8518 | 0.8683 | No |
| BERTScore_F1 | ch6 | Form vs Chat | 440.0 | 0.003 | -0.390 | medium | Chat > Form | 0.8518 | 0.8736 | **Yes** |
| BERTScore_F1 | ch6 | Ask vs Chat | 569.0 | 0.114 | -0.211 | small | Chat > Ask | 0.8683 | 0.8736 | No |
| SBERT_ModernBERT | ch1 | Form vs Ask | 524.0 | 0.084 | -0.234 | small | Ask > Form | 0.9752 | 0.9778 | No |
| SBERT_ModernBERT | ch1 | Form vs Chat | 760.5 | 0.689 | 0.054 | negligible | Form > Chat | 0.9752 | 0.9743 | No |
| SBERT_ModernBERT | ch1 | Ask vs Chat | 903.0 | 0.060 | 0.252 | small | Ask > Chat | 0.9778 | 0.9743 | No |
| SBERT_ModernBERT | ch2 | Form vs Ask | 784.0 | 0.284 | 0.145 | small | Form > Ask | 0.9811 | 0.9785 | No |
| SBERT_ModernBERT | ch2 | Form vs Chat | 556.0 | 0.086 | -0.229 | small | Chat > Form | 0.9811 | 0.9828 | No |
| SBERT_ModernBERT | ch2 | Ask vs Chat | 485.0 | 0.014 | -0.328 | medium | Chat > Ask | 0.9785 | 0.9828 | **Yes** |
| SBERT_ModernBERT | ch3 | Form vs Ask | 1160.0 | <0.001 | 0.695 | large | Form > Ask | 0.9821 | 0.9736 | **Yes** |
| SBERT_ModernBERT | ch3 | Form vs Chat | 1236.0 | <0.001 | 0.713 | large | Form > Chat | 0.9821 | 0.9751 | **Yes** |
| SBERT_ModernBERT | ch3 | Ask vs Chat | 712.0 | 0.925 | -0.013 | negligible | Chat > Ask | 0.9736 | 0.9751 | No |
| SBERT_ModernBERT | ch4 | Form vs Ask | 831.0 | 0.114 | 0.214 | small | Form > Ask | 0.9716 | 0.9682 | No |
| SBERT_ModernBERT | ch4 | Form vs Chat | 809.0 | 0.366 | 0.121 | small | Form > Chat | 0.9716 | 0.9739 | No |
| SBERT_ModernBERT | ch4 | Ask vs Chat | 675.0 | 0.633 | -0.064 | negligible | Chat > Ask | 0.9682 | 0.9739 | No |
| SBERT_ModernBERT | ch5 | Form vs Ask | 657.0 | 0.770 | -0.040 | negligible | Ask > Form | 0.9442 | 0.9441 | No |
| SBERT_ModernBERT | ch5 | Form vs Chat | 437.0 | 0.003 | -0.394 | medium | Chat > Form | 0.9442 | 0.9542 | **Yes** |
| SBERT_ModernBERT | ch5 | Ask vs Chat | 516.0 | 0.033 | -0.285 | small | Chat > Ask | 0.9441 | 0.9542 | No |
| SBERT_ModernBERT | ch6 | Form vs Ask | 495.0 | 0.041 | -0.277 | small | Ask > Form | 0.9615 | 0.9745 | No |
| SBERT_ModernBERT | ch6 | Form vs Chat | 434.0 | 0.003 | -0.398 | medium | Chat > Form | 0.9615 | 0.9756 | **Yes** |
| SBERT_ModernBERT | ch6 | Ask vs Chat | 616.0 | 0.275 | -0.146 | small | Chat > Ask | 0.9745 | 0.9756 | No |
| SBERT_MiniLM | ch1 | Form vs Ask | 454.0 | 0.013 | -0.337 | medium | Ask > Form | 0.6156 | 0.7646 | **Yes** |
| SBERT_MiniLM | ch1 | Form vs Chat | 694.5 | 0.783 | -0.037 | negligible | Chat > Form | 0.6156 | 0.6429 | No |
| SBERT_MiniLM | ch1 | Ask vs Chat | 952.0 | 0.017 | 0.319 | medium | Ask > Chat | 0.7646 | 0.6429 | No |
| SBERT_MiniLM | ch2 | Form vs Ask | 763.0 | 0.399 | 0.115 | small | Form > Ask | 0.7672 | 0.7615 | No |
| SBERT_MiniLM | ch2 | Form vs Chat | 948.0 | 0.019 | 0.314 | medium | Form > Chat | 0.7672 | 0.7240 | No |
| SBERT_MiniLM | ch2 | Ask vs Chat | 846.0 | 0.198 | 0.173 | small | Ask > Chat | 0.7615 | 0.7240 | No |
| SBERT_MiniLM | ch3 | Form vs Ask | 778.0 | 0.315 | 0.137 | small | Form > Ask | 0.7786 | 0.7640 | No |
| SBERT_MiniLM | ch3 | Form vs Chat | 1105.0 | <0.001 | 0.532 | large | Form > Chat | 0.7786 | 0.6998 | **Yes** |
| SBERT_MiniLM | ch3 | Ask vs Chat | 915.0 | 0.045 | 0.268 | small | Ask > Chat | 0.7640 | 0.6998 | No |
| SBERT_MiniLM | ch4 | Form vs Ask | 659.0 | 0.787 | -0.037 | negligible | Ask > Form | 0.6933 | 0.6979 | No |
| SBERT_MiniLM | ch4 | Form vs Chat | 480.0 | 0.012 | -0.335 | medium | Chat > Form | 0.6933 | 0.7510 | **Yes** |
| SBERT_MiniLM | ch4 | Ask vs Chat | 578.0 | 0.137 | -0.199 | small | Chat > Ask | 0.6979 | 0.7510 | No |
| SBERT_MiniLM | ch5 | Form vs Ask | 819.0 | 0.147 | 0.196 | small | Form > Ask | 0.5076 | 0.4662 | No |
| SBERT_MiniLM | ch5 | Form vs Chat | 531.0 | 0.048 | -0.264 | small | Chat > Form | 0.5076 | 0.5778 | No |
| SBERT_MiniLM | ch5 | Ask vs Chat | 451.0 | 0.005 | -0.375 | medium | Chat > Ask | 0.4662 | 0.5778 | **Yes** |
| SBERT_MiniLM | ch6 | Form vs Ask | 642.0 | 0.650 | -0.062 | negligible | Ask > Form | 0.6836 | 0.7175 | No |
| SBERT_MiniLM | ch6 | Form vs Chat | 606.0 | 0.232 | -0.160 | small | Chat > Form | 0.6836 | 0.7342 | No |
| SBERT_MiniLM | ch6 | Ask vs Chat | 668.0 | 0.582 | -0.074 | negligible | Chat > Ask | 0.7175 | 0.7342 | No |

### Summary Counts of Significant Cells

Family-wise correction across the 60 (metric × chapter) cells yields α = 0.05/60 ≈ 0.000833 for the family-wise-corrected Friedman count.

| Test | Significant cells / total | Threshold |
|---|---|---|
| Kruskal-Wallis omnibus           | 45 / 60   | α = 0.05 |
| Friedman omnibus (uncorrected)   | 45 / 60   | α = 0.05 |
| Friedman omnibus (Bonferroni-60) | 19 / 60 | α ≈ 0.000833 |
| Wilcoxon pairwise                | 68 / 180  | α = 0.0167 (per-cell Bonferroni-3) |
| Mann-Whitney pairwise            | 66 / 180  | α = 0.0167 (per-cell Bonferroni-3) |
## Per-Mode Completion Time

Source: timing line `Time elapsed: NNN seconds` emitted by ROPAgen at the end of every generated document (one value per participant × mode). Extracted via `metrics/scripts/per_mode_timing.py`. Sample sizes match the NLP doc-level analysis: full n = 113 (Form 37, Ask 37, Chat 39); matched-triple within-subjects subset n = 26.

### Descriptives (full dataset, n = 113)

| Mode | n | Mean (s) | SD (s) | Median (s) | IQR (s) | Min (s) | Max (s) |
|---|---|---|---|---|---|---|---|
| Form | 37 | 564.2 | 394.4 | 420.0 | 292.0 | 203 | 1993 |
| Ask | 37 | 989.8 | 675.8 | 858.0 | 443.0 | 289 | 3099 |
| Chat | 39 | 979.1 | 1015.4 | 717.0 | 616.5 | 182 | 6199 |

### Shapiro-Wilk normality (matched n = 26)

| Mode | W | p | Normal? |
|---|---|---|---|
| Form | 0.780 | <0.001 | No |
| Ask | 0.912 | 0.030 | No |
| Chat | 0.601 | <0.001 | No |

Distributions deviate from normality on at least one mode; non-parametric tests used throughout (consistent with the NLP and survey pipelines).

### Friedman test (within-subjects, n = 26)

| χ² | df | p | Kendall's W | Significant (α=0.05) |
|---|---|---|---|---|
| 18.692 | 2 | <0.001 | 0.359 | Yes |

Friedman is significant → pairwise Wilcoxon signed-rank post-hoc with Bonferroni-corrected α = 0.0167 (3 comparisons). Effect size: matched-pairs rank-biserial r (positive when the first-named mode in the pair is *higher*, i.e. *slower*).

### Pairwise Wilcoxon signed-rank (matched n = 26)

| Pair | W | p | r | Median diff (s) | Sig (Bonf) |
|---|---|---|---|---|---|
| form vs ask | 19.0 | <0.001 | -0.892 | -400.0 | **Yes** |
| form vs chat | 34.0 | <0.001 | -0.806 | -274.0 | **Yes** |
| ask vs chat | 162.0 | 0.745 | -0.077 | +68.5 | No |

### Kruskal-Wallis sensitivity (full n = 113, unbalanced)

| H | p | ε² | Significant (α=0.05) |
|---|---|---|---|
| 16.455 | <0.001 | 0.147 | Yes |

Reported as a between-groups sensitivity check on the unbalanced full sample; the matched-triple Wilcoxon family above is the primary inferential result.

### Pairwise Mann-Whitney U (full n = 113)

| Pair | U | p | r | Median A (s) | Median B (s) | Sig (Bonf α=0.0167) |
|---|---|---|---|---|---|---|
| form vs ask | 334.0 | <0.001 | +0.512 | 420.0 | 858.0 | **Yes** |
| form vs chat | 420.0 | 0.002 | +0.418 | 420.0 | 717.0 | **Yes** |
| ask vs chat | 793.5 | 0.457 | -0.100 | 858.0 | 717.0 | No |

### Data-quality notes

All 113 retained documents contain a canonical `Time elapsed: NNN seconds` line. No missing entries, no phrasing irregularities.

Cross-check vs. total survey duration:
- Extracted rows: 113 (expected 113)
- Per-mode counts: {'chat': 39, 'form': 37, 'ask': 37} (expected form=37, ask=37, chat=39)
- 1 participants where Σ(per-mode time) > total survey duration:
-   - AMR2620: Σmodes=3245s > duration=2870s
- 3 participants in docs but not in survey (no duration available): EII0925, IHB1316, LOT2142
- 8 participants with survey duration < 0 (encoded missing): EHN0215, IIV2704, IOL1223, Jer1205, RIT1851, UAB0821, UOR0445, thg1620

