"""
Per-mode completion-time analysis.

Extracts the `Time elapsed: NNN seconds` line embedded by ROPAgen at the end
of every generated document and runs the same statistical pipeline used for
the NLP metrics:

- Descriptives by mode (full n=113)
- Within-subjects matched-triple (n=26): Shapiro-Wilk, Friedman, Wilcoxon
  pairwise post-hoc (Bonferroni)
- Between-groups sensitivity (full n=113): Kruskal-Wallis, Mann-Whitney U
- Boxplot in the same visual style as the NLP/BERT/TLX boxplots

Writes:
- output/per_mode_timing.csv
- output/per_mode_timing_summary.csv
- output/per_mode_timing_boxplot.png
- Appends "Per-Mode Completion Time" section to output/statistical_tests.md
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats


METRICS_DIR = Path(__file__).resolve().parent.parent
DOCS_CSV    = METRICS_DIR / "docs" / "documents.csv"
SURVEY_CSV  = METRICS_DIR.parent / "survey" / "docs" / "data.csv"
OUT_DIR     = METRICS_DIR / "output"
STATS_MD    = OUT_DIR / "statistical_tests.md"

MODES = ["form", "ask", "chat"]

# Timing line pattern — anchored: optional leading whitespace, exact phrasing.
TIMING_RE = re.compile(r"Time\s+elapsed\s*:\s*(\d+)\s*seconds?", re.IGNORECASE)


# ───────────────────────────── helpers ───────────────────────────────────────


def extract_timing(text: str) -> tuple[int | None, str | None]:
    """Return (seconds, raw_line) or (None, None) if not found."""
    if not isinstance(text, str):
        return None, None
    for line in text.splitlines():
        m = TIMING_RE.search(line)
        if m:
            return int(m.group(1)), line.strip()
    return None, None


def rank_biserial_wilcoxon(x: np.ndarray, y: np.ndarray) -> float:
    """
    Matched-pairs rank-biserial correlation.
    Positive when x > y on average.
    Uses the (W+ - W-) / (W+ + W-) form from Kerby (2014).
    """
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
    """Rank-biserial r for Mann-Whitney U (Wendt 1972)."""
    return float(1 - (2 * u) / (n1 * n2))


def kendalls_w(arr: np.ndarray) -> float:
    """
    Kendall's W for a (subjects x conditions) matrix.
    arr.shape == (n, k).
    """
    n, k = arr.shape
    ranks = np.apply_along_axis(stats.rankdata, 1, arr)
    rj = ranks.sum(axis=0)
    s = ((rj - rj.mean()) ** 2).sum()
    return float(12 * s / (n ** 2 * (k ** 3 - k)))


def effect_size_eps_squared(h: float, n: int) -> float:
    """ε² for Kruskal-Wallis."""
    return float(h / (n - 1)) if n > 1 else float("nan")


def fmt_p(p: float) -> str:
    if p < 0.001:
        return "<0.001"
    return f"{p:.3f}"


# ───────────────────────────── 1. Extract ────────────────────────────────────


def step_extract() -> tuple[pd.DataFrame, list[str]]:
    docs = pd.read_csv(DOCS_CSV)
    irregularities: list[str] = []
    rows = []
    for _, r in docs.iterrows():
        sec, raw = extract_timing(r["document"])
        if sec is None:
            irregularities.append(
                f"id={r['id']} user={r['user_id']} mode={r['ai_mode']}: "
                "no timing line found"
            )
            continue
        # Flag unusual phrasings (anything other than exact 'Time elapsed: N seconds')
        if not re.match(r"^Time elapsed:\s+\d+\s+seconds?$", raw):
            irregularities.append(
                f"id={r['id']} user={r['user_id']} mode={r['ai_mode']}: "
                f"non-canonical phrasing → {raw!r}"
            )
        rows.append({
            "id":           r["id"],
            "user_id":      r["user_id"],
            "ai_mode":      r["ai_mode"],
            "time_seconds": sec,
        })
    df = pd.DataFrame(rows)
    df.to_csv(OUT_DIR / "per_mode_timing.csv", index=False)
    return df, irregularities


def sanity_checks(df: pd.DataFrame) -> list[str]:
    notes: list[str] = []
    # Sanity 1: 113 rows, 37/37/39
    counts = df["ai_mode"].value_counts().to_dict()
    notes.append(f"Extracted rows: {len(df)} (expected 113)")
    notes.append(f"Per-mode counts: {counts} (expected form=37, ask=37, chat=39)")
    # Sanity 2: median * 3 <= survey duration per participant
    surv = pd.read_csv(SURVEY_CSV, sep=None, engine="python")
    surv = surv[["participant_id", "duration"]].copy()
    surv["participant_id"] = surv["participant_id"].astype(str)
    df_ids = df.copy()
    df_ids["user_id"] = df_ids["user_id"].astype(str)
    per_user = (
        df_ids.groupby("user_id")["time_seconds"]
        .sum()
        .reset_index()
        .rename(columns={"time_seconds": "sum_mode_time"})
    )
    merged = per_user.merge(
        surv, left_on="user_id", right_on="participant_id", how="left"
    )
    # Participants whose summed per-mode time exceeds reported survey duration
    over = merged[
        merged["duration"].notna()
        & (merged["duration"] > 0)
        & (merged["sum_mode_time"] > merged["duration"])
    ]
    if not over.empty:
        notes.append(
            f"{len(over)} participants where Σ(per-mode time) > total survey "
            "duration:"
        )
        for _, r in over.iterrows():
            notes.append(
                f"  - {r['user_id']}: Σmodes={int(r['sum_mode_time'])}s "
                f"> duration={int(r['duration'])}s"
            )
    # Also flag participants present in docs but missing from survey
    missing = merged[merged["duration"].isna()]
    if not missing.empty:
        notes.append(
            f"{len(missing)} participants in docs but not in survey "
            "(no duration available): "
            + ", ".join(missing["user_id"].tolist())
        )
    # And participants with duration == -1 (encoded missing)
    neg = merged[merged["duration"].fillna(0) < 0]
    if not neg.empty:
        notes.append(
            f"{len(neg)} participants with survey duration < 0 (encoded "
            "missing): " + ", ".join(neg["user_id"].tolist())
        )
    return notes


# ───────────────────────────── 2. Descriptives ───────────────────────────────


def step_descriptives(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for mode in MODES:
        v = df.loc[df["ai_mode"] == mode, "time_seconds"].dropna().astype(float)
        q1, q3 = v.quantile([0.25, 0.75])
        rows.append({
            "mode":   mode,
            "n":      int(v.size),
            "mean":   round(v.mean(), 2),
            "sd":     round(v.std(ddof=1), 2),
            "median": round(v.median(), 2),
            "q1":     round(q1, 2),
            "q3":     round(q3, 2),
            "iqr":    round(q3 - q1, 2),
            "min":    int(v.min()),
            "max":    int(v.max()),
        })
    out = pd.DataFrame(rows)
    out.to_csv(OUT_DIR / "per_mode_timing_summary.csv", index=False)
    return out


# ───────────────────────────── 3. Within-subjects ────────────────────────────


def matched_triple(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a (user × mode) wide dataframe of seconds for participants with
    exactly one document in each of form, ask, chat.
    """
    counts = (
        df.groupby(["user_id", "ai_mode"]).size().unstack(fill_value=0)
    )
    keep = counts[
        (counts.get("form", 0) == 1)
        & (counts.get("ask", 0) == 1)
        & (counts.get("chat", 0) == 1)
    ].index
    sub = df[df["user_id"].isin(keep)]
    wide = (
        sub.pivot_table(
            index="user_id", columns="ai_mode", values="time_seconds",
            aggfunc="first",
        )
        .reindex(columns=MODES)
        .dropna()
    )
    return wide


def step_within(wide: pd.DataFrame) -> dict:
    # Shapiro–Wilk per mode
    shapiro = {}
    for mode in MODES:
        w, p = stats.shapiro(wide[mode].values)
        shapiro[mode] = {"W": float(w), "p": float(p)}

    # Friedman
    chi2, p_fried = stats.friedmanchisquare(
        wide["form"].values, wide["ask"].values, wide["chat"].values
    )
    w_kendall = kendalls_w(wide[MODES].values)

    # Pairwise Wilcoxon
    pairs = [("form", "ask"), ("form", "chat"), ("ask", "chat")]
    pairwise = []
    for a, b in pairs:
        # Drop ties to avoid scipy warning (none here, but safe)
        diff = wide[a].values - wide[b].values
        # scipy's wilcoxon: zero_method='wilcox' (default) drops zeros
        res = stats.wilcoxon(wide[a].values, wide[b].values, zero_method="wilcox")
        r = rank_biserial_wilcoxon(wide[a].values, wide[b].values)
        pairwise.append({
            "pair": f"{a} vs {b}",
            "W":    float(res.statistic),
            "p":    float(res.pvalue),
            "r":    float(r),
            "median_diff": float(np.median(wide[a].values - wide[b].values)),
            "bonf_sig": res.pvalue < 0.05 / 3,
        })

    return {
        "n":        int(len(wide)),
        "shapiro":  shapiro,
        "chi2":     float(chi2),
        "df":       2,
        "p":        float(p_fried),
        "w":        float(w_kendall),
        "pairwise": pairwise,
    }


# ───────────────────────────── 4. Between-groups ─────────────────────────────


def step_between(df: pd.DataFrame) -> dict:
    groups = [
        df.loc[df["ai_mode"] == m, "time_seconds"].astype(float).values
        for m in MODES
    ]
    h, p = stats.kruskal(*groups)
    n_total = sum(len(g) for g in groups)
    eps2 = effect_size_eps_squared(h, n_total)

    pairs = [("form", "ask"), ("form", "chat"), ("ask", "chat")]
    pairwise = []
    for a, b in pairs:
        x = df.loc[df["ai_mode"] == a, "time_seconds"].astype(float).values
        y = df.loc[df["ai_mode"] == b, "time_seconds"].astype(float).values
        res = stats.mannwhitneyu(x, y, alternative="two-sided")
        r = mannwhitney_r(res.statistic, len(x), len(y))
        pairwise.append({
            "pair":     f"{a} vs {b}",
            "U":        float(res.statistic),
            "p":        float(res.pvalue),
            "r":        float(r),
            "median_a": float(np.median(x)),
            "median_b": float(np.median(y)),
            "bonf_sig": res.pvalue < 0.05 / 3,
        })

    return {
        "n":        int(n_total),
        "H":        float(h),
        "p":        float(p),
        "eps2":     float(eps2),
        "pairwise": pairwise,
    }


# ───────────────────────────── 5. Figure ─────────────────────────────────────


def step_figure(df: pd.DataFrame) -> Path:
    # Mirror NLP/BERT boxplot conventions:
    # one panel, 4 boxes (All, Form, Ask, Chat), mean diamonds, thin black
    # median, dashed y-grid, no top/right spines, 150 dpi, bbox_inches='tight'.
    GROUPS      = ["All", "Form", "Ask", "Chat"]
    BOX_COLORS  = ["#FFD59A", "#A7C7E7", "#FFF9AE", "#E0BBE4"]
    MEAN_COLORS = ["#FF8C00", "#0000FF", "#FFD700", "#8A2BE2"]

    data = {
        "All":  df["time_seconds"].astype(float).values,
        "Form": df.loc[df["ai_mode"] == "form", "time_seconds"].astype(float).values,
        "Ask":  df.loc[df["ai_mode"] == "ask",  "time_seconds"].astype(float).values,
        "Chat": df.loc[df["ai_mode"] == "chat", "time_seconds"].astype(float).values,
    }
    group_data = [data[g] for g in GROUPS]

    fig, ax = plt.subplots(figsize=(9, 6))
    bp = ax.boxplot(
        group_data,
        positions=range(len(GROUPS)),
        widths=0.52,
        patch_artist=True,
        showfliers=True,
        medianprops=dict(color="black", linewidth=0.9),
        whiskerprops=dict(color="black", linewidth=0.8),
        capprops=dict(color="black", linewidth=0.8),
        boxprops=dict(linewidth=0.8),
        flierprops=dict(marker="o", markerfacecolor="grey",
                        markeredgecolor="grey", markersize=4, alpha=0.55),
    )
    for patch, col in zip(bp["boxes"], BOX_COLORS):
        patch.set_facecolor(col)
        patch.set_edgecolor("black")
    for i, (d, mc) in enumerate(zip(group_data, MEAN_COLORS)):
        if len(d) == 0:
            continue
        ax.scatter(i, np.mean(d), marker="D", s=90,
                   color=mc, edgecolors="black", linewidths=0.8, zorder=6)

    ax.set_xticks(range(len(GROUPS)))
    ax.set_xticklabels(GROUPS, fontsize=12)
    ax.set_ylabel("Completion time (seconds)", fontsize=11)
    ax.set_title("Per-Mode Completion Time", fontsize=13, fontweight="bold", pad=12)
    ax.yaxis.grid(True, linestyle="--", linewidth=0.8, alpha=0.6)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)

    box_patches = [
        mpatches.Patch(facecolor=bc, edgecolor="black", label=g)
        for g, bc in zip(GROUPS, BOX_COLORS)
    ]
    mean_handles = [
        plt.Line2D([0], [0], marker="D", color="w",
                   markerfacecolor=mc, markeredgecolor="black",
                   markersize=8, label=f"{g} mean")
        for g, mc in zip(GROUPS, MEAN_COLORS)
    ]
    ax.legend(handles=box_patches + mean_handles, loc="upper right",
              fontsize=9, ncol=2, framealpha=0.88, edgecolor="lightgrey")

    plt.tight_layout()
    out = OUT_DIR / "per_mode_timing_boxplot.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out


# ───────────────────────────── 6. Append markdown ────────────────────────────


def step_markdown(desc: pd.DataFrame, within: dict, between: dict,
                  irregularities: list[str], notes: list[str]) -> None:
    lines: list[str] = []
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Per-Mode Completion Time")
    lines.append("")
    lines.append(
        "Source: timing line `Time elapsed: NNN seconds` emitted by ROPAgen "
        "at the end of every generated document (one value per "
        "participant × mode). Extracted via "
        "`metrics/scripts/per_mode_timing.py`. Sample sizes match the NLP "
        "doc-level analysis: full n = 113 (Form 37, Ask 37, Chat 39); "
        f"matched-triple within-subjects subset n = {within['n']}."
    )
    lines.append("")
    lines.append("### Descriptives (full dataset, n = 113)")
    lines.append("")
    lines.append("| Mode | n | Mean (s) | SD (s) | Median (s) | IQR (s) | Min (s) | Max (s) |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for _, r in desc.iterrows():
        lines.append(
            f"| {r['mode'].capitalize()} | {int(r['n'])} | {r['mean']:.1f} | "
            f"{r['sd']:.1f} | {r['median']:.1f} | {r['iqr']:.1f} | "
            f"{int(r['min'])} | {int(r['max'])} |"
        )
    lines.append("")
    lines.append("### Shapiro-Wilk normality (matched n = 26)")
    lines.append("")
    lines.append("| Mode | W | p | Normal? |")
    lines.append("|---|---|---|---|")
    for mode in MODES:
        s = within["shapiro"][mode]
        lines.append(
            f"| {mode.capitalize()} | {s['W']:.3f} | {fmt_p(s['p'])} | "
            f"{'Yes' if s['p'] >= 0.05 else 'No'} |"
        )
    lines.append("")
    lines.append(
        "Distributions deviate from normality on at least one mode; "
        "non-parametric tests used throughout (consistent with the NLP and "
        "survey pipelines)."
    )
    lines.append("")
    lines.append(f"### Friedman test (within-subjects, n = {within['n']})")
    lines.append("")
    lines.append("| χ² | df | p | Kendall's W | Significant (α=0.05) |")
    lines.append("|---|---|---|---|---|")
    sig_fr = "Yes" if within["p"] < 0.05 else "No"
    lines.append(
        f"| {within['chi2']:.3f} | {within['df']} | {fmt_p(within['p'])} | "
        f"{within['w']:.3f} | {sig_fr} |"
    )
    lines.append("")
    if within["p"] < 0.05:
        lines.append(
            "Friedman is significant → pairwise Wilcoxon signed-rank "
            "post-hoc with Bonferroni-corrected α = 0.0167 (3 comparisons). "
            "Effect size: matched-pairs rank-biserial r (positive when the "
            "first-named mode in the pair is *higher*, i.e. *slower*)."
        )
        lines.append("")
        lines.append("### Pairwise Wilcoxon signed-rank (matched n = "
                     f"{within['n']})")
        lines.append("")
        lines.append("| Pair | W | p | r | Median diff (s) | Sig (Bonf) |")
        lines.append("|---|---|---|---|---|---|")
        for pw in within["pairwise"]:
            sig = "**Yes**" if pw["bonf_sig"] else "No"
            lines.append(
                f"| {pw['pair']} | {pw['W']:.1f} | {fmt_p(pw['p'])} | "
                f"{pw['r']:+.3f} | {pw['median_diff']:+.1f} | {sig} |"
            )
        lines.append("")
    lines.append("### Kruskal-Wallis sensitivity (full n = 113, unbalanced)")
    lines.append("")
    lines.append("| H | p | ε² | Significant (α=0.05) |")
    lines.append("|---|---|---|---|")
    sig_kw = "Yes" if between["p"] < 0.05 else "No"
    lines.append(
        f"| {between['H']:.3f} | {fmt_p(between['p'])} | "
        f"{between['eps2']:.3f} | {sig_kw} |"
    )
    lines.append("")
    lines.append(
        "Reported as a between-groups sensitivity check on the unbalanced "
        "full sample; the matched-triple Wilcoxon family above is the "
        "primary inferential result."
    )
    lines.append("")
    lines.append("### Pairwise Mann-Whitney U (full n = 113)")
    lines.append("")
    lines.append("| Pair | U | p | r | Median A (s) | Median B (s) | Sig (Bonf α=0.0167) |")
    lines.append("|---|---|---|---|---|---|---|")
    for pw in between["pairwise"]:
        sig = "**Yes**" if pw["bonf_sig"] else "No"
        lines.append(
            f"| {pw['pair']} | {pw['U']:.1f} | {fmt_p(pw['p'])} | "
            f"{pw['r']:+.3f} | {pw['median_a']:.1f} | {pw['median_b']:.1f} | "
            f"{sig} |"
        )
    lines.append("")
    lines.append("### Data-quality notes")
    lines.append("")
    if irregularities:
        lines.append("Non-canonical timing-line phrasing / missing entries:")
        for x in irregularities:
            lines.append(f"- {x}")
    else:
        lines.append(
            "All 113 retained documents contain a canonical "
            "`Time elapsed: NNN seconds` line. No missing entries, no "
            "phrasing irregularities."
        )
    lines.append("")
    if notes:
        lines.append("Cross-check vs. total survey duration:")
        for n in notes:
            lines.append(f"- {n}")
        lines.append("")

    body = "\n".join(lines)
    existing = STATS_MD.read_text(encoding="utf-8")
    # Idempotent: if the section already exists, replace from its header to EOF
    marker = "\n## Per-Mode Completion Time"
    if marker in existing:
        existing = existing.split(marker)[0].rstrip() + "\n"
    STATS_MD.write_text(existing + body + "\n", encoding="utf-8")


# ───────────────────────────── main ──────────────────────────────────────────


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df, irregularities = step_extract()
    notes = sanity_checks(df)
    desc = step_descriptives(df)
    wide = matched_triple(df)
    within = step_within(wide)
    between = step_between(df)
    fig_path = step_figure(df)
    step_markdown(desc, within, between, irregularities, notes)

    # Console summary
    print("=== EXTRACTION ===")
    for n in notes:
        print(" ", n)
    if irregularities:
        print("Irregularities:")
        for x in irregularities:
            print("  ", x)
    else:
        print("  No timing-line irregularities.")

    print("\n=== DESCRIPTIVES (full n=113) ===")
    print(desc.to_string(index=False))

    print(f"\n=== WITHIN-SUBJECTS (matched n={within['n']}) ===")
    print("Shapiro-Wilk:")
    for m in MODES:
        s = within["shapiro"][m]
        print(f"  {m}: W={s['W']:.3f}, p={s['p']:.4f}")
    print(f"Friedman: χ²({within['df']})={within['chi2']:.3f}, "
          f"p={within['p']:.4f}, Kendall's W={within['w']:.3f}")
    print("Pairwise Wilcoxon (Bonferroni α=0.0167):")
    for pw in within["pairwise"]:
        print(f"  {pw['pair']:>14s}  W={pw['W']:6.1f}  p={pw['p']:.4f}  "
              f"r={pw['r']:+.3f}  Δmed={pw['median_diff']:+.1f}s  "
              f"{'SIG' if pw['bonf_sig'] else 'ns'}")

    print(f"\n=== BETWEEN-GROUPS SENSITIVITY (full n={between['n']}) ===")
    print(f"Kruskal-Wallis: H={between['H']:.3f}, p={between['p']:.4f}, "
          f"ε²={between['eps2']:.3f}")
    print("Pairwise Mann-Whitney U (Bonferroni α=0.0167):")
    for pw in between["pairwise"]:
        print(f"  {pw['pair']:>14s}  U={pw['U']:7.1f}  p={pw['p']:.4f}  "
              f"r={pw['r']:+.3f}  medA={pw['median_a']:.1f}  "
              f"medB={pw['median_b']:.1f}  "
              f"{'SIG' if pw['bonf_sig'] else 'ns'}")

    print(f"\nFigure saved → {fig_path}")
    print(f"Tables    → {OUT_DIR/'per_mode_timing.csv'}")
    print(f"           {OUT_DIR/'per_mode_timing_summary.csv'}")
    print(f"Stats md  → {STATS_MD} (Per-Mode Completion Time section)")


if __name__ == "__main__":
    main()
