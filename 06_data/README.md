# 06_data — corpora

**Not version-controlled** (see `.gitignore`). Large, and mostly redistributable only under
the original terms. Each subfolder needs a `SOURCE.md` recording where the data came from,
when it was downloaded, and the licence.

| Folder | Corpus | Role | Status |
|---|---|---|---|
| `bird-mini-dev/` | BIRD Mini-Dev, 500 gold queries, PostgreSQL **and** SQLite variants | Paired experiment: same question to human and model | **downloaded 2026-10-25**, all 500 profiled |
| `sqlshare/` | 11,137 hand-written statements, 57 scientists, 5 years | How humans write SQL in the wild | dialect + licence unverified |
| `job/` | Join Order Benchmark, 113 hand-written queries over real IMDB | Index and optimizer testbed | not downloaded |
| `beaver/` | 9,128 question-SQL pairs from real enterprise query logs | Strongest "genuinely human" claim | dialect + licence unverified |

**The PostgreSQL variant is a machine port.** Measured 2026-10-26: 59.6 % of queries differ
textually from the SQLite original, though 92 % keep their structure. Composition and sargability
survive the port; function- and operator-level counts do not — use the SQLite variant for those.
Details in `08_analysis/2026-10-25_gold_query_first_pass.md`.

**The schemas are here; the data is not.** `baseline_inference/postgresql_schema.json` holds real
PostgreSQL DDL for all 11 databases, together with the benchmark's own prompt template, so query
generation is possible. The databases themselves are a separate, much larger download and are still
needed for execution, EXPLAIN and the index experiments.

Why more than one corpus: BIRD gold queries were written *to annotate a benchmark*.
SQLShare, JOB and BEAVER queries were written *to do a job*. For the language-structure
comparison the latter are better evidence of how humans actually write SQL — and the human
side of that comparison does not need natural-language pairing at all.
