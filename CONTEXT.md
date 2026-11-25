# Scope and research direction

Source of truth for **what the thesis is about**. Last updated 2026-10-27.

For *what the supervisors asked for*, with their comments quoted verbatim, see
`01_supervision/SUPERVISOR_REQUIREMENTS.md`. Where the two disagree, that file is the newer record.

## 1. What this project is

A Master's thesis (Informatics, Westfälische Hochschule, Fachbereich Informatik und Kommunikation,
**written in English**, six months from registration).

**Topic (current title):** *Generated Queries and the Evolution of SQL — A structural comparison
with human-written queries and its consequences for optimizer and index design.*

**Supervisor / first examiner:** Prof. Dr. Katja Zeume. **Second examiner:** Prof. Dr. Gleim,
confirmed — he shaped the index-structure angle and signed the Antrag.

## 2. The research direction

The scope has changed twice — in the meeting of 15.07.2026, and again in the comments of
29.07.2026. This is the current state.

**The thesis is about the language, not about the measurements.**

- **Primary question:** how do models use SQL as a language compared with people — the composition
  of queries (*Aufbau*), the operators they choose (*Operatoren*), and how they express logic
  (*Logik*) — and where do those constructs sit in the development of SQL?
- **Correctness is a control, not a contribution.** The supervisor's position: models already handle
  correctness, so a correctness result is unsurprising. It serves as the **inclusion criterion** —
  only queries matching the reference result enter the structural comparison.
- **Efficiency and execution plans are supporting evidence.** They answer whether a structural
  difference survives the optimizer. Not the headline.
- **Index structures are the extension** (Gleim's proposal, building on the bachelor thesis).
  **This is not a comparison of index types.** The question is whether a generated query can use the
  indexes that exist — index configuration is an experimental condition (present / absent /
  expression index), not a contest between B-tree, GIN and others.
- **NoSQL is named in the framing.** The narrative runs SQL → NoSQL families → vector databases as
  an evolution of query languages.
- **The extensions are deliberately not fixed.** Asked to choose between index structures and a
  second paradigm, the supervisor declined the choice (2026-08-07) and confirmed it again on
  2026-10-27: *"it's good that we have still some open extension possibilities."* Four paths are now
  named as legitimate — docking onto the cited literature and following its structure, extending
  toward NoSQL systems, extending toward index structures, and the one she added herself:
  **SQL operators that invoke a language model** (she raised Snowflake's AI operators — *"SQL can
  also use an LLM call. So, is this used by an LLM or by a human or differently?"*). Individually or
  combined, and trying several during the work is *encouraged*. Do not re-close this into a single
  committed extension. The fourth path is a candidate only; the operators themselves are unverified.
- **Keeping up with the literature is the student's own job**, and reacting to work that appears
  late is expected rather than resented — *"it shows that you work on a very active topic."* Using
  AI tooling for that monitoring was explicitly endorsed (2026-10-27).
- **The one fixed constraint is the focus:** the structure and development of the query language.
  Extensions serve that focus and must not replace it.
- **The plan is held loosely on purpose.** The supervisor's guidance is that a Master's plan should
  not be fixed in every detail up front and that the direction is expected to shift. She found the
  exposé *"a bit too long and too concrete in places"*. Resist over-specification in the thesis.
- **The title is a working title** and can be changed later without formal consequence.

**Key nuance:** the model produces SQL *text*, not an execution plan. The optimizer still compiles
it. The question is whether phrasing survives optimization. Proof that it does not always:
`WHERE upper(city) = 'ESSEN'` versus `WHERE city = 'Essen'` — same rows, but the first prevents an
index on that column from being used.

## 3. Research questions

1. **RQ1 — Language structure.** Which constructs do generated and human-written queries use, and
   how do they differ in *Aufbau*, *Operatoren*, *Logik*?
2. **RQ2 — Evolution.** Where do those constructs sit in the development of SQL — recent
   capabilities, or older idioms?
3. **RQ3 — Optimizer.** Do the differences survive optimization, or converge on the same plan?
4. **RQ4 — Physical design.** Can a generated query use the indexes that are available, and does
   adding or removing an index change the answer to RQ3?

RQ1 and RQ2 need only the query text. RQ3 and RQ4 need execution.

## 4. The corpora question

The hardest constraint: a human-versus-AI comparison needs genuinely human-written reference
queries. The supervisor asked about this directly and called it mandatory. **BIRD alone is not an
acceptable answer** — she asked in a comment attached to the paragraph reporting BIRD's 52.8 %
annotation error rate (Jin et al., CIDR 2026).

| Corpus | Role | Status |
|---|---|---|
| **BIRD Mini-Dev** | Paired experiment (same question → model and reference). A **control**, not the human baseline. | **downloaded 2026-10-25**, PostgreSQL and SQLite variants; all 500 queries profiled |
| **SQLShare** | ~11,000 hand-written statements, 57 scientists, five years | dialect + licence unverified |
| **Join Order Benchmark** | 113 hand-written queries over real IMDB; built to stress optimizers | identified, not downloaded |
| *(the BIRD databases themselves)* | Needed before any query can be generated or executed — the JSON carries question and gold SQL but **no schema** | not downloaded |
| **BEAVER** | Question-SQL pairs from real enterprise query logs | dialect + licence unverified |

The supporting argument: for a *structure* comparison the human side needs no natural-language
pairing at all. Benchmark gold queries were written to annotate a dataset; these were written to do
a job.

## 5. Closely related work

**Pecuchova & Benko (2026), FLAIRS 39** — compared 669 Snowflake queries (189 human, 480 AI) and
found models use nested subqueries where humans use joins, and the reverse. **The construct
comparison is already published.** It measured code metrics (Halstead, cognitive complexity) and
never executed anything, so the open question is whether the differences have consequences. Every
novelty claim must be positioned against this.

**Obtained and read 2026-10-26** — `03_literature/2026-10-26_reading_note_Pecuchova_Benko_FLAIRS.md`.
Verified by full-text search: EXPLAIN, execution plan, optimizer, index and PostgreSQL each occur
**zero** times. Their human baseline is **189 assessment answers from 30 students**, and their own
limitations section calls for *"expand[ing] the human baseline to professional developers"* — so the
corpus argument can be cited rather than asserted.

## 6. Technical setup

- **PostgreSQL.** Always write `EXPLAIN (ANALYZE, BUFFERS)` explicitly — `BUFFERS` is only on by
  default from PostgreSQL 18; the target may be 16/17.
- **Models:** two to three LLMs of differing size. Free APIs available, including NVIDIA-hosted.
- **Timing is untrustworthy** — cold vs. warm cache dominates. Containerised execution, fixed seeds,
  repeated runs, outlier removal. Plan-level signals are the stable evidence.
- **Gold queries are not assumed correct** — validation is part of the method, and a failed
  comparison may mean a bad reference rather than a bad model.
- Known structural patterns with physical consequences: non-sargable predicates, unnecessary joins,
  missing predicates, unnecessary `DISTINCT`, optimization-blocking subqueries/CTEs, wrong
  aggregation level, inefficient `ORDER BY`/`LIMIT` placement.

## 7. Status — 2026-11-24

- **REGISTERED. The deadline is 11.05.2027 inclusive.** The module exam of 05.10.2026 was passed,
  bringing the total to the 78 CP required for admission, and the Prüfungsamt confirmed the
  Zulassung. The Bearbeitungszeit **starts on the day the application was submitted** — not on a
  later issue of the topic — so the clock began in November 2026 and runs to **11 May 2027**.
- **The exposé is approved** (2026-08-07) and the direction was re-confirmed on 2026-10-27. No change
  was requested: *"the pre-research sounds very good"*, *"I'm fairly satisfied with the status of the
  work."*
- **Both examiners confirmed.** Prof. Zeume as first examiner, Prof. Gleim as second; both signed
  the Antrag. The August signature was accepted without renewal, as the Prüfungsamt confirmed.
- Three strands: research question ~35 %, corpora ~65 %, framework ~35 %.
- **Results exist on two corpora.**
  - *BIRD Mini-Dev, text only* — all 500 gold queries profiled and the two variants diffed:
    87.2 % have no subquery nesting, window functions appear in 1 %, 10.8 % contain non-sargable
    predicates (90.7 % of them present before the port), and the PostgreSQL variant is a machine
    port (59.6 % of text differs, 92 % of structure survives).
    See `08_analysis/2026-10-25_gold_query_first_pass.md`.
  - *Spider 1.0, executed* — a pilot of the whole pipeline, **held outside this repository** in
    `C:\Users\mhju1\Downloads\spider_sql_study_nvidia_nim\spider_sql_study_starter`. 30 tasks over
    20 databases, two models, generated SQL executed and compared with the reference. One model uses
    nested SELECT in 9 of 30 responses against 4 of 30 human; the other barely differs, so the effect
    is model-dependent. Nine counterexample tests show that `NOT IN` / `NOT EXISTS` and
    `ORDER BY … LIMIT 1` / `= MAX` agree on benchmark data but diverge under NULLs and ties.
- **Next technical step: obtain the BIRD database data.** The *schemas* turned out to be available
  all along (`06_data/bird-mini-dev/SOURCE.md`, found 2026-11-24), together with the benchmark's own
  prompt template, so generation on BIRD is possible and honest. Only the data is missing, and only
  execution, EXPLAIN and the index work depend on it. The BIRD-versus-Spider question put to Prof.
  Zeume on 27.10 is therefore much less sharp than it looked.
