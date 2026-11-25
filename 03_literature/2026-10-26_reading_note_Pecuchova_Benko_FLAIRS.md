# Reading note — Pecuchova & Benko (2026), the closest related work

**Pecuchova, J. & Benko, Ľ. (2026). Structural Differences Between Human and AI-Generated SQL
Queries.** *The International FLAIRS Conference Proceedings* 39(1).
DOI: `10.32473/flairs.39.1.141617` · published 06-05-2026 · CC BY-NC 4.0 · 7 pages.
Both authors: Constantine the Philosopher University in Nitra, Slovakia.

PDF: `03_literature/papers/Pecuchova_2026_StructuralDifferences_HumanAI_SQL.pdf` (obtained 2026-10-26).

Until now §2.3 of the exposé rested on the abstract alone. The full text is read; everything below
is verified against it.

---

## What they did

| | |
|---|---|
| Platform | **Snowflake** |
| Total solutions | 669 |
| Human | **189 submissions from 30 participants** |
| AI | 480, from 3 systems × 4 prompt variants |
| Systems | ChatGPT 5.2, Cortex AI, Claude 4.5 Sonnet |
| Tasks | 4 groups × 10 tasks |
| Human inclusion filter | ≥ 4 of 5 points — *"not a direct execution-based correctness measure"* |
| AI inclusion | first generated solution per condition; correctness assumed, tasks "simple enough" |
| Statistics | nonparametric tests |

**Measures:** verbosity (lines of code, token count, Halstead vocabulary); structural complexity
(Halstead difficulty, cognitive complexity, weighted composite); SQL constructs (CTEs, subqueries,
aggregates, window functions, nesting depth).

## What they found

AI-generated SQL is **significantly higher** on difficulty, nesting depth, subquery use, aggregate
use, CTE use and weighted complexity. Decomposition-oriented prompting reliably increases CTE usage,
and models differ in how sensitive they are to prompt wording.

One nuance worth keeping: *"AI solutions can appear more consistent in aggregate when pooling across
tasks, while human solutions tend to be more consistent within the same task"* — people converge on
a shared task-appropriate formulation once the task is fixed.

---

## What they did not do — verified by full-text search

Occurrences in the complete 27,384-character text:

| term | count |
|---|---|
| EXPLAIN | **0** |
| execution plan | **0** |
| query plan | **0** |
| optimizer / optimiser | **0** |
| index | **0** |
| PostgreSQL | **0** |
| execution time / latency | **0** |
| evolution | **0** |

The paper measures query **text** and never executes anything. The §2.3 claim — that the structural
comparison stops at the text and never reaches the optimizer or the physical design — is now
confirmed against the full paper rather than inferred from the abstract.

They also state explicitly that they *"analyze queries in their original written form rather than
mapping semantically equivalent SQL formulations to a canonical representation."*

---

## Their human baseline is students — and they say so

> *"The human baseline consists of student solutions, while results may differ for professional SQL
> developers. … **Future work should therefore expand the human baseline to professional
> developers**, evaluate additional AI assistants on a larger dataset, and stratify analyses by
> query family (e.g., join-heavy, aggregation-heavy, window-function-driven, or deeply nested
> tasks)."*

189 answers from 30 students in a graded assessment, kept when scored ≥ 4/5.

**This is the single most useful sentence in the paper.** The corpus argument put to the supervisor
in August — that the human baseline should be real working SQL rather than queries written to be
marked — is the authors' own stated future work. It can be cited as such rather than asserted.

---

## How this positions the thesis

Five differences, each now citable rather than claimed:

| | Pecuchova & Benko | this thesis |
|---|---|---|
| Human baseline | 189 student assessment answers | real working SQL — SQLShare, JOB, BEAVER — which their future work calls for |
| Execution | none | `EXPLAIN (ANALYZE, BUFFERS)` on both sides |
| Physical design | not considered | index configuration as an experimental condition |
| System | Snowflake | PostgreSQL, where the plan is fully inspectable |
| Language history | not considered | constructs related to the development of SQL (RQ2) |

Their result is the **premise**, not the competition: the structural difference exists and is
measurable. The open question is whether it has consequences.

### Against the Mini-Dev measurements of 25–26.10

Their finding (AI uses more subqueries, CTEs, nesting) sits directly against the gold-query baseline
measured here: **87.2 % of BIRD gold queries have no nesting at all, 1.2 % use CTEs, 1.0 % use
window functions.**

Two different human populations — their students, BIRD's annotators — both produce structurally
plain SQL. That is a convergence worth noting, and it makes the expected contrast with generated
queries larger rather than smaller.

Caution: the populations differ and so do the platforms (Snowflake vs PostgreSQL), so this is
consistency between two samples, not a replication.

---

## For the exposé and thesis

- §2.3 may now describe their method precisely; the "do not characterise beyond the abstract"
  restriction in `02_expose/draft_sections_2.3_and_3.md` is lifted.
- The novelty claim should cite their future-work sentence rather than assert a gap.
- Their metric set (Halstead, cognitive complexity) is the software-engineering framing §2.3
  criticises — the criticism is accurate and can now quote the paper.
- Reference entry [15] is confirmed: authors, venue, volume, DOI, date.
- Licence CC BY-NC 4.0 — quoting and figure reuse are fine with attribution.
