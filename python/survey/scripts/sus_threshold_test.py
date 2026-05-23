"""
One-sample Wilcoxon signed-rank test of Form's SUS composite against the
Bangor (2008) acceptability threshold of 68.

Reproduces the SUS scoring used in `ROPAgen_SURVEY.ipynb` (standard Brooke
procedure) and tests whether Form's distribution sits significantly above
68 (two-sided test). Effect size: matched-pairs rank-biserial r computed
against the constant threshold (Kerby 2014).

Run: python python/survey/scripts/sus_threshold_test.py
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "docs" / "data.csv"

ODD_COLS = ["1_sus", "3_sus", "5_sus", "7_sus", "9_sus"]
EVEN_COLS = ["2_sus", "4_sus", "6_sus", "8_sus", "10_sus"]
SUS_COLS = ["1_sus", "2_sus", "3_sus", "4_sus", "5_sus",
            "6_sus", "7_sus", "8_sus", "9_sus", "10_sus"]

THRESHOLD = 68.0  # Bangor 2008 acceptability cutoff


def load_per_mode_dfs() -> dict[str, pd.DataFrame]:
    """Reproduce the long-to-per-mode reshape used in the notebook."""
    df = pd.read_csv(DATA, sep=";")
    order_cols = sorted(
        [c for c in df.columns if re.fullmatch(r"\d+_order", c)],
        key=lambda c: int(c.split("_")[0]),
    )

    def get_measure_cols(pos: str, df_cols) -> list[str]:
        pattern = re.compile(rf"^{re.escape(pos)}_(?!order$).+")
        return [c for c in df_cols if pattern.match(c)]

    meta_cols = ["p_0001"]
    records: dict[str, list[dict]] = {"Form": [], "Ask": [], "Chat": []}

    for _, row in df.iterrows():
        meta = {c: row[c] for c in meta_cols}
        for order_col in order_cols:
            pos = order_col.split("_")[0]
            condition = row[order_col]
            if pd.isna(condition) or condition not in records:
                continue
            measure_data = {}
            for col in get_measure_cols(pos, df.columns):
                new_name = re.sub(rf"^{re.escape(pos)}_", "", col)
                measure_data[new_name] = row[col]
            records[condition].append({**meta, **measure_data})

    return {k: pd.DataFrame(v) for k, v in records.items()}


def sus_composite(df: pd.DataFrame) -> pd.Series:
    """Brooke SUS: odd-1, even: 5-x; sum * 2.5 -> 0..100."""
    conv = df.copy()
    for col in ODD_COLS:
        conv[col] = df[col] - 1
    for col in EVEN_COLS:
        conv[col] = 5 - df[col]
    return conv[SUS_COLS].sum(axis=1) * 2.5


def rank_biserial_one_sample(x: np.ndarray, ref: float) -> float:
    """Matched-pairs rank-biserial r against a constant reference (Kerby 2014).

    r = (W_pos - W_neg) / (W_pos + W_neg), where W_pos / W_neg are sums of
    ranks of |x - ref| for positive / negative differences (zeros dropped).
    Positive r -> x tends to sit above ref.
    """
    d = np.asarray(x, float) - ref
    d = d[d != 0]
    if d.size == 0:
        return 0.0
    ranks = stats.rankdata(np.abs(d))
    w_pos = ranks[d > 0].sum()
    w_neg = ranks[d < 0].sum()
    total = w_pos + w_neg
    if total == 0:
        return 0.0
    return float((w_pos - w_neg) / total)


def main() -> None:
    dfs = load_per_mode_dfs()
    form_df = dfs["Form"]
    form_df_sus = form_df[form_df["p_0001"] >= 1][SUS_COLS].copy()
    form_sus = sus_composite(form_df_sus).dropna()

    n = int(form_sus.size)
    mean = float(form_sus.mean())
    median = float(form_sus.median())
    sd = float(form_sus.std(ddof=1))
    minv = float(form_sus.min())
    maxv = float(form_sus.max())

    # Wilcoxon one-sample (two-sided) against THRESHOLD.
    # scipy.stats.wilcoxon supports a one-sample form when passing (x - ref).
    diffs = form_sus.values - THRESHOLD
    nonzero = diffs[diffs != 0]
    n_used = int(nonzero.size)
    n_zero = int(np.sum(diffs == 0))

    res = stats.wilcoxon(diffs, alternative="two-sided", zero_method="wilcox")
    W = float(res.statistic)
    p = float(res.pvalue)

    r_rb = rank_biserial_one_sample(form_sus.values, THRESHOLD)

    print("SUS Threshold Test (Form vs 68)")
    print("===============================")
    print(f"n total              : {n}")
    print(f"n zero diffs dropped : {n_zero}")
    print(f"n used in test       : {n_used}")
    print(f"Form SUS mean        : {mean:.2f}")
    print(f"Form SUS median      : {median:.2f}")
    print(f"Form SUS SD          : {sd:.2f}")
    print(f"Form SUS min/max     : {minv:.2f} / {maxv:.2f}")
    print(f"Threshold            : {THRESHOLD}")
    print()
    print("Wilcoxon signed-rank (two-sided, zero_method='wilcox')")
    print(f"  W = {W:.2f}")
    print(f"  p = {p:.4g}")
    print(f"  matched-pairs rank-biserial r = {r_rb:+.3f}")
    print()
    # Cohen-style label for |r|
    abs_r = abs(r_rb)
    if abs_r < 0.1:
        label = "negligible"
    elif abs_r < 0.3:
        label = "small"
    elif abs_r < 0.5:
        label = "medium"
    else:
        label = "large"
    print(f"  |r| label (Cohen)  : {label}")


if __name__ == "__main__":
    main()
