# Exposé — draft of §7 (Timeline)

Draft, 2026-08-07. Replaces the seven-phase table in the current exposé, which Prof. Zeume
rejected as a waterfall plan in the meeting of 15.07.2026.

Assumptions and open points at the end.

---

## 7 Plan of work

The work is not organised as a sequence of phases. Three strands run in parallel and are already at
different levels of maturity: the research question is partly settled, the benchmark and corpus work
is well advanced, and the measurement framework has not been started. A sequential plan would hold
back the two strands that are further along until the third catches up.

Months are counted from registration.

| Strand | M1 | M2 | M3 | M4 | M5 | M6 |
|---|---|---|---|---|---|---|
| **A — Research question** (from ~30 %) | sharpen, position against related work | construct taxonomy | taxonomy revised against first results | — | interpretation | — |
| **B — Corpora** (from ~60 %) | obtain, check dialects and licences | port, validate reference queries | validation continues | — | — | — |
| **C — Measurement framework** (from 0 %) | — | static analysis layer | first structural results | execution layer | index conditions | — |
| **Exploration** | E1: manual query review | — | — | E2: manual plan experiments | — | — |
| **Writing** | continuous — each strand is written up as it produces results | | | | | |
| **Buffer** | — | — | — | — | — | ~3 weeks unallocated |

### The three strands

**A — Research question.** Sharpening the question, positioning it against related work, and — the
substantive piece — defining the construct taxonomy: what counts as a difference in composition,
in operator choice, and in the expression of logic, and which revision of the SQL standard
introduced each construct. This taxonomy is where strand A feeds strand C, since it is what the
analysis implements.

**B — Corpora.** Obtaining the human-written corpora, checking their SQL dialect and licence terms,
porting where necessary, and validating a sample of the reference queries. Because published
analyses report substantial annotation errors in text-to-SQL benchmarks, this validation is part of
the method rather than a preliminary.

**C — Measurement framework.** Built in three layers, in this order:

1. *Static analysis.* Parses queries and extracts the structural profile. **Requires no database.**
   This layer answers RQ1 and RQ2 and can therefore produce results before any execution
   infrastructure exists.
2. *Execution.* Runs each query pair against PostgreSQL and captures `EXPLAIN (ANALYZE, BUFFERS)`.
   Answers RQ3.
3. *Index conditions.* Repeats the execution layer under varying index configurations. Answers RQ4.

### Exploratory phases

Two are planned explicitly, because both involve decisions that cannot be made from the literature.

**E1 — manual query review (about two weeks, at the start).** Reading real queries from both corpora
by hand before any parser is written. The construct taxonomy has to come from what the queries
actually contain; designing it in the abstract and discovering afterwards that it does not fit the
material would be the more expensive order.

**E2 — manual plan experiments (about one week, before the execution layer).** Running a small
number of query pairs by hand and comparing their plans, to establish which plan signals are stable
enough to automate. Execution time is strongly affected by cache state, so the measures that carry
the argument are expected to be plan-level rather than temporal. Which ones those are is an
empirical question, and it is cheaper to answer before building the pipeline than after.

### Dependencies and independence

Only three orderings are fixed: E1 precedes the construct taxonomy, the static analysis layer
precedes the execution layer, and the execution layer precedes the index conditions. Everything else
can proceed independently, and the strands can absorb delay separately rather than passing it along.
In particular, BIRD Mini-Dev is already available in a PostgreSQL port, so the static analysis layer
can start on it while the remaining corpora are still being obtained.

### Review points and buffer

Supervision meetings every two to three weeks serve as the review points. Each is oriented on the
working document and on results actually obtained, rather than on progress against a schedule.

About three weeks are left unallocated before submission. They are not assigned to a task and are
intended to absorb slippage — most plausibly in strand B, where the licence and dialect of two
corpora are not yet confirmed, or in the execution layer, where measurement noise may require more
repetition than planned.

---

## Assumptions and open points

1. **Six months is assumed to start at registration** and the plan is drawn in months relative to
   it, since the date is not yet fixed. The formal provision for a four-week extension on medical
   grounds is not treated as planning slack.
2. **The plan assumes index structures are the extension**, in line with Prof. Gleim's proposal, and
   does not allocate time to a second query paradigm. If that is reversed, strand C's third layer
   and roughly month 5 change; the rest of the plan does not.
3. **The month boundaries are indicative.** They mark ordering and overlap, not deadlines. If a
   firmer schedule is wanted, it should be fixed after E1, when the size of the taxonomy work is
   known.
4. **Writing is deliberately not a final phase.** The previous version placed it in months 5–6,
   which is the pattern the supervisor rejected. Each strand is written up as it produces results.
5. **Three weeks of buffer is thin** for a six-month project with an unbuilt framework. If the
   corpus checks in month 1 go badly, the honest response is to reduce the number of corpora rather
   than to compress the buffer.
