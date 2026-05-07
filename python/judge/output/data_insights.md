# Data Insights — ropagen Document Quality Analysis

Generated from `all_scores_combined.csv` (113 documents: Form n=37, Ask n=37, Chat n=39).

---

## Insight 1 — Consistent high vs. low performers across all three modes

**Finding:** A small group of participants produced consistently high-quality documents across all three modes, while another group produced uniformly poor output regardless of the interaction paradigm offered.

**Evidence:**

Top 3 consistent HIGH performers (users with all 3 mode docs, ranked by composite BERTScore F1 + judge Overall):

| user_id | BERTScore F1 mean | BERTScore F1 std | Overall mean | Doc IDs (form/ask/chat) |
|---|---|---|---|---|
| AAL1220 | 0.904 | 0.009 | 4.0 | 25/27/26 |
| UOR0445 | 0.912 | 0.007 | 3.67 | 93/92/94 |
| NUG0102 | 0.907 | 0.012 | 3.67 | 21/19/18 |

Top 3 consistent LOW performers:

| user_id | BERTScore F1 mean | BERTScore F1 std | Overall mean | Doc IDs (form/ask/chat) |
|---|---|---|---|---|
| PVV2109 | 0.882 | 0.014 | 1.0 | 60/59/63 |
| EHJ2314 | 0.894 | 0.011 | 1.67 | 96/97/100 |
| VAG2434 | 0.901 | 0.007 | 1.67 | 88/90/89 |

PVV2109 is the most extreme case: the mode-level best scores barely exceed the study average, and judge Overall = 1 (poor) for all three modes. By contrast, AAL1220 consistently achieves Overall ≥ 3 with minimal variability. PVV2109's doc 59 (Ask) is the existing Fallbeispiel for the confidence-quality gap — this cross-mode data confirms it is not an Ask-mode artefact but a user-level pattern.

**Thesis relevance:** Evaluation chapter, RQ2 — mode effects are modulated by participant-level factors. The spread in individual performance suggests that prior GDPR/legal familiarity (or document-writing competence) is a stronger determinant of quality than mode choice.

---

## Insight 2 — No systematic learning effect; document quality driven by session order

**Finding:** Among the 25 participants with session-1 and session-3 data, quality changes between first and last mode were small and unsystematic. The five largest improvements all began with Ask (session 1), while the five largest drops all began with Form.

**Evidence:**

Largest BERTScore F1 improvements (session 1 → session 3):

| user_id | Session 1 mode | Session 3 mode | S1 BERTScore F1 | S3 BERTScore F1 | Δ | Δ Overall |
|---|---|---|---|---|---|---|
| aea2442 | ask | form | 0.898 | 0.918 | +0.020 | 0 |
| UAB0821 | ask | chat | 0.891 | 0.906 | +0.015 | +2 |
| AHR0531 | chat | ask | 0.896 | 0.910 | +0.014 | +2 |
| IAR1116 | ask | chat | 0.898 | 0.909 | +0.011 | +2 |

Largest BERTScore F1 drops (session 1 → session 3):

| user_id | Session 1 mode | Session 3 mode | S1 BERTScore F1 | S3 BERTScore F1 | Δ | Δ Overall |
|---|---|---|---|---|---|---|
| EHJ2314 | form | chat | 0.906 | 0.885 | −0.021 | −1 |
| EHN0215 | form | ask | 0.918 | 0.897 | −0.021 | −1 |
| NIL1922 | form | chat | 0.912 | 0.892 | −0.020 | −1 |
| MIN0453 | form | ask | 0.911 | 0.894 | −0.017 | +1 |

The pattern inverts the expected learning-effect direction: starting with Form (the most structured mode) tends to produce a higher session-1 score, and subsequent modes can only go down. Starting with Ask (the weakest mode) leaves room for improvement. This is a Latin Square confound, not a learning effect.

**Thesis relevance:** Evaluation/Discussion chapters — helps address the counterbalancing design; confirms there is no dominant "learning effect" that inflates later-session scores. The EHN0215 trajectory (Form=0.918 → Ask=0.897) matches the macro-level Ask underperformance finding and provides an individual-level illustration.

---

## Insight 3 — NLP metric disagreements: surface vs. semantic mismatch

**Finding:** Several documents show meaningful divergence between surface-overlap metrics (BLEU, ROUGE) and semantic metrics (BERTScore, SBERT), illustrating the limits of surface metrics for legal text generation.

**Evidence:**

No documents meet the strict threshold of BLEU < 0.08 AND BERTScore F1 > 0.91 simultaneously (the minimum BLEU in the dataset is 0.047). Using the empirical lower quartile (BLEU < 0.093) as the "low surface" threshold and BERTScore F1 > 0.90 as "high semantic":

Documents with very low BLEU but still high BERTScore F1 (semantic richness despite surface mismatch):

| doc_id | user_id | mode | BLEU | BERTScore F1 | SBERT | Overall |
|---|---|---|---|---|---|---|
| 7 | RIT1851 | ask | 0.085 | 0.904 | 0.987 | 4 |
| 48 | ENB1054 | form | 0.088 | 0.901 | 0.982 | 2 |
| 112 | DLZ2800 | form | 0.087 | 0.900 | 0.984 | 2 |

Documents with high BLEU but below-average BERTScore F1 (surface overlap without semantic depth):

| doc_id | user_id | mode | BLEU | BERTScore F1 | SBERT | Overall |
|---|---|---|---|---|---|---|
| 103 | NAB0152 | ask | 0.151 | 0.882 | 0.987 | 1 |
| 101 | ALB0226 | chat | 0.165 | 0.890 | 0.987 | 1 |
| 64 | NIL1922 | chat | 0.187 | 0.892 | 0.987 | 1 |
| 117 | UTP0442 | chat | 0.164 | 0.893 | 0.988 | 1 |

The second group is particularly notable: BLEU ≥ 0.15 (well above the median of 0.128), suggesting substantial n-gram overlap with the reference, yet BERTScore F1 falls below 0.895 (below the Ask mode mean) and judge Overall = 1 for all four cases. These are documents that copied surface phrasing without producing semantically coherent ROPA content — a pattern consistent with formulaic completion without understanding.

**Thesis relevance:** Methodology chapter (metric validity) and Discussion — supports the use of BERTScore and SBERT as primary quality indicators over BLEU/ROUGE for this task. The second group is direct evidence that high BLEU does not imply high quality for legal document generation.

---

## Insight 4 — Judge vs. NLP divergence: the clearest RQ2 evidence

**Finding:** Eleven documents have NLP composite scores in the top quartile but judge Overall ≤ 2 ("looks good by metrics, poor by legal quality"). Five documents have NLP composite in the bottom quartile but judge Overall ≥ 4 ("genuine quality despite weak surface metrics").

**Evidence:**

NLP composite = mean(BLEU×10, ROUGE-1, METEOR, BERTScore F1, SBERT). Q25 = 0.729, Q75 = 0.886.

High NLP / Low judge (11 documents):

| doc_id | user_id | mode | NLP composite | BERTScore F1 | Overall | Completeness | Halluc_inv | Scenario_faith |
|---|---|---|---|---|---|---|---|---|
| 30 | IOL1223 | ask | 1.095 | 0.917 | 2 | 2 | 4 | 2 |
| 35 | IOL1223 | chat | 1.042 | 0.912 | 2 | 2 | 3 | 2 |
| 36 | IOL1223 | chat | 1.037 | 0.912 | 2 | 2 | 3 | 2 |
| 71 | IHB1316 | ask | 1.028 | 0.913 | 1 | 2 | 3 | 2 |
| 42 | EII0925 | chat | 0.992 | 0.912 | 2 | 2 | 2 | 3 |
| 61 | NIL1922 | form | 0.989 | 0.912 | 2 | 3 | 2 | 2 |
| 17 | NOC2416 | chat | 0.948 | 0.909 | 2 | 2 | 2 | 2 |
| 22 | IHL0436 | form | 0.941 | 0.907 | 2 | 3 | 2 | 2 |
| 64 | NIL1922 | chat | 0.906 | 0.892 | 1 | 1 | 4 | 1 |
| 46 | MIN0453 | form | 0.898 | 0.911 | 2 | 5 | 1 | 2 |
| 15 | NOC2416 | form | 0.889 | 0.907 | 2 | 5 | 2 | 2 |

Doc 30 (IOL1223/Ask) is the clearest case: highest NLP composite in the dataset (1.095), BERTScore F1 = 0.918 (top decile), yet judge Overall = 2. The judge rationale (see `judge_results.csv`) shows this document completely omits the parking lot authorization (a key scenario element), fails to specify actual data categories, and misuses legal citation structure — none of which surface metrics can detect. IOL1223's Ask document (doc 29) achieves the highest BLEU in the entire dataset (0.246) yet receives Overall = 3; the Ask doc is even worse (Overall = 2). This participant appears to have copied reference phrasing closely while missing the substantive content requirements.

Low NLP / High judge (5 documents):

| doc_id | user_id | mode | NLP composite | BERTScore F1 | Overall | Completeness | Halluc_inv | Scenario_faith |
|---|---|---|---|---|---|---|---|---|
| 27 | AAL1220 | ask | 0.699 | 0.895 | 4 | 5 | 3 | 4 |
| 28 | thg1620 | chat | 0.700 | 0.896 | 4 | 5 | 3 | 3 |
| 7 | RIT1851 | ask | 0.714 | 0.904 | 4 | 5 | 2 | 4 |
| 19 | NUG0102 | ask | 0.717 | 0.894 | 4 | 5 | 3 | 4 |
| 52 | ENB1054 | chat | 0.718 | 0.902 | 4 | 5 | 3 | 4 |

These five documents — all with judge Overall = 4, Completeness = 5 — diverge from the reference structurally (low BLEU) but are substantively complete and legally sound. They represent participants who understood the task well enough to express the required content in their own words, producing documents that pass legal quality checks even when failing the n-gram matching test.

**Thesis relevance:** This is the core RQ2 evidence. The 11 "high NLP / low judge" documents prove that NLP metrics can mislead — high scores do not guarantee GDPR-compliant content. The 5 "low NLP / high judge" documents prove the mirror: reference-dissimilar documents can still be high quality. Together, they motivate the dual-evaluation design (NLP + LLM-as-judge) and support the Discussion argument that neither metric family alone suffices.

---

## Insight 5 — Completeness paradox: Form's structural completeness masks systematic hallucination

**Finding:** 31 out of 37 Form documents (84%) score Completeness = 5 (maximum) but simultaneously score Hallucination_inverse ≤ 2 (i.e., the judge detected significant fabricated content). Form's checkbox interface fills every field but does not prevent — and may actively encourage — users to invent plausible-sounding content to satisfy required fields.

**Evidence:**

- Form Completeness distribution: score=3 (n=3), score=5 (n=34). No intermediate values — Form produces either complete or near-complete documents.
- Form Hallucination_inverse distribution: score=1 (n=17, "significant hallucination"), score=2 (n=17, "moderate hallucination"), score=3 (n=2), score=4 (n=1).
- 17 Form documents score both Completeness=5 AND Hallucination_inverse=1 — structurally perfect but with the worst fabrication score.

Example documents (Completeness=5, Hallucination_inverse=1):

| doc_id | user_id | BERTScore F1 | Overall | Scenario_faithfulness |
|---|---|---|---|---|
| 60 | PVV2109 | 0.898 | 1 | 1 |
| 91 | KIR2546 | 0.893 | 1 | 1 |
| 110 | UAB0821 | 0.887 | 2 | 1 |
| 53 | ATN238 | 0.893 | 2 | 1 |
| 54 | YÜI1752 | 0.897 | 2 | 1 |

For comparison, this structural completeness advantage disappears in judge Overall scores: Form mean Overall = 2.41, Ask mean = 2.49, Chat mean = 2.62 (judge_summary.csv). Completeness alone does not drive quality.

**Thesis relevance:** Evaluation and Discussion chapters, RQ2 — the completeness paradox is one of the thesis's strongest arguments. Form's design guarantees structural completeness at the cost of accuracy; users are prompted to enter *something* for each field, and when they lack knowledge, they fabricate. This is a GDPR compliance risk that surface NLP metrics (which reward coverage) cannot capture.

---

## Insight 6 — Ask mode outliers: low recall = incomplete short documents, not errors

**Finding:** The 4 Ask documents with BERTScore Recall < 0.88 are not randomly distributed — they cluster at Overall = 1 and Completeness = 1, suggesting they are extremely short or incomplete outputs rather than structurally different documents.

**Evidence:**

| doc_id | user_id | BERTScore Recall | BLEU | ROUGE-1 | Completeness | Overall | Halluc_inv |
|---|---|---|---|---|---|---|---|
| 75 | DAB1519 | 0.861 | 0.112 | 0.371 | 1 | 1 | 4 |
| 57 | OAZ2611 | 0.863 | 0.146 | 0.392 | 1 | 1 | 4 |
| 32 | thg1620 | 0.865 | 0.134 | 0.382 | 1 | 1 | 4 |
| 103 | NAB0152 | 0.874 | 0.151 | 0.421 | 1 | 1 | 3 |

All four have Completeness = 1 (missing most required ROPA fields) and Overall = 1. Hallucination_inverse = 4 (low hallucination) — these are documents that said very little rather than documents that said wrong things. Low recall means they cover little of the reference content; paired with low ROUGE-1 and below-average BLEU, these are short outputs. Doc 32 (thg1620/Ask) is particularly striking: the same participant's Chat document (doc 28) scores Overall = 4 with Completeness = 5, confirming this is a mode-specific failure rather than a participant-level pattern.

SBERT scores for these four documents (0.979–0.987) remain within the normal range, indicating that even these very short documents are not semantically incoherent — they just lack substance.

**Thesis relevance:** Evaluation chapter — explains the Ask mode's lower mean BERTScore Recall (0.908 vs Form 0.923). These four documents are not randomly poor; they are documents where the Ask interaction did not elicit sufficient information from the participant. The guided-dialogue format may have allowed participants to give minimal responses at each step, producing an incomplete but non-hallucinatory document.

---

## Insight 7 — Confidence (item 5_ai) does not track hallucination within mode

**Operationalisation note (corrected):** Earlier versions of this insight used
`survey_summary.csv`'s `AI_confidence` column, which was computed from item
`6_ai` ("I would use this mode again") — an *intent-to-use* item, not a
confidence item. The corrected primary confidence measure is item **`5_ai`**
("I am confident the AI identified the correct legal basis"). The numbers
below use `5_ai`. For comparison, the 6-item Perceived AI Support composite is
reported as a secondary measure in `statistical_tests.md`.

**Finding:** With the corrected operationalisation, within-mode Pearson
correlations between item `5_ai` and `Hallucination_inverse` are essentially
zero in Form (r = −0.06) and Ask (r = −0.08), and weakly positive in Chat
(r = +0.16). The earlier "Form confidence-hallucination anti-correlation" of
r = −0.25 was an artefact of using item `6_ai` (intent-to-use); it is **not**
present when confidence is operationalised as item `5_ai`.

**Evidence (joined sample n = 106; per-mode n = 34/34/38):**

Form users with AI_confidence (5_ai) = 5: n = 4 (not 18). Among these:
- Hallucination_inverse = 1: 2 users
- Hallucination_inverse = 2: 1 user
- Hallucination_inverse = 3: 1 user
- Mean Hallucination_inverse: 1.75
- Mean Overall: 2.75

The high-confidence Form group is too small (n = 4) to support a within-cell
claim about hallucination rates.

Pearson correlations (5_ai vs Hallucination_inverse):
- Form: r = −0.06 (p = 0.75, n = 34)
- Ask:  r = −0.08 (p = 0.64, n = 34)
- Chat: r = +0.16 (p = 0.34, n = 38)

None are significant. The directional pattern (negative in Form/Ask, positive
in Chat) matches the BERTScore F1 correlations reported in
`statistical_tests.md` but the effect is too small to claim a within-mode
confidence-hallucination link.

**Thesis relevance:** What survives is the **between-mode rank inversion**
(Form lowest confidence + highest BERTScore F1; Ask 2nd confidence + lowest
quality), not a within-mode confidence-hallucination correlation. The
mechanistic Discussion argument should now read: Form's checkbox interface
produces structurally complete but frequently fabricated content (Insight 5),
**and** Form users — who lack the interactive AI commentary that Ask and Chat
provide — report the lowest legal-basis confidence even though their
documents score highest by NLP metrics. The compliance risk argument is
unchanged; the confidence-as-warning-signal sub-argument is weaker than
previously stated and should be framed cautiously.

---

## Cross-insight summary for Discussion

The seven insights above collectively support three thesis-level arguments:

1. **Mode effects are real but small; individual variation is larger** (Insights 1, 2): The NLP metric differences between modes (ΔBERTScore F1 ≈ 0.008) are statistically significant but practically small. Individual-level performance variation dwarfs mode-level differences. The study identifies consistent high and low performers whose quality trajectories are stable across modes.

2. **NLP metrics and judge scores measure different things, and both are needed** (Insights 3, 4): Surface metrics (BLEU) reward n-gram copying but miss legal completeness and scenario faithfulness. Judge Overall captures these but is correlated only weakly with NLP scores (see 11 "high NLP / low judge" documents). The dual-evaluation design is justified by this divergence.

3. **Form's completeness advantage is structurally enforced and comes at a compliance cost** (Insight 5): Form's checkbox design guarantees Completeness = 5 for most users but simultaneously produces the highest rate of hallucinated content. Users fill every field, but novices without domain knowledge invent plausible-sounding answers. This is arguably the most policy-relevant finding of the thesis. The original confidence-hallucination anti-correlation (former Insight 7) does not survive correct operationalisation of confidence (item 5_ai); the surviving cross-mode rank-inversion (Form lowest 5_ai confidence + highest BERTScore F1) supports the same Discussion conclusion via a different mechanism — see `statistical_tests.md` RQ2 section.
