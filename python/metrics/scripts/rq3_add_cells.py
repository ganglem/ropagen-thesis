"""Append RQ3 triangulation cells to ROPAgen_METRICS.ipynb.

Idempotent: removes any previous '## RQ3 Triangulation' section
before appending the freshly-built cells. Run from python/.
"""
from __future__ import annotations
import json
import uuid
from pathlib import Path

NB_PATH = Path('metrics/ROPAgen_METRICS.ipynb')
MARKER = '## RQ3 Triangulation'


def _cell_id() -> str:
    return uuid.uuid4().hex[:8]


def md_cell(text: str) -> dict:
    return {
        'cell_type': 'markdown',
        'id': _cell_id(),
        'metadata': {},
        'source': text.splitlines(keepends=True),
    }


def code_cell(text: str) -> dict:
    return {
        'cell_type': 'code',
        'execution_count': None,
        'id': _cell_id(),
        'metadata': {},
        'outputs': [],
        'source': text.splitlines(keepends=True),
    }


nb = json.loads(NB_PATH.read_text(encoding='utf-8'))

# ── Remove any existing RQ3 section (everything from the marker onward) ──────
keep = []
for cell in nb['cells']:
    src = ''.join(cell['source'])
    if cell['cell_type'] == 'markdown' and MARKER in src:
        break
    keep.append(cell)
# If the marker was found, the loop broke before appending it; drop trailing
# cells after the marker we kept. We need to also drop subsequent cells that
# were part of the RQ3 section. The break above already accomplishes that —
# everything from the marker onward is excluded.
nb['cells'] = keep

# ── New cells ────────────────────────────────────────────────────────────────
cells_to_add: list[dict] = []

cells_to_add.append(md_cell(
    """## RQ3 Triangulation — Confidence vs Quality

This section produces the numbers that lead the RQ3 (alignment between user
confidence and document quality) discussion. The framing is:

1. **Primary triangulation** — user AI-confidence (survey item 5 "AI identified
   the correct legal basis" and the overall `AI_support` mean of items 1–6)
   against reference-based NLP metrics (BERTScore F1 and SBERT primary; BLEU,
   ROUGE-L, METEOR secondary).
2. **Supplementary cross-check** — bring in the LLM-as-judge scores
   (`legal_correctness`, `overall`) as a *third*, reference-free lens, not as
   the headline measure.

### Data audit and duplicate-resolution rule

`metrics/output/document_results.csv` contains 113 rows for 47 unique
participants — fewer than the planned 73 × 3 = 219 because not all
participant documents were recoverable from the ropagen logs. Four
participant × mode pairs have multiple `id` rows in the source
`docs/documents.csv`:

| user_id | mode | dupes | note |
| --- | --- | --- | --- |
| AMR2620 | chat | 3 (ids 105, 106, 107) | 105/106 identical; 107 is a longer revised submission |
| IHB1316 | form | 2 (ids 69, 70) | identical content |
| IOL1223 | ask  | 2 (ids 29, 30) | identical content |
| IOL1223 | chat | 2 (ids 35, 36) | near-identical, last is the final revision |

**Rule:** keep the row with the highest `id` per (`user_id`, `ai_mode`) — i.e.
the latest/canonical submission. This yields 108 unique participant × mode
documents. The same rule is applied to the judge file so the two stay
aligned.

After inner-joining with the survey on `participant_id` ↔ `user_id`, three
users in the documents file have no matching survey row (`LOT2142`,
`IHB1316`, `EII0925`), reducing the analysis dataset to **n = 102** total
(form n=34, ask n=33, chat n=35) across **44 unique participants**.
"""
))

cells_to_add.append(md_cell(
    """### Step 1 — AI confidence × NLP metrics (primary triangulation)

Join survey item 5 + `AI_support` mean per (participant, mode) with the
deduped per-document NLP scores. Then compute:

- Per-mode means and ranks for `item5`, `AI_support`, `BERTScore_F1`, `SBERT`.
- Spearman ρ (and p-value) — pooled and per-mode — for confidence vs each
  NLP metric. Spearman is rank-based and so makes no normality assumption,
  which fits the Likert item 5 and the skewed NLP distributions.

Outputs (saved to `output/`):

- `rq3_confidence_nlp_corr.csv` — pooled + per-mode correlations.
- `rq3_per_mode_ranks.csv` — compact rank table.
"""
))

cells_to_add.append(code_cell(
    '''# ── RQ3 Step 1: AI confidence × NLP metrics ────────────────────────────────
import pandas as pd
import numpy as np
from scipy.stats import spearmanr
from IPython.display import display

OUT = "output"

# ── Load NLP per-document scores and deduplicate (keep latest id) ───────────
nlp_raw = pd.read_csv(f"{OUT}/document_results.csv")
nlp = (nlp_raw.sort_values("id")
              .drop_duplicates(["user_id", "ai_mode"], keep="last")
              .reset_index(drop=True))
print(f"NLP: {len(nlp_raw)} raw rows → {len(nlp)} after dedup "
      f"({nlp.user_id.nunique()} unique users)")

# ── Load survey, unpivot to (participant_id, mode) long form ────────────────
survey = pd.read_csv("../survey/docs/data.csv", sep=";")

ai_records = []
for _, row in survey.iterrows():
    for pos in (1, 2, 3):
        mode = row[f"{pos}_order"]
        if pd.isna(mode):
            continue
        rec = {"participant_id": row["participant_id"],
               "mode": str(mode).lower()}
        for q in range(1, 7):
            v = row[f"{pos}_{q}_ai"]
            rec[f"item{q}"] = np.nan if v == -99 else v
        ai_records.append(rec)

conf = pd.DataFrame(ai_records)
conf = conf[conf["mode"].isin(["form", "ask", "chat"])].reset_index(drop=True)
conf["AI_support"] = conf[[f"item{i}" for i in range(1, 7)]].mean(axis=1)
print(f"Confidence long: {len(conf)} rows ({conf.participant_id.nunique()} participants)")

# ── Inner-join (only documents with matching survey responses) ──────────────
merged = conf.merge(nlp,
                    left_on=["participant_id", "mode"],
                    right_on=["user_id", "ai_mode"],
                    how="inner")
print(f"Merged: {len(merged)} rows | participants = {merged.participant_id.nunique()}")
print("Per-mode n:", merged["mode"].value_counts().to_dict())

# ── Helper: pairwise Spearman with NaN handling ─────────────────────────────
def spearman(x: pd.Series, y: pd.Series) -> tuple[float, float, int]:
    mask = (~x.isna()) & (~y.isna())
    if mask.sum() < 4:
        return (np.nan, np.nan, int(mask.sum()))
    r, p = spearmanr(x[mask], y[mask])
    return (float(r), float(p), int(mask.sum()))


# ── Pooled + per-mode Spearman, all confidence × NLP pairs ──────────────────
PRIMARY_X   = ["item5", "AI_support"]
PRIMARY_Y   = ["BERTScore_F1", "SBERT_ModernBERT"]   # headline
SECONDARY_Y = ["BLEU", "ROUGE-L", "METEOR"]          # robustness panel
ALL_Y       = PRIMARY_Y + SECONDARY_Y

corr_rows: list[dict] = []
groups = [("pooled", merged)] + [
    (m, merged[merged["mode"] == m]) for m in ("form", "ask", "chat")
]
for group_name, sub in groups:
    for xv in PRIMARY_X:
        for yv in ALL_Y:
            r, p, n = spearman(sub[xv], sub[yv])
            corr_rows.append({
                "group":       group_name,
                "confidence":  xv,
                "nlp_metric":  yv,
                "spearman_rho": round(r, 4) if not np.isnan(r) else np.nan,
                "p_value":      round(p, 4) if not np.isnan(p) else np.nan,
                "n":            n,
                "tier":         "primary" if yv in PRIMARY_Y else "secondary",
            })

corr_df = pd.DataFrame(corr_rows)
corr_df.to_csv(f"{OUT}/rq3_confidence_nlp_corr.csv", index=False)
print(f"\\nSaved {OUT}/rq3_confidence_nlp_corr.csv ({len(corr_df)} rows)")

# ── Per-mode rank table: item5, AI_support, BERTScore_F1, SBERT ─────────────
RANK_COLS = ["item5", "AI_support", "BERTScore_F1", "SBERT_ModernBERT"]
mode_means = merged.groupby("mode")[RANK_COLS].mean().round(4)
mode_ranks = mode_means.rank(ascending=False, method="min").astype(int)
mode_ranks.columns = [f"{c}_rank" for c in mode_means.columns]
rank_table = pd.concat([mode_means, mode_ranks], axis=1)
rank_table.to_csv(f"{OUT}/rq3_per_mode_ranks.csv")
print(f"Saved {OUT}/rq3_per_mode_ranks.csv")

# ── Display ─────────────────────────────────────────────────────────────────
print("\\n── Per-mode means + ranks (Step 1) ──")
display(rank_table)

print("── Spearman correlations (Step 1) ──")
pivot = corr_df.pivot_table(
    index=["group", "confidence"],
    columns="nlp_metric",
    values="spearman_rho",
)
display(pivot)
'''
))

cells_to_add.append(md_cell(
    """### Step 2 — Supplementary LLM-judge cross-check

Bring in the judge scores (`legal_correctness`, `overall` from
`../judge/output/judge_results.csv`, 1–5 scale) as a third lens. The judge
is reference-free, so disagreement with the reference-based NLP metrics is
informative rather than contradictory.

We compute Spearman ρ for:
- confidence ↔ judge (`item5` ↔ `legal_correctness`; `item5` ↔ `overall`)
- NLP ↔ judge convergent validity (`BERTScore_F1` ↔ `overall`;
  `SBERT_ModernBERT` ↔ `overall`)

…both pooled and per-mode. Then we extend the per-mode rank table with
columns for the judge means.

Output: `../judge/output/rq3_judge_vs_confidence_nlp.csv`
"""
))

cells_to_add.append(code_cell(
    '''# ── RQ3 Step 2: Supplementary judge cross-check ────────────────────────────
# Reuses `merged` (102 rows) and `spearman()` from Step 1.
import pandas as pd
import numpy as np
from IPython.display import display

JUDGE_PATH = "../judge/output/judge_results.csv"
JUDGE_OUT  = "../judge/output"

# ── Load judge long-format scores and dedupe by (user_id, ai_mode) ──────────
judge_raw = pd.read_csv(JUDGE_PATH)
judge_raw["_id_max"] = judge_raw.groupby(["user_id", "ai_mode"])["id"].transform("max")
judge_dedup = (judge_raw[judge_raw["id"] == judge_raw["_id_max"]]
               .drop(columns="_id_max")
               .reset_index(drop=True))
ndocs = judge_dedup.groupby(["user_id", "ai_mode"]).ngroups
print(f"Judge: {len(judge_raw)} raw rows → {len(judge_dedup)} after dedup "
      f"({ndocs} unique docs)")

# ── Pivot judge to wide ─────────────────────────────────────────────────────
judge_wide = (judge_dedup
              .pivot_table(index=["user_id", "ai_mode"],
                           columns="metric",
                           values="score")
              .reset_index())
judge_wide.columns.name = None
JUDGE_METRICS = ["completeness", "hallucination_inverse",
                 "legal_correctness", "overall", "scenario_faithfulness"]
print("Judge wide columns:", judge_wide.columns.tolist())

# ── Join judge onto the Step 1 merged frame ─────────────────────────────────
merged_j = merged.merge(judge_wide, on=["user_id", "ai_mode"], how="left")
missing_j = merged_j["overall"].isna().sum()
print(f"Merged with judge: {len(merged_j)} rows | missing judge.overall: {missing_j}")

# ── Spearman pairs of interest ──────────────────────────────────────────────
CONF_JUDGE_PAIRS = [
    ("item5",            "legal_correctness"),
    ("item5",            "overall"),
    ("AI_support",       "legal_correctness"),
    ("AI_support",       "overall"),
]
NLP_JUDGE_PAIRS = [
    ("BERTScore_F1",     "overall"),
    ("SBERT_ModernBERT", "overall"),
]

judge_rows: list[dict] = []
groups = [("pooled", merged_j)] + [
    (m, merged_j[merged_j["mode"] == m]) for m in ("form", "ask", "chat")
]
for group_name, sub in groups:
    for xv, yv in CONF_JUDGE_PAIRS + NLP_JUDGE_PAIRS:
        r, p, n = spearman(sub[xv], sub[yv])
        judge_rows.append({
            "group":       group_name,
            "x":           xv,
            "judge":       yv,
            "spearman_rho": round(r, 4) if not np.isnan(r) else np.nan,
            "p_value":      round(p, 4) if not np.isnan(p) else np.nan,
            "n":            n,
        })

judge_corr_df = pd.DataFrame(judge_rows)

# ── Per-mode judge means (also part of the same output) ─────────────────────
judge_mode_means = merged_j.groupby("mode")[JUDGE_METRICS].mean().round(4)

# ── Extend the Step 1 per-mode rank table with judge columns ────────────────
EXT_RANK_COLS = ["item5", "AI_support", "BERTScore_F1", "SBERT_ModernBERT",
                 "legal_correctness", "overall"]
mode_means_ext = merged_j.groupby("mode")[EXT_RANK_COLS].mean().round(4)
mode_ranks_ext = mode_means_ext.rank(ascending=False, method="min").astype(int)
mode_ranks_ext.columns = [f"{c}_rank" for c in mode_means_ext.columns]
rank_table_ext = pd.concat([mode_means_ext, mode_ranks_ext], axis=1)

# Update the Step 1 file with the extended (judge-augmented) version so the
# Discussion can pull a single rank table from disk.
rank_table_ext.to_csv(f"{OUT}/rq3_per_mode_ranks.csv")
print(f"Updated {OUT}/rq3_per_mode_ranks.csv with judge columns")

# ── Save Step 2 output: correlations + judge means in one CSV ───────────────
judge_means_long = (judge_mode_means
                    .reset_index()
                    .melt(id_vars="mode",
                          var_name="judge_metric",
                          value_name="mean_score"))
judge_means_long["row_type"] = "mode_mean"

corr_out = judge_corr_df.rename(columns={"x": "predictor",
                                         "judge": "outcome"})
corr_out["row_type"] = "spearman"

# Stack the two views so the file is self-explanatory
step2 = pd.concat([
    corr_out.assign(judge_metric=np.nan, mean_score=np.nan)[
        ["row_type", "group", "predictor", "outcome",
         "spearman_rho", "p_value", "n", "judge_metric", "mean_score"]
    ],
    judge_means_long.assign(group=judge_means_long["mode"],
                            predictor=np.nan, outcome=np.nan,
                            spearman_rho=np.nan, p_value=np.nan, n=np.nan)[
        ["row_type", "group", "predictor", "outcome",
         "spearman_rho", "p_value", "n", "judge_metric", "mean_score"]
    ],
], ignore_index=True)
step2.to_csv(f"{JUDGE_OUT}/rq3_judge_vs_confidence_nlp.csv", index=False)
print(f"Saved {JUDGE_OUT}/rq3_judge_vs_confidence_nlp.csv ({len(step2)} rows)")

# ── Display ─────────────────────────────────────────────────────────────────
print("\\n── Judge per-mode means ──")
display(judge_mode_means)

print("── Per-mode rank table extended with judge (1 = best) ──")
display(rank_table_ext)

print("── Spearman: confidence/NLP × judge ──")
display(judge_corr_df.pivot_table(
    index=["group", "x"], columns="judge", values="spearman_rho"
))
'''
))

# Append and write
nb['cells'].extend(cells_to_add)
NB_PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + '\n',
                   encoding='utf-8')
print(f'Appended {len(cells_to_add)} cells to {NB_PATH}')
print(f'Total cells now: {len(nb["cells"])}')
