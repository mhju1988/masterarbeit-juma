# First structural pass over the BIRD Mini-Dev gold queries

2026-10-25, extended 2026-10-26 with the SQLite/PostgreSQL diff. Exploratory phase E1, as described in the exposé: read the real queries before building
anything. Prepared for the supervision meeting of 27.10.2026.

> ## ⚠ Superseded input — added 2026-11-24
>
> Every figure in this document was measured on `mini_dev_pg.json` / `mini_dev_sqlite.json`,
> downloaded 25.10.2026. Those files are the **archived `2025-07-04` revision**; the BIRD
> maintainers have since replaced them.
>
> The current release — "Mini-Dev 1024", revision `colleague_review_fixes_20261025` — is in
> `06_data/bird-mini-dev/current_mini_dev_*.jsonl`, hash-verified against the official manifest.
> It carries **12 corrected gold queries**, records all 1500 queries executing with 0 errors, and
> reports 493 of 500 agreeing across dialects within 0.001 (7 approved exceptions). The
> `question_id` scheme changed too, so ids are **not** comparable between revisions.
>
> **Re-run before citing.** The scripts take a file path; the only change needed is reading JSON
> Lines instead of a JSON array. Details in `06_data/bird-mini-dev/SOURCE.md`.

**Method.** All 500 gold queries of the Mini-Dev PostgreSQL variant parsed into an abstract syntax
tree with `sqlglot` (PostgreSQL dialect) and profiled along the three dimensions from the exposé —
*Aufbau*, *Operatoren*, *Logik*. 500 of 500 parsed without error, across 11 databases. No database
was executed; this is text analysis only.

Code: `05_harness/src/{profile_queries,diff_variants,nonsarg_origin}.py` · Output:
`07_experiments/results/2026-10-25_gold_profile.json`

---

## What the human reference queries actually look like

### Aufbau — they are flat

| | queries | share |
|---|---|---|
| no subquery nesting at all | 436 | **87.2 %** |
| one level of nesting | 58 | 11.6 % |
| two or more levels | 6 | 1.2 % |
| use at least one join | 407 | **81.4 %** |
| common table expressions | 6 | **1.2 %** |
| derived tables in FROM | 24 | 4.8 % |

Joins per query: 18.6 % none, 61.0 % exactly one, 17.2 % two, 3.2 % three or more.

The characteristic gold query is a single join with an aggregate and no nesting — 124 queries match
that shape exactly.

### Operatoren — a narrow slice of the language

| construct | share | | construct | share |
|---|---|---|---|---|
| aggregates | 49.2 % | | CASE | 19.0 % |
| CAST | 24.2 % | | DISTINCT | 16.8 % |
| ORDER BY | 21.2 % | | GROUP BY | 11.4 % |
| LIMIT | 20.0 % | | HAVING | 2.8 % |
| **window functions** | **1.0 %** | | **set operations** | **0.4 %** |

### Logik

EXISTS 0.4 % · IN-with-subquery 2.2 % · NOT 4.6 % · LIKE 4.2 % · BETWEEN 5.8 % · IS NULL 8.0 %

---

## Four findings

### 1. The human baseline uses old SQL

Window functions appear in 5 queries out of 500. CTEs in 6. Set operations in 2. EXISTS in 2.
Almost everything is expressible in SQL-92: joins, aggregates, GROUP BY, CASE.

This gives RQ2 a measured starting point. If generated queries reach for window functions and CTEs
at anything above a few per cent, the contrast against a 1 % baseline is immediate and large. It
also sharpens the question: is the gold set old-fashioned because *people* write that way, or
because a benchmark annotator writes the simplest thing that returns the right rows?

### 2. One in nine reference queries already defeats an index

54 queries (10.8 %) wrap a column in a function inside a WHERE predicate — the `upper(city)` pattern
from the supervision meeting, present in the **human** reference set.

`TO_CHAR` 29 · `SUBSTRING` 15 · `EXTRACT` 9 · `CAST` 6 · `RIGHT` 3 · `DATE` 2 · `LENGTH` 1

Example — four queries over `debit_card_specializing` all filter a year this way:

```sql
WHERE SUBSTR(T2.Date, 1, 4) = '2013' AND T1.Segment = 'SME'
```

**But the schema invites it.** `yearmonth.Date` is stored as text, so substring extraction is the
only way to get a year. The non-sargability comes from the data model, not from carelessness. That
is worth saying plainly rather than presenting these as human error — and it is itself an argument
for RQ4: whether a predicate can use an index is a property of the schema and the available indexes
as much as of the phrasing.

These 54 queries are a ready-made target set for the index-configuration experiments.

### 3. The PostgreSQL variant is not purely human-written text — 36.4 %

This is the most consequential finding, and it was not expected.

| marker | queries | share |
|---|---|---|
| `NULLIF(…, 0)` division guards | 96 | 19.2 % |
| `NULLS LAST` / `NULLS FIRST` added to ORDER BY | 84 | 16.8 % |
| `::` PostgreSQL cast operator | 9 | 1.8 % |
| `SPLIT_PART` (PostgreSQL-only) | 4 | 0.8 % |
| **at least one marker** | **182** | **36.4 %** |

The clearest case:

```sql
SELECT AVG(T2.Consumption) / NULLIF(12, 0) FROM ...
```

No person writes `NULLIF(12, 0)`. Dividing by the literal 12 and guarding it against division by
zero is a mechanical rewrite. Likewise `NULLS LAST`, added because SQLite and PostgreSQL order NULLs
differently — a porting fix, not an authorial choice.

**Consequence.** Mini-Dev's PostgreSQL variant is human SQL passed through an automated dialect
conversion. Finding 5 below establishes how far that reaches.

### 4. The method works

500 of 500 queries parsed with no failures, and the three exposé dimensions map onto AST features
without strain. The static-analysis layer is viable as described, and it needed no database, no
Docker and no model API.

### 5. The port changed surface, not shape — and that is measurable

The SQLite variant of the same 500 questions was downloaded and profiled identically, then matched
on `question_id`. The difference between the two is the converter's contribution.

| | queries | share |
|---|---|---|
| SQL text identical after whitespace normalisation | 202 | 40.4 % |
| SQL text differs | 298 | **59.6 %** |
| **structure identical** (nesting, joins, CTEs, subqueries, window, set ops, GROUP BY, DISTINCT) | 460 | **92.0 %** |
| structure differs | 40 | 8.0 % |

So three fifths of the queries were textually rewritten, but nine tenths kept their shape.

**Where structure did change, it is almost entirely CASE** — 37 of the 40 queries. Two SQLite idioms
have no PostgreSQL equivalent and force one:

```sql
-- SQLite: a comparison is 0/1 and can be summed directly
SELECT CAST(SUM(status = 'C') AS REAL) * 100 / COUNT(account_id) FROM loan WHERE amount < 100000
-- PostgreSQL: rewritten with CASE, and the divisor guarded
SELECT CAST(SUM(CASE WHEN status = 'C' THEN 1 ELSE 0 END) AS REAL) * 100
       / NULLIF(COUNT(account_id), 0) FROM loan WHERE amount < 100000
```

`IIF(a, b, c)` → `CASE WHEN a THEN b ELSE c END` does the same. **The 19.0 % CASE figure reported
above is therefore inflated by roughly 7 percentage points**; human CASE usage is nearer 12 %.

**Function-level surface is rewritten heavily.** Added by the port: `NULLIF` 107, `CAST` 67, `CASE`
63, `EXTRACT` 40, `SPLIT_PART` 32. Removed: SQLite's `STRFTIME` family 113, `INSTR` 25, `JULIANDAY`
3. `NULLS LAST` / `NULLS FIRST` goes from **0 occurrences in SQLite to 84 in PostgreSQL** — entirely
the converter, compensating for the two systems ordering NULLs differently.

**The non-sargability is genuine.** Of the 54 queries with a function wrapping a column in WHERE,
**49 (90.7 %) were already non-sargable in the SQLite original.** The port renamed the function —
`STRFTIME` became `EXTRACT` or `TO_CHAR` — without changing what the predicate does to an index. The
5 converter-introduced cases are `::text` and `::integer` casts added for type compatibility.

### What this means in practice

| dimension | status on the PostgreSQL variant |
|---|---|
| ***Aufbau*** — nesting, joins, CTEs, subqueries, derived tables | **Usable.** 92 % structural identity, and the 8 % is isolated to CASE. |
| ***Operatoren*** — at the level of function and operator names | **Contaminated.** Use the SQLite variant as the human reference, or exclude converter-touched constructs. |
| ***Logik*** — predicate placement, sargability | **Usable.** 91 % of the sargability signal survives from the original. |

This is a better outcome than finding 3 alone suggested. The porting problem is real but bounded,
and the boundary can be stated precisely rather than guessed at. It also means the comparison of
*composition* — the dimension carrying most of RQ1 — can proceed on the PostgreSQL variant without
further work.

It does not remove the argument for SQLShare, the Join Order Benchmark and BEAVER. Benchmark gold
queries remain queries written to annotate a dataset, whatever dialect they are in.

---

## Open questions for the meeting

1. Does a flat, SQL-92-shaped baseline change what we expect to find? If models write more deeply
   nested SQL, the contrast is sharp — but the gold set may be flat because of how it was produced.
2. The porting artifacts are now bounded: *Aufbau* is safe, function-level *Operatoren* is not.
   Is using the SQLite variant for the operator comparison and the PostgreSQL variant for execution
   a sound division, or does mixing variants create a problem of its own?
3. Is the schema-driven non-sargability (dates stored as text) a finding in its own right, or a
   confound to control for?
4. Does the 36 % figure strengthen the case for obtaining SQLShare / JOB / BEAVER sooner?

## Limitations

- Benchmark gold queries only. Nothing here says how people write SQL at work; that is what the
  other corpora are for.
- "Non-sargable" is determined syntactically — a function wrapping a column inside a WHERE
  comparison. Whether an index actually exists, and whether the planner could still use it, requires
  execution and is not claimed here.
- The porting markers are heuristics. `NULLIF` and `NULLS LAST` are legitimate SQL that a person
  could write; the inference rests on their frequency and on cases like `NULLIF(12, 0)` that have no
  authorial reading.
- No SQL standard revision is named anywhere above. Assigning constructs to revisions needs checking
  against ISO/IEC 9075 and has not been done.
