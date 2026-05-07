# Appendix: LLM-as-a-Judge Pipeline — Prompt and Scenario

This appendix documents the full inputs to the LLM-as-a-judge evaluation layer used to score the 113 ROPA documents produced by participants. It is intended for verbatim inclusion in the thesis appendix and contains: (1) the study scenario shown to all participants, in the German original and an English translation; (2) the verbatim system prompt used to instruct the judge model; (3) the five-dimension rubric with its 1–5 Likert scale; and (4) the judge configuration (model, temperature, response schema, etc.) needed to reproduce the evaluation.

---

## 1. Study Scenario

The scenario was presented to participants in German. Every participant — regardless of interaction mode (Form, Ask, Chat) — was given exactly this text. The thesis is written in English, so the English translation below is the primary reference; the German original is reproduced for transparency and for any reviewer wishing to verify the translation.

### 1.1 German Original (verbatim)

```text
Szenario: Mitarbeiterverwaltung (Arbeitszeit/Urlaub) & Parkplatzberechtigung

Sie sind Mitarbeitender namens A.I. und arbeiten für die APOR GmbH, ein
Softwareunternehmen mit ca. 50 Mitarbeitenden in Ulm. Sie handeln im Namen
des Unternehmens und sind im Szenario sowohl Verantwortlicher (Data
Controller) als auch Datenschutzbeauftragte:r (DPO/DSB).

Zur Organisation:

Rolle: Data Controller, DPO
Adresse: Mainstraße 67, Ulm
E-Mail: mail@apor.eu
Telefon: 012345678
Vertreter: (Sie), A. I., ai@apor.eu
DPO: Das sind auch Sie

Verarbeitung
Das Unternehmen verarbeitet personenbezogene Daten, um Mitarbeitende vom
Eintritt bis zum Austritt zu verwalten. Im Fokus stehen:

- Anlegen neuer Mitarbeitender
- Dokumentation von Arbeitszeiten
- Verwaltung von Urlaub und Abwesenheiten

Zusätzlich verwaltet APOR für berechtigte Mitarbeitende eine
Parkplatzberechtigung für einen Firmenparkplatz mit Schranke. Damit
berechtigte Mitarbeitende den Parkplatz nutzen können, wird ein geeignetes
Merkmal zur Zuordnung der Berechtigung hinterlegt (z. B. ein
Fahrzeugkennzeichen).

APOR arbeitet mit intern gehostetem Microsoft Office sowie internen Servern
(keine externe Cloud). Krankentage oder medizinische Angaben sind für diese
Verarbeitung nicht erforderlich.

Für die Verwaltung sind technische und organisatorische Maßnahmen
vorgesehen, wie z.B. Zugriffsbeschränkung nach Rollen (Need-to-know),
Passwortschutz (ggf. MFA), regelmäßige Backups, Zutrittskontrolle zu
Serverraum/Archiv und Vertraulichkeitsverpflichtung der berechtigten
Mitarbeitenden.

Alle in diesem Zusammenhang gespeicherten Informationen werden spätestens
3 Monate nach Austritt der jeweiligen Person gelöscht.
```

### 1.2 English Translation

```text
Scenario: Employee Administration (Working Time / Leave) & Parking
Authorisation

You are an employee named A.I., working for APOR GmbH, a software company
with approximately 50 employees in Ulm. You act on behalf of the company
and, in this scenario, are both the Data Controller and the Data
Protection Officer (DPO).

Organisation details:

Role: Data Controller, DPO
Address: Mainstraße 67, Ulm
E-mail: mail@apor.eu
Phone: 012345678
Representative: (You), A. I., ai@apor.eu
DPO: Also you

Processing
The company processes personal data in order to administer employees from
onboarding to exit. The focus is on:

- Onboarding new employees
- Documentation of working hours
- Administration of leave and absences

In addition, APOR manages a parking authorisation for entitled employees
for a company car park with a barrier. To allow entitled employees to use
the car park, a suitable feature for assigning the authorisation is
recorded (e.g. a vehicle licence plate).

APOR uses internally hosted Microsoft Office and internal servers (no
external cloud). Sick days or medical information are not required for
this processing.

For administration, technical and organisational measures (TOMs) are
provided, such as role-based access restriction (need-to-know), password
protection (where appropriate, MFA), regular backups, physical access
control to the server room / archive, and a confidentiality obligation for
authorised employees.

All information stored in this context is deleted no later than 3 months
after the person's departure.
```

---

## 2. LLM-as-a-Judge System Prompt

The following system prompt is taken verbatim from `python/judge/prompt.json` (`judge.system`). It is sent as the `system` role on every evaluation call.

```text
You are an expert GDPR compliance reviewer evaluating Records of
Processing Activities (ROPA) documents under Article 30 GDPR. The
documents are written by novices (non-experts, no prior GDPR training)
who described the same processing scenario using different LLM-assisted
tools. Your job is to judge each ROPA document against (a) the provided
scenario and (b) GDPR Article 30 requirements. Be strict but fair. Do not
reward verbosity. Do not penalise a document for merely restating
scenario facts. Respond with valid JSON only - no prose, no Markdown
fences, no commentary before or after the JSON object.
```

The accompanying user-message template (sent on every call, with `{scenario}` and `{document}` substituted) is:

```text
You will evaluate one ROPA document against the scenario it is supposed
to cover.

=== SCENARIO (verbatim, German) ===
{scenario}
=== END SCENARIO ===

=== ROPA DOCUMENT TO EVALUATE ===
{document}
=== END DOCUMENT ===

Score the document on each of the following five metrics using a 1-5
Likert scale, and give a short rationale (max 2 sentences, English) for
each score. The scale for all metrics is:
1 = very poor, 2 = poor, 3 = adequate, 4 = good, 5 = excellent.

Metrics and what to assess:
- completeness: Coverage of Art. 30(1) GDPR required elements -
  controller identity and contact, DPO, purposes of processing, legal
  basis, categories of data subjects and personal data, categories of
  recipients, retention periods, and technical/organisational measures
  (TOMs). Missing elements lower the score.
- scenario_faithfulness: How accurately the document reflects the
  concrete facts of THIS scenario - APOR GmbH, Ulm (Mainstraße 67), ~50
  employees, internally hosted Microsoft Office and internal servers (NO
  external cloud), no medical/sickness data, 3-month deletion after
  employee departure, parking lot authorisation using a distinguishing
  feature such as a licence plate. Generic ROPA boilerplate that ignores
  these specifics lowers the score.
- legal_correctness: Correct use of GDPR terminology and correct citation
  of legal basis (typically Art. 6(1)(b) performance of contract for
  employment data, Art. 6(1)(c) legal obligation where applicable, Art.
  6(1)(f) legitimate interest for parking authorisation). Wrong articles,
  invented legal bases, or confusing controller/processor/DPO roles lower
  the score.
- hallucination_inverse: Inverse score for invented facts not supported
  by the scenario (e.g. invented third-party processors, invented data
  categories like medical data, invented addresses, invented retention
  periods different from 3 months). 5 = no hallucinations, 1 = many
  invented facts.
- overall: Holistic judgement of how useful this document would be as a
  real Art. 30 ROPA record for this scenario, taking the four dimensions
  above into account.

Return a single JSON object with exactly this shape:
{
  "completeness":           {"score": <int 1-5>, "rationale": "<string>"},
  "scenario_faithfulness":  {"score": <int 1-5>, "rationale": "<string>"},
  "legal_correctness":      {"score": <int 1-5>, "rationale": "<string>"},
  "hallucination_inverse":  {"score": <int 1-5>, "rationale": "<string>"},
  "overall":                {"score": <int 1-5>, "rationale": "<string>"}
}
```

---

## 3. Judge Rubric — Five Dimensions

All five dimensions share the same 1–5 Likert scale:

| Score | Anchor      |
|-------|-------------|
| 1     | very poor   |
| 2     | poor        |
| 3     | adequate    |
| 4     | good        |
| 5     | excellent   |

Each dimension targets a distinct quality aspect of the ROPA document. The fourth dimension, `hallucination_inverse`, is *inverted* so that for all five dimensions higher = better.

| Dimension                  | What is assessed                                                                                                                                                                                                                                                                                                              | Notes on the scale                                                                                                                       |
|----------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| **Completeness**           | Coverage of Art. 30(1) GDPR required elements: controller identity and contact, DPO, purposes of processing, legal basis, categories of data subjects and personal data, categories of recipients, retention periods, technical/organisational measures (TOMs). Missing elements lower the score.                              | 1 = most required elements missing; 5 = all Art. 30(1) elements explicitly addressed.                                                    |
| **Scenario Faithfulness**  | Accuracy with respect to the concrete facts of *this* scenario: APOR GmbH, Ulm (Mainstraße 67), ~50 employees, internally hosted Microsoft Office and internal servers (no external cloud), no medical/sickness data, 3-month deletion after employee departure, parking authorisation using a distinguishing feature (e.g. licence plate). Generic ROPA boilerplate lowers the score. | 1 = ignores scenario specifics, generic ROPA template; 5 = scenario facts faithfully reflected throughout.                               |
| **Legal Correctness**      | Correct use of GDPR terminology and correct citation of legal basis. Typical expected bases: Art. 6(1)(b) (performance of contract) for employment data, Art. 6(1)(c) (legal obligation) where applicable, Art. 6(1)(f) (legitimate interest) for parking authorisation. Wrong articles, invented legal bases, or confused controller/processor/DPO roles lower the score. | 1 = wrong or invented legal bases, role confusion; 5 = correct articles, correct terminology, correct role attribution.                  |
| **Hallucination_inverse**  | Inverse score for invented facts not supported by the scenario (e.g. invented third-party processors, invented categories such as medical data, invented addresses, retention periods different from 3 months).                                                                                                               | **Inverted:** 5 = no hallucinations, 1 = many invented facts. Higher is still better.                                                    |
| **Overall**                | Holistic judgement of how useful the document would be as a real Art. 30 ROPA record for this scenario, taking the four dimensions above into account.                                                                                                                                                                        | 1 = would not function as a ROPA record; 5 = would function as a real Art. 30 ROPA record for this scenario.                             |

For each dimension the judge returns both a score (integer 1–5) and a short English rationale (max two sentences).

---

## 4. Judge Configuration

The configuration below is taken from the `judge` block of `python/judge/prompt.json` and the corresponding cells of `python/judge/ROPAgen_JUDGE.ipynb`. It is the minimal information required to reproduce the evaluation.

| Setting               | Value                                                                                              |
|-----------------------|----------------------------------------------------------------------------------------------------|
| Model                 | `google/gemini-3.1-pro-preview` (accessed via the OpenRouter API)                                  |
| Temperature           | `0.0` (deterministic decoding)                                                                     |
| Output format         | JSON object, enforced via OpenRouter `response_format = json_schema` with `strict: true`           |
| Schema name           | `ropa_judge_result`                                                                                |
| Required JSON keys    | `completeness`, `scenario_faithfulness`, `legal_correctness`, `hallucination_inverse`, `overall`   |
| Per-key shape         | `{"score": int in [1, 5], "rationale": string}`                                                    |
| Additional properties | Disallowed (`additionalProperties: false`) at every object level                                   |
| Documents evaluated   | 113 ROPA documents (subset of the 219 across N=73 participants × 3 modes; unequal mode groups)     |
| Caching               | Per-document result caching on disk (one JSON per `participant_id × mode`); cached calls are reused on re-runs to avoid duplicate API charges |
| Retry behaviour       | On schema-validation failure or transient API error, the call is retried with the same prompt; persistent failures are logged and skipped rather than allowed to corrupt the dataset |
| Logging               | Each call logs model, latency, prompt token count, completion token count, and raw response payload to enable post-hoc auditing |

### 4.1 JSON response schema (verbatim)

The judge is constrained to return output matching this schema (extracted from `prompt.json`, `judge.response_schema`):

```json
{
  "type": "json_schema",
  "json_schema": {
    "name": "ropa_judge_result",
    "strict": true,
    "schema": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "completeness",
        "scenario_faithfulness",
        "legal_correctness",
        "hallucination_inverse",
        "overall"
      ],
      "properties": {
        "completeness": {
          "type": "object",
          "additionalProperties": false,
          "required": ["score", "rationale"],
          "properties": {
            "score":     {"type": "integer", "minimum": 1, "maximum": 5},
            "rationale": {"type": "string"}
          }
        },
        "scenario_faithfulness": {
          "type": "object",
          "additionalProperties": false,
          "required": ["score", "rationale"],
          "properties": {
            "score":     {"type": "integer", "minimum": 1, "maximum": 5},
            "rationale": {"type": "string"}
          }
        },
        "legal_correctness": {
          "type": "object",
          "additionalProperties": false,
          "required": ["score", "rationale"],
          "properties": {
            "score":     {"type": "integer", "minimum": 1, "maximum": 5},
            "rationale": {"type": "string"}
          }
        },
        "hallucination_inverse": {
          "type": "object",
          "additionalProperties": false,
          "required": ["score", "rationale"],
          "properties": {
            "score":     {"type": "integer", "minimum": 1, "maximum": 5},
            "rationale": {"type": "string"}
          }
        },
        "overall": {
          "type": "object",
          "additionalProperties": false,
          "required": ["score", "rationale"],
          "properties": {
            "score":     {"type": "integer", "minimum": 1, "maximum": 5},
            "rationale": {"type": "string"}
          }
        }
      }
    }
  }
}
```

### 4.2 Known limitations of the judge layer

For full transparency, the following limitations of this evaluation layer are noted (and discussed further in the Discussion chapter):

- **Single-judge bias.** Only one judge model (Gemini 3.1 Pro Preview) operationalises the rubric. Inter-rater agreement with a human GDPR expert is not established.
- **Model-family bias.** The documents being judged were generated by Mistral Large 3 (2512) inside ropagen, while the judge is from a different model family (Google). This reduces but does not eliminate stylistic-preference bias toward outputs that resemble the judge's own training distribution.
- **Single-scenario bias.** All scores are conditional on this one scenario; generalisation to other ROPA contexts is not claimed.
- **Reference-free.** Unlike the NLP metric layer, the judge does not compare against the expert reference document — it scores against the scenario and Art. 30 directly.
