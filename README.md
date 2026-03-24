# ROPAgen Document Evaluation

NLP evaluation pipeline for the **ROPAgen** Master's thesis — measuring how closely AI-generated German GDPR ROPA documents match a human-written reference, across three AI generation modes.

## Background

ROPAgen is a web application that helps users create **Records of Processing Activities (ROPA)** documents required under GDPR. It supports three AI-assisted generation modes:

| Mode | Description |
|---|---|
| `form` | User fills checkboxes; AI suggests remaining fields (most user input) |
| `ask` | Conversational Q&A — AI asks targeted questions, user has to provide answers |
| `chat` | Free-form chat — AI generates the document from open-ended user input |

This notebook evaluates 117 generated documents (38 ask · 39 form · 40 chat) against a single human-written reference document using seven NLP metrics.

---

## Metrics

| Metric | Type | Description |
|---|---|---|
| **BLEU** | Lexical | Modified n-gram precision; surface-level overlap |
| **ROUGE-1 / ROUGE-2** | Lexical | Unigram / bigram recall against reference |
| **ROUGE-L** | Lexical | Longest common subsequence recall |
| **METEOR** | Lexical | Stem- and synonym-aware recall via WordNet alignment |
| **BERTScore Precision** | Semantic | Per candidate token: max cosine sim to any reference token |
| **BERTScore Recall** | Semantic | Per reference token: max cosine sim to any candidate token |
| **BERTScore F1** | Semantic | Harmonic mean of BERTScore P and R |
| **SBERT Similarity** | Semantic | Global document cosine similarity via pooled embeddings |

**Model:** [`answerdotai/ModernBERT-base`](https://huggingface.co/answerdotai/ModernBERT-base) — alternating global-local attention + RoPE, 8,192-token native context window. BERTScore is implemented directly via `AutoModel` (the `bert_score` library does not support ModernBERT's architecture). All documents are well within the 8,192-token limit — no truncation occurs.

---

## Results Summary

### Overall (117 documents)

| Metric | Mean | Median | Std | Min | Max |
|---|---|---|---|---|---|
| BLEU | 0.1306 | 0.1259 | 0.0499 | 0.0002 | 0.2463 |
| ROUGE-1 | 0.4815 | 0.4848 | 0.1015 | 0.0456 | 0.6446 |
| ROUGE-2 | 0.2799 | 0.2657 | 0.0824 | 0.0114 | 0.4549 |
| ROUGE-L | 0.3693 | 0.3564 | 0.0952 | 0.0388 | 0.5656 |
| METEOR | 0.3833 | 0.3860 | 0.0732 | 0.0588 | 0.5142 |
| BERTScore Precision | 0.8885 | 0.8907 | 0.0206 | 0.7298 | 0.9219 |
| BERTScore Recall | 0.9116 | 0.9179 | 0.0259 | 0.7197 | 0.9355 |
| BERTScore F1 | 0.8998 | 0.9038 | 0.0213 | 0.7247 | 0.9219 |
| SBERT Similarity | 0.9856 | 0.9882 | 0.0144 | 0.8534 | 0.9936 |

### Per-mode mean scores

| Metric | ask | form | chat |
|---|---|---|---|
| BLEU | 0.1267 | 0.1248 | **0.1398** |
| ROUGE-1 | 0.4675 | 0.4771 | **0.4989** |
| ROUGE-2 | 0.2577 | **0.2971** | 0.2843 |
| ROUGE-L | 0.3484 | **0.3782** | 0.3805 |
| METEOR | 0.3654 | **0.4012** | 0.3827 |
| BERTScore Precision | 0.8860 | 0.8882 | **0.8913** |
| BERTScore Recall | 0.9082 | **0.9184** | 0.9082 |
| BERTScore F1 | 0.8968 | **0.9029** | 0.8996 |
| SBERT Similarity | **0.9860** | 0.9848 | 0.9861 |

---

## Project Structure

```
ropagen-bert/
├── docs/
│   ├── reference.txt          # Human-written reference ROPA document
│   └── documents.csv          # 117 AI-generated documents (id, user_id, ai_mode, document)
├── metrics_output/
│   ├── evaluation_results.csv # Full per-document scores (all 9 metrics)
│   ├── summary_overall.csv    # describe() + extreme IDs — all modes combined
│   ├── summary_ask.csv        # describe() + extreme IDs — ask mode
│   ├── summary_form.csv       # describe() + extreme IDs — form mode
│   ├── summary_chat.csv       # describe() + extreme IDs — chat mode
│   └── *_boxplot.png          # One boxplot per metric (9 total)
├── ROPAgen_DOCUMENT.ipynb     # Main evaluation notebook
├── .env                       # HF_TOKEN (not committed)
├── .gitignore
└── README.md
```

---

## Setup

### Requirements

```bash
pip install torch transformers sentence-transformers evaluate
pip install pandas numpy matplotlib tqdm
pip install python-dotenv
# NLTK data (downloaded automatically on first run)
```

### HuggingFace Token

Create a `.env` file in the project root:

```
HF_TOKEN=your_token_here
```

This is used for authenticated model downloads from HuggingFace Hub.

### Running

Open `ROPAgen_DOCUMENT.ipynb` and run all cells in order. On first run, `answerdotai/ModernBERT-base` (~150MB) will be downloaded and cached by HuggingFace. Subsequent runs use the local cache.

**Hardware:** Tested on RTX 4070 (12.9 GB VRAM). Batch size is set conservatively (`BERT_BATCH_SIZE = 4`) to avoid OOM on 2,000-token documents. CPU fallback is supported but will be significantly slower.

---

## Notebook Structure

| Cell | Description |
|---|---|
| 1 | Imports, `.env` loading, configuration |
| 2 | Load `reference.txt` and `documents.csv`; split by mode |
| 3 | Metric definitions (markdown) |
| 4 | Load `evaluate` metrics (BLEU, ROUGE, METEOR); define `compute_baseline_metrics` |
| 5 | Load ModernBERT via `AutoModel`; define `compute_bertscore` (P/R/F1) |
| 6 | Load ModernBERT via `SentenceTransformer`; define `compute_sbert_similarity` |
| 7 | Run all metrics per mode; assemble result DataFrames |
| 8 | Combine modes; display & save summary statistics and extreme document IDs |
| 9 | Visualisation description (markdown) |
| 10 | Generate and save one boxplot per metric (9 figures) |
