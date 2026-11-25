# BIRD Mini-Dev

Source: `https://huggingface.co/datasets/birdsql/bird_mini_dev`
Upstream: BIRD benchmark (Li et al., NeurIPS 2023), Mini-Dev subset.
Licence: the HuggingFace dataset card states CC-BY-SA-4.0 for the mirror —
**verify against the upstream BIRD terms before publishing results.**

## What is here

| File | Size | Downloaded | Revision |
|---|---|---|---|
| `mini_dev_pg.json`, `mini_dev_sqlite.json`, `mini_dev_mysql.json` | 283 KB each | 2026-10-25 | **archive `bird_mini_dev_2025-07-04` — superseded** |
| `current_mini_dev_postgresql.jsonl` | 525 KB | 2026-11-24 | **current: release "Mini-Dev 1024", revision `colleague_review_fixes_20261025`** |
| `current_mini_dev_sqlite.jsonl` | 471 KB | 2026-11-24 | current |
| `current_mini_dev_mysql.jsonl` | 474 KB | 2026-11-24 | current |
| `baseline_inference/postgresql_schema.json` | 80 KB | 2026-11-24 | current |
| `baseline_inference/prompt_template.txt` | 1 KB | 2026-11-24 | current |
| `baseline_inference/manifest.json` | 2 KB | 2026-11-24 | current |

All three `current_*.jsonl` files were verified against the SHA-256 values in `manifest.json` and
match exactly.

## Two things found on 2026-11-24

### 1. The schemas were available all along

`baseline_inference/postgresql_schema.json` holds **real PostgreSQL DDL** for all 11 databases —
75 `CREATE TABLE` statements with column comments, example values, primary keys and foreign keys.
The database names in it match the 11 `db_id` values in the query files exactly.

`prompt_template.txt` is the benchmark's own prompt format, with `{engine}`, `{schema}` and
`{question_block}` placeholders.

**This overturns the assumption recorded since October** that BIRD ships no schema and that
generation would therefore require inventing one from the gold query. Generation on BIRD is possible
and honest, using the benchmark's own schema and its own prompt.

**Still missing: the databases themselves** — the data, not the structure. Those are a separate,
much larger download from the BIRD site and are needed for execution, `EXPLAIN` and the index
experiments. Schemas alone are enough for RQ1 and RQ2, not for RQ3 and RQ4.

### 2. The analysed files are a superseded revision

`mini_dev_pg.json` is 283,551 bytes, byte-identical in size to the archived `2025-07-04` copy on
HuggingFace. The analysis in `08_analysis/2026-10-25_gold_query_first_pass.md` was therefore run on
a revision the maintainers have since replaced.

What the current `manifest.json` records about the newer revision:

- `annotations_modified: true`, with **12 `owner_authorized_corrected_ids`**: 57, 62, 86, 101, 235,
  258, 259, 260, 332, 383, 385, 389
- All 1500 queries (3 dialects x 500) executed with **0 errors and 0 empty results**
- Cross-dialect comparison run on all three pairs: **493 of 500 agree within 0.001**, with 7
  `owner_approved_cross_dialect_exception_ids`: 132, 172, 175, 177, 184, 185, 216
- The `question_id` scheme changed: the old files use the original BIRD dev ids (e.g. 1471), the
  current release uses 0–499. **Matching across revisions needs care; the ids are not comparable.**

**Consequence.** Every number in the first-pass analysis — 87.2 % without nesting, 59.6 % textual
difference, 92 % structural identity, 10.8 % non-sargable — was measured on the superseded files and
should be re-measured on the current release before anything is written up.

The 7 cross-dialect exceptions are worth looking at directly: they are the cases where the
maintainers accept that the dialects do **not** return the same result.
