"""
Worked-example NLP metrics for the Evaluation chapter.

Goal
----
Extract two chapter passages (Ch2 — Zwecke und Rechtsgrundlagen, Ch5 —
Aufbewahrungsfristen und Löschung) from three documents:

  - reference  (plain-text expert reference, docs/reference.txt)
  - IAR1116    (Chat mode, id=11)
  - AEB2451    (Form mode, id=80)

then compute the same chapter-level metrics used by the main pipeline so the
worked-example values in the thesis are directly comparable to the chapter
tables.

Metrics
-------
- Retention passages (lexical example): BLEU, ROUGE-2, METEOR
- Purpose passages   (semantic example): BERTScore P / R / F1, SBERT (ModernBERT)

The splitter logic, alias table, and scoring config are copied verbatim from
the notebook cells `extract_reference_chapters`, `extract_chapters_markdown`,
`map_doc_chapters_to_canonical`, `compute_bertscore`, and the SBERT cell.

Output
------
A single Markdown report at python/output/worked_examples.md with the three
verbatim passages per chapter and the per-candidate metric tables (4 decimal
places). No interpretive prose — the thesis agent writes that.
"""

from __future__ import annotations

import difflib
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
import evaluate
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer


# ─── paths ─────────────────────────────────────────────────────────────────

ROOT          = Path(__file__).resolve().parents[2]            # python/
METRICS_DIR   = ROOT / "metrics"
DOCS_DIR      = METRICS_DIR / "docs"
REFERENCE_TXT = DOCS_DIR / "reference.txt"
DOCUMENTS_CSV = DOCS_DIR / "documents.csv"
OUTPUT_MD     = ROOT / "output" / "worked_examples.md"

MODEL_NAME = "answerdotai/ModernBERT-base"
DEVICE     = "cuda" if torch.cuda.is_available() else "cpu"

# ─── canonical chapter list + alias table (verbatim from notebook cell 19) ──

CANONICAL_CHAPTERS = [
    "Verantwortliche Stelle und Kontaktdaten",
    "Zwecke und Rechtsgrundlagen der Verarbeitung",
    "Kategorien personenbezogener Daten und Datenquellen",
    "Betroffene Personen und Empfänger",
    "Aufbewahrungsfristen und Löschung",
    "Technische und organisatorische Maßnahmen",
]

CHAPTER_ALIASES: dict[str, list[str]] = {
    "Verantwortliche Stelle und Kontaktdaten": [
        "verantwortliche stelle und kontaktdaten",
        "verantwortliche stelle und datenschutzbeauftragte",
        "verantwortliche stelle und datenschutzbeauftragter",
    ],
    "Zwecke und Rechtsgrundlagen der Verarbeitung": [
        "zwecke und rechtsgrundlagen der verarbeitung",
        "zwecke der verarbeitung und rechtsgrundlagen",
    ],
    "Kategorien personenbezogener Daten und Datenquellen": [
        "kategorien personenbezogener daten und datenquellen",
        "kategorien personenbezogener daten",
    ],
    "Betroffene Personen und Empfänger": [
        "betroffene personen und empfänger",
        "betroffene personen und empfänger der daten",
        "betroffene personen und empfänger:innen der daten",
    ],
    "Aufbewahrungsfristen und Löschung": [
        "aufbewahrungsfristen und löschung",
        "löschfristen und aufbewahrungsdauern",
        "löschfristen und aufbewahrungsfristen",
        "löschfristen und datenaufbewahrung",
        "löschfristen und speicherdauer",
        "aufbewahrungsfristen und datenlöschung",
    ],
    "Technische und organisatorische Maßnahmen": [
        "technische und organisatorische maßnahmen",
        "technische und organisatorische maßnahmen (tom)",
        "technische und organisatorische massnahmen",
    ],
}

_SUBSECTION_RE     = re.compile(r"^\s*\d+\.\d+")
_LEADING_NUMBER_RE = re.compile(r"^\d+\.?\s+")


def _normalize_header(line: str) -> str:
    s = line.strip()
    s = _LEADING_NUMBER_RE.sub("", s, count=1)
    s = s.strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s


def _match_canonical(line: str) -> str | None:
    raw = line.strip()
    if not raw:
        return None
    if _SUBSECTION_RE.match(raw):
        return None
    if ":" in raw:
        return None

    norm = _normalize_header(raw)
    if not norm:
        return None
    for canonical, aliases in CHAPTER_ALIASES.items():
        for alias in aliases:
            if norm == alias:
                return canonical
            if norm.startswith(alias) and (len(norm) - len(alias)) <= 8:
                return canonical
        best = max(
            (difflib.SequenceMatcher(None, norm, a).ratio() for a in aliases),
            default=0.0,
        )
        if best >= 0.92:
            return canonical
    return None


def _is_sub_chapter(header: str) -> bool:
    return bool(_SUBSECTION_RE.match(header.strip()))


def _strip_metadata_footer(text: str) -> str:
    lines = text.split("\n")
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip() == "---":
            return "\n".join(lines[:i])
    return text


def extract_chapters_markdown(text: str) -> dict[str, str]:
    """Split a markdown ROPA document into H2 sections (notebook copy)."""
    text = text.strip()
    if text.startswith("```"):
        text = text[text.index("\n") + 1:]
    if text.endswith("```"):
        text = text[:text.rindex("```")]
    text = _strip_metadata_footer(text)

    pattern = re.compile(r"^## (.+)", re.MULTILINE)
    matches = [
        m for m in pattern.finditer(text)
        if not _is_sub_chapter(m.group(1).strip())
    ]

    chapters: dict[str, str] = {}
    for idx, match in enumerate(matches):
        header = match.group(1).strip()
        start  = match.end()
        end    = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        chapters[header] = text[start:end].strip()
    return chapters


def extract_reference_chapters(
    reference_text: str,
    canonical_list: list[str] = CANONICAL_CHAPTERS,
) -> dict[str, str]:
    text = _strip_metadata_footer(reference_text)
    lines = text.split("\n")

    header_positions: list[tuple[int, str]] = []
    for i, line in enumerate(lines):
        canonical = _match_canonical(line)
        if canonical is not None:
            header_positions.append((i, canonical))

    result: dict[str, str] = {c: "" for c in canonical_list}
    for idx, (line_i, canonical) in enumerate(header_positions):
        next_i = header_positions[idx + 1][0] if idx + 1 < len(header_positions) else len(lines)
        content_lines = lines[line_i + 1:next_i]
        result[canonical] = "\n".join(content_lines).strip()
    return result


def map_doc_chapters_to_canonical(
    raw_dict: dict[str, str],
    canonical_list: list[str] = CANONICAL_CHAPTERS,
) -> dict[str, str]:
    headers_in_order = list(raw_dict.keys())
    result: dict[str, str] = {}
    used_headers: set[str] = set()

    # Stage 1
    for h in headers_in_order:
        canonical = _match_canonical(h)
        if canonical is not None and canonical not in result:
            result[canonical] = raw_dict[h]
            used_headers.add(h)

    # Stage 2
    for canonical in canonical_list:
        if canonical in result:
            continue
        best_score, best_header = 0.0, None
        for h in headers_in_order:
            if h in used_headers:
                continue
            h_clean = re.sub(r"^\d+[.,]?\d*[\s.]+", "", h).strip()
            ratio = difflib.SequenceMatcher(None, h_clean.lower(), canonical.lower()).ratio()
            if ratio > best_score:
                best_score, best_header = ratio, h
        if best_score >= 0.45 and best_header is not None:
            result[canonical] = raw_dict[best_header]
            used_headers.add(best_header)

    # Stage 3
    unmatched_headers  = [h for h in headers_in_order if h not in used_headers]
    missing_canonicals = [c for c in canonical_list if c not in result]
    for i, canonical in enumerate(missing_canonicals):
        if i < len(unmatched_headers):
            result[canonical] = raw_dict[unmatched_headers[i]]
            used_headers.add(unmatched_headers[i])
        else:
            result[canonical] = ""

    return result


# ─── scoring code (verbatim notebook config) ───────────────────────────────


def make_bertscore_fn(tokenizer, model):
    """Closure over the loaded ModernBERT for BERTScore P/R/F1."""

    def _embed(texts: list[str]) -> list[torch.Tensor]:
        out_embs: list[torch.Tensor] = []
        enc = tokenizer(
            texts, padding=True, truncation=True, max_length=8192,
            return_tensors="pt",
        ).to(DEVICE)
        with torch.no_grad():
            out = model(**enc)
        hidden = out.last_hidden_state
        mask   = enc["attention_mask"].bool()
        for j in range(len(texts)):
            emb = hidden[j][mask[j]]
            out_embs.append(F.normalize(emb, dim=-1))
        if DEVICE == "cuda":
            torch.cuda.empty_cache()
        return out_embs

    def _score(candidate: str, reference: str) -> tuple[float, float, float]:
        [ref_emb]  = _embed([reference])
        [cand_emb] = _embed([candidate])
        sim = ref_emb @ cand_emb.T              # (T_ref, T_cand)
        r   = sim.max(dim=1).values.mean().item()
        p   = sim.max(dim=0).values.mean().item()
        f1  = (2 * p * r / (p + r)) if (p + r) > 0 else 0.0
        return p, r, f1

    return _score


def sbert_modernbert_cosine(sbert_model, candidate: str, reference: str) -> float:
    ref_emb = sbert_model.encode(
        [reference], batch_size=1, convert_to_numpy=True,
        normalize_embeddings=True, show_progress_bar=False,
    )
    cand_emb = sbert_model.encode(
        [candidate], batch_size=1, convert_to_numpy=True,
        normalize_embeddings=True, show_progress_bar=False,
    )
    return float((cand_emb @ ref_emb.T).squeeze())


# ─── main ──────────────────────────────────────────────────────────────────


def main() -> None:
    print(f"Device: {DEVICE}")

    # 1. Load reference + split into canonical chapters
    reference_text = REFERENCE_TXT.read_text(encoding="utf-8")
    ref_chapters   = extract_reference_chapters(reference_text)

    # 2. Load candidate documents + split
    docs_df = pd.read_csv(DOCUMENTS_CSV)

    cand_specs = [
        {"label": "IAR1116-chat", "id": 11, "user_id": "IAR1116", "ai_mode": "chat"},
        {"label": "AEB2451-form", "id": 80, "user_id": "AEB2451", "ai_mode": "form"},
    ]
    for c in cand_specs:
        row = docs_df[
            (docs_df["id"] == c["id"])
            & (docs_df["user_id"] == c["user_id"])
            & (docs_df["ai_mode"] == c["ai_mode"])
        ]
        if len(row) != 1:
            raise SystemExit(
                f"Expected exactly 1 row for {c['label']} (id={c['id']}, "
                f"user_id={c['user_id']}, ai_mode={c['ai_mode']}); got {len(row)}"
            )
        text = str(row.iloc[0]["document"])
        raw_chapters = extract_chapters_markdown(text)
        c["chapters"] = map_doc_chapters_to_canonical(raw_chapters)

    purpose_key   = "Zwecke und Rechtsgrundlagen der Verarbeitung"
    retention_key = "Aufbewahrungsfristen und Löschung"

    ref_purpose   = ref_chapters.get(purpose_key, "")
    ref_retention = ref_chapters.get(retention_key, "")

    # Sanity-check non-empty
    missing = []
    if not ref_purpose.strip():
        missing.append(f"reference / {purpose_key}")
    if not ref_retention.strip():
        missing.append(f"reference / {retention_key}")
    for c in cand_specs:
        for k, label in [(purpose_key, "Purpose"), (retention_key, "Retention")]:
            if not c["chapters"].get(k, "").strip():
                missing.append(f"{c['label']} / {label} ({k})")
    if missing:
        raise SystemExit("Empty chapter(s) extracted:\n  - " + "\n  - ".join(missing))

    # 3. Load metric models
    print("Loading evaluate metrics …")
    bleu_metric   = evaluate.load("bleu")
    rouge_metric  = evaluate.load("rouge")
    meteor_metric = evaluate.load("meteor")

    print(f"Loading {MODEL_NAME} for BERTScore …")
    bert_tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    bert_model     = AutoModel.from_pretrained(MODEL_NAME).to(DEVICE)
    bert_model.eval()
    bertscore = make_bertscore_fn(bert_tokenizer, bert_model)

    print(f"Loading SentenceTransformer {MODEL_NAME} …")
    sbert_model = SentenceTransformer(MODEL_NAME, device=DEVICE)
    sbert_model.max_seq_length = 8192

    # 4. Score
    retention_rows: list[dict] = []
    purpose_rows:   list[dict] = []

    for c in cand_specs:
        cand_ret = c["chapters"][retention_key]
        cand_pur = c["chapters"][purpose_key]

        # Retention — lexical example
        try:
            b = bleu_metric.compute(
                predictions=[cand_ret], references=[[ref_retention]]
            )
            bleu = float(b["bleu"])
        except Exception:
            bleu = 0.0
        rouge = rouge_metric.compute(
            predictions=[cand_ret], references=[ref_retention]
        )
        meteor = meteor_metric.compute(
            predictions=[cand_ret], references=[ref_retention]
        )
        retention_rows.append({
            "candidate": c["label"],
            "BLEU":     bleu,
            "ROUGE-2":  float(rouge["rouge2"]),
            "METEOR":   float(meteor["meteor"]),
        })

        # Purpose — semantic example
        p, r, f1 = bertscore(cand_pur, ref_purpose)
        sbert_cos = sbert_modernbert_cosine(sbert_model, cand_pur, ref_purpose)
        purpose_rows.append({
            "candidate":      c["label"],
            "BERTScore_P":    p,
            "BERTScore_R":    r,
            "BERTScore_F1":   f1,
            "SBERT_ModernBERT": sbert_cos,
        })

    # 5. Render markdown
    def fmt(x: float) -> str:
        return f"{x:.4f}"

    L: list[str] = []
    L.append("# Worked Examples: Chapter-Level NLP Metrics")
    L.append("")
    L.append(
        "Two-chapter worked example feeding the Evaluation chapter. All passages "
        "are extracted verbatim from the same chapter splitter used by the main "
        "pipeline (`extract_reference_chapters`, `extract_chapters_markdown`, "
        "`map_doc_chapters_to_canonical`); all metric values use the identical "
        "scoring code and ModernBERT (`answerdotai/ModernBERT-base`) configuration "
        f"as `chapter_results.csv`, computed on `{DEVICE}`."
    )
    L.append("")
    L.append("Candidates:")
    L.append("")
    L.append("- `IAR1116-chat` — Chat mode, document id 11")
    L.append("- `AEB2451-form` — Form mode, document id 80")
    L.append("")

    # ── Retention block ──
    L.append("## 1. Retention worked example (Ch5 — *Aufbewahrungsfristen und Löschung*)")
    L.append("")
    L.append("Lexical metrics: BLEU, ROUGE-2, METEOR.")
    L.append("")

    L.append("### Reference passage")
    L.append("")
    L.append("```text")
    L.append(ref_retention)
    L.append("```")
    L.append("")

    L.append("### IAR1116 (Chat) passage")
    L.append("")
    L.append("```text")
    L.append(cand_specs[0]["chapters"][retention_key])
    L.append("```")
    L.append("")

    L.append("### AEB2451 (Form) passage")
    L.append("")
    L.append("```text")
    L.append(cand_specs[1]["chapters"][retention_key])
    L.append("```")
    L.append("")

    L.append("### Lexical scores against the reference passage")
    L.append("")
    L.append("| Candidate | BLEU | ROUGE-2 | METEOR |")
    L.append("|---|---|---|---|")
    for r in retention_rows:
        L.append(
            f"| {r['candidate']} | {fmt(r['BLEU'])} | "
            f"{fmt(r['ROUGE-2'])} | {fmt(r['METEOR'])} |"
        )
    L.append("")

    # ── Purpose block ──
    L.append("## 2. Purpose worked example (Ch2 — *Zwecke und Rechtsgrundlagen der Verarbeitung*)")
    L.append("")
    L.append("Semantic metrics: BERTScore Precision/Recall/F1 and SBERT cosine similarity (ModernBERT).")
    L.append("")

    L.append("### Reference passage")
    L.append("")
    L.append("```text")
    L.append(ref_purpose)
    L.append("```")
    L.append("")

    L.append("### IAR1116 (Chat) passage")
    L.append("")
    L.append("```text")
    L.append(cand_specs[0]["chapters"][purpose_key])
    L.append("```")
    L.append("")

    L.append("### AEB2451 (Form) passage")
    L.append("")
    L.append("```text")
    L.append(cand_specs[1]["chapters"][purpose_key])
    L.append("```")
    L.append("")

    L.append("### Semantic scores against the reference passage")
    L.append("")
    L.append("| Candidate | BERTScore P | BERTScore R | BERTScore F1 | SBERT (ModernBERT) |")
    L.append("|---|---|---|---|---|")
    for r in purpose_rows:
        L.append(
            f"| {r['candidate']} | {fmt(r['BERTScore_P'])} | "
            f"{fmt(r['BERTScore_R'])} | {fmt(r['BERTScore_F1'])} | "
            f"{fmt(r['SBERT_ModernBERT'])} |"
        )
    L.append("")

    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_MD.write_text("\n".join(L), encoding="utf-8")
    print(f"\nWrote: {OUTPUT_MD}")

    # 6. Console summary for the agent's report
    print("\n=== passage lengths (chars / words) ===")
    def _lw(s: str) -> str:
        return f"{len(s):>5} chars / {len(s.split()):>4} words"
    print(f"Reference  Ch2 Purpose   : {_lw(ref_purpose)}")
    print(f"Reference  Ch5 Retention : {_lw(ref_retention)}")
    for c in cand_specs:
        print(f"{c['label']} Ch2 Purpose   : "
              f"{_lw(c['chapters'][purpose_key])}")
        print(f"{c['label']} Ch5 Retention : "
              f"{_lw(c['chapters'][retention_key])}")

    print("\n=== Retention scores ===")
    print(pd.DataFrame(retention_rows).to_string(index=False))
    print("\n=== Purpose scores ===")
    print(pd.DataFrame(purpose_rows).to_string(index=False))


if __name__ == "__main__":
    main()
