At the document level the user-study Form-leading verdict breaks
into a trade-off. Form documents recover more of what the
reference \emph{says}, Chat documents stay closer to what the
reference \emph{means}, and Ask documents do neither. -> perfekt, das muss nochmal in der Discussion aufgegriffen werden.

The embedding-based view keeps the same three-zone pattern as the
lexical metrics but compresses the absolute range. Chapter 1
stays at the top of the BERT range with Ask still ahead;
the smaller MiniLM encoder makes the Ask lead more apparent (SBERT
MiniLM Ask $0.736$ versus Form $0.663$, Chat $0.662$). The middle
chapters favor Form, with the document-level Recall-versus-Precision
trade-off appearing locally on Chapters 2 and 4: Form leads
Recall and F1 while Chat takes a narrow Precision lead on both.
Chapter 3 is the cleanest sweep, with Form highest on every
BERT-based metric (F1 $0.903$ versus Ask $0.865$, Chat $0.872$).
The last two chapters favour Chat: Chapter 5 has Chat ahead on
every BERT-based metric, and the MiniLM SBERT pass widens the gap
visibly (Chat $0.566$ versus Form $0.516$, Ask $0.474$); Chapter
6 has Chat narrowly ahead on every BERT-based metric. -> sowas muss auch nochmal in der Discussion aufgegriffen werden, und nochmal analysiert werden. die frage ist dazu: warum könnte das so sein?

Ask trails on every metric and is the inferior mode in every
significant pairwise comparison. -> grad solche signifikanzen kann man dann auch diskutieren. was bedeutet das für die praxis etc

summary of doc and chapter level: Eigentlich solltest du genau das was du hier super schön zusammenfasst in der discussion dann interpretieren. Du hast wirklich eine sehr gute Basis!

chapter 5.2: llm as a judge: Du hast diese analyse ja gemacht also solltest du sie dann auch immerhin kurz in der discussion mit aufgreifen

Three patterns emerge. First, the Completeness ordering (Form
$>$ Ask $>$ Chat) is the exact inverse of the Scenario
Faithfulness and Hallucination orderings (Form $<$ Ask $<$ Chat):
Form documents are the most structurally complete but also the
most fabricated, Chat documents the most faithful to the scenario
but the least complete, Ask between the two extremes on every
metric. Second, Legal Correctness is flat relative to the
Completeness spread (roughly $0.45$ versus $1.66$ points). The
judge distinguishes modes more sharply on whether the required
Article~30(1) fields are present than on whether the legal
terminology itself is appropriate. Third, the holistic Overall
scores compress the per-metric spread into a narrow $0.21$-point
range. Form's high Completeness is offset by its low Faithfulness
and high Hallucination, leaving Chat with the smallest of
advantages.: Die gerne auch in der discussion aufgreifen

The chapter has reported the reference-based NLP metrics at both document and
chapter resolutions (Sections 5.1.1–5.1.2) and the supplementary LLM-as-a-Judge
layer (Section 5.2). This section brings the document-quality findings together and
frames the questions the Discussion takes up.: hier sagst du es nämlich genau richtig: du setzt den rahmen hier und musst dann später diskutieren und ausweiten

beginning of discussion: genau wie gestern angemerkt, beantwortet wurden die noch nicht, sonst hättest du es explizit schon im vorherigen Kapitel erwähnen müssen dass du grad die RQs beantwortest, wobei das in der Discussion natürlich der Ort ist. Also 4 und 5 haben die Analysen zur beantwortung geliefert. Du hast ja hier nur nochmal wiederholt welcher modus in welcher metrik vorne lag. Wa sbedeutet das aber für die Praxis? Welche zusammenhänge oder patterns ergeben sich hieraus? Alles was du hier schreibst kann ich im vorherigen Kapitel ja auch bereits lesen.

Wenn du die Frage hast WIE werden die Nutzer beeinflusst, dann muss man die Daten in einen größeren Kontext bringen zb wa sbedeutet das für andere anwendungen, was lässt sich aus den Daten ableiten? Das fehlt hier bisher

6.2: ask and co author: der Inhalt dieser section ist gut aber wieder sehr verwirrend präsentiert
6.4: limitations: Inhaltlich passt das auch aber kann man besser darstellen