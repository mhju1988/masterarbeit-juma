# -*- coding: utf-8 -*-
"""Was the non-sargable predicate already in the SQLite original, or added by the port?"""
import io, json, sys, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import sqlglot
from sqlglot import exp

sqlite = {r["question_id"]: r for r in json.load(open(sys.argv[1], encoding="utf-8"))}
pg = {r["question_id"]: r for r in json.load(open(sys.argv[2], encoding="utf-8"))}
AGGS = (exp.Count, exp.Sum, exp.Avg, exp.Min, exp.Max)
CMP = (exp.EQ, exp.NEQ, exp.GT, exp.LT, exp.GTE, exp.LTE, exp.Like, exp.ILike, exp.In, exp.Between)


def nonsarg(sql, dialect):
    t = sqlglot.parse_one(sql, dialect=dialect)
    out = []
    for w in t.find_all(exp.Where):
        for fn in w.find_all(exp.Func):
            if isinstance(fn, AGGS):
                continue
            if list(fn.find_all(exp.Column)) and isinstance(fn.parent, CMP):
                nm = type(fn).__name__.upper()
                if isinstance(fn, exp.Anonymous):
                    nm = str(fn.this).upper()
                out.append(nm)
    return out


both, only_pg, only_sq = [], [], []
for qid in sorted(set(sqlite) & set(pg)):
    try:
        s, p = nonsarg(sqlite[qid]["SQL"], "sqlite"), nonsarg(pg[qid]["SQL"], "postgres")
    except Exception:
        continue
    if p and s:
        both.append((qid, s, p))
    elif p and not s:
        only_pg.append((qid, p))
    elif s and not p:
        only_sq.append((qid, s))

tot = len(both) + len(only_pg)
print(f"queries with a non-sargable predicate in the PostgreSQL variant : {tot}")
print(f"  ... also non-sargable in the SQLite original (genuine)        : {len(both)}  ({len(both)/tot*100:.1f}%)")
print(f"  ... non-sargable ONLY after porting (converter-introduced)    : {len(only_pg)}  ({len(only_pg)/tot*100:.1f}%)")
print(f"non-sargable in SQLite but no longer in PostgreSQL              : {len(only_sq)}")

print("\n-- how the wrapping function was renamed (genuine cases) --")
pairs = collections.Counter((tuple(sorted(set(s))), tuple(sorted(set(p)))) for _, s, p in both)
for (s, p), c in pairs.most_common(8):
    print(f"   {'+'.join(s):<28} ->  {'+'.join(p):<28}{c:>4}")

if only_pg:
    print("\n-- converter-introduced examples --")
    for qid, p in only_pg[:3]:
        print(f"\n[{qid}] now wraps: {p}")
        print(f"  sqlite: {' '.join(sqlite[qid]['SQL'].split())[:200]}")
        print(f"  pg    : {' '.join(pg[qid]['SQL'].split())[:200]}")
