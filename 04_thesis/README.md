# 04_thesis — the thesis itself (LaTeX)

| Folder | Contents |
|---|---|
| `chapters/` | One `.tex` per chapter; `main.tex` at this level includes them |
| `figures/` | Generated plots copied from `../08_analysis`, plus hand-drawn diagrams |
| `tables/` | Generated `.tex` tables — do not hand-edit anything a script writes |

**Language: English**, deliberately plain — the supervisor explicitly asked for simpler,
non-inflated prose. The German source documents are more formal; do not mirror them.

Figures and tables produced by analysis code must stay regenerable. A number in the thesis
that cannot be traced back to a script in `../08_analysis` will not survive the Kolloquium.
