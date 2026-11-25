# Generated Queries and the Evolution of SQL

A structural comparison with human-written queries, and its consequences for optimizer and index
design.

Master's thesis, Westfälische Hochschule, Fachbereich Informatik und Kommunikation.
Written in English.

| | |
|---|---|
| **Author** | Mohamad Juma |
| **First examiner** | Prof. Dr. Katja Zeume |
| **Second examiner** | Prof. Dr. Gleim |
| **Registered** | November 2026 |
| **Submission deadline** | 11 May 2027 |

## The question

Not whether language models write *correct* SQL — they largely do, and that result would be
unsurprising. The question is how they use SQL **as a language** compared with people: the
composition of their queries, the operators they choose, how they express logic, and where those
constructs sit in the development of the language.

Two further questions follow from it. Do the differences survive the optimizer, or does the planner
erase them? And can a generated query use the indexes that exist?

## Where things are

| Folder | Contents |
|---|---|
| `02_expose/` | The exposé |
| `03_literature/` | Reading notes and BibTeX |
| `04_thesis/` | The thesis itself |
| `05_harness/` | The measurement code |
| `08_analysis/` | Results, figures and tables |
| `01_supervision/` | Meeting protocols and the record of supervisor requirements |
| `00_admin/` | Formalities |
| `06_data/`, `07_experiments/` | Documentation only — the corpora and raw results are not version-controlled, for size and licence reasons. Each folder records where its data came from. |

Start with `CONTEXT.md` for the scope and research direction, and
`08_analysis/` for what has been measured so far.

## Status

The static-analysis layer runs: all 500 BIRD Mini-Dev gold queries have been parsed and profiled
along the three dimensions of composition, operators and logic, and the SQLite and PostgreSQL
variants have been compared. A pilot of the full pipeline — question, model, generated SQL,
execution, comparison against the reference result — runs on Spider 1.0.

The PostgreSQL execution layer, which carries the optimizer and index questions, is the next piece
of work.

## A note on this repository

It exists so that the supervision record and the analyses are not lost, and so that anything
discussed can be looked up later. It is a working repository, not a finished document; the thesis
itself is in `04_thesis/`.
