# Worked Examples: Chapter-Level NLP Metrics

Two-chapter worked example feeding the Evaluation chapter. All passages are extracted verbatim from the same chapter splitter used by the main pipeline (`extract_reference_chapters`, `extract_chapters_markdown`, `map_doc_chapters_to_canonical`); all metric values use the identical scoring code and ModernBERT (`answerdotai/ModernBERT-base`) configuration as `chapter_results.csv`, computed on `cuda`.

Candidates:

- `IAR1116-chat` — Chat mode, document id 11
- `AEB2451-form` — Form mode, document id 80

## 1. Retention worked example (Ch5 — *Aufbewahrungsfristen und Löschung*)

Lexical metrics: BLEU, ROUGE-2, METEOR.

### Reference passage

```text
Wir löschen die personenbezogenen Daten drei Monate nach Beendigung des Beschäftigungsverhältnisses, sofern keine gesetzlichen Aufbewahrungspflichten entgegenstehen.
```

### IAR1116 (Chat) passage

```text
### 5.1 Löschfristen
Die personenbezogenen Daten werden gemäß folgender Regelungen gelöscht:

- **Grundsatz:** Die Daten werden spätestens **3 Monate nach Austritt der Mitarbeitenden** gelöscht.
- **Ausnahmen:** Sofern gesetzliche Aufbewahrungspflichten (z. B. im Rahmen laufender Verfahren) bestehen, erfolgt die Löschung erst nach Ablauf dieser Fristen.

### 5.2 Verfahren zur Löschung
Die Löschung erfolgt entweder automatisiert durch unsere Systeme oder manuell durch die zuständigen Mitarbeitenden. Die Einhaltung der Löschfristen wird regelmäßig überprüft.

---
```

### AEB2451 (Form) passage

```text
Wir bewahren personenbezogene Daten unserer Mitarbeitenden gemäß den gesetzlichen Vorgaben auf und löschen diese nach Ablauf der festgelegten Fristen. Die Aufbewahrungsfristen richten sich nach den folgenden Grundsätzen:

- **Grundsatz:** 6 Jahre nach Beendigung des Beschäftigungsverhältnisses (gemäß § 257 HGB und § 147 AO für steuerrelevante Unterlagen).
- **Ausnahmen:**
  - Sozialversicherungsnummern und Vertragsdaten können bis zu 10 Jahre aufbewahrt werden, sofern dies aufgrund rechtlicher Auseinandersetzungen oder Verdachtsmomenten (z. B. Sozialversicherungsbetrug) erforderlich ist.
  - Biometrische Daten und Videoüberwachungsdaten werden nur so lange gespeichert, wie dies für den jeweiligen Zweck (z. B. Zutrittskontrolle) notwendig ist.

Nach Ablauf der Aufbewahrungsfristen werden die Daten automatisch gelöscht, sofern keine gesetzlichen oder vertraglichen Gründe für eine längere Speicherung vorliegen.

---
```

### Lexical scores against the reference passage

| Candidate | BLEU | ROUGE-2 | METEOR |
|---|---|---|---|
| IAR1116-chat | 0.0000 | 0.0625 | 0.1724 |
| AEB2451-form | 0.0356 | 0.1185 | 0.3790 |

## 2. Purpose worked example (Ch2 — *Zwecke und Rechtsgrundlagen der Verarbeitung*)

Semantic metrics: BERTScore Precision/Recall/F1 and SBERT cosine similarity (ModernBERT).

### Reference passage

```text
2.1 Verarbeitungszwecke
Wir verarbeiten personenbezogene Daten für folgende Zwecke:
• Verwaltung von Mitarbeitenden vom Eintritt bis zum Austritt, einschließlich:
• Anlegen neuer Mitarbeitender
• Dokumentation von Arbeitszeiten
• Verwaltung von Urlaub und Abwesenheiten
• Verwaltung von Parkplatzberechtigungen für berechtigte Mitarbeitende

2.2 Rechtsgrundlagen der Verarbeitung
Die Verarbeitung erfolgt auf Grundlage folgender Rechtsnormen:
• Art. 6 Abs. 1 lit. b DSGVO (Erfüllung eines Vertrags oder vorvertraglicher Maßnahmen)
• § 26 BDSG (Datenverarbeitung für Zwecke des Beschäftigungsverhältnisses)
```

### IAR1116 (Chat) passage

```text
### 2.1 Zwecke der Verarbeitung
Wir verarbeiten personenbezogene Daten unserer Mitarbeitenden zur ganzheitlichen Verwaltung von deren Beschäftigungsverhältnis – vom Eintritt bis zum Austritt aus dem Unternehmen. Die Verarbeitung dient folgenden Zwecken:

- Erfassung und Pflege von Stammdaten neuer und bestehender Mitarbeitender,
- Dokumentation von Arbeitszeiten sowie Verwaltung von Urlaubs- und Abwesenheitszeiten,
- Zuweisung und Verwaltung von Parkplatzberechtigungen für den firmeneigenen Parkplatz mit Schranke. Hierfür wird ein eindeutiges Merkmal (Fahrzeugkennzeichen) hinterlegt, um die Nutzung zu ermöglichen.

Die Verarbeitung erfolgt ausschließlich auf internen Systemen (Microsoft Office 365 und eigene Server) ohne Nutzung externer Cloud-Dienste. Medizinische Daten oder Krankentage sind nicht Gegenstand dieser Verarbeitungstätigkeit.

### 2.2 Rechtsgrundlagen der Verarbeitung
Die Verarbeitung personenbezogener Daten erfolgt auf folgenden Rechtsgrundlagen gemäß Art. 6 Abs. 1 DSGVO sowie ergänzenden nationalen Vorschriften:

- **Art. 6 Abs. 1 lit. b DSGVO (Vertragserfüllung):**
  Die Verarbeitung ist für die Durchführung des Beschäftigungsverhältnisses erforderlich, insbesondere zur Verwaltung von Arbeitszeiten, Urlaub und Parkplatzberechtigungen.

- **Art. 6 Abs. 1 lit. f DSGVO (Berechtigtes Interesse):**
  Die Verarbeitung dient unserem berechtigten Interesse an einer effizienten Verwaltung der Mitarbeiterressourcen sowie der Sicherstellung einer geordneten Nutzung des firmeneigenen Parkplatzes.

- **§ 26 BDSG (Datenverarbeitung für Zwecke des Beschäftigungsverhältnisses):**
  Die Verarbeitung erfolgt im Rahmen des Beschäftigungsverhältnisses und ist für dessen Durchführung erforderlich.

---
```

### AEB2451 (Form) passage

```text
Wir verarbeiten personenbezogene Daten unserer Mitarbeitenden ausschließlich zur Verwaltung des Beschäftigungsverhältnisses von der Einstellung bis zum Austritt. Dies umfasst folgende Zwecke:

- Erfassung und Pflege von Stammdaten der Mitarbeitenden
- Dokumentation von Arbeitszeiten und Anwesenheiten
- Verwaltung von Urlaubs- und Abwesenheitszeiten
- Verwaltung von Parkplatzberechtigungen (z. B. Fahrzeugkennzeichen)
- Erfüllung gesetzlicher Aufbewahrungs- und Meldepflichten
- Sicherstellung der betrieblichen Abläufe und Compliance

Die Verarbeitung erfolgt auf Grundlage folgender Rechtsgrundlagen:

- **Art. 6 Abs. 1 lit. b DSGVO** (Erfüllung eines Vertrags oder vorvertraglicher Maßnahmen)
- **§ 26 BDSG** (Datenverarbeitung für Zwecke des Beschäftigungsverhältnisses)
- **§ 257 HGB** (Aufbewahrung von Handelsbüchern und Unterlagen)
- **§ 147 AO** (Aufbewahrung von steuerrelevanten Unterlagen)
- **§ 239 Abs. 1 HGB** (Führung der Handelsbücher)
- **§ 2 Abs. 1 Nr. 1 BDSG** (Verarbeitung personenbezogener Daten im Beschäftigungskontext)

---
```

### Semantic scores against the reference passage

| Candidate | BERTScore P | BERTScore R | BERTScore F1 | SBERT (ModernBERT) |
|---|---|---|---|---|
| IAR1116-chat | 0.8797 | 0.9180 | 0.8984 | 0.9810 |
| AEB2451-form | 0.8954 | 0.9336 | 0.9141 | 0.9882 |
