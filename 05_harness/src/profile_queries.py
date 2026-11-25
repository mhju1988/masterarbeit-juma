# -*- coding: utf-8 -*-
"""First structural pass over BIRD Mini-Dev gold queries (E1 exploration).
Usage: python -I profile_queries.py <path-to-json> [out.json]
"""
import io, json, sys, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import sqlglot
from sqlglot import exp

src = sys.argv[1]
items = json.load(open(src, encoding="utf-8"))

AGG = {"SUM", "COUNT", "AVG", "MIN", "MAX"}


def depth(node, d=0):
    """Max nesting depth of SELECT statements."""
    best = d
    for sub in node.find_all(exp.Select):
        if sub is node:
            continue
        best = max(best, depth(sub, d + 1))
    return best


def analyse(sql):
    t = sqlglot.parse_one(sql, dialect="postgres")
    f = lambda *k: list(t.find_all(*k))

    where_nodes = f(exp.Where)
    # function wrapping a column inside a WHERE predicate -> non-sargable
    nonsarg = []
    for w in where_nodes:
        for fn in w.find_all(exp.Func):
            if isinstance(fn, (exp.Count, exp.Sum, exp.Avg, exp.Min, exp.Max)):
                continue
            if list(fn.find_all(exp.Column)):
                parent = fn.parent
                if isinstance(parent, (exp.EQ, exp.NEQ, exp.GT, exp.LT, exp.GTE,
                                       exp.LTE, exp.Like, exp.ILike, exp.In, exp.Between)):
                    nonsarg.append(fn.sql(dialect="postgres")[:60])

    sel = t if isinstance(t, exp.Select) else (t.find(exp.Select) or t)
    aggs = [a for a in f(exp.AnonymousAggFunc, exp.Count, exp.Sum, exp.Avg, exp.Min, exp.Max)]

    return {
        # Aufbau
        "depth": depth(t),
        "ctes": len(f(exp.CTE)),
        "joins": len(f(exp.Join)),
        "subq_total": max(0, len(f(exp.Select)) - 1),
        "derived": sum(1 for s in f(exp.Subquery) if isinstance(s.parent, (exp.From, exp.Join))),
        # Operatoren
        "window": len(f(exp.Window)),
        "distinct": len(f(exp.Distinct)),
        "group_by": len(f(exp.Group)),
        "having": len(f(exp.Having)),
        "order_by": len(f(exp.Order)),
        "limit": len(f(exp.Limit)),
        "setop": len(f(exp.Union, exp.Intersect, exp.Except)),
        "case": len(f(exp.Case)),
        "agg": len(aggs),
        "cast": len(f(exp.Cast)),
        # Logik
        "exists": len(f(exp.Exists)),
        "in_subq": sum(1 for i in f(exp.In) if i.args.get("query")),
        "not_": len(f(exp.Not)),
        "like": len(f(exp.Like, exp.ILike)),
        "between": len(f(exp.Between)),
        "is_null": sum(1 for n in f(exp.Is) if isinstance(n.expression, exp.Null)),
        "nonsarg": nonsarg,
    }


rows, failed = [], []
for it in items:
    try:
        r = analyse(it["SQL"])
        r["question_id"] = it["question_id"]
        r["db_id"] = it["db_id"]
        r["difficulty"] = it.get("difficulty", "")
        r["sql"] = it["SQL"]
        rows.append(r)
    except Exception as e:
        failed.append((it.get("question_id"), str(e)[:80]))

n = len(rows)
print(f"parsed {n} / {len(items)} gold queries   (failed: {len(failed)})")
print(f"databases: {len(set(r['db_id'] for r in rows))}")
print()

KEYS = [("Aufbau", ["depth", "ctes", "joins", "subq_total", "derived"]),
        ("Operatoren", ["window", "distinct", "group_by", "having", "order_by",
                        "limit", "setop", "case", "agg", "cast"]),
        ("Logik", ["exists", "in_subq", "not_", "like", "between", "is_null"])]

print(f"{'construct':<14}{'queries using':>14}{'share':>9}{'total':>8}")
for group, keys in KEYS:
    print(f"\n-- {group} --")
    for k in keys:
        used = sum(1 for r in rows if r[k] > 0)
        tot = sum(r[k] for r in rows)
        print(f"{k:<14}{used:>14}{used/n*100:>8.1f}%{tot:>8}")

print("\n-- nesting depth distribution --")
for d, c in sorted(collections.Counter(r["depth"] for r in rows).items()):
    print(f"  depth {d}: {c:>4}  ({c/n*100:.1f}%)")

print("\n-- joins per query --")
for j, c in sorted(collections.Counter(min(r["joins"], 5) for r in rows).items()):
    lbl = f"{j}" if j < 5 else "5+"
    print(f"  {lbl} joins: {c:>4}  ({c/n*100:.1f}%)")

ns = [r for r in rows if r["nonsarg"]]
print(f"\n-- non-sargable predicates (function wrapping a column in WHERE) --")
print(f"  {len(ns)} queries ({len(ns)/n*100:.1f}%)")
ex = collections.Counter(x.split("(")[0].upper() for r in ns for x in r["nonsarg"])
for name, c in ex.most_common(10):
    print(f"    {name:<12}{c:>4}")

if failed:
    print("\n-- parse failures --")
    for qid, err in failed[:5]:
        print(f"  {qid}: {err}")

if len(sys.argv) > 2:
    json.dump(rows, open(sys.argv[2], "w", encoding="utf-8"), indent=1)
    print(f"\nwrote {sys.argv[2]}")
