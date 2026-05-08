# Statistical Test Results — Survey

Source: `python/survey/ROPAgen_SURVEY.ipynb`. Sample sizes: see `thesis/chapters/sources.tex`
(Appendix, Section "Sample-Size Derivation").

---

## Dataset

- **N = 73** recruited; **n = 69** valid participants after consent and quality filtering
  (`p_0001 >= 1`).
- **Within-subjects design**: every participant completed all three modes (Form, Ask, Chat).
  All tests use the matched-triple n = 69 unless stated otherwise.
- **Counterbalancing**: Latin Square (6 groups), controls for order effects.

---

## Normality Testing (Shapiro-Wilk, n = 69 per mode)

Non-normal distributions detected across nearly all measures. Non-parametric tests used
throughout.

| Measure | Mode | W | p | Normal? |
|---|---|---|---|---|
| SUS | Form | 0.944 | 0.004 | No |
| SUS | Ask | 0.976 | 0.210 | Yes |
| SUS | Chat | 0.927 | 0.001 | No |
| RTLX composite | Form | 0.940 | 0.003 | No |
| RTLX composite | Ask | 0.926 | 0.001 | No |
| RTLX composite | Chat | 0.945 | 0.005 | No |
| AI Support (6-item) | Form | 0.923 | <0.001 | No |
| AI Support (6-item) | Ask | 0.965 | 0.048 | No |
| AI Support (6-item) | Chat | 0.952 | 0.010 | No |
| AI Confidence (5_ai) | Form | 0.846 | <0.001 | No |
| AI Confidence (5_ai) | Ask | 0.856 | <0.001 | No |
| AI Confidence (5_ai) | Chat | 0.864 | <0.001 | No |
| AI Reuse (6_ai) | Form | 0.799 | <0.001 | No |
| AI Reuse (6_ai) | Ask | 0.872 | <0.001 | No |
| AI Reuse (6_ai) | Chat | 0.861 | <0.001 | No |

---

## Friedman Omnibus Test (n = 69 matched triple)

Non-parametric repeated-measures test across all three modes. Kendall's W effect-size
labels: 0–0.1 weak, 0.1–0.3 moderate, 0.3–0.5 strong.

| Measure | χ² | df | p | W | Significant |
|---|---|---|---|---|---|
| SUS (0–100, higher = better) | 5.51 | 2 | 0.064 | 0.040 | No |
| R-TLX composite (1–21) | 5.24 | 2 | 0.073 | 0.038 | No |
| R-TLX Mental Demand | 3.13 | 2 | 0.209 | 0.023 | No |
| R-TLX Physical Demand | 2.08 | 2 | 0.354 | 0.015 | No |
| R-TLX Temporal Demand | 12.77 | 2 | 0.002 | 0.093 | **Yes** |
| R-TLX Effort | 3.78 | 2 | 0.151 | 0.027 | No |
| R-TLX Frustration | 8.93 | 2 | 0.012 | 0.065 | **Yes** |
| R-TLX Performance (pos-coded) | 2.33 | 2 | 0.311 | 0.017 | No |
| AI Confidence (item 5_ai) | 3.76 | 2 | 0.152 | 0.027 | No |
| AI Support (6-item composite) | 1.05 | 2 | 0.592 | 0.008 | No |
| AI Reuse intention (item 6_ai) | 11.12 | 2 | 0.004 | 0.081 | **Yes** |

**Significant omnibus effects**: Temporal Demand (W = 0.093), Frustration (W = 0.065),
AI Reuse intention (W = 0.081) — all weak to near-moderate. SUS and overall RTLX composite
do not reach significance, though effect sizes are in the negligible-to-weak range.

---

## Post-hoc Pairwise Wilcoxon Signed-Rank Tests (n, Bonferroni α = 0.0167)

Post-hoc tests run only for measures with a significant Friedman result. Sign convention:
positive r means the first-named mode scores higher. Effect-size labels: |r| < 0.1
negligible, 0.1–0.3 small, 0.3–0.5 medium, ≥ 0.5 large.

| Measure | Pair | n | W | p | r | Significant (Bonf) |
|---|---|---|---|---|---|---|
| SUS | Form vs Ask | 60 | 578.5 | 0.013 | +0.368 (medium) | **Yes** |
| SUS | Form vs Chat | 58 | 549.5 | 0.018 | +0.358 (medium) | No |
| SUS | Ask vs Chat | 61 | 885.5 | 0.666 | −0.063 (negligible) | No |
| R-TLX composite | Form vs Ask | 65 | 684.0 | 0.011 | −0.362 (medium) | **Yes** |
| R-TLX composite | Form vs Chat | 65 | 636.0 | 0.004 | −0.407 (medium) | **Yes** |
| R-TLX composite | Ask vs Chat | 63 | 995.5 | 0.932 | +0.012 (negligible) | No |
| Temporal Demand | Form vs Ask | 43 | 237.0 | 0.004 | −0.499 (medium) | **Yes** |
| Temporal Demand | Form vs Chat | 46 | 233.0 | <0.001 | −0.569 (large) | **Yes** |
| Temporal Demand | Ask vs Chat | 46 | 427.0 | 0.211 | −0.210 (small) | No |
| Frustration | Form vs Ask | 52 | 403.5 | 0.009 | −0.414 (medium) | **Yes** |
| Frustration | Form vs Chat | 57 | 519.5 | 0.014 | −0.371 (medium) | **Yes** |
| Frustration | Ask vs Chat | 52 | 629.0 | 0.584 | +0.087 (negligible) | No |
| AI Reuse (6_ai) | Form vs Ask | 49 | 402.5 | 0.034 | +0.343 (medium) | No |
| AI Reuse (6_ai) | Form vs Chat | 43 | 216.0 | 0.002 | +0.543 (large) | **Yes** |
| AI Reuse (6_ai) | Ask vs Chat | 45 | 454.5 | 0.468 | +0.122 (small) | No |

**Key pattern:** Form consistently outperforms on usability (SUS Form > Ask, medium effect)
and imposes lower cognitive load (RTLX Form < Ask and Form < Chat, both medium effects;
Temporal Demand and Frustration follow the same pattern). Ask and Chat do not differ
significantly on any measure. Form is also preferred for reuse over Chat (large effect).

---

## Mode Preference Ranking (n = 69)

Participants ranked all three modes after completing the study (1 = most preferred).

| Mode | Rank-1 votes | Share | Mean rank (1–3) |
|---|---|---|---|
| Form | 37 | 53.6 % | 1.78 |
| Chat | 20 | 29.0 % | 2.07 |
| Ask | 12 | 17.4 % | 2.14 |

**Chi-square goodness-of-fit** (rank-1 votes vs. uniform null):
χ²(2, N = 69) = 14.17, p < 0.001, Cramér's V = 0.320 (medium effect).

**Friedman on full rank scores** (1–3): χ²(2) = 5.07, p = 0.079, W = 0.037. The omnibus
on rank scores is non-significant, reflecting that the strong Form preference at rank 1
is partially balanced by variance at ranks 2 and 3. The chi-square on rank-1 votes
is the more interpretable test for preference.

---

## Descriptive Statistics by Mode (n = 69 per mode, matched triple)

| Measure | Form | Ask | Chat |
|---|---|---|---|
| SUS (0–100) mean ± SD | 78.62 ± 16.09 | 72.97 ± 15.36 | 72.93 ± 19.03 |
| SUS median | 80.0 | 72.5 | 75.0 |
| R-TLX composite (1–21) mean | 5.50 | 6.33 | 6.33 |
| AI Support composite (1–5) mean | 3.86 | 3.97 | 3.80 |
| AI Confidence 5_ai (1–5) mean | 3.58 | 3.74 | 3.81 |
| AI Reuse 6_ai (1–5) mean | 3.99 | 3.55 | 3.42 |

### R-TLX Subscale Means by Mode (1–21 scale, n = 69)

| Subscale | Form | Ask | Chat |
|---|---|---|---|
| Mental Demand | 5.77 ± 4.23 | 6.80 ± 4.60 | 6.36 ± 5.27 |
| Physical Demand | 2.77 ± 2.69 | 3.54 ± 3.89 | 3.26 ± 3.43 |
| Temporal Demand | 4.16 ± 3.79 | 4.97 ± 4.12 | 5.54 ± 4.74 |
| Effort | 5.68 ± 4.53 | 6.39 ± 4.37 | 6.32 ± 4.74 |
| Frustration | 5.88 ± 4.80 | 7.58 ± 5.30 | 7.13 ± 5.41 |
| Performance (pos-coded) | 8.71 ± 5.44 | 8.68 ± 5.60 | 9.39 ± 6.32 |

Form scores lower than Ask/Chat on all demand subscales; Frustration shows the largest
absolute gap (Form 5.88 vs Ask 7.58). Ask and Chat are similar across all subscales.

### AI Support Per-Item Means (1–5 Likert, n = 69)

| Item | Text | Form | Ask | Chat |
|---|---|---|---|---|
| 1_ai | The AI was helpful in creating this document. | 4.23 | 4.32 | 4.13 |
| 2_ai | The AI helped me to complete the document faster. | 4.43 | 4.25 | 3.99 |
| 3_ai | I understood why the AI suggested specific GDPR fields. | 3.51 | 4.16 | 3.75 |
| 4_ai | I trust that the AI made correct suggestions. | 3.41 | 3.80 | 3.68 |
| 5_ai | I am confident that the AI identified the correct legal basis. | 3.58 | 3.74 | 3.81 |
| 6_ai | I would use this mode again. | 3.99 | 3.55 | 3.42 |

Notable: Ask and Chat score higher than Form on transparency (3_ai) and trust (4_ai),
but Form scores highest on efficiency (2_ai) and reuse intent (6_ai). Legal-basis
confidence (5_ai) increases monotonically with LLM involvement: Form < Ask < Chat.

---

## Limitations

- All survey tests use n = 69 within-subjects; no between-subjects comparisons.
- Likert items are ordinal; non-parametric tests appropriate throughout.
- SUS and RTLX omnibus effects are non-significant — observed differences are descriptive
  trends, not confirmed by formal inference.
- Mode preference (rank-1 votes) shows a clear Form plurality but Friedman on full
  rank scores does not reach significance, indicating preference strength varies across
  participants.
- Single GDPR scenario (APOR GmbH); sample is student-only with high chatbot familiarity
  but low GDPR/ROPA prior knowledge.
