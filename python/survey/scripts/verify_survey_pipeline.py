"""
Independent reverification of every survey-side statistic that appears in
the thesis Evaluation chapter. Reads raw `python/survey/docs/data.csv`,
recomputes per-mode descriptives and inferential tests from scratch, and
prints them to stdout next to the thesis-reported values.

Run from `python/survey/` (or anywhere — paths are resolved relative to
this file).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "docs" / "data.csv"
TIMING = HERE.parent.parent / "metrics" / "output" / "per_mode_timing.csv"

pd.set_option("display.width", 160)
pd.set_option("display.max_columns", 30)


# ───────────────────────── helpers ──────────────────────────


def rank_biserial_wilcoxon(x: np.ndarray, y: np.ndarray) -> float:
    """Matched-pairs rank-biserial r (Kerby 2014). Positive: x > y."""
    d = np.asarray(x, float) - np.asarray(y, float)
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


def mannwhitney_r(u: float, n1: int, n2: int) -> float:
    """Rank-biserial r for Mann-Whitney U (Wendt 1972). Positive: x > y."""
    return float((2 * u) / (n1 * n2) - 1)


def kendalls_w(arr: np.ndarray) -> float:
    n, k = arr.shape
    ranks = np.apply_along_axis(stats.rankdata, 1, arr)
    rj = ranks.sum(axis=0)
    s = ((rj - rj.mean()) ** 2).sum()
    return float(12 * s / (n ** 2 * (k ** 3 - k)))


def friedman_with_w(form: np.ndarray, ask: np.ndarray, chat: np.ndarray) -> tuple:
    """
    Return (chi2, p, w_simple, w_full) where:
      w_simple = chi2 / (N * (k-1))            (notebook + thesis convention)
      w_full   = full Kendall's W with rank-ties correction
    """
    chi2, p = stats.friedmanchisquare(form, ask, chat)
    n = len(form)
    k = 3
    w_simple = chi2 / (n * (k - 1))
    arr = np.column_stack([form, ask, chat])
    w_full = kendalls_w(arr)
    return chi2, p, w_simple, w_full


def fmt_p(p: float) -> str:
    if not np.isfinite(p):
        return "NaN"
    if p < 0.001:
        return "<0.001"
    return f"{p:.3f}"


# ───────────────────────── load + reshape ──────────────────────────


def load_long() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df = pd.read_csv(DATA, sep=";")
    print(f"Raw rows (recruited N): {len(df)}")

    # Identify the three positions (1,2,3) and their order columns.
    order_cols = [c for c in df.columns if c in ("1_order", "2_order", "3_order")]
    positions = [c.split("_")[0] for c in order_cols]

    def position_cols(pos: str) -> list[str]:
        # Everything that starts "<pos>_" but is not "<pos>_order"
        prefix = f"{pos}_"
        return [c for c in df.columns if c.startswith(prefix) and c != f"{pos}_order"]

    records: dict[str, list[dict]] = {"Form": [], "Ask": [], "Chat": []}
    for _, row in df.iterrows():
        for order_col in order_cols:
            pos = order_col.split("_")[0]
            mode = row[order_col]
            if pd.isna(mode) or mode not in records:
                continue
            data = {"p_0001": row["p_0001"], "participant_id": row.get("participant_id")}
            for col in position_cols(pos):
                new = col[len(pos) + 1 :]  # strip "<pos>_"
                data[new] = row[col]
            records[mode].append(data)

    form_df = pd.DataFrame(records["Form"])
    ask_df = pd.DataFrame(records["Ask"])
    chat_df = pd.DataFrame(records["Chat"])

    print(f"Per-mode rows (all consent values): Form={len(form_df)}, "
          f"Ask={len(ask_df)}, Chat={len(chat_df)}")

    # Filter to valid participants (consent recorded as p_0001 >= 1).
    form_v = form_df[form_df["p_0001"] >= 1].reset_index(drop=True)
    ask_v = ask_df[ask_df["p_0001"] >= 1].reset_index(drop=True)
    chat_v = chat_df[chat_df["p_0001"] >= 1].reset_index(drop=True)

    print(f"Valid n per mode (p_0001>=1): Form={len(form_v)}, "
          f"Ask={len(ask_v)}, Chat={len(chat_v)}")

    return df, form_v, ask_v, chat_v


# ───────────────────────── analyses ──────────────────────────


def section(label: str) -> None:
    print()
    print("=" * 78)
    print(label)
    print("=" * 78)


def sample_size_check(raw_df: pd.DataFrame) -> None:
    section("A. Sample size derivation")
    n_raw = len(raw_df)
    n_valid = int((raw_df["p_0001"] >= 1).sum())
    n_invalid = int((raw_df["p_0001"] < 1).sum())
    n_missing = int(raw_df["p_0001"].isna().sum())
    n_neg1 = int((raw_df["p_0001"] == -1).sum())
    n_zero = int((raw_df["p_0001"] == 0).sum())
    print(f"Recruited (raw rows in CSV): {n_raw}")
    print(f"p_0001 missing: {n_missing}")
    print(f"p_0001 == -1: {n_neg1}")
    print(f"p_0001 == 0:  {n_zero}")
    print(f"p_0001 <  1 (invalid total): {n_invalid}")
    print(f"p_0001 >= 1 (valid total):   {n_valid}")
    print()
    print(f"Thesis claim: recruited 73, valid 69. "
          f"Observed: recruited {n_raw}, valid {n_valid}.")


def sus_composite(df: pd.DataFrame) -> np.ndarray:
    odd = ["1_sus", "3_sus", "5_sus", "7_sus", "9_sus"]
    even = ["2_sus", "4_sus", "6_sus", "8_sus", "10_sus"]
    conv = df.copy()
    for c in odd:
        conv[c] = df[c].astype(float) - 1
    for c in even:
        conv[c] = 5 - df[c].astype(float)
    cols = odd + even
    return conv[cols].sum(axis=1).to_numpy() * 2.5


def rtlx_composite(df: pd.DataFrame) -> np.ndarray:
    """Unweighted mean of 5 demand items + 1 performance item (positive-coded)."""
    cols = [
        "1_tlx_demand", "2_tlx_demand", "3_tlx_demand",
        "4_tlx_demand", "5_tlx_demand", "1_tlx_performance",
    ]
    arr = df[cols].astype(float).to_numpy()
    return arr.mean(axis=1)


def ai_composite(df: pd.DataFrame) -> np.ndarray:
    cols = [f"{i}_ai" for i in range(1, 7)]
    return df[cols].astype(float).mean(axis=1).to_numpy()


def descriptive_block(form: pd.DataFrame, ask: pd.DataFrame, chat: pd.DataFrame) -> None:
    section("B. Descriptive statistics — composites and per-item")

    # ── SUS composite
    sus_f = sus_composite(form)
    sus_a = sus_composite(ask)
    sus_c = sus_composite(chat)
    print("SUS composite (0-100):")
    for label, vals in (("Form", sus_f), ("Ask", sus_a), ("Chat", sus_c)):
        print(f"  {label}: mean={vals.mean():.2f}, sd={vals.std(ddof=1):.2f}, "
              f"median={np.median(vals):.1f}, n={len(vals)}")
    print("  Thesis: Form 78.62 (SD 16.09, median 80.0); "
          "Ask 72.97 (SD 15.36, median 72.5); "
          "Chat 72.93 (SD 19.03, median 75.0)")

    # ── R-TLX composite
    rtlx_f = rtlx_composite(form)
    rtlx_a = rtlx_composite(ask)
    rtlx_c = rtlx_composite(chat)
    print()
    print("R-TLX composite (1-21):")
    for label, vals in (("Form", rtlx_f), ("Ask", rtlx_a), ("Chat", rtlx_c)):
        print(f"  {label}: mean={vals.mean():.2f}, sd={vals.std(ddof=1):.2f}, "
              f"median={np.median(vals):.2f}, n={len(vals)}")
    print("  Thesis: Form 5.50, Ask 6.33, Chat 6.33")

    # ── R-TLX subscale means (1-21)
    print()
    print("R-TLX subscale means (mean ± SD):")
    subs = {
        "Mental Demand":    "1_tlx_demand",
        "Physical Demand":  "2_tlx_demand",
        "Temporal Demand":  "3_tlx_demand",
        "Effort":           "4_tlx_demand",
        "Frustration":      "5_tlx_demand",
        "Performance (+)":  "1_tlx_performance",
    }
    for name, col in subs.items():
        vals = {m: d[col].astype(float).to_numpy() for m, d in (
            ("Form", form), ("Ask", ask), ("Chat", chat))}
        print(f"  {name:18}: Form {vals['Form'].mean():.2f}±{vals['Form'].std(ddof=1):.2f}  "
              f"Ask {vals['Ask'].mean():.2f}±{vals['Ask'].std(ddof=1):.2f}  "
              f"Chat {vals['Chat'].mean():.2f}±{vals['Chat'].std(ddof=1):.2f}")

    # ── SUS per-item (raw, not reverse-keyed)
    print()
    print("SUS per-item raw means (1-5 Likert, NO reverse-keying):")
    for i in range(1, 11):
        col = f"{i}_sus"
        f_m = form[col].astype(float).mean()
        a_m = ask[col].astype(float).mean()
        c_m = chat[col].astype(float).mean()
        print(f"  Item {i:2}: Form {f_m:.2f}  Ask {a_m:.2f}  Chat {c_m:.2f}")

    # ── AI per-item
    print()
    print("AI Support per-item means (1-5 Likert):")
    for i in range(1, 7):
        col = f"{i}_ai"
        f_m = form[col].astype(float).mean()
        a_m = ask[col].astype(float).mean()
        c_m = chat[col].astype(float).mean()
        print(f"  Item {i}: Form {f_m:.2f}  Ask {a_m:.2f}  Chat {c_m:.2f}")


def mode_preference_check(raw_df: pd.DataFrame) -> None:
    section("Mode preference ranking")
    valid = raw_df[raw_df["p_0001"] >= 1].copy()
    rank_counts = {m: 0 for m in ("Form", "Ask", "Chat")}
    for v in valid["rank_1"].dropna():
        v = str(v).strip()
        if v in rank_counts:
            rank_counts[v] += 1

    n = sum(rank_counts.values())
    print(f"Rank-1 votes (n={n}):")
    for m, c in rank_counts.items():
        print(f"  {m}: {c}  ({c / n * 100:.1f}%)")

    # Mean ranks: convert text columns rank_1/2/3 into per-participant rank.
    ranks_per_mode = {m: [] for m in ("Form", "Ask", "Chat")}
    for _, row in valid.iterrows():
        for r_idx, col in enumerate(["rank_1", "rank_2", "rank_3"], start=1):
            v = row[col]
            if isinstance(v, str):
                v = v.strip()
                if v in ranks_per_mode:
                    ranks_per_mode[v].append(r_idx)
    print()
    print("Mean rank assigned (1=most preferred):")
    for m, rs in ranks_per_mode.items():
        print(f"  {m}: {np.mean(rs):.2f}  (n={len(rs)})")

    # χ² goodness-of-fit (uniform null)
    obs = np.array([rank_counts["Form"], rank_counts["Chat"], rank_counts["Ask"]])
    exp = np.full(3, n / 3)
    chi2 = ((obs - exp) ** 2 / exp).sum()
    p = 1 - stats.chi2.cdf(chi2, df=2)
    cramers_v = np.sqrt(chi2 / n / (3 - 1))
    print()
    print(f"χ² goodness-of-fit (uniform null): χ²(2,N={n}) = {chi2:.2f}, "
          f"p = {fmt_p(p)}, Cramér's V = {cramers_v:.3f}")
    print("Thesis: χ²(2) = 14.17, p < 0.001, Cramér's V = 0.32")


def normality_check(form_d: pd.DataFrame, ask_d: pd.DataFrame, chat_d: pd.DataFrame) -> None:
    section("Normality (Shapiro–Wilk) — composites and key items")
    measures = {
        "SUS":   (sus_composite(form_d), sus_composite(ask_d), sus_composite(chat_d)),
        "RTLX":  (rtlx_composite(form_d), rtlx_composite(ask_d), rtlx_composite(chat_d)),
        "AI":    (ai_composite(form_d),  ai_composite(ask_d),  ai_composite(chat_d)),
        "5_ai":  (form_d["5_ai"].astype(float).to_numpy(),
                  ask_d["5_ai"].astype(float).to_numpy(),
                  chat_d["5_ai"].astype(float).to_numpy()),
        "6_ai":  (form_d["6_ai"].astype(float).to_numpy(),
                  ask_d["6_ai"].astype(float).to_numpy(),
                  chat_d["6_ai"].astype(float).to_numpy()),
    }
    for name, (f, a, c) in measures.items():
        for label, vals in (("Form", f), ("Ask", a), ("Chat", c)):
            w, p = stats.shapiro(vals)
            verdict = "NORMAL" if p >= 0.05 else "NOT normal"
            print(f"  {name:5} / {label:4}: W={w:.3f}, p={fmt_p(p)}  ({verdict})")
        print()


def friedman_block(form_d: pd.DataFrame, ask_d: pd.DataFrame, chat_d: pd.DataFrame) -> None:
    section("C. Inferential tests — Friedman omnibus (n=69)")
    tests = [
        ("SUS composite",
         sus_composite(form_d), sus_composite(ask_d), sus_composite(chat_d),
         "Thesis: χ²=5.51, p=0.064, W=0.040 (NOT sig)"),
        ("R-TLX composite",
         rtlx_composite(form_d), rtlx_composite(ask_d), rtlx_composite(chat_d),
         "Thesis: χ²=5.24, p=0.073, W=0.038 (NOT sig)"),
    ]
    # Per-subscale tests
    sub_map = {
        "R-TLX Mental":     "1_tlx_demand",
        "R-TLX Physical":   "2_tlx_demand",
        "R-TLX Temporal":   "3_tlx_demand",
        "R-TLX Effort":     "4_tlx_demand",
        "R-TLX Frustration":"5_tlx_demand",
        "R-TLX Performance":"1_tlx_performance",
    }
    sub_expectations = {
        "R-TLX Temporal":   "Thesis: χ²=12.77, p=0.002, W=0.093 (SIG)",
        "R-TLX Frustration":"Thesis: χ²=8.93, p=0.012, W=0.065 (SIG)",
    }
    for label, col in sub_map.items():
        f = form_d[col].astype(float).to_numpy()
        a = ask_d[col].astype(float).to_numpy()
        c = chat_d[col].astype(float).to_numpy()
        tests.append((label, f, a, c, sub_expectations.get(label, "(no thesis target)")))

    # AI composite + item 5 + item 6
    tests.append(("AI composite (6-item)",
                  ai_composite(form_d), ai_composite(ask_d), ai_composite(chat_d),
                  "Thesis: χ²=1.05, p=0.592, W=0.008 (NOT sig)"))
    tests.append(("AI item 5 (legal-basis)",
                  form_d["5_ai"].astype(float).to_numpy(),
                  ask_d["5_ai"].astype(float).to_numpy(),
                  chat_d["5_ai"].astype(float).to_numpy(),
                  "Thesis: χ²=3.76, p=0.152 (NOT sig)"))
    tests.append(("AI item 6 (reuse)",
                  form_d["6_ai"].astype(float).to_numpy(),
                  ask_d["6_ai"].astype(float).to_numpy(),
                  chat_d["6_ai"].astype(float).to_numpy(),
                  "Thesis: χ²=11.12, p=0.004, W=0.081 (SIG)"))

    for label, f, a, c, expect in tests:
        chi2, p, w_simple, w_full = friedman_with_w(f, a, c)
        sig = "SIG" if p < 0.05 else "ns"
        print(f"  {label:24}: χ²={chi2:.3f}, p={fmt_p(p)}, "
              f"W_simple={w_simple:.3f} (W_full={w_full:.3f})  [{sig}]")
        print(f"      {expect}")


def pairwise_block(form_d: pd.DataFrame, ask_d: pd.DataFrame, chat_d: pd.DataFrame) -> None:
    section("D. Post-hoc pairwise Wilcoxon signed-rank + rank-biserial r")
    bonf_alpha = 0.05 / 3
    targets = [
        ("R-TLX Temporal Demand",  form_d["3_tlx_demand"], ask_d["3_tlx_demand"], chat_d["3_tlx_demand"]),
        ("R-TLX Frustration",      form_d["5_tlx_demand"], ask_d["5_tlx_demand"], chat_d["5_tlx_demand"]),
        ("AI item 6 (reuse)",      form_d["6_ai"],         ask_d["6_ai"],         chat_d["6_ai"]),
        ("SUS composite",          sus_composite(form_d),  sus_composite(ask_d),  sus_composite(chat_d)),
        ("R-TLX composite",        rtlx_composite(form_d), rtlx_composite(ask_d), rtlx_composite(chat_d)),
    ]
    for label, f, a, c in targets:
        print(f"\n  {label}:")
        for n1, x_name, x, y_name, y in [
            ("Form vs Ask",  "Form", f, "Ask", a),
            ("Form vs Chat", "Form", f, "Chat", c),
            ("Ask vs Chat",  "Ask",  a, "Chat", c),
        ]:
            x_arr = np.asarray(x, float)
            y_arr = np.asarray(y, float)
            # Wilcoxon excludes zero differences by default
            non_zero = x_arr - y_arr != 0
            try:
                res = stats.wilcoxon(x_arr, y_arr, zero_method="wilcox")
                w_stat = float(res.statistic)
                p = float(res.pvalue)
            except ValueError:
                w_stat, p = float("nan"), float("nan")
            r = rank_biserial_wilcoxon(x_arr, y_arr)
            n_used = int(non_zero.sum())
            sig = "**" if p < bonf_alpha else ("." if p < 0.05 else "")
            print(f"    {n1:14}  n_used={n_used:3}  W={w_stat:>7.1f}  "
                  f"p={fmt_p(p):>7}  r={r:+.3f}  {sig}")


def completion_time_block() -> None:
    section("E. Completion-time (Kruskal–Wallis + Mann–Whitney U)")
    if not TIMING.exists():
        print(f"Timing file not found: {TIMING}")
        return
    t = pd.read_csv(TIMING)
    print(f"Timing rows: {len(t)}")
    print(t.groupby("ai_mode")["time_seconds"].describe()[["count", "mean", "50%", "std", "min", "max"]])

    form_t = t[t["ai_mode"] == "form"]["time_seconds"].to_numpy(float)
    ask_t  = t[t["ai_mode"] == "ask"]["time_seconds"].to_numpy(float)
    chat_t = t[t["ai_mode"] == "chat"]["time_seconds"].to_numpy(float)

    h, p = stats.kruskal(form_t, ask_t, chat_t)
    n = len(t)
    eps2 = h / (n - 1)
    print(f"\nKruskal–Wallis (between-groups, n={n}): H={h:.2f}, p={fmt_p(p)}, ε²={eps2:.3f}")
    print("Thesis: H=16.46, p<0.001, ε²=0.15 (large)")

    print("\nPairwise Mann–Whitney U (Bonferroni α=0.0167):")
    for label, x_name, x, y_name, y in [
        ("Form vs Ask",  "Form", form_t, "Ask",  ask_t),
        ("Form vs Chat", "Form", form_t, "Chat", chat_t),
        ("Ask vs Chat",  "Ask",  ask_t,  "Chat", chat_t),
    ]:
        u, pp = stats.mannwhitneyu(x, y, alternative="two-sided")
        r = mannwhitney_r(u, len(x), len(y))
        sig = "**" if pp < 0.05 / 3 else ("." if pp < 0.05 else "")
        print(f"  {label:14}  n1={len(x):2}, n2={len(y):2}  U={u:>7.1f}  "
              f"p={fmt_p(pp):>7}  r={r:+.3f}  {sig}")
    print("\nThesis: Form vs Ask r=0.512 (large); Form vs Chat r=0.418 (medium); "
          "Ask vs Chat NOT sig.")


def matched_triple_check(form_d: pd.DataFrame, ask_d: pd.DataFrame, chat_d: pd.DataFrame) -> None:
    section("F. Matched-triple check")
    print(f"Per-mode row counts after p_0001>=1: "
          f"Form={len(form_d)}, Ask={len(ask_d)}, Chat={len(chat_d)}")
    print("Because the reshape preserves participant index, all three frames "
          "share the same 69 valid participants (within-subjects).")
    # Spot-check that no participant is missing any mode
    n_form_complete = int(form_d.notna().all(axis=1).sum())
    n_ask_complete  = int(ask_d.notna().all(axis=1).sum())
    n_chat_complete = int(chat_d.notna().all(axis=1).sum())
    print(f"Rows where every column is non-NaN (incl. free-text): "
          f"Form={n_form_complete}, Ask={n_ask_complete}, Chat={n_chat_complete}")
    # NaN per key item per mode
    for label, d in (("Form", form_d), ("Ask", ask_d), ("Chat", chat_d)):
        keys = ["5_ai", "6_ai", "1_tlx_demand", "1_tlx_performance",
                "1_sus", "2_sus", "10_sus"]
        nans = {k: int(d[k].isna().sum()) for k in keys}
        print(f"  {label}: NaN counts for key items: {nans}")


def spot_check(raw_df: pd.DataFrame) -> None:
    section("Spot-check of raw participant rows")
    valid = raw_df[raw_df["p_0001"] >= 1].reset_index(drop=True)
    # First three valid participants
    print("First 3 valid participants (showing order, SUS-2/SUS-8/Perf):")
    for i in range(3):
        row = valid.iloc[i]
        pid = row.get("participant_id")
        print(f"  Participant {pid}: order = "
              f"({row['1_order']}, {row['2_order']}, {row['3_order']})")
        print(f"    Position 1 ({row['1_order']}): "
              f"sus_2={row['1_2_sus']} (negatively keyed; lower=better), "
              f"sus_8={row['1_8_sus']}, "
              f"sus_1={row['1_1_sus']}, "
              f"perf={row['1_1_tlx_performance']} (positive-keyed)")
        print(f"    Position 2 ({row['2_order']}): "
              f"sus_2={row['2_2_sus']}, sus_8={row['2_8_sus']}, "
              f"perf={row['2_1_tlx_performance']}")
        print(f"    Position 3 ({row['3_order']}): "
              f"sus_2={row['3_2_sus']}, sus_8={row['3_8_sus']}, "
              f"perf={row['3_1_tlx_performance']}")


# ───────────────────────── main ──────────────────────────


def main() -> None:
    raw_df, form_d, ask_d, chat_d = load_long()
    sample_size_check(raw_df)
    matched_triple_check(form_d, ask_d, chat_d)
    descriptive_block(form_d, ask_d, chat_d)
    mode_preference_check(raw_df)
    normality_check(form_d, ask_d, chat_d)
    friedman_block(form_d, ask_d, chat_d)
    pairwise_block(form_d, ask_d, chat_d)
    completion_time_block()
    spot_check(raw_df)


if __name__ == "__main__":
    main()
