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
