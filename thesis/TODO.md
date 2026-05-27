Es gibt noch Verbesserungspotenzial in der Darstellung, da immer noch keine ganz konsistente Storyline existiert. Ein paar Vorschläge, die den Lesefluss verbessern können:

- Anordnung der Figures und Text: Du analysierst oft mehrere Tabellen und Diagramme in der gleichen Section/Subsection und platzierst die Bilder und Tabellen am Schluss. Es wäre besser den text immer wieder zu unterbrechen und die Sachen da platzieren wo sie auch im Text referenziert und beschrieben werden.

- Man muss nicht alle Tabellen und Grafiken in einzelnen Sätzen referenzieren. Wenn sie ca die gleichen daten zeigen immer am Anfang der Section direkt alles referenzieren und dann im Text beschreiben

- Die Captions für Tabellen, Grafiken und Listings gerne mit Schriftgröße \tiny. Kannst du auch in Tabellen nutzen, dann musst du sie manchmal evtl garnicht drehen. Ich finde es sehr störend wenn eine recht kleine Tabelle eine ganze Seite belegt.

- Keine neue Seite anfangen für neue Sections oder Subsections! (Das macht man nur für Kapitel)

- In Tabellen auch öfter mit bold arbeiten oder besondere werte mit grau hinterlegt und/oder fett hervorheben. Muss nicht immer aber an manchen Stellen würde das den Text unterstützen wenn die "Gewinner" oder andere besondere Werte nochmal extra hervorgehoben werden

- Manchmal sehr harte Unterbrechungen durch die Signifikanz Tests

- Immer noch Probleme mit dem Fluss. Oft wechseln die Themen sehr hart

- Es fehlt schon noch bisschen warum welche Analysen gemacht wurden (Präsentation der Ergebnisse ist auf der richtigen Granularität; es muss nur durch Begründungen etwas zusammengeführt werden, bzw die Begründungen werden noch nicht klar; hin und wieder kommen ganz gute aber es fehlen auch welche)
  -> oft kann ich zwischen einzelnen Absätzen die Verbindung nicht erkennen warum genau diese analyse nach der anderen was zeigt die eine im Gegensatz zur anderen

- Bei der Präsentation der Quantitativen Evaluation tu ich mir immernoch sehr schwer. Granularität passt auch aber die Reihenfolge der Tabellen, dokumentenauszüge und dem Text ist vogelwild und verwirrt mic sehr beim Lesen. Ich erkenne aktuell noch keine Storyline

## Final-pass typographic consistency (added 2026-05-27)

Pre-existing inconsistencies surfaced during the *SUS* / *R-TLX*
italics pass. Not new findings; address during the final typographic
sweep.

- `chapters/evaluation/userstudy_summary.tex` uses `RTLX` (no hyphen)
  while the rest of the thesis uses `R-TLX`. Normalize to `R-TLX`.
- "perceived AI support" wanders between lowercase and Title Case
  across `methodology.tex`, `demographics.tex`, and `userstudy.tex`.
  Pick one form (likely Title Case, as a proper instrument name) and
  apply consistently.
- The instrument is referred to as *Perceived AI Support* in some
  places and *Perceived LLM Support* in others (e.g.
  `ai_questions.tex` line 7 vs line 69 — same construct, two names).
  Pick one and apply throughout, including the section title and
  table captions.