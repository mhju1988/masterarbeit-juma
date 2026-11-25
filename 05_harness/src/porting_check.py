# -*- coding: utf-8 -*-
import io, json, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
rows = json.load(open(sys.argv[1], encoding="utf-8"))
n = len(rows)

pats = {
    "NULLIF(<literal>,0)  div-guard": r"NULLIF\(\s*\d+(\.\d+)?\s*,\s*0\s*\)",
    "NULLIF( anything ,0)": r"NULLIF\(",
    "NULLS LAST / NULLS FIRST": r"NULLS\s+(LAST|FIRST)",
    "SPLIT_PART (pg-only)": r"\bSPLIT_PART\s*\(",
    "CAST(... AS REAL)": r"CAST\s*\([^)]*AS\s+REAL\s*\)",
    "SUBSTR( (sqlite spelling)": r"\bSUBSTR\s*\(",
    "SUBSTRING( (sql std)": r"\bSUBSTRING\s*\(",
    "STRFTIME (sqlite-only)": r"\bSTRFTIME\s*\(",
    "IIF( (sqlite-ism)": r"\bIIF\s*\(",
    "::  (pg cast op)": r"::",
}
print(f"{'pattern':<34}{'queries':>9}{'share':>9}")
for name, p in pats.items():
    c = sum(1 for r in rows if re.search(p, r["sql"], re.I))
    print(f"{name:<34}{c:>9}{c/n*100:>8.1f}%")

any_pat = r"NULLIF\(|NULLS\s+(LAST|FIRST)|SPLIT_PART\s*\(|::"
hit = [r for r in rows if re.search(any_pat, r["sql"], re.I)]
print(f"\nqueries showing at least one porting marker: {len(hit)}  ({len(hit)/n*100:.1f}%)")

print("\n--- clearest examples of mechanical rewriting ---")
for r in rows:
    if re.search(r"NULLIF\(\s*\d+", r["sql"], re.I):
        print(f"\n[{r['question_id']}] {' '.join(r['sql'].split())[:260]}")
        break
for r in rows:
    if re.search(r"SPLIT_PART", r["sql"], re.I):
        print(f"\n[{r['question_id']}] {' '.join(r['sql'].split())[:260]}")
        break
