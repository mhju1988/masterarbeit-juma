# 07_experiments — runs and raw output

| Folder | Contents |
|---|---|
| `configs/` | One config per run: models, corpus, index configuration, seeds, repeats |
| `results/` | Raw output. **Append-only — never edit or overwrite a completed run.** |

Name each run `YYYY-MM-DD_<what-varied>` so the question it answers is visible from the
folder name.

Every run must record enough to be reproduced: model and version, prompt, corpus version,
PostgreSQL version, index configuration, seeds, repeat count, hardware. A result whose
conditions were not recorded is not a result.
