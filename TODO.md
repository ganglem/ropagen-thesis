## P0 — Content gaps (must close before defence)

### ROPAgen appendix (Appendix D)

- [ ] **Three mode screenshots.** Form/Ask/Chat UI captures on the same
      scenario step for visual comparability. Section frames and labels
      already exist in `appendix_ropagen.tex` (\S~D.2.1/2/3); only the
      PNGs themselves are missing. Emilija is supplying these.

### Discussion (currently a stub — extensive prep in `discussion.md`)

**Themes to cover (rough order):**

- **Why Form won thle user-study ranking, Chat second, Ask third.**
  
  \textbf{Form (1st).} Control + speed. SUS leads on the
  feel-of-using items (ease, complexity, integration,
  learnability, cumbersomeness); R-TLX lowest on every workload
  dimension except Performance; completion time about half the
  wall-clock of either LLM mode (median 7 min vs 12--14 min).
  Free-text quote: \emph{``nimmt dir am meisten Arbeit ab''}
  (thg1620).
  
  \textbf{Chat (2nd).} Subjective safety, not measurable
  quality. Comments cite \emph{``die KI macht das''} /
  \emph{``AI takes care of it''} as the reason for placing Chat
  second. Item 5 (legal-basis confidence) peaks at Chat
  ($3.81$) -- but item 6 (reuse intent) falls to last ($3.42$):
  they trust the AI's output in the moment but wouldn't want
  to come back to it. Save the deeper confidence-vs-quality
  framing for the next subsection (Point 2); here just note
  Chat won second because participants felt safe with it.
  
  \textbf{Ask (3rd).} Workflow friction sharpened by an
  architectural finding. Comments converge on copy-paste between
  the LLM chat panel and the section text field, plus the lack
  of persistent context across sections. The architectural
  reason (Point 4 of this Discussion plan) is the cleaner
  framing: Ask is the only mode where the AI does no
  labour-saving on the structured side, so the friction
  participants feel maps onto a real mechanism rather than just
  a UI complaint.
  
  \textbf{Quotes budget.} Two or three strategic German verbatim
  quotes in this point at most, one per mode. The hybrid-mode
  suggestion from the comments is deferred to Point 5
  (implications for tooling).

- **The confidence-vs-correctness gap (central argument).**
  Self-report confidence rises monotonically Form $\to$ Ask $\to$
  Chat on item 5 (legal-basis confidence): $3.58 \to 3.74 \to 3.81$.
  Measured document quality follows no such single ordering — Form
  leads recall, Chat leads precision and scenario fidelity, the
  judge declares no winner. Single strongest illustrative number:
  $83.8\,\%$ of Form documents combine maximum Completeness with
  ``moderate'' or worse Hallucination, and nearly half pair maximum
  Completeness with the floor Hallucination score. The checkbox
  scaffolding pushes Form documents to coverage completeness but
  doesn't constrain what the LLM invents during the final
  generation step.

- **BERT / SBERT picture and the Precision/Recall trade-off.**
  Form's Recall edge (BERTScore Recall Form-vs-Ask $r = 0.756$,
  Form-vs-Chat $r = 0.512$) is the largest single effect in the
  chapter. Chat's Precision and SBERT edge: stays on topic, less
  extraneous material. Implication: Form casts a wider net (higher
  recall, more fabrication risk); Chat tighter focus (higher
  precision, less coverage). At chapter level the trade-off
  redistributes by chapter (Form sweeps Ch 2--4, Chat sweeps Ch
  5--6).

- **Why Ask underperformed specifically.**
  The free-text comments converge on workflow: per-section
  copy-paste is the principal source of friction; the lack of
  persistent context across fields forces re-entry of the same
  information. Several participants suggest a hybrid mode
  (Form structure + Ask/Chat conversation) — this is the closest
  thing to a design recommendation the data supports.
  
  \textbf{Architectural note (verified against the ropagen
  source).} Ask mode's LLM is an \emph{explainer only}: the
  system prompt does not request any \texttt{DATA\_UPDATE} block
  and the front-end has no handler that would apply one. The user
  writes the free-text \texttt{other} field for each section
  themselves; the predefined boolean flags are untouched in Ask.
  This sharpens the three-way comparison:
  \begin{itemize}
    \item Form: user clicks the booleans directly; LLM only fires on the optional ``AI Suggest'' button.
    \item Ask: user types the free-text field themselves; LLM explains but populates nothing.
    \item Chat: LLM extracts structured data and flips booleans via \texttt{DATA\_UPDATE}; user never sees the schema.
  \end{itemize}
  Ask is therefore the only mode where the AI offers \emph{no}
  labour-saving on the structured side. This matches the
  free-text complaints (``copy-paste'', ``redundant'') and is a
  cleaner explanation for Ask's third-place ranking than just
  ``copy-paste friction''.

- **Implications for ROPA tooling.**
  The hybrid suggestion from comments is supported by the data,
  not just by user preference: Form leads on structural completeness,
  Chat leads on scenario fidelity. A hybrid would in principle
  capture both. Generation-step hallucination is independent of
  interface mode and would need a separate guardrail.

- **Limitations.**
  Single standardized scenario; novice-only sample (university
  students, no professional GDPR background); single Form-mode
  reference document for NLP scoring (introduces a Form-style
  framing effect on the metrics); single-pass single-model LLM
  judge (Gemini 3.1 Pro Preview, $T = 0$), no inter-rater, no
  legal-expert validation; German-primary corpus with English
  glosses; chapter-level MiniLM SBERT pass is a robustness check
  rather than a primary measure.

**Case study (expanded scope):**

Two participants already identified:
- **AEB2451** and **IAR1116** (one good match, one bad match with high
  self-reported confidence). Confirm which is which when extracting the
  raw data.

The case study triangulates three independent signals for each
participant:

1. **User-study side** — SUS composite + per-item ratings, R-TLX
   composite + per-subscale, AI Support per-item, mode preference
   ranking, free-text comments. Goal: the participant's own report
   of what they experienced and how confident they felt.
2. **NLP metric side** — every metric, not just BERTScore: BLEU,
   ROUGE-1/2/L, METEOR, BERTScore P/R/F1, SBERT (ModernBERT, plus
   MiniLM at chapter level). For each metric, pick a representative
   passage from the participant's document and the matching
   reference passage, place them side-by-side, and quote the
   computed metric value so the number-to-text mapping is concrete.
3. **LLM-as-Judge side** — all five metrics (Completeness, Scenario
   Faithfulness, Legal Correctness, Hallucination, Overall).

The triangulation shows where the three signals agree (a ``good''
document where the participant felt confident, the NLP metrics scored
high, and the judge rated highly) and where they disagree (a ``bad''
document where the participant felt confident but the NLP metrics
were mediocre and the judge flagged faithfulness or hallucination
problems).

**Placement:**

- Full case study lives in Discussion as its own subsection. This
  is where the cross-signal synthesis belongs.
- One or two short illustrative passages may be quoted inline in
  the Eval chapter at strategic points (e.g., the BERTScore Recall
  paragraph or the judge Hallucination paragraph) as
  ``what does this number look like'' anchors. Keep these short
  enough that the Eval chapter stays number-driven.
- Each illustrative excerpt should compute the relevant metric value
  for the specific passage shown, so the reader can see the
  number-to-text mapping at the relevant point in the argument.

### Conclusion

- Plain-English answers to RQ1 and RQ2.
- Bring back the human-side framing: the thesis is about people using
  AI to make legal documents.
- Avoid restating Evaluation statistics; reserve statistical detail
  for Eval, the answer goes here.


