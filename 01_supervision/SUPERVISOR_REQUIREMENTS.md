# What the supervisor wants — consolidated

Working record of everything Prof. Dr. Katja Zeume (supervisor / first examiner) has asked for,
plus the input from Prof. Dr. Gleim. Compiled 2026-08-07.

German originals are quoted verbatim — they are the authoritative record. English glosses and
anything marked *Interpretation* are my reading, not her words.

## Sources

| Date | Source | Status |
|---|---|---|
| 2026-07-15 | `Gespraechsprotokoll_15.07.2026.docx` — supervision meeting | Scope decisions |
| 2026-07-29 | `Expose_Masterarbeit_Juma_final with_comments.pdf` — 12 comments, author `katja` | Concrete redlines |
| 2026-07-29 (with the PDF) | Email from Zeume, after consulting Prof. Gleim | Newest direction |

## The one thing that changed

**Before:** *Are AI-generated queries correct and efficient?*
**Now:** *How do LLMs use the SQL language itself — and do they use it differently than humans?*

Her reason, stated plainly: correctness is not an interesting result, because LLMs are already good
at it. The measurement apparatus (EX, R-VES, execution plans) is no longer the contribution — it is
the evidence for a **language-design** argument.

## Her comments on the exposé (2026-07-29)

| Where | Comment (verbatim) | What it means |
|---|---|---|
| **Title** | *"Der Fokus sollte auf der Evolution der Sprache liegen"* | Language evolution is the organizing frame. The title must change. |
| §1, at "Vektordatenbanken" | *"hier NoSQL nennen, sonst wirkt der Übergang zu VektorDB unnatürlich"* | §1 jumps from relational SQL straight to vector DBs. NoSQL is the missing bridge. |
| §1, at "Qualität dieser Anfragen" | *"und Struktur (!) der Sprache"* | Not just quality — **structure** of the language. Her emphasis. |
| §1, at "überwiegend Korrektheit" | *"bitte nicht überwiegend Korrektheit. Die Korrektheit können LLMs :)"* | Correctness becomes a side note. |
| §1, at the efficiency sentence | *"Effizienz ist nur ein Punkt. Wir wollen auch Sprachstruktur: Aufbau der anfragen, Operatoren, Logik"* | **The most operational comment.** Three concrete dimensions — see below. |
| §2.1, at the graph paragraph | *"Deswegen oben auch noSQL nennen"* | Repeat of the NoSQL point. |
| §2.1, at the annotation-error paragraph | *"haben sie etwas zu manuellen Anfragemengen gefunden? Wir benötigen zwingend Anfragen die vom Menschen geschrieben worden sind, für den Vergleich"* | **A direct question requiring an answer.** *"zwingend"* = mandatory. |
| §2.3 (Forschungslücke) | *"standardisiert, optimiert, effizienzbewusst -> klingt gut, ist aber undefiniert, können sie das genauer erklären und vor allem auch die Sprachstruktur mit aufnehmen"* | Define the vague terms; add language structure to the gap. |
| §2.3, next paragraph | *"s.o."* | Same criticism. |
| §3, Leitfrage | *"muss noch umformuliert werden"* | Rewrite the main research question. |
| §3, FF2 | *"s.o."* | Same. |
| §3, FF4 | *"Der Rest des Exposes muss auch an die Forschungsfrage angepasst werden, und kann deutlich gekürzt werden."* | Sections 4–9 get adapted **and shortened**. |

Note the placement of the *"manuelle Anfragemengen"* question: it sits directly on the paragraph
reporting BIRD's 52.8 % annotation error rate. *Interpretation:* answering "BIRD gold queries" is
circular — she was questioning BIRD when she asked.

## Her email (with Gleim)

> *"we agreed that we should put the analysis of the evolution of the query language more in focus"*
> *"you can look into correctness and efficiency for those benchmarks but it will rather not be too surprising. LLMs will be better than humans on this one"*
> *"My focus for your work is to also analysis the query language design and how LLMs are using SQL for their purpose (and whether they do this differently than humans)"*
> *"Prof. Gleim also proposed to extend this on index structures, which I believe is a good idea because it follows well on your bachelor thesis"*

*Interpretation:* Gleim is now materially involved in shaping the topic. He was already listed in the
July protocol as a candidate second examiner — worth acting on.

## What must actually be measured

From *"Sprachstruktur: Aufbau der anfragen, Operatoren, Logik"*:

| Dimension | In practice |
|---|---|
| **Aufbau** | How the query is composed — nesting depth, CTE vs. subquery vs. join, flat or layered |
| **Operatoren** | Which constructs are used — window functions vs. correlated subqueries, `EXISTS` vs. `IN`, `DISTINCT`, set operations |
| **Logik** | How conditions are expressed — predicate placement, negation, quantification |

**All three are readable from the query text alone — no database, no execution, no harness.**
The first result does not depend on the pipeline that does not exist yet.

Execution then answers the second-order question: does a structural difference survive the
optimizer, or is it normalized away? That is where `EXPLAIN (ANALYZE, BUFFERS)` and the index work
come in.

## New priority order

| Axis | Status |
|---|---|
| Query language design / evolution — which SQL do LLMs write | **Primary** |
| Index structures (B-tree vs. GIN, PostgreSQL only — decided) | **Secondary, new** |
| Execution plans / the optimizer "why" | Supporting evidence |
| Correctness + efficiency (EX, R-VES) | Control. Report, don't headline. |

The `upper(city)` example carries all three top axes at once: a language-structure difference
(function-wrapping vs. direct comparison), an index consequence (index unusable), and an optimizer
consequence (sequential scan). Lead with it.

## Changes required to the exposé

Ordered by dependency — the argument first, everything else follows from it.

1. **§2.3 + §3** — argue a *language-design* gap, not an efficiency-measurement gap. The current gap
   ("SQL and vector search in one execution model") collapses once vector is demoted. Define the
   vague terms she flagged. Rewrite the Leitfrage and all four FF.
2. **§7 timeline** — replace the seven sequential phases (the waterfall she rejected in July) with
   three parallel strands: research question ~30 %, benchmarks ~60 %, framework ~0 %, plus explicit
   exploratory phases and uncertainty buffers.
3. **Title** — drop "und Vektorsuche", carry the language-evolution framing.
4. **§1** — lead with the language question. Name NoSQL as the bridge before vector DBs. Add the
   `upper(city)` example.
5. **§2.1** — keep vector/NoSQL as the *endpoint of an evolution narrative*, not as a measurement
   target. Promote the annotation-error finding from side remark to methodology.
6. **§4–§6, §9** — adapt to the new question and **cut**. She explicitly asked for a shorter document.
7. **Header block** — four `[bitte ergänzen]` placeholders (Studiengang, Universität/Lehrstuhl,
   Matrikelnummer, Datum). These block the Anmeldung.
8. **Language pass last** — translate to English and simplify in one sweep. Translating twice wastes
   work.

## The question she asked directly

> *"Haben Sie etwas zu manuellen Anfragemengen gefunden?"*

Answer to give her — **BIRD is the experimental control, not the human baseline.** The human baseline
is real query corpora:

| Corpus | What it is | Role |
|---|---|---|
| **BEAVER** | 9,128 question-SQL pairs from **real enterprise query logs**, NL written with DBAs; 7,978 public | Strongest "genuinely human" claim — production queries, not annotator queries |
| **SQLShare** | 11,137 hand-written statements, 57 real scientists, 5 years | How humans write SQL in the wild |
| **Join Order Benchmark (JOB)** | 113 hand-written analytical queries, real IMDB data, PostgreSQL | Built to stress optimizers — the index testbed |
| **BIRD Mini-Dev** | ~500 expert gold queries, native PostgreSQL port | The paired experiment (same question → human + LLM) |

Supporting argument: for *Aufbau / Operatoren / Logik*, the human side does **not** need NL pairing.
Real working SQL is better evidence of how humans write than benchmark gold queries, which were
written to annotate a dataset rather than to do a job.

Still to verify: SQLShare dialect (SQL Server → needs porting?) and licence; BEAVER dialect
(likely Snowflake/BigQuery) and licence.

## Closely related work — must be addressed in §2

**Pecuchova, J. & Benko, Ľ. (2026). Structural Differences Between Human and AI-Generated SQL
Queries. FLAIRS 39.** 669 Snowflake queries — 189 human, 480 AI (ChatGPT, Cortex, Claude). Measured
verbosity, Halstead metrics, cognitive complexity, and SQL constructs. Finding: LLMs used nested
subqueries where humans used plain joins, and vice versa.

This is the construct comparison, already published. It does **not** undermine the thesis, because
they measured **code metrics only and never executed anything** — no plans, no optimizer, no indexes.
They showed the text differs; the open question is whether the difference has any *consequence*.
Cite it as the starting point and position the thesis as what comes after.

Also relevant: **SQLStructEval** (arXiv 2604.06736, 2026) — structural *self*-consistency of LLM
output across paraphrases, no human comparison.

Full text of the FLAIRS paper not yet obtained (journal returns 403) — get it via the university
library before writing §2.

## Meeting of 2026-10-27 — what she settled

Full record: `meetings/Gespraechsprotokoll_27.10.2026.md`. Quotations are English; the meeting was
held in English.

| Question put to her | Her answer |
|---|---|
| Does a flat, SQL-92-shaped baseline change what we expect to find? | **Yes.** *"If it doesn't change what it shows, then it's a strange baseline."* |
| Is splitting the two BIRD variants sound — SQLite for operators, PostgreSQL for execution? | **Approved.** *"Fair enough, because of availability for systems."* |
| Is schema-driven non-sargability a result or a confound? | **A result.** *"That's a research question."* |
| Does the porting result make the working-SQL corpora more urgent? | **Not answered** — the phrasing did not carry. Re-ask in writing, naming the finding. |
| The three extension paths | **Stay open.** *"For four to six, that's also what I had in mind."* |

Assessment: *"The pre-research sounds very good, sounds interesting."* · *"I'm fairly satisfied with
the status of the work."* No change of direction requested.

### New — a fourth extension path, proposed by her

> *"I also read about, because you mentioned Snowflake, that they also have published some AI
> operators, which I think is interesting maybe also for this work, because then it's like SQL can
> also use an LLM call. So, is this used by an LLM or by a human or differently? So I think that
> would also be a nice extension."*

SQL gaining operators that invoke a language model — the evolution of the query language observed as
it happens. **Candidate only; nothing committed, and the operators themselves are unverified.**

### Standing obligations she placed on the student

- **Monitor the literature continuously.** *"I don't have a news feed for exactly this kind of
  question. You are now much more focused on this topic than I am."* Using AI tooling for this was
  proposed and endorsed: *"Yeah, of course. You should do this."*
- **React to late-breaking work rather than ignoring it.** *"If this happens, then I think you
  should react to this, because it shows that you work on a very active topic, which is very
  relevant."*
- **The standard for the Kolloquium:** *"After six months you are an expert on the current status of
  this problem."* · *"Not producing a piece of paper any more, but being an expert in your topic and
  being able to defend it."*

### Registration — resolved

The August signature stands; no re-signing. Submit the Antrag to the Prüfungsamt **with her in CC**,
stating the matter was discussed with her. *"It's transparent because I'm in CC, so I could say no."*

### Still open after the meeting

- ~~**Second examiner.**~~ **Settled 11.2026** — Prof. Dr. Gleim confirmed and signed the Antrag.
  The meeting record showed it as open only because the transcript's speaker attribution was
  unreliable at that point.
- **BIRD versus Spider** for the paired experiment — the question did not get through.
- She invited the six questions **in writing** for fuller answers: *"I only briefly answered them."*

## Open decisions — put these to her

1. **Index structures *or* a second paradigm — not both.** July planned the extension as Cypher or
   MongoDB; the email proposes index structures instead. Six months, framework at 0 %. Recommendation:
   index structures (builds on the bachelor thesis, stays in PostgreSQL, no second system), second
   paradigm becomes future work. Needs her confirmation.
2. **"Evolution of the language" — backward or forward?** Backward = which era of SQL do LLMs write
   (SQL-92 correlated subqueries vs. SQL:2003 window functions). Forward = how *should* the language
   evolve now that its main author is a machine. Recommendation: backward as the empirical core,
   forward as the discussion chapter.
3. ~~**Second examiner.**~~ **Settled 11.2026** — Prof. Dr. Gleim confirmed and signed the Antrag.

## Decided

- **Index work stays inside PostgreSQL** — B-tree vs. GIN (inverted). Same tree-vs-inverted
  comparison as the bachelor thesis, one system, no Elasticsearch.
- Bachelor thesis for reference: *"Baumstrukturierte und invertierte Indexe: Eine praktische
  vergleichende Analyse von Indexierungsstrategien in einem RDBMS und Elasticsearch"* (B.Sc., 67 pp.,
  supervised by Zeume and Conen). It already describes Elasticsearch as a NoSQL database — citable
  for the NoSQL framing she asked for, without running Elasticsearch.
