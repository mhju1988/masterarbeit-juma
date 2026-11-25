# -*- coding: utf-8 -*-
import io, json, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
rows = json.load(open(sys.argv[1], encoding="utf-8"))

def show(title, sel, limit=3, maxlen=320):
    hits = [r for r in rows if sel(r)]
    print(f"\n{'='*76}\n{title}  —  {len(hits)} queries\n{'='*76}")
    for r in hits[:limit]:
        s = " ".join(r["sql"].split())
        print(f"\n[{r['question_id']}] db={r['db_id']}  depth={r['depth']} joins={r['joins']}")
        print(f"  {s[:maxlen]}{'...' if len(s)>maxlen else ''}")
        if r["nonsarg"]:
            print(f"  NON-SARGABLE: {r['nonsarg'][:3]}")

show("WINDOW FUNCTIONS", lambda r: r["window"] > 0, 5)
show("CTEs (WITH)", lambda r: r["ctes"] > 0, 3)
show("DEEPEST NESTING", lambda r: r["depth"] >= 2, 3)
show("NON-SARGABLE PREDICATES", lambda r: r["nonsarg"], 4)
show("TYPICAL: flat, single join, aggregate",
     lambda r: r["depth"] == 0 and r["joins"] == 1 and r["agg"] > 0, 3)
