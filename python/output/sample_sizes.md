# Sample Sizes — Canonical Source of Truth

This document is the single canonical reference for every reported sample
size in the thesis *Assessing the Effectiveness of Large Language Model
Support for Generating GDPR ROPA Documentation*. All counts are derived
directly from the raw data files committed to the repository.

## Raw Data Sources

| Source | File | Rows |
|---|---|---|
| Survey responses | `python/survey/docs/data.csv` | 73 |
| Generated documents | `python/metrics/docs/documents.csv` | 113 |
| Free-text comments (extracted) | `python/survey/output/free_text_comments.csv` | 88 |

The survey file is one row per participant (wide format); 90 columns
covering ordering, the three per-mode SUS/TLX/AI blocks, ranking,
free-text fields, and demographics. The documents file is long format,
one row per generated ROPA document, keyed by `user_id` × `ai_mode`.

---

## Survey Sample Sizes

| Population | n | Definition |
|---|---|---|
| Recruited | 73 | All rows in `data.csv` |
| Valid | 69 | `p_0001 >= 1` (consent + quality filter); 4 rows had `p_0001 == -1` |
| Per-mode (Form / Ask / Chat) | 69 / 69 / 69 | All 22 per-mode items (10 SUS + 6 AI + 5 TLX demand + 1 TLX performance) present and within scale |
| Matched triple | 69 | All three modes fully complete for the same participant |
| Ranking | 69 | `rank_1`, `rank_2`, `rank_3` all present |
| Free-text comments | 88 across 44 unique participants | Non-empty `i_free` fields collected across `1_free` … `4_free` |

All 69 valid participants completed all three modes — there is no
participant in the valid set with a missing mode. The matched-triple n is
identical to the per-mode n, and identical to the valid n.

## Demographics Sample Sizes

| Variable | n reporting | Note |
|---|---|---|
| Duration | 69 | Includes one sentinel `-1` value (non-response) |
| GDPR / ROPA / Chatbot expertise | 69 each | All valid participants reported |
| Gender | 66 | Three valid participants did not report |
| Age | 69 | |
| Degree | 68 | One non-response |
| Profession | 69 | |
| Field | 69 | |

(`demographics_categorical_freq.csv` reports Degree counts summing to 68,
not 69 — one participant did not report Degree.)

---

## Document Sample Sizes

| Population | n | Definition |
|---|---|---|
| Retained documents | 113 | All rows in `documents.csv` |
| Form / Ask / Chat | 37 / 37 / 39 | `ai_mode` column |
| Unique participants in docs | 47 | Distinct `user_id` |
| Loose-match participants (≥ 1 doc per mode) | 28 | At least one document in each of Form, Ask, Chat |
| Strict matched-triple (exactly 1 doc per mode) | 26 | Exactly one document per mode — basis for all within-subjects NLP/judge tests |
| Duplicates | 4 user×mode cells | Three participants (AMR2620, IHB1316, IOL1223) submitted multiple documents in the same mode |

### Non-Completion Accounting

The expected full N (73 participants × 3 modes = 219 documents) is not
realised; the gap is 106 documents. The breakdown is:

- 26 participants have one document per mode (78 docs).
- 2 participants have ≥ 1 doc per mode but with duplicates (loose-match
  minus strict = 2, accounting for at most a few extra rows).
- 19 participants are represented in docs but missing at least one mode.
- 26 of the original 73 participants have no documents at all.

The dominant cause is per-participant non-completion (parsing failures or
sessions that ended before all three modes were submitted), not per-mode
selection bias: missing-mode counts are roughly balanced across the three
modes (Form 36, Ask 36, Chat 34 of 73 missing).

---

## Joined Sample Sizes (Survey × NLP)

The survey × NLP inner join links each surviving document to its
participant's survey row by `user_id == participant_id`. Two variants
exist:

| Variant | n rows | Form | Ask | Chat | Unique participants | Triangulated (≥ 1 per mode) |
|---|---|---|---|---|---|---|
| Join on all 73 survey rows (unfiltered) | 106 | 34 | 34 | 38 | 44 | 27 |
| Join on valid 69 survey rows (p_0001 ≥ 1) | 105 | 33 | 34 | 38 | 43 | 26 |

The thesis reports the **unfiltered (n = 106 / 44 unique / 27
triangulated)** join. Three document `user_id`s do not match any survey
row (EII0925, IHB1316, LOT2142), accounting for the difference between
113 docs and 106 join rows.

---

## Inferential-Test Sample Sizes (canonical Ns by test)

| Test family | n | Source population |
|---|---|---|
| SUS, R-TLX, AI questionnaire, ranking — within-subjects Friedman / Wilcoxon | 69 | Valid survey matched triple |
| Per-mode SUS/R-TLX/AI descriptives | 69 per mode | Valid survey |
| NLP & judge — within-subjects Friedman / Wilcoxon | 26 | Strict matched-triple docs |
| NLP & judge — full-sample Kruskal–Wallis / Mann–Whitney sensitivity | 113 (37/37/39) | All retained docs |
| Per-mode Spearman correlations (confidence × quality) | 34 / 34 / 38 | Survey × NLP join, no triple requirement |
| Triangulated correlations (all three modes per participant) | 27 | Survey × NLP join, ≥ 1 doc per mode |
| Per-mode completion-time within-subjects tests | 26 | Strict matched-triple docs (timing per doc) |

---

## Known Discrepancies vs. Earlier Thesis Drafts

- Earlier draft of `methodology.tex` line 69 claimed "valid N = 70" and
  "one participant has a valid Form response but no Ask/Chat." Both are
  **incorrect**: the valid N is 69 (not 70), and every valid participant
  completed all three modes (so per-mode n and matched-triple n are
  both 69, not 69 / 69 with the second derived as a subset).
- `freeform.tex` line 17 claims "$46$ unique participants" contributed
  the 88 free-text comments. The actual unique count in
  `free_text_comments.csv` is **44**.
- `methodology.tex` line 98 claims "73 participants × 3 modes = 219
  documents" but only 113 were retained; the 106-document gap is
  attributable to per-participant non-completion (26 of 73 participants
  have no documents at all; the remaining gap is per-mode dropout
  within partially-completed participants).

---

## Reproducibility

This file is regenerable from the raw data. To rebuild:

```python
import pandas as pd

survey = pd.read_csv('python/survey/docs/data.csv', sep=';')
docs = pd.read_csv('python/metrics/docs/documents.csv')
ft = pd.read_csv('python/survey/output/free_text_comments.csv')

# Recruited and valid
recruited = len(survey)                          # 73
valid = survey[survey['p_0001'] >= 1]            # 69
n_valid = len(valid)

# Per-mode and matched triple — all participant slots i in {1,2,3}
# carry 10 SUS + 6 AI + 5 TLX demand + 1 TLX performance items
def all_three_complete(row):
    for slot in (1, 2, 3):
        cols = (
            [f'{slot}_{j}_sus' for j in range(1, 11)]
            + [f'{slot}_{j}_ai' for j in range(1, 7)]
            + [f'{slot}_{j}_tlx_demand' for j in range(1, 6)]
            + [f'{slot}_1_tlx_performance']
        )
        if not (valid.loc[row.name, cols].fillna(-99) >= 1).all():
            return False
    return True
matched_triple = valid.apply(all_three_complete, axis=1).sum()  # 69

# Document sample
n_docs = len(docs)                                    # 113
mode_counts = docs['ai_mode'].value_counts().to_dict()  # form=37, ask=37, chat=39
n_unique = docs['user_id'].nunique()                  # 47
counts = docs.groupby(['user_id', 'ai_mode']).size().unstack(fill_value=0)
loose = (counts[['form', 'ask', 'chat']] >= 1).all(axis=1).sum()  # 28
strict = ((counts['form'] == 1) & (counts['ask'] == 1)
          & (counts['chat'] == 1)).sum()                            # 26

# Survey × NLP join (unfiltered — full 73)
join = docs.merge(survey[['participant_id']],
                  left_on='user_id', right_on='participant_id',
                  how='inner')
n_join = len(join)                          # 106
n_join_unique = join['user_id'].nunique()   # 44
joined_modes = join.groupby('user_id')['ai_mode'].apply(set)
triangulated = joined_modes.apply(
    lambda s: {'form', 'ask', 'chat'}.issubset(s)).sum()  # 27

# Free-text
n_ft = len(ft)                              # 88
n_ft_unique = ft['participant_id'].nunique()  # 44
```

Last regenerated: 2026-05-19 (Python 3.13, pandas 2.x).
