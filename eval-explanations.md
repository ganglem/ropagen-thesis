# Eval-chapter within-metric explanations (planning)

Goal: add explanations for the observed patterns to each section of the
evaluation chapter, but keep each explanation grounded in evidence *internal
to that section's instrument or metric*. No cross-referencing (e.g., don't
explain SUS results via NLP scores; don't explain Chat's Faithfulness via
participants' SUS confidence). User study can cross within itself
(SUS / R-TLX / AI / freeform / ranking); NLP can cross within itself
(doc-level / chapter-level); Judge stays within Judge.

Status legend: `[STRONG]` = clearly supported by the section's own data;
`[MODERATE]` = defensible but inferential; `[FLAG]` = speculative, push to
Discussion instead.

---

## 1. Demographics

Nothing to explain — the section is sample description, not results.

## 2. SUS

- **Form leads on the moment-to-moment-feel items, modes flatten on the
  user-state items.** `[STRONG]`
  Items 1, 3, 5, 7 (positive: intent-to-reuse, ease, integration,
  learnability) and 2, 8 (negative: complexity, cumbersomeness) all
  measure something about *interacting with the system right now*. Items
  4, 6, 9, 10 (positive: confidence; negative: technical-support need,
  inconsistency, prior learning needed) measure something about the
  *user's relationship with the system over time* — these flatten
  because they're not affected by which mode the participant just used.
  This explains the cluster pattern within SUS.

- **Item 8 (cumbersomeness) has the largest spread of any SUS item.**
  `[STRONG]`
  Cumbersomeness is the SUS item most directly tied to interaction
  friction; the LLM-driven modes introduce extra interaction steps (chat
  panel, conversation turns) that the cumbersomeness item picks up
  cleanly.

## 3. R-TLX

- **Form is lightest on every dimension except Performance, with
  Temporal Demand and Frustration firing strongest.** `[STRONG within
  R-TLX, can use completion time as it's the supplementary part of this
  section]`
  Form's completion time (median 7 min) is about half the LLM-driven
  modes' (12--14 min); the Temporal Demand subscale measures perceived
  time pressure and tracks the actual time-on-task directly. Frustration
  fires because the LLM-driven modes introduce wait states (conversation
  turns, copy-paste) that Form does not.

- **Performance flattens.** `[MODERATE]`
  Performance asks how successful the participant felt at the task.
  Without ground-truth feedback during the task, novices have no anchor
  for "I succeeded" / "I failed", so the rating defaults to a similar
  mid-range across modes.

## 4. Perceived AI Support (AI questionnaire)

- **Transparency (item 3) leads in Ask by the widest margin of any
  item.** `[STRONG]`
  Ask is the only mode where the LLM's job is explicitly to explain the
  section to the user. Form's LLM only fires on demand; Chat's LLM
  silently extracts. So Ask is structurally the most-explained mode, and
  item 3 (transparency) picks this up directly.

- **The split between content-judgment items (3, 4, 5) and
  productivity items (2, 6).** `[STRONG]`
  Items 3, 4, 5 ask how well the AI did its content work
  (transparency, trust, legal-basis confidence); items 2, 6 ask how
  much the AI helped the *participant* finish the document.
  Participants credit the LLM-driven modes for content judgment they
  cannot themselves assess, and credit Form for productivity they can
  measure on the clock.

- **Item 5 (legal-basis confidence) peaks in Chat; item 6 (reuse intent)
  bottoms out in Chat.** `[MODERATE]`
  Confidence is a snapshot of the moment; reuse intent is a forward-looking
  preference. Participants felt safe with Chat *during* the session but
  weren't sure enough to return to it — within AI Support alone, this is
  the cleanest signal that confidence and preference can decouple.

## 5. Mode Preference and Free-Text Feedback (Freeform)

- **Form first because of the user-typed reasons.** `[STRONG, grounded in
  the comments themselves]`
  Speed, control, "takes the most work off" --- these are the recurring
  themes in the comments, and they explain the rank-1 vote concentration.

- **Chat second because of subjective safety, not measurable confidence.**
  `[STRONG, grounded in the overall comments]`
  Several participants explicitly say "the AI takes care of it" /
  "die KI macht das" / similar. The reuse-intent item already showed
  participants wouldn't actually come back to Chat — the second-place
  ranking captures a one-session impression, not a durable preference.

- **Ask third because of the copy-paste workflow.** `[STRONG, grounded
  in the comments + the architectural fact that the AI does not
  populate any field in Ask mode]`
  Multiple participants name this explicitly. The architectural fact
  (Ask AI is an explainer only) is fair game here as part of the
  ropagen design surface that the free-text comments reflect.

## 6. NLP Document-Level Metrics

- **Form's BERTScore Recall edge tracks the structural-coverage
  property of the Form interface.** `[STRONG within NLP, since the
  participants' Form documents are observably more complete in absolute
  text length and section coverage]`
  Form requires the user to address every section (checkbox interface);
  Ask and Chat let participants underspecify in free text. Reference
  recall measures how much of the reference's content is reproduced;
  Form's interface mechanically pushes recall up.

- **Chat's Precision and SBERT edge tracks the scenario-absorption
  property of free-form input.** `[MODERATE]`
  Chat's free-form conversational input means the participant describes
  their processing in their own words, and the LLM populates fields from
  exactly that description. There's less drift toward generic ROPA
  language, so precision (less extraneous content) and document-level
  semantic alignment go up.

- **Ask underperforms every metric where a significant pair survives.**
  `[STRONG with the architectural finding]`
  Ask's per-section copy-paste workflow with no labour-saving on the
  structured side produces documents that combine Form's manual burden
  with Chat's open-ended outputs --- the worst of both. Within NLP this
  reads as Ask consistently sitting at the lower tail.

## 7. NLP Chapter-Level Metrics

- **Chapter 1 (Controller and Contact Details): templated address block,
  scenario provides exact content.** `[STRONG]`
  The scenario gives participants the exact organisation name, address,
  contact details, and DPO assignment. There's almost no room for
  paraphrase. Surface overlap with the reference is naturally high, and
  Ask leads here because Ask's section-by-section dialogue fills the
  address-block content with reference-aligned wording.

- **Chapter 2 (Purposes and Legal Bases): open-ended legal-prose
  register.** `[STRONG]`
  The scenario gives the processing purposes in plain language, but
  writing them into ROPA prose is open-ended: which Article 6 sub-clause
  to cite, how to phrase the purpose, what legal-register to use. The
  raw participant text confirms wide variation. Lexical overlap with the
  reference is therefore much lower than at Chapter 1.

- **Chapter 3 (Categories of Personal Data) and Chapter 4 (Data
  Subjects and Recipients): constrained-but-varied list content.**
  `[STRONG]`
  The categories and subjects are bounded by the scenario (name,
  contact, working hours, vehicle plate; employees, drivers with
  parking authorisation; internal IT, no external cloud). Participants
  converge on the same set but enumerate in different orders and
  phrasings (\emph{E-Mail-Adresse} vs \emph{Kontakt}). Lexical metrics
  see the variation, embedding metrics rescue the semantic agreement.

- **Chapter 5 (Retention and Deletion): wide variance because of
  participant-varied treatment of the same fact.** `[STRONG]`
  The scenario specifies "3 months after departure". Some participants
  quote this verbatim, others paraphrase, others add archiving or
  legal-grounds context. The variance shows up as the widest standard
  deviations of the chapter set.

- **Chapter 6 (Technical and Organizational Measures): variance from
  subset selection.** `[STRONG]`
  The scenario lists several TOMs (role-based access, MFA, backups,
  server-room control, confidentiality obligation). Participants pick
  different subsets in different detail levels; lexical metrics pick up
  the wide spread, embedding metrics show the semantic content is
  similar.

- **Form sweeps chapters 2--4, Chat sweeps chapters 5--6, Ask wins
  chapter 1.** `[MODERATE]`
  The three-zone split tracks chapter content type: chapters with
  list-like constrained content (2--4) reward the structural coverage
  of Form; chapters with free-prose content (5--6) reward the
  scenario-absorbing free-form input of Chat; the templated address
  block (1) rewards Ask's per-section dialogue. This is within-NLP
  reasoning supported by the chapter content types.

## 8. LLM-as-a-Judge

- **Form: highest Completeness, lowest Faithfulness, highest
  Hallucination.** `[STRONG within Judge]`
  The judge metrics measure different properties. Form's interface
  enforces field-by-field coverage (drives Completeness up). The
  finalropa LLM still synthesises the prose from the structured fields
  during the final generation step, which can invent details not in
  the scenario (drives Hallucination up, Faithfulness down). These
  two effects co-occur in the same document set: 83.8\% of Form
  documents combine maximum Completeness with moderate-or-worse
  Hallucination.

- **Chat: lowest Completeness, highest Faithfulness, lowest
  Hallucination.** `[STRONG]`
  Chat's free-form input means the LLM only populates what the
  participant described --- leading to gaps (Completeness drops) but
  also to fewer fabrications (the final generation has less to invent
  on top of the participant's own scenario specifics).

- **Overall collapses everything into a narrow range with no winner.**
  `[STRONG]`
  Overall weighs the four metrics holistically. Form's high
  Completeness cancels its low Faithfulness; Chat's high Faithfulness
  cancels its low Completeness; Ask sits between both. The Overall
  range ($2.41$ to $2.62$) shows the trade-off does not favour any
  mode at the rubric level.
