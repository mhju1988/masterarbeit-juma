# -*- coding: utf-8 -*-
"""Diff the SQLite and PostgreSQL variants of BIRD Mini-Dev.
The difference is the dialect converter's contribution.
Usage: python -I diff_variants.py <sqlite.json> <pg.json>
"""
import io, json, re, sys, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import sqlglot
from sqlglot import exp

sqlite = {r["question_id"]: r for r in json.load(open(sys.argv[1], encoding="utf-8"))}
pg = {r["question_id"]: r for r in json.load(open(sys.argv[2], encoding="utf-8"))}
ids = sorted(set(sqlite) & set(pg))
n = len(ids)
print(f"matched {n} question_ids  (sqlite {len(sqlite)}, pg {len(pg)})\n")

# ---- structural features: shape of the query, independent of function names
STRUCT = ["depth", "joins", "ctes", "subq", "derived", "setop", "window",
          "group_by", "having", "order_by", "limit", "distinct", "case",
          "exists", "in_subq", "union_all"]
# ---- surface features: which functions/operators are spelled out
SURFACE = ["funcs", "casts", "nulls_order"]


def depth(node, d=0):
    best = d
    for sub in node.find_all(exp.Select):
        if sub is node:
            continue
        best = max(best, depth(sub, d + 1))
    return best


def feats(sql, dialect):
    t = sqlglot.parse_one(sql, dialect=dialect)
    f = lambda *k: list(t.find_all(*k))
    names = collections.Counter()
    for fn in f(exp.Func):
        nm = type(fn).__name__.upper()
        if isinstance(fn, exp.Anonymous):
            nm = str(fn.this).upper()
        names[nm] += 1
    return {
        "depth": depth(t), "joins": len(f(exp.Join)), "ctes": len(f(exp.CTE)),
        "subq": max(0, len(f(exp.Select)) - 1),
        "derived": sum(1 for s in f(exp.Subquery) if isinstance(s.parent, (exp.From, exp.Join))),
        "setop": len(f(exp.Union, exp.Intersect, exp.Except)),
        "window": len(f(exp.Window)), "group_by": len(f(exp.Group)),
        "having": len(f(exp.Having)), "order_by": len(f(exp.Order)),
        "limit": len(f(exp.Limit)), "distinct": len(f(exp.Distinct)),
        "case": len(f(exp.Case)), "exists": len(f(exp.Exists)),
        "in_subq": sum(1 for i in f(exp.In) if i.args.get("query")),
        "union_all": sum(1 for u in f(exp.Union) if u.args.get("distinct") is False),
        "funcs": names, "casts": len(f(exp.Cast)),
        "nulls_order": len(re.findall(r"NULLS\s+(LAST|FIRST)", sql, re.I)),
    }


norm = lambda s: " ".join(s.split()).rstrip(";").strip()
identical, struct_same, struct_diff, failed = 0, 0, [], []
fn_added, fn_removed = collections.Counter(), collections.Counter()
changed_keys = collections.Counter()

for qid in ids:
    s_sql, p_sql = sqlite[qid]["SQL"], pg[qid]["SQL"]
    if norm(s_sql).lower() == norm(p_sql).lower():
        identical += 1
    try:
        a, b = feats(s_sql, "sqlite"), feats(p_sql, "postgres")
    except Exception as e:
        failed.append((qid, str(e)[:60]))
        continue
    diffs = [k for k in STRUCT if a[k] != b[k]]
    if diffs:
        struct_diff.append((qid, diffs, a, b))
        for k in diffs:
            changed_keys[k] += 1
    else:
        struct_same += 1
    for name, c in (b["funcs"] - a["funcs"]).items():
        fn_added[name] += c
    for name, c in (a["funcs"] - b["funcs"]).items():
        fn_removed[name] += c

print(f"SQL text byte-identical after whitespace normalisation : {identical:>4}  ({identical/n*100:.1f}%)")
print(f"SQL text differs                                        : {n-identical:>4}  ({(n-identical)/n*100:.1f}%)")
print()
ok = struct_same + len(struct_diff)
print(f"STRUCTURE identical (Aufbau/Operatoren shape)           : {struct_same:>4}  ({struct_same/ok*100:.1f}%)")
print(f"STRUCTURE differs                                       : {len(struct_diff):>4}  ({len(struct_diff)/ok*100:.1f}%)")
if failed:
    print(f"parse failures                                          : {len(failed):>4}")

print("\n-- which structural features the port changed --")
if changed_keys:
    for k, c in changed_keys.most_common():
        print(f"   {k:<12}{c:>4} queries")
else:
    print("   none")

print("\n-- functions the PostgreSQL variant ADDS (top 15) --")
for name, c in fn_added.most_common(15):
    print(f"   {name:<22}{c:>5}")
print("\n-- functions present in SQLite but GONE in PostgreSQL (top 15) --")
for name, c in fn_removed.most_common(15):
    print(f"   {name:<22}{c:>5}")

print("\n-- NULLS LAST/FIRST --")
sl = sum(1 for q in ids if re.search(r"NULLS\s+(LAST|FIRST)", sqlite[q]["SQL"], re.I))
pl = sum(1 for q in ids if re.search(r"NULLS\s+(LAST|FIRST)", pg[q]["SQL"], re.I))
print(f"   sqlite variant: {sl}   postgres variant: {pl}")

print("\n-- examples where STRUCTURE changed --")
for qid, diffs, a, b in struct_diff[:4]:
    print(f"\n[{qid}] changed: {diffs}")
    print(f"  sqlite: { ' '.join(sqlite[qid]['SQL'].split())[:230]}")
    print(f"  pg    : { ' '.join(pg[qid]['SQL'].split())[:230]}")
