"""
Per-(metric, chapter) inferential tests for the chapter-level NLP metrics.

Mirrors the doc-level pipeline in `statistical_tests.md` (Kruskal-Wallis →
Friedman → Wilcoxon → Mann-Whitney U) but applied to each of the six ROPA
chapters separately, so the chapter-level Evaluation prose has a significance
layer matching the doc-level analysis.

Sample sizes (canonical, from `python/output/sample_sizes.md`):
- Full unbalanced: n = 113 documents (Form 37 / Ask 37 / Chat 39) for
  Kruskal-Wallis and Mann-Whitney U.
- Strict matched-triple within-subjects: n = 26 participants with exactly
  one document in each of Form, Ask, Chat — for Friedman and Wilcoxon.

Metrics covered (10): BLEU, ROUGE-1, ROUGE-2, ROUGE-L, METEOR,
BERTScore_Precision, BERTScore_Recall, BERTScore_F1, SBERT_ModernBERT,
SBERT_MiniLM (the last is chapter-level only; doc-level pipeline does not
include MiniLM, by user instruction).

Chapters (6): ch1 .. ch6.

Output:
- output/chapter_kruskal.csv
- output/chapter_friedman.csv
- output/chapter_wilcoxon.csv
- output/chapter_mannwhitney.csv
- Appends "Per-Chapter Inferential Tests" section to
  output/statistical_tests.md (idempotent).
"""

from __future__ import annotations

import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


METRICS_DIR = Path(__file__).resolve().parent.parent
CHAPTER_CSV = METRICS_DIR / "output" / "chapter_results.csv"
OUT_DIR     = METRICS_DIR / "output"
STATS_MD    = OUT_DIR / "statistical_tests.md"

MODES   = ["form", "ask", "chat"]
PAIRS   = [("form", "ask"), ("form", "chat"), ("ask", "chat")]
METRICS = [
    "BLEU", "ROUGE-1", "ROUGE-2", "ROUGE-L", "METEOR",
    "BERTScore_Precision", "BERTScore_Recall", "BERTScore_F1",
    "SBERT_ModernBERT", "SBERT_MiniLM",
]

# Friendly ch1..ch6 labels matching the order chapters appear per document
# in chapter_results.csv. These match `chapter_nlp_summary.csv` ordering.
CHAPTER_ORDER = [
    "Verantwortliche Stelle und Kontaktdaten",
    "Zwecke und Rechtsgrundlagen der Verarbeitung",
    "Kategorien personenbezogener Daten und Datenquellen",
    "Betroffene Personen und Empfänger",
    "Aufbewahrungsfristen und Löschung",
    "Technische und organisatorische Maßnahmen",
]
CHAPTER_LABELS = {name: f"ch{i+1}" for i, name in enumerate(CHAPTER_ORDER)}

BONF_ALPHA = 0.05 / 3   # 0.01667 for 3 pairwise comparisons within a cell


# ───────────────────────────── effect sizes ─────────────────────────────────


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
    return float(1 - (2 * u) / (n1 * n2))


def kendalls_w(arr: np.ndarray) -> float:
    """Kendall's W for a (subjects x conditions) matrix."""
    n, k = arr.shape
    ranks = np.apply_along_axis(stats.rankdata, 1, arr)
    rj = ranks.sum(axis=0)
    s = ((rj - rj.mean()) ** 2).sum()
    return float(12 * s / (n ** 2 * (k ** 3 - k)))


def eps_squared(h: float, n: int) -> float:
    return float(h / (n - 1)) if n > 1 else float("nan")


def label_r(r: float) -> str:
    """Match doc-level conventions: negligible/small/medium/large."""
    a = abs(r)
    if a < 0.1:
        return "negligible"
    if a < 0.3:
        return "small"
    if a < 0.5:
        return "medium"
    return "large"


def label_w(w: float) -> str:
    """Kendall's W: weak / moderate / strong (matches doc-level wording)."""
    if w < 0.1:
        return "weak"
    if w < 0.3:
        return "moderate"
    return "strong"


def label_eps2(eps2: float) -> str:
    """ε² interpretation matching doc-level."""
    if not np.isfinite(eps2):
        return "—"
    if eps2 < 0.01:
        return "negligible"
    if eps2 < 0.06:
        return "small"
    if eps2 < 0.14:
        return "moderate"
    return "large"


def fmt_p(p: float) -> str:
    if not np.isfinite(p):
        return "NaN"
    if p < 0.001:
        return "<0.001"
    return f"{p:.3f}"


def fmt_stat(x: float, nd: int = 3) -> str:
    if not np.isfinite(x):
        return "NaN"
    return f"{x:.{nd}f}"


# ───────────────────────────── data helpers ─────────────────────────────────


def load_chapter_results() -> pd.DataFrame:
    df = pd.read_csv(CHAPTER_CSV)
    df["chapter_id"] = df["chapter"].map(CHAPTER_LABELS)
    if df["chapter_id"].isna().any():
        bad = df.loc[df["chapter_id"].isna(), "chapter"].unique().tolist()
        raise ValueError(f"Unmapped chapter label(s): {bad}")
    return df


def strict_matched_users(df: pd.DataFrame) -> list[str]:
    """
    Participants with exactly one document in each of Form, Ask, Chat,
    derived from chapter_results (each doc contributes 6 chapter rows).
    """
    docs_per = df.groupby(["user_id", "ai_mode"])["id"].nunique().unstack(fill_value=0)
    keep = docs_per[
        (docs_per.get("form", 0) == 1)
        & (docs_per.get("ask",  0) == 1)
        & (docs_per.get("chat", 0) == 1)
    ].index.tolist()
    return sorted(keep)


# ───────────────────────────── tests per cell ───────────────────────────────


def kruskal_cell(values_by_mode: dict[str, np.ndarray]) -> dict:
    groups = [values_by_mode[m] for m in MODES]
    n_total = sum(len(g) for g in groups)
    # Guard: if every value across all groups is identical, scipy raises.
    flat = np.concatenate(groups)
    if flat.size == 0 or np.unique(flat).size <= 1:
        return {
            "H": float("nan"), "p": float("nan"), "eps2": float("nan"),
            "n": n_total, "degenerate": True,
        }
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        h, p = stats.kruskal(*groups)
    return {
        "H": float(h), "p": float(p),
        "eps2": eps_squared(h, n_total),
        "n": n_total, "degenerate": False,
    }


def friedman_cell(wide: pd.DataFrame) -> dict:
    """wide: index=user, columns=MODES. All rows complete (matched triple)."""
    arr = wide[MODES].to_numpy(float)
    n = arr.shape[0]
    # Degeneracy guard: scipy returns NaN χ² when every subject's values are
    # tied across all conditions (e.g. BLEU == 0 on every chapter for some
    # chapters). We catch the warning and return NaN explicitly.
    if n == 0:
        return {"chi2": float("nan"), "p": float("nan"),
                "w": float("nan"), "n": 0, "degenerate": True}
    # Check column-constancy / row-constancy
    row_const = np.all(arr == arr[:, [0]], axis=1).all()
    col_const = np.all(arr == arr[[0], :], axis=0).all()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            chi2, p = stats.friedmanchisquare(arr[:, 0], arr[:, 1], arr[:, 2])
        except ValueError:
            chi2, p = float("nan"), float("nan")
    # Kendall's W is also degenerate if all ranks are tied; compute defensively
    try:
        w = kendalls_w(arr)
    except Exception:
        w = float("nan")
    degenerate = bool(row_const or col_const or not np.isfinite(chi2))
    return {"chi2": float(chi2), "p": float(p),
            "w": float(w), "n": int(n), "degenerate": degenerate}


def wilcoxon_pairs(wide: pd.DataFrame) -> list[dict]:
    rows = []
    for a, b in PAIRS:
        x = wide[a].to_numpy(float)
        y = wide[b].to_numpy(float)
        diff = x - y
        # If every paired difference is zero, the test is undefined.
        if np.all(diff == 0):
            rows.append({
                "pair": f"{a} vs {b}",
                "W": float("nan"), "p": float("nan"),
                "r": float("nan"), "direction": "—",
                "bonf_sig": False, "degenerate": True,
            })
            continue
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                res = stats.wilcoxon(x, y, zero_method="wilcox")
                W = float(res.statistic); p = float(res.pvalue)
            except ValueError:
                W, p = float("nan"), float("nan")
        r = rank_biserial_wilcoxon(x, y)
        direction = "—"
        if np.isfinite(r):
            if r > 0:
                direction = f"{a.capitalize()} > {b.capitalize()}"
            elif r < 0:
                direction = f"{b.capitalize()} > {a.capitalize()}"
            else:
                direction = "tie"
        rows.append({
            "pair": f"{a.capitalize()} vs {b.capitalize()}",
            "W": W, "p": p, "r": float(r),
            "direction": direction,
            "bonf_sig": (np.isfinite(p) and p < BONF_ALPHA),
            "degenerate": False,
        })
    return rows


def mannwhitney_pairs(values_by_mode: dict[str, np.ndarray]) -> list[dict]:
    rows = []
    for a, b in PAIRS:
        x = values_by_mode[a]; y = values_by_mode[b]
        if len(x) == 0 or len(y) == 0:
            rows.append({
                "pair": f"{a.capitalize()} vs {b.capitalize()}",
                "U": float("nan"), "p": float("nan"),
                "r": float("nan"), "direction": "—",
                "median_a": float("nan"), "median_b": float("nan"),
                "bonf_sig": False, "degenerate": True,
            })
            continue
        # Mann-Whitney is undefined if both groups are identical constants
        if (np.unique(np.concatenate([x, y])).size <= 1):
            rows.append({
                "pair": f"{a.capitalize()} vs {b.capitalize()}",
                "U": float("nan"), "p": float("nan"),
                "r": float("nan"), "direction": "—",
                "median_a": float(np.median(x)),
                "median_b": float(np.median(y)),
                "bonf_sig": False, "degenerate": True,
            })
            continue
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                res = stats.mannwhitneyu(x, y, alternative="two-sided")
                U = float(res.statistic); p = float(res.pvalue)
            except ValueError:
                U, p = float("nan"), float("nan")
        r = mannwhitney_r(U, len(x), len(y)) if np.isfinite(U) else float("nan")
        direction = "—"
        if np.isfinite(r):
            if r > 0:
                direction = f"{a.capitalize()} > {b.capitalize()}"
            elif r < 0:
                direction = f"{b.capitalize()} > {a.capitalize()}"
            else:
                direction = "tie"
        rows.append({
            "pair": f"{a.capitalize()} vs {b.capitalize()}",
            "U": U, "p": p, "r": float(r),
            "direction": direction,
            "median_a": float(np.median(x)),
            "median_b": float(np.median(y)),
            "bonf_sig": (np.isfinite(p) and p < BONF_ALPHA),
            "degenerate": False,
        })
    return rows


# ───────────────────────────── driver ───────────────────────────────────────


def compute_all(df: pd.DataFrame, matched_users: list[str]) -> dict:
    kw_rows:    list[dict] = []
    fr_rows:    list[dict] = []
    wx_rows:    list[dict] = []
    mw_rows:    list[dict] = []
    degenerate: list[str]  = []

    for metric in METRICS:
        for chap_name in CHAPTER_ORDER:
            ch_id = CHAPTER_LABELS[chap_name]
            sub = df[df["chapter"] == chap_name]

            # Full-sample values per mode (n=113 unbalanced, may include duplicates)
            full_vals = {
                m: sub.loc[sub["ai_mode"] == m, metric].dropna().to_numpy(float)
                for m in MODES
            }

            # Matched within-subjects: take the row per (user, mode) from the
            # 26 matched users. They have exactly one document each, so each
            # chapter has exactly one value per (user, mode).
            sub_m = sub[sub["user_id"].isin(matched_users)]
            wide = (
                sub_m.pivot_table(
                    index="user_id", columns="ai_mode",
                    values=metric, aggfunc="first",
                )
                .reindex(columns=MODES)
            )
            # In principle no NaNs since all 26 users have all 3 modes;
            # guard anyway:
            wide = wide.dropna()

            # 1. Kruskal-Wallis
            kw = kruskal_cell(full_vals)
            kw_rows.append({
                "metric": metric, "chapter": ch_id,
                "n": kw["n"], "H": kw["H"], "p": kw["p"],
                "eps2": kw["eps2"],
                "eps2_label": label_eps2(kw["eps2"]),
                "sig_05": (np.isfinite(kw["p"]) and kw["p"] < 0.05),
                "degenerate": kw["degenerate"],
            })
            if kw["degenerate"]:
                degenerate.append(f"Kruskal-Wallis {metric}/{ch_id}: all values identical (n={kw['n']})")

            # 2. Friedman
            fr = friedman_cell(wide)
            fr_rows.append({
                "metric": metric, "chapter": ch_id,
                "n": fr["n"], "chi2": fr["chi2"], "df": 2,
                "p": fr["p"], "w": fr["w"],
                "w_label": label_w(fr["w"]) if np.isfinite(fr["w"]) else "—",
                "sig_05": (np.isfinite(fr["p"]) and fr["p"] < 0.05),
                "degenerate": fr["degenerate"],
            })
            if fr["degenerate"]:
                degenerate.append(
                    f"Friedman {metric}/{ch_id}: degenerate (constant rows/cols), "
                    f"χ²={fr['chi2']}, p={fr['p']}"
                )

            # 3. Pairwise Wilcoxon (only on the matched subset)
            for pw in wilcoxon_pairs(wide):
                wx_rows.append({
                    "metric": metric, "chapter": ch_id,
                    "pair": pw["pair"],
                    "n": int(len(wide)),
                    "W": pw["W"], "p": pw["p"],
                    "r": pw["r"],
                    "r_label": label_r(pw["r"]) if np.isfinite(pw["r"]) else "—",
                    "direction": pw["direction"],
                    "bonf_sig": pw["bonf_sig"],
                    "degenerate": pw["degenerate"],
                })
                if pw["degenerate"]:
                    degenerate.append(
                        f"Wilcoxon {metric}/{ch_id} {pw['pair']}: "
                        "all paired differences are 0"
                    )

            # 4. Pairwise Mann-Whitney U
            for mw in mannwhitney_pairs(full_vals):
                mw_rows.append({
                    "metric": metric, "chapter": ch_id,
                    "pair": mw["pair"],
                    "n_a": int(len(full_vals[mw["pair"].split(" vs ")[0].lower()])),
                    "n_b": int(len(full_vals[mw["pair"].split(" vs ")[1].lower()])),
                    "U": mw["U"], "p": mw["p"],
                    "r": mw["r"],
                    "r_label": label_r(mw["r"]) if np.isfinite(mw["r"]) else "—",
                    "direction": mw["direction"],
                    "median_a": mw["median_a"],
                    "median_b": mw["median_b"],
                    "bonf_sig": mw["bonf_sig"],
                    "degenerate": mw["degenerate"],
                })
                if mw["degenerate"]:
                    degenerate.append(
                        f"Mann-Whitney {metric}/{ch_id} {mw['pair']}: "
                        "degenerate (constant values)"
                    )

    return {
        "kruskal":     pd.DataFrame(kw_rows),
        "friedman":    pd.DataFrame(fr_rows),
        "wilcoxon":    pd.DataFrame(wx_rows),
        "mannwhitney": pd.DataFrame(mw_rows),
        "degenerate":  degenerate,
    }


# ───────────────────────────── markdown writer ──────────────────────────────


def render_markdown(results: dict, matched_n: int) -> str:
    L: list[str] = []
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Per-Chapter Inferential Tests")
    L.append("")
    L.append(
        "Per-(metric, chapter) significance layer for the chapter-level NLP "
        "metrics, mirroring the doc-level Kruskal-Wallis → Friedman → "
        "Wilcoxon → Mann-Whitney U pipeline. Each cell is one of the 10 "
        "metrics applied to one of the six ROPA chapters (ch1–ch6); 60 "
        "(metric × chapter) combinations per test family."
    )
    L.append("")
    L.append(
        "Chapter labels: **ch1** = Verantwortliche Stelle und Kontaktdaten · "
        "**ch2** = Zwecke und Rechtsgrundlagen der Verarbeitung · "
        "**ch3** = Kategorien personenbezogener Daten und Datenquellen · "
        "**ch4** = Betroffene Personen und Empfänger · "
        "**ch5** = Aufbewahrungsfristen und Löschung · "
        "**ch6** = Technische und organisatorische Maßnahmen."
    )
    L.append("")
    L.append(
        f"Sample sizes match the doc-level NLP analysis: full unbalanced "
        f"n = 113 (Form 37 / Ask 37 / Chat 39) for Kruskal-Wallis and "
        f"Mann-Whitney U; strict matched-triple within-subjects n = "
        f"{matched_n} for Friedman and Wilcoxon (identical participant "
        "list to the doc-level analysis, derived as the 26 users with "
        "exactly one document per mode in `chapter_results.csv`)."
    )
    L.append("")
    L.append(
        "Significance thresholds and effect-size labels are identical to "
        "the doc-level pipeline: Kruskal-Wallis / Friedman use α = 0.05; "
        "Wilcoxon and Mann-Whitney are Bonferroni-corrected to α = 0.0167 "
        "(3 comparisons within each cell). Effect-size labels for "
        "rank-biserial r: |r| < 0.1 negligible, < 0.3 small, < 0.5 medium, "
        "≥ 0.5 large. Kendall's W: < 0.1 weak, < 0.3 moderate, ≥ 0.3 strong. "
        "ε² for Kruskal-Wallis: < 0.01 negligible, < 0.06 small, < 0.14 "
        "moderate, ≥ 0.14 large."
    )
    L.append("")
    L.append(
        "Degenerate cells — typically the lexical metrics (BLEU, ROUGE-2) "
        "on Purposes (ch2) and Categories (ch3), where reference-overlap "
        "collapses to zero across every document — are reported as NaN with "
        "a footnote flag. `scipy.stats.friedmanchisquare` returns NaN χ² and "
        "p when every subject's values are tied across all three conditions, "
        "and `scipy.stats.kruskal` raises on fully constant input (caught "
        "and reported as NaN)."
    )
    L.append("")

    # ── Kruskal-Wallis table
    L.append("### Kruskal-Wallis Omnibus (full unbalanced n = 113)")
    L.append("")
    L.append("| Metric | Chapter | H | p | ε² | ε² label | Significant (α=0.05) |")
    L.append("|---|---|---|---|---|---|---|")
    for _, r in results["kruskal"].iterrows():
        sig = "**Yes**" if r["sig_05"] else "No"
        if r["degenerate"]:
            sig = "— (degenerate)"
        L.append(
            f"| {r['metric']} | {r['chapter']} | {fmt_stat(r['H'])} | "
            f"{fmt_p(r['p'])} | {fmt_stat(r['eps2'])} | "
            f"{r['eps2_label']} | {sig} |"
        )
    L.append("")

    # ── Friedman table
    L.append(f"### Friedman Omnibus (matched within-subjects n = {matched_n})")
    L.append("")
    L.append("| Metric | Chapter | χ² | df | p | Kendall's W | W label | Significant (α=0.05) |")
    L.append("|---|---|---|---|---|---|---|---|")
    for _, r in results["friedman"].iterrows():
        sig = "**Yes**" if r["sig_05"] else "No"
        if r["degenerate"]:
            sig = "— (degenerate)"
        L.append(
            f"| {r['metric']} | {r['chapter']} | {fmt_stat(r['chi2'])} | "
            f"{int(r['df'])} | {fmt_p(r['p'])} | {fmt_stat(r['w'])} | "
            f"{r['w_label']} | {sig} |"
        )
    L.append("")

    # ── Wilcoxon
    L.append(
        f"### Pairwise Wilcoxon Signed-Rank Post-hoc "
        f"(matched n = {matched_n}, Bonferroni α = 0.0167)"
    )
    L.append("")
    L.append(
        "Effect size: matched-pairs rank-biserial r (positive when the "
        "first-named mode in the pair scores higher)."
    )
    L.append("")
    L.append("| Metric | Chapter | Pair | W | p | r | r label | Direction | Sig (Bonf) |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for _, r in results["wilcoxon"].iterrows():
        sig = "**Yes**" if r["bonf_sig"] else "No"
        if r["degenerate"]:
            sig = "— (degenerate)"
        L.append(
            f"| {r['metric']} | {r['chapter']} | {r['pair']} | "
            f"{fmt_stat(r['W'], 1)} | {fmt_p(r['p'])} | "
            f"{fmt_stat(r['r'])} | {r['r_label']} | "
            f"{r['direction']} | {sig} |"
        )
    L.append("")

    # ── Mann-Whitney
    L.append(
        f"### Pairwise Mann-Whitney U Sensitivity "
        f"(full unbalanced n = 113, Bonferroni α = 0.0167)"
    )
    L.append("")
    L.append(
        "Reported as a between-groups sensitivity check on the unbalanced "
        "full sample; the matched-pairs Wilcoxon family above is the "
        "primary inferential result. Effect size: rank-biserial r "
        "(positive when the first-named mode scores higher)."
    )
    L.append("")
    L.append(
        "| Metric | Chapter | Pair | U | p | r | r label | Direction | "
        "Median A | Median B | Sig (Bonf) |"
    )
    L.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for _, r in results["mannwhitney"].iterrows():
        sig = "**Yes**" if r["bonf_sig"] else "No"
        if r["degenerate"]:
            sig = "— (degenerate)"
        L.append(
            f"| {r['metric']} | {r['chapter']} | {r['pair']} | "
            f"{fmt_stat(r['U'], 1)} | {fmt_p(r['p'])} | "
            f"{fmt_stat(r['r'])} | {r['r_label']} | "
            f"{r['direction']} | {fmt_stat(r['median_a'], 4)} | "
            f"{fmt_stat(r['median_b'], 4)} | {sig} |"
        )
    L.append("")

    # ── Summary counts
    n_kw_sig   = int(results["kruskal"]["sig_05"].sum())
    n_fr_sig   = int(results["friedman"]["sig_05"].sum())
    bonf60     = 0.05 / 60.0
    n_fr_sig_b = int((results["friedman"]["p"] < bonf60).sum())
    n_wx_sig   = int(results["wilcoxon"]["bonf_sig"].sum())
    n_mw_sig   = int(results["mannwhitney"]["bonf_sig"].sum())

    L.append("### Summary Counts of Significant Cells")
    L.append("")
    L.append(
        "Family-wise correction across the 60 (metric × chapter) cells "
        f"yields α = 0.05/60 ≈ {bonf60:.6f} for the family-wise-corrected "
        "Friedman count."
    )
    L.append("")
    L.append("| Test | Significant cells / total | Threshold |")
    L.append("|---|---|---|")
    L.append(f"| Kruskal-Wallis omnibus           | {n_kw_sig} / 60   | α = 0.05 |")
    L.append(f"| Friedman omnibus (uncorrected)   | {n_fr_sig} / 60   | α = 0.05 |")
    L.append(f"| Friedman omnibus (Bonferroni-60) | {n_fr_sig_b} / 60 | α ≈ 0.000833 |")
    L.append(f"| Wilcoxon pairwise                | {n_wx_sig} / 180  | α = 0.0167 (per-cell Bonferroni-3) |")
    L.append(f"| Mann-Whitney pairwise            | {n_mw_sig} / 180  | α = 0.0167 (per-cell Bonferroni-3) |")
    L.append("")

    # ── Degenerate-cell footnote
    if results["degenerate"]:
        L.append("### Degenerate / Ill-Defined Cells (data-quality flags)")
        L.append("")
        L.append(
            "Cells flagged below are tests whose input is degenerate "
            "(all values identical across modes or all paired differences "
            "zero); reported as NaN above. These almost all correspond to "
            "BLEU and ROUGE-2 on Purposes (ch2) and Categories (ch3), where "
            "all generated chapters share zero n-gram overlap with the "
            "reference."
        )
        L.append("")
        # Compact the list: collapse identical-test entries
        from collections import Counter
        counts = Counter(results["degenerate"])
        for msg, c in sorted(counts.items()):
            suffix = f" (×{c})" if c > 1 else ""
            L.append(f"- {msg}{suffix}")
        L.append("")

    return "\n".join(L)


# ───────────────────────────── append-or-replace md ─────────────────────────


def upsert_section(md_body: str) -> None:
    existing = STATS_MD.read_text(encoding="utf-8")
    marker = "\n## Per-Chapter Inferential Tests"
    if marker in existing:
        # Replace from our marker up to (but not including) the next top-level
        # section that follows it, or EOF if none.
        pre, _, rest = existing.partition(marker)
        # Find next top-level section after the marker (next "\n## ")
        next_idx = rest.find("\n## ")
        if next_idx == -1:
            # No section after ours → drop everything from marker onward
            new_md = pre.rstrip() + "\n" + md_body.lstrip("\n") + "\n"
        else:
            # Keep everything from the next section onward
            tail = rest[next_idx:]
            new_md = (
                pre.rstrip() + "\n"
                + md_body.lstrip("\n").rstrip("\n") + "\n"
                + tail.lstrip("\n")
            )
        STATS_MD.write_text(new_md, encoding="utf-8")
        return

    # Otherwise, insert before the "## Per-Mode Completion Time" section if
    # present; else append at end.
    timing_marker = "\n## Per-Mode Completion Time"
    if timing_marker in existing:
        pre, _, post = existing.partition(timing_marker)
        new_md = (
            pre.rstrip() + "\n"
            + md_body.lstrip("\n").rstrip("\n") + "\n\n"
            + timing_marker.lstrip("\n") + post
        )
        STATS_MD.write_text(new_md, encoding="utf-8")
    else:
        STATS_MD.write_text(existing.rstrip() + "\n" + md_body + "\n",
                            encoding="utf-8")


# ───────────────────────────── main ─────────────────────────────────────────


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_chapter_results()
    matched = strict_matched_users(df)
    print(f"Matched-triple users (n={len(matched)}): {matched}")

    results = compute_all(df, matched)

    # Write CSVs (drop-in parallel to doc-level csvs)
    results["kruskal"].to_csv(OUT_DIR / "chapter_kruskal.csv", index=False)
    results["friedman"].to_csv(OUT_DIR / "chapter_friedman.csv", index=False)
    results["wilcoxon"].to_csv(OUT_DIR / "chapter_wilcoxon.csv", index=False)
    results["mannwhitney"].to_csv(OUT_DIR / "chapter_mannwhitney.csv", index=False)

    # Append / upsert markdown section
    md = render_markdown(results, matched_n=len(matched))
    upsert_section(md)

    # Console summary
    print("\n=== SIG COUNTS (uncorrected per-cell α=0.05) ===")
    print(f"  Kruskal-Wallis: {int(results['kruskal']['sig_05'].sum())} / 60")
    print(f"  Friedman:       {int(results['friedman']['sig_05'].sum())} / 60")
    bonf60 = 0.05 / 60.0
    print(f"  Friedman Bonf-60 (α≈{bonf60:.6f}): "
          f"{int((results['friedman']['p'] < bonf60).sum())} / 60")
    print(f"  Wilcoxon (Bonf α=0.0167): "
          f"{int(results['wilcoxon']['bonf_sig'].sum())} / 180")
    print(f"  Mann-Whitney (Bonf α=0.0167): "
          f"{int(results['mannwhitney']['bonf_sig'].sum())} / 180")
    if results["degenerate"]:
        print(f"\n=== DEGENERATE CELLS ({len(results['degenerate'])}) ===")
        for d in results["degenerate"][:20]:
            print("  -", d)
        if len(results["degenerate"]) > 20:
            print(f"  … (+{len(results['degenerate'])-20} more)")
    print(f"\nMarkdown updated: {STATS_MD}")
    print(f"CSVs written to:  {OUT_DIR}")


if __name__ == "__main__":
    main()
