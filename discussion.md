# Discussion — Working Notes

Scratchpad for the Discussion chapter. Numbers, candidates, structure, open
questions. Not prose yet — we'll write the chapter from this.

---

## Cross-chapter TODOs (touch other chapters, not just Discussion)

These are things that need to be added elsewhere in the thesis but are
load-bearing for the Discussion's framing. Capturing them here so we don't
lose them.

### 2. Add the original hypothesis: Chat > Form > Ask
- **Where it belongs**: Introduction, immediately after the RQs.
  Framed as the prediction the study set out to test.
- **Wording sketch** (to be polished):
  > Going into the study, the implicit prediction was that more LLM
  > support would translate into a better user experience and a more
  > preferred mode: the ordering Chat $\succ$ Form $\succ$ Ask was
  > anticipated, with Chat — the freeform conversational mode where the
  > LLM does the most work — expected to be the overall favourite. The
  > evaluation that follows tests this prediction against the
  > experience and outputs of $73$ novice users.
- **Pay-off in Discussion**: the chapter-level finding (Form 53.6 % of
  rank-1 votes; $\chi^2 = 14.17$, $p < 0.001$, $V = 0.32$) is the
  opposite of the prediction. Opening sentence of the Discussion can
  lean on this:
  > Contrary to the prior expectation that increasing LLM involvement
  > would produce a correspondingly more preferred and more confident
  > experience, the study found the opposite ordering on preference and
  > a *miscalibrated* ordering on confidence. The remainder of this
  > chapter interprets that double reversal.
- Why this matters: makes the Form paradox land as a *finding*, not a
  description. A reversed prediction has more rhetorical force than an
  unframed result.

---

## Argumentative spine (one paragraph)

The Evaluation chapter delivered two findings the Discussion has to interpret
together. **First**: the mode users prefer (Form) is *also* the mode that
hallucinates most — Form's checkbox UI guarantees every Article-30 field gets
populated, but does not constrain what the LLM invents during the final
generation step. **Second**: self-report confidence in the AI's legal-basis
identification rises monotonically Form → Ask → Chat, while measured document
quality refuses to follow any single ordering — Form leads Recall, Chat leads
SBERT and Faithfulness, judge Overall barely separates. Confidence tracks
*degree of AI involvement*, not output quality. The two findings combine into
a single story about novices using LLM assistance for high-stakes documents:
**scaffolding the input does not scaffold the output, and the user has no
internal signal that anything is wrong.**

---

## Lead claim

Both tensions are sides of the same coin: **novices can't see what's wrong
with an LLM-generated compliance document, and the system doesn't tell them.**

The Form paradox is the *what* (checkbox UI lets fabrications through).
The confidence gap is the *why it matters* (users won't catch it).

Pitch the chapter as twin findings rather than choosing one as primary.

---

## Section-by-section outline

### 1. Opening (1 paragraph)
- Recap the two tensions in 3 sentences.
- Name what the chapter does: interpret them, link to related work, name
  limitations, draw out design implications inline.

### 2. Why participants prefer Form
- The behavioural backbone: Form is *measurably* about 7 minutes per
  document faster than either LLM-driven mode (median 420s vs 858s Ask /
  717s Chat; $H = 16.46$, $p < 0.001$, $\varepsilon^2 = 0.15$ large).
- The perceptual backbone: SUS composite Form 78.62 vs Ask 72.97 / Chat
  72.93; cumbersomeness ratings clearest single SUS gap (Form 1.65 vs Chat
  2.29).
- The qualitative backbone: free-text comments cluster on speed, visible
  option space, "takes the most work off you".
- Frame this human-side first: people prefer the mode that respects their
  time and shows them the whole task. The LLM modes win on perceived AI
  value (transparency, trust) but lose on the things people optimise for in
  practice.

### 3. The completeness–hallucination tradeoff
- The headline number: 83.8 % of Form documents combine maximum
  Completeness ($5/5$) with moderate-or-worse Hallucination
  (inverse score $\leq 2$); 17 of 37 combine max Completeness with the
  floor hallucination score of 1.
- Why: the checkbox UI guarantees *that* a field is populated, not *that*
  the value is true to the scenario. The Boolean flag for "AWS" gets ticked;
  the final-generation prompt then writes prose around "AWS" even though
  the scenario explicitly says "no external cloud."
- Chat inverts: weaker scaffold, but the user's own free-text description
  anchors the output to the scenario (Faithfulness Chat 2.49 vs Form 1.84;
  Hallucination-inverse Chat 2.54 vs Form 1.65).
- This is where to drop the central claim:
  > **Scaffolding *completeness* is not the same as scaffolding *truth*.**
- Design implication (inline): scaffolds that constrain *what the form
  contains* must be paired with scaffolds that constrain *what the
  generation step writes*.

### 4. The confidence–quality gap (RQ2.3) — with case study
- Setup: confidence rises monotonically Form 3.58 → Ask 3.74 → Chat 3.81.
  Measured quality refuses to follow.
- Spearman correlations between confidence item 5_ai and judge Overall:
  Form $\rho = +0.07$ ns, Ask $-0.21$ ns, Chat $+0.41$ ($p = 0.012$),
  pooled $+0.14$ ns. Calibration is only visible in Chat — and is
  *negative* in Ask.
- **Case study A — AEB2451** (see §6 below for full numbers): a
  reflective participant who wrote thoughtful per-mode commentary and
  even diagnosed Chat's failure mode ("here it simply took over what's
  in the scenario without any evaluation attempt as to whether it's
  legally compliant") — yet rated their legal-basis confidence in that
  same Chat mode at **5/5**, and at **4/5** in Form and Ask whose
  documents the judge rated 2/5 Overall (severely hallucinated:
  biometric data, health data, video surveillance, AES-256, 6–10 year
  retention — none in the scenario). They ranked Form first overall,
  mirroring the chapter aggregate. The case shows that *engagement is
  not the same as calibration*: a novice can diagnose UX problems and
  even spot specific LLM behaviors, yet still fail to detect
  scenario-level quality issues.
- **Case study B — IAR1116** (calibrated counter-case): legal-basis
  confidence Chat = 5/5, judge Overall on the same Chat document = 5/5.
  Calibration is *possible*, but it's the exception.
- Take-away: novice confidence in LLM-assisted compliance work tracks
  *degree of AI involvement* much more reliably than it tracks
  document quality. In a compliance setting that is a calibration
  failure with real consequences.

### 5. Why Ask trails on everything
- Quantitative backbone: lowest on every NLP metric that reaches
  significance; lowest on judge Completeness after Chat; SUS composite
  72.97; second-highest Frustration (7.58, the highest of any
  subscale-mode cell after Chat Performance).
- Qualitative backbone: the copy-paste step. Free-text comments
  repeatedly cite the manual copy of the AI's free-text suggestion into
  the structured form field as the principal source of friction. The mode
  combines the cognitive cost of Form (you still fill every field) with
  the wait time of Chat (you wait for the LLM to explain).
- Implication: this is a *workflow* failure, not an LLM-capability
  failure. The explanatory text Ask produces is judged most informative
  of the three modes (Transparency 4.16 vs Form 3.51 / Chat 3.75).
- A "hybrid mode" — visible option set of Form, contextual explanation
  of Ask, no manual copy step — is the obvious next design.

### 6. Case studies — full data

#### Case study A: AEB2451 — the engaged but miscalibrated participant

A 51-minute session (`duration = 3088s`); ranked **Form** first, **Chat**
second, **Ask** third — matching the chapter-level ranking
($\chi^2 = 14.17$, $V = 0.32$).

| Mode | Order | NLP BERT-F1 | NLP SBERT | Judge Completeness | Judge Faithfulness | Judge Hallucination (inv.) | Judge Legal | Judge Overall |
|---|---|---|---|---|---|---|---|---|
| Form | 1st presented | 0.908 | 0.988 | 5 | 1 | 1 | 3 | **2** |
| Ask  | 2nd presented | 0.893 | 0.983 | 5 | 2 | 2 | 4 | **2** |
| Chat | 3rd presented | 0.911 | 0.992 | 5 | 3 | 3 | 5 | **4** |

Per-mode AI questionnaire (items 1–6: helpful / efficient / transparent / trust / **confidence** / reuse):

| Mode | Helpful | Efficient | Transparent | Trust | **Confidence (5_ai)** | Reuse |
|---|---|---|---|---|---|---|
| Form | 5 | 5 | 5 | 5 | **4** | 5 |
| Ask  | 5 | 2 | 4 | 3 | **4** | 5 |
| Chat | 5 | 4 | 5 | 5 | **5** | 5 |

**Per-mode free-text and final summary (verbatim DE + EN gloss):**

*Form — no per-mode comment.*

*Ask (DE):* "Es wäre viel angenehmer, wenn man dem KI-Modell einmal am
Anfang den Kontext geben kann und dann den Chat zu den jeweiligen Felder
verwenden kann. So musste bei jedem Feld der Kontext neu gegeben werden,
was man sich sparen kann. Ich weiß nicht ob es gewollt ist, aber in dem
Modus ist nur Freitext als Eingabe möglich. Mit den Kästchen von davor
war das deutlich angenehmer und vor allem schneller. Erklärungen sind
natürlich viel besser als bei den KI-Vorschlägen"

*Ask (EN gloss):* It would be much nicer to give the AI model the
context once at the start and then use the chat for each individual
field. As it is, the context had to be given again for every field,
which is wasted work. I don't know if it's intentional, but in this mode
only free-text input is possible. The checkboxes from before were much
nicer and especially faster. The explanations are of course much better
than the AI suggestions.

*Chat (DE):* "Es hat zwei Generierungen des Dokuments gebraucht, um die
Rechtsgrundlagen einzutragen, obwohl es am Ende des Chats beim ersten
Mal hieß: Ich habe die Verarbeitungsgrundlagen entsprechend
aktualisiert. Bei den Aufbewahrungsfristen wurden im Modus davor mehr
Vorschläge gemacht. **Hier wurde einfach übernommen, was im Szenario
steht ohne Hinweis bzw. Bewertungsversuch, ob das gesetzeskonform ist.**"

*Chat (EN gloss):* It took two document generations to enter the legal
bases, even though at the end of the chat the first time it said: "I
have updated the processing bases accordingly." For the retention
periods, more suggestions were made in the previous mode. **Here, it
simply took over what was in the scenario without any indication or
evaluation attempt as to whether it is legally compliant.**

*Summary (DE):* "Bei Chat und Ask wäre es wie erwähnt angenehmer das
Szenario einmal am Anfang als Kontext zu geben. Form ist deutlich
übersichtlicher, da man schnell überblicken kann was ausgewählt wurde.
Bei Ask musste zusätzlich teilweise nach einer Formulierung gefragt
werden, die dann in das Freitextfeld kopiert werden kann, was es am
umständlichsten macht — Chat hat selbst ergänzt. Am besten fände ich
eine Mischung aus Form und Ask/Chat für bessere Explainability."

*Summary (EN gloss):* For Chat and Ask, it would be nicer to give the
scenario as context once at the start, as mentioned. Form is much
clearer because you can quickly see what was selected. With Ask you
sometimes also had to ask for a formulation that you could then copy
into the free-text field, which makes it the most cumbersome — Chat
filled it in itself. I would most like a mix of Form and Ask/Chat for
better explainability.

**The story:**

- **Form** (presented first). Document scored 5/5 Completeness — every
  Article-30 field populated — but 1/5 Faithfulness and 1/5
  Hallucination-inverse. Judge: *"The text invents a massive amount of
  unsupported information, including financial data, biometric data,
  video surveillance, external recipients like banks and authorities,
  and specific technical standards like AES-256 and SIEM. The document
  explicitly contradicts the scenario's constraints by including
  sickness/health data and defining retention periods of 6 to 10 years
  instead of the specified maximum of 3 months."* The participant rated
  their legal-basis confidence on this document **4/5**. They did not
  write a per-mode comment for Form — Form's UX did not generate
  feedback-worthy friction.

- **Ask** (presented second). Document scored 5/5 Completeness but
  2/5 Faithfulness, 2/5 Hallucination-inverse, 4/5 Legal Correctness.
  Judge: *"Although structurally complete and legally plausible for a
  generic company, the document fails to accurately reflect the
  specific, constrained scenario."* The hallucinations are different
  but the pattern is the same: tax advisors, IT service providers, cloud
  systems, 10-year retention — none in the APOR scenario. Confidence
  again **4/5**. The free-text complains about workflow (copy-paste,
  no persistent context) and praises the *explanations* — but says
  nothing about the document being wrong. The participant noticed the
  UX problem, not the quality problem.

- **Chat** (presented third). Document scored best of the three —
  Completeness 5/5, Faithfulness 3/5, Hallucination-inverse 3/5, Legal
  Correctness 5/5, Overall 4/5. Confidence **5/5** (max). And in the
  *same* per-mode comment in which they rated maximum confidence in
  the AI's legal-basis identification, the participant wrote: *"Here
  it simply took over what's in the scenario without any evaluation
  attempt as to whether it's legally compliant."* They diagnosed the
  exact failure mode — the LLM doesn't evaluate its own legal output —
  and rated their confidence in that LLM's legal output at the ceiling
  anyway. This is the confidence-quality gap captured in a single
  participant in their own words.

- **The ranking pay-off**: they put **Form** first — the mode whose
  document was 1/5 on Faithfulness and 1/5 on Hallucination, full of
  invented biometric, financial, and health data. The mode whose
  document the judge called *"highly inaccurate for this specific
  processing activity."*

- **Lead-in sentence for the chapter draft**: *"As previously
  discussed, this participant mirrors the chapter-level finding in
  microcosm: their confidence in the AI's legal-basis identification
  rises monotonically Form → Ask → Chat ($4 \to 4 \to 5$), even as the
  document they produced under their most-confident mode was the only
  one not heavily hallucinated. The mode they ranked first — Form —
  produced the document the judge rated lowest on faithfulness."*

#### Case study B: IAR1116 — the calibrated counter-case

| Mode | Order | NLP BERT-F1 | NLP SBERT | Judge Completeness | Judge Faithfulness | Judge Hallucination (inv.) | Judge Legal | Judge Overall |
|---|---|---|---|---|---|---|---|---|
| Ask  | 1st presented | 0.898 | 0.985 | 5 | 3 | 2 | 5 | **3** |
| Form | 2nd presented | 0.907 | 0.985 | 5 | 2 | 2 | 4 | **3** |
| Chat | 3rd presented | 0.909 | 0.990 | 5 | 5 | 4 | 5 | **5** |

Per-mode AI questionnaire (items 1–6):

| Mode | Helpful | Efficient | Transparent | Trust | **Confidence (5_ai)** | Reuse |
|---|---|---|---|---|---|---|
| Ask  | 5 | 2 | 5 | 3 | **3** | 5 |
| Form | 5 | 5 | 4 | 3 | **4** | 5 |
| Chat | 5 | 5 | 5 | 5 | **5** | 5 |

Mode ranking: **Ask**, Chat, Form.

A 45-minute session (`duration = 2721s`). Only a final summary was
written — no per-mode comments. The summary discusses both Chat and
Ask in some detail.

*Summary, Chat portion (DE):* "Chat verbindet die KI mit der direkten
Einarbeitung in das Dokument. Es gibt zwar keine Option, die
Informationen direkt selbst anzugeben, doch es schadet vermutlich nie,
wenn die KI kurz drüber schaut, auch wenn man sich eigentlich sicher
ist, dass alles vorhanden ist."

*Summary, Chat portion (EN gloss):* Chat connects the AI directly to
the work on the document. There is admittedly no option to enter the
information directly yourself, but it presumably never hurts when the
AI takes a quick look, even when you are basically sure that everything
is there.

*Summary, Ask portion (DE):* "Ask war von den drei Versionen deutlich
am umständlichsten. Entweder man sucht die Informationen erst selbst
heraus (dann wäre die KI unnötig) oder man kopiert die Informationen
der KI, jedoch habe ich da nicht verstanden, dass bei der Erstellung
erneut eine KI drüber arbeitet und alles von der KI versucht in die
kleinen Inputs umzuformatieren."

*Summary, Ask portion (EN gloss):* Ask was by far the most cumbersome
of the three versions. Either you look up the information yourself
first (in which case the AI would be unnecessary) or you copy the
AI's information — but I didn't understand there that during the
generation another AI works on top of it and tries to reformat
everything from the AI into the small inputs.

The story:
- Ask first: confidence 3/5 (the participant knew they were uncertain).
  Document scored 3/5. **Perfectly calibrated.**
- Form second: confidence rose to 4/5. Document scored 3/5. Slight
  over-confidence.
- Chat third: confidence and every AI item maxed out (all 5/5). Document
  scored 5/5 — the only 5/5 Chat document in this triangulation.
- Calibration is *possible* for novices. IAR1116 is the existence proof.
  But notice: they still ranked **Ask first overall**, despite Chat being
  measurably their best mode. **Calibration of quality and preference for a
  mode are not the same thing** — the same person can know a mode produced
  the best document and still prefer not to use it.
- The free-text on Ask confirms the chapter-wide finding about copy-paste
  friction; the free-text on Chat captures the trust-the-AI rationale that
  drives Chat's higher confidence ratings in the aggregate.

### 7. Comparison to related work
- **Su et al.\ (JuDGE)**: dual evaluation template confirmed. Lexical
  metrics alone underdescribe what's happening; the judge layer is what
  reveals the Form completeness–hallucination paradox.
- **von Schwerin et al.\ (2024)**: their open-source / Qwen finding that
  ROPA data categories can be generated locally to GPT-4 quality validates
  ROPAgen's architectural choice (Mistral); this thesis extends from
  category-level extraction to whole-document drafting with novice users
  in the loop.
- **Abualhaija et al.\ (2025)**: their finding that high BERTScore can
  coexist with low BLEU when the model paraphrases rather than copies —
  see this thesis's BERTScore F1 ~0.90 paired with BLEU ~0.13. Confirms
  that what BERTScore measures is semantic alignment, not factual
  correctness — which is exactly why we needed the judge layer.
- **Surya, Vayadande et al.**: their accessibility framing for legal AI is
  the right gap to target, but neither did a controlled user study. This
  thesis fills that gap by measuring what novice users actually do, what
  they trust, and what they produce.
- **Nigam et al.\ (MAW), Lin & Cheng, Li et al.\ (CaseGen)**: architecture
  varies across these (wrapper, fine-tune, multi-stage). ROPAgen fixes the
  architecture and varies *interaction modality* instead. The finding that
  modality has measurable effects on output quality (Form leads Recall,
  Chat leads SBERT and Faithfulness) is the contribution from holding the
  underlying pipeline constant.

### 8. Limitations
- **Single scenario** (APOR GmbH). All findings are conditional on it.
  Templated chapters (Controller, T\&O Measures) saturate the metrics;
  free-form chapters (Purposes, Legal Bases) collapse them. A different
  scenario could redistribute these effects.
- **Novice-only sample**. Most studies of legal-AI tooling evaluate with
  expert raters or expert users. Whether the patterns observed here hold
  for trained DPOs is open.
- **Single reference document** for the NLP metrics, authored in Form
  mode. The methodology chapter already flags this as a framing effect:
  reference-based metrics inevitably advantage Form-style outputs on
  recall measures. The Form recall lead may be partially metric artifact;
  the Form completeness–hallucination tradeoff is **not**, because the
  judge is reference-free.
- **Single-pass single-model judge.** No inter-rater replication, no
  legal-expert validation. Judge scores are indicative, not definitive.
- **Self-report confidence on a single Likert item.** "I am confident
  that the AI identified the correct legal basis" is one question among
  six and only one dimension of calibration. A richer confidence
  instrument might surface other patterns.
- **Sample is IT-leaning Bachelor students from one university.**
  Demographics chapter already flagged this.

### 9. Closing paragraph
- Recap: scaffolding completeness ≠ scaffolding truth. Confidence ≠
  calibration.
- The design lesson: input scaffolding is a strong UX win (Form was
  preferred 53.6 % of the time) but it does not constrain hallucination.
  Future LLM-assisted compliance tools need *output* scaffolding too —
  reference-document grounding, fact-extraction against the user's
  description, hallucination detection at the generation step.
- The methodological lesson: dual-evaluation (NLP metrics + LLM-judge +
  user study) revealed effects no single layer could have. Single-layer
  evaluations would have missed the Form paradox entirely.

---

## Threads to weave in

- The **chi-square ranking result** ($\chi^2 = 14.17$, $V = 0.32$): 53.6 %
  picked Form first. This is statistically significant against chance and
  is the strongest single user-preference signal in the data.
- The **monotonic confidence ordering** Form → Ask → Chat: this is what
  makes the calibration finding clean. If confidence didn't change with
  mode, the calibration question would be moot.
- The **chapter-level patterns**: *Retention and Deletion* and *Technical
  and Organisational Measures* are where Chat's chapter-level lead is
  largest. These are the most free-text-heavy chapters. The structural
  finding has a within-document signature.
- The **completion-time finding** (Form 7 minutes faster): worth mentioning
  in §2 to ground "Form is preferred" in something measurable.

---

## Open questions for us to decide

1. **Do we include both case studies, or just PVV2109?** PVV2109 alone is
   stronger as the central confidence-gap exemplar. IAR1116 risks reading
   as "but also some people get it right" and diluting the main claim.
   Recommendation: keep both, but PVV2109 is the headliner. IAR1116 is the
   ~5-line counter-case at the end of §4.

2. **Where do the case studies live structurally?** Inside §4 as
   subsections, or as their own §6 (as currently sketched)? Either works.
   Inline is more readable, but standalone §6 keeps §4 short and
   argumentative.

3. **How much numerical detail in the case studies?** The tables above are
   thesis-ready; we could also use prose only and put the tables in an
   appendix. Recommendation: keep the per-mode table in the chapter — it's
   the most efficient way to show the discrepancy at a glance.

4. **Length of the chapter?** Estimate based on this outline:
   ~8–10 pages: tight opening, 3–4 finding sections, two case studies (one
   substantial, one short), related work, limitations, close.
   This is ~the right size for the Evaluation chapter's weight (~40 pages
   of results need 8–10 pages of discussion, not 4 and not 15).

5. **Design implications: inline or as a §7?** Recommendation: inline.
   Each finding section ends with one sentence that names the design
   implication. Conclusion picks them up as a list.

6. **Do we want to draft a hybrid-mode sketch?** Several free-text comments
   suggested a Form-structure + Chat-context hybrid. Worth a paragraph in
   §5, or possibly a short standalone subsection. Pragmatically useful for
   future work even if it's not "in" the empirical contribution.

---

## To-do for the chapter draft

- [ ] Decide on case-study placement (inline vs §6)
- [ ] Decide on the order: confidence-gap-first vs Form-paradox-first
- [ ] Pull the per-chapter NLP boxplot numbers we want for §3 (Retention /
      T\&O lead)
- [ ] Check whether to cite the chapter-level Friedman/Mann-Whitney
      results explicitly or just appeal to the descriptive direction
- [ ] Run the German free-text translations through one more pass for
      quality — the IAR1116 quote in §6 is currently raw German
