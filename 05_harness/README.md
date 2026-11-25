# 05_harness — the measurement code

The main engineering deliverable.

**Layer 1 (static analysis) works** as of 2026-10-26 — `src/` holds five scripts that profile query
structure with `sqlglot`, needing no database:

| script | what it does |
|---|---|
| `profile_queries.py` | Profiles a corpus along *Aufbau* / *Operatoren* / *Logik* |
| `diff_variants.py` | Diffs two dialect variants to isolate a converter's contribution |
| `nonsarg_origin.py` | Traces whether a non-sargable predicate predates a port |
| `show_examples.py` | Pulls example queries by category |
| `porting_check.py` | Counts dialect-conversion markers |

    python src/profile_queries.py ../06_data/bird-mini-dev/mini_dev_pg.json out.json

**Layer 2 (execution) has not been started.** It needs the BIRD database *data*, which has not been
obtained. The schemas are available — see `06_data/bird-mini-dev/SOURCE.md` — so generation is not
blocked; only execution, EXPLAIN and the index work are.

| Folder | Contents |
|---|---|
| `src/` | Pipeline code |
| `sql/` | Schema setup, index definitions, `EXPLAIN` helpers |
| `docker/` | Containerised PostgreSQL — required for reproducible timing |
| `tests/` | Tests. Running a single benchmark item is the primary debugging loop. |

## Two layers, and they are independent

**1. Static analysis — needs no database.** Parse queries and extract the structure
profile: *Aufbau* (nesting, CTE vs. subquery vs. join), *Operatoren* (which constructs
appear), *Logik* (predicate placement, negation, quantification). This answers the
supervisor's primary question and can produce results before any execution infrastructure
exists. Build this first.

**2. Execution — needs PostgreSQL.** Per item: run the AI query *and* the human reference,
capture `EXPLAIN (ANALYZE, BUFFERS)`, compute correctness, efficiency and plan metrics.
Answers whether a structural difference survives the optimizer.

## Constraints that shape the design

- **Always write `EXPLAIN (ANALYZE, BUFFERS)` explicitly.** `BUFFERS` is only on by default
  from PostgreSQL 18; the target may be 16/17.
- **Both queries per item, always.** Every core metric is relative to the human reference.
- **Timing is untrustworthy.** Cold vs. warm cache dominates. Repeated runs, fixed seeds,
  outlier removal, containerised execution. Plan-level signals (buffers, estimated vs.
  actual rows, rows removed by filter, temp spills) are the stable evidence.
- **Reference queries are not assumed correct.** BIRD's documented annotation errors mean
  gold-query validation needs a place in the pipeline *and* in the result schema.
- **Index configuration is an experimental variable, not a fixture.** B-tree vs. GIN,
  PostgreSQL only (decided). The same query set runs under different index setups.

Document the real commands here once they exist — especially how to run a single item.
