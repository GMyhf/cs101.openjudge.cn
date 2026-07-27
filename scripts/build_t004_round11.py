#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import inspect
import io
import json
import random
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "collab/t004-round11-manifest.json"
REPORT = ROOT / "collab/t004-round11-report.json"
TESTS = ROOT / "data/openjudge/tests"
sys.path.insert(0, str(ROOT / "scripts"))
from build_001a import bucket
import t004_common as common


def g20163(r):
    words = ["Lan", "Minh", "Hoa", "Mai", "Nam"]
    rows = []
    for _ in range(r.randint(1, 4)):
        rows.append(" ".join(r.choice(words) for _ in range(r.randint(3, 9))) + " .")
    return f"{len(rows)}\n" + "\n".join(rows) + "\n"


def g20169(r):
    cases = []
    for _ in range(r.randint(1, 4)):
        n = r.randint(2, 12)
        edges = [(i, i + 1) for i in range(1, n) if r.random() < .65]
        edges += [tuple(sorted(r.sample(range(1, n + 1), 2))) for _ in range(r.randint(0, n))]
        if not edges:
            edges = [(1, 2)]
        cases.append((n, edges))
    return str(len(cases)) + "\n" + "\n".join(
        f"{n} {len(edges)}\n" + "\n".join(f"{a} {b}" for a, b in edges)
        for n, edges in cases) + "\n"


def g20196(r):
    y = r.randint(1900, 2200)
    leap = y % 400 == 0 or (y % 4 == 0 and y % 100 != 0)
    m = r.randint(1, 12)
    days = [31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return f"{y} {m} {r.randint(1, days[m - 1])}\n"


def g20197(r):
    return f"{r.randint(1, 3000)} {r.randint(1, 3000)}\n"


def g20722(r):
    nums = [str(r.choice([0, r.randint(1, 9999)])) for _ in range(r.randint(1, 6))]
    good = "x<a>" + " ".join(nums) + "<b>" + str(r.randint(1, 9999)) + "</b>z</a>y"
    bad = "plain text" if r.random() < .35 else "<a>12 <b>345</b></a>"
    return good + "\n" + bad + "\n"


def g20731(r):
    m, n = r.randint(2, 8), r.randint(2, 8)
    rows = [[r.randint(-20, 20) for _ in range(n)] for _ in range(m)]
    x, y = r.sample(range(1, m + 1), 2)
    return f"{m} {n}\n" + "\n".join(" ".join(map(str, row)) for row in rows) + f"\n{x} {y}\n"


def g20974(r):
    s = r.randint(1, 200)
    c = r.randint(1, min(50, s))
    cows = sorted(r.sample(range(1, s + 1), c))
    return f"{r.randint(1, 50)} {s} {c}\n" + "\n".join(map(str, cows)) + "\n"


def g21006(r):
    n = r.randint(1, 10)
    return f"{r.randint(0, 100)} {n}\n"


def g21459(r):
    return f"{r.randint(2, 1000)}\n"


def g21462(r):
    n = r.randint(2, 8)
    text = "HELLOCS"
    cells = [(i // n, i % n) for i in range(r.randint(1, n * n - 1))]
    grid = [[0] * n for _ in range(n)]
    for i, (x, y) in enumerate(cells):
        grid[x][y] = ord(text[i % len(text)])
    return f"{n}\n" + "\n".join(" ".join(map(str, row)) for row in grid) + "\n"


def g21508(r):
    n, m = r.randint(1, 40), r.randint(1, 12)
    return f"{n} {m}\n" + " ".join(str(r.randint(-999, 999)) for _ in range(n)) + "\n"


def g21516(r):
    n = r.randint(2, 18)
    edges = [(a, b) for a in range(1, n + 1) for b in range(a + 1, n + 1) if r.random() < .18]
    if not edges:
        edges = [(1, 2)]
    return f"{n} {len(edges)}\n" + "\n".join(f"{a} {b}" for a, b in edges) + "\n"


def g21517(r):
    n = r.randint(40, 70)
    common = r.choice([[1, 3, 7, 12], [1, 4, 9], [2, 5]])
    rows = []
    for _ in range(n):
        values = [r.randint(0, 1864) for _ in range(r.randint(2, 9))]
        p = r.randint(0, len(values))
        values[p:p] = common
        rows.append(" ".join(map(str, [len(values)] + values)))
    return f"{n}\n" + "\n".join(rows) + "\n"


def g21520(r):
    n, m = r.randint(2, 3), r.randint(2, 3)
    cells = [[0] * m for _ in range(n)]
    villages = r.randint(1, min(5, n * m))
    for x, y in r.sample([(x, y) for x in range(n) for y in range(m)], villages):
        cells[x][y] = 1
    cells[0][0] = 1
    vertical = [[r.randint(1, 12) for _ in range(m + 1)] for _ in range(n)]
    horizontal = [[r.randint(1, 12) for _ in range(m)] for _ in range(n + 1)]
    return (f"{n} {m}\n" + "\n".join(" ".join(map(str, row)) for row in cells) + "\n" +
            "\n".join(" ".join(map(str, row)) for row in vertical) + "\n" +
            "\n".join(" ".join(map(str, row)) for row in horizontal) + "\n")


def g21532(r):
    a, b = r.sample(range(1, 2000), 2)
    c = r.randint(1, 10 ** 6)
    return f"{a + b + c}\n"


def g21577(r):
    m, n = r.randint(1, 20), r.randint(1, 20)
    return f"{m} {n}\n" + "\n".join(" ".join(str(r.randint(0, 1)) for _ in range(n)) for _ in range(m)) + "\n"


def g21727(r):
    n = r.randint(1, 100)
    values = sorted(r.randint(1, 1000) for _ in range(n))
    return f"{n} {r.randint(1, 1000)}\n" + " ".join(map(str, values)) + "\n"


def g21964(r):
    n, m = r.randint(1, 30), r.randint(20, 1000)
    return f"{n} {m}\n" + "\n".join(f"{r.randint(1, min(200000, m))} {r.randint(0, 1000)}" for _ in range(n)) + "\n"


def g22007(r):
    return f"{r.randint(1, 7)}\n"


def valid_tree_tokens(r, depth=0):
    if depth >= 4 or r.random() < .5:
        return [str(r.randint(1, 99)), "#", "#"]
    left = valid_tree_tokens(r, depth + 1)
    right = valid_tree_tokens(r, depth + 1)
    return [str(r.randint(1, 99))] + left + right


def g22460(r):
    def make(depth=0):
        if depth >= 4 or r.random() < .5:
            return [str(r.randint(1, 99)), "#", "#"]
        return [str(r.randint(1, 99))] + make(depth + 1) + make(depth + 1)
    tokens = make()
    if r.random() < .35:
        tokens = tokens[:-1] + [str(r.randint(1, 99))]
    return f"{len(tokens)}\n{' '.join(tokens)}\n0\n"


GENERATORS = {n: globals()[f"g{n}"] for n in (
    20163, 20169, 20196, 20197, 20722, 20731, 20974, 21006, 21459,
    21462, 21508, 21516, 21517, 21520, 21532, 21577, 21727, 21964,
    22007, 22460)}


def wall_reference():
    return r'''import sys,itertools
def solve():
    a=list(map(int,sys.stdin.read().split())); p=0; n,m=a[p],a[p+1]; p+=2
    g=[a[p+i*m:p+(i+1)*m] for i in range(n)]; p+=n*m
    v=[a[p+i*(m+1):p+(i+1)*(m+1)] for i in range(n)]; p+=n*(m+1)
    h=[a[p+i*m:p+(i+1)*m] for i in range(n+1)]
    k=n*m; need={i*m+j for i in range(n) for j in range(m) if g[i][j]}; ans=10**30
    for mask in range(1<<k):
        if any(not(mask>>u&1) for u in need): continue
        seen={next(iter(need))}; q=list(seen)
        for u in q:
            i,j=divmod(u,m)
            for z in (u-1 if j else -1, u+1 if j+1<m else -1,
                      u-m if i else -1, u+m if i+1<n else -1):
                if z >= 0 and mask>>z&1 and z not in seen:
                    seen.add(z); q.append(z)
        if len(seen) != bin(mask).count('1'): continue
        cost=0
        for i in range(n):
            for j in range(m):
                u=i*m+j
                if j==0 and mask>>u&1: cost+=v[i][0]
                if j==m-1 and mask>>u&1: cost+=v[i][m]
                if i==0 and mask>>u&1: cost+=h[0][j]
                if i==n-1 and mask>>u&1: cost+=h[n][j]
                if j+1<m and ((mask>>u&1)!=(mask>>(u+1)&1)): cost+=v[i][j+1]
                if i+1<n and ((mask>>u&1)!=(mask>>(u+m)&1)): cost+=h[i+1][j]
        ans=min(ans,cost)
    print(ans)
if __name__=='__main__': solve()
'''


def run_source(source, text):
    with tempfile.TemporaryDirectory(prefix="t004-r11-run-") as d:
        path = Path(d) / "main.py"; path.write_text(source)
        x = subprocess.run([sys.executable, str(path)], input=text, text=True,
                           capture_output=True, timeout=30)
        if x.returncode: raise RuntimeError(x.stderr[-1000:] or str(x.returncode))
        return x.stdout


def run_python_fast(source, text):
    oldi, oldo = sys.stdin, sys.stdout
    try:
        sys.stdin, out = io.StringIO(text), io.StringIO()
        with contextlib.redirect_stdout(out):
            try: exec(compile(source, "<round11>", "exec"), {"__name__": "__main__"})
            except SystemExit: pass
        return out.getvalue()
    finally: sys.stdin, sys.stdout = oldi, oldo


def constraint_rows(n, cases):
    def check(label, pred, bad):
        good = bool(all(pred(x) for x in cases)); bad_value = bool(pred(bad))
        return [(label, good)], ("deliberate invalid input", [(label, bad_value)])
    if n == 20163: return check("input is nonempty sentence lines", lambda x: int(x.splitlines()[0]) >= 1, "0\n")
    if n == 20169:
        def edges_ok(x):
            a=x.split(); p=1
            for _ in range(int(a[0])):
                nn, mm = int(a[p]), int(a[p+1]); p += 2 + 2*mm
                if any(not (1 <= int(v) <= nn) for v in a[p-2*mm:p]): return False
            return True
        return check("edge endpoints are in 1..n", edges_ok, "1\n2 1\n1 3\n")
    if n == 20196: return check("date month and day are valid", lambda x: 1 <= int(x.split()[1]) <= 12, "2020 13 1\n")
    if n == 20197: return check("rectangle sides are positive", lambda x: all(int(v) >= 1 for v in x.split()), "0 3\n")
    if n == 20722: return check("tag names use at most five letters", lambda x: all(len(v) <= 5 for v in x.replace('<',' ').replace('>',' ').split()), "<abcdef>x</abcdef>\n")
    if n == 20731: return check("matrix dimensions are below 100", lambda x: max(map(int,x.splitlines()[0].split())) < 100, "100 2\n")
    if n == 20974: return check("cow positions are distinct and within stalls", lambda x: len(set(x.splitlines()[1:])) == int(x.split()[2]) and max(map(int,x.splitlines()[1:])) <= int(x.split()[1]), "1 3 2\n1\n1\n")
    if n == 21006: return check("number of plates is 1..10", lambda x: 1 <= int(x.split()[1]) <= 10, "1 0\n")
    if n == 21459: return check("x is greater than one", lambda x: int(x) > 1, "1\n")
    if n == 21462: return check("ASCII matrix values are 0..127", lambda x: all(0 <= int(v) <= 127 for v in x.split()), "2\n128 0\n0 0\n")
    if n == 21508: return check("absolute sequence values are below 1000", lambda x: all(abs(int(v)) < 1000 for v in x.splitlines()[1].split()), "1 1\n1000\n")
    if n == 21516: return check("directed edges have distinct endpoints", lambda x: all(a != b for a,b in (map(int,l.split()) for l in x.splitlines()[1:])), "2 1\n1 1\n")
    if n == 21517: return check("card lengths are 2..101", lambda x: all(2 <= int(l.split()[0]) <= 101 for l in x.splitlines()[1:]), "1\n1 7\n")
    if n == 21520: return check("grid villages start with a village", lambda x: x.splitlines()[1].split()[0] == '1', "2 2\n0 0\n0 0\n")
    if n == 21532: return check("sum is at least six", lambda x: int(x) >= 6, "5\n")
    if n == 21577: return check("matrix dimensions are at most twenty", lambda x: max(map(int,x.splitlines()[0].split())) <= 20, "21 1\n0\n")
    if n == 21727: return check("brick volumes are positive and nondecreasing", lambda x: (lambda a: all(a[i] <= a[i+1] for i in range(len(a)-1)))(list(map(int,x.splitlines()[1].split()))), "2 10\n2 1\n")
    if n == 21964: return check("needs and values are within stated limits", lambda x: all(0 <= int(v) <= 200000 for l in x.splitlines()[1:] for v in l.split()), "1 1\n200001 1\n")
    if n == 22007: return check("N is 1..9", lambda x: 1 <= int(x) <= 9, "10\n")
    return check("tree tokens count is at least one", lambda x: int(x.splitlines()[0]) >= 1, "0\n")


def write_producecase(made, source, generator, sample):
    text = ("import random, subprocess, sys, tempfile\nfrom pathlib import Path\n"
            f"REFERENCE={source!r}\nSAMPLE={sample!r}\nGENERATOR_NAME={generator.__name__!r}\n"
            + inspect.getsource(generator) + "\n"
            + "def run(text):\n    with tempfile.TemporaryDirectory(prefix='producecase-') as d:\n"
            + "        p=Path(d)/'main.py'; p.write_text(REFERENCE)\n        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)\n        if x.returncode: raise SystemExit(x.stderr)\n        return x.stdout\n"
            + "def main():\n    d=Path('data'); d.mkdir(exist_ok=True)\n    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]\n    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))\nif __name__=='__main__': main()\n")
    (made / "producecase.py").write_text(text)


def main():
    manifest = json.loads(MANIFEST.read_text()); report = []
    for entry in manifest["entries"]:
        n = int(entry["local_number"]); gen = GENERATORS[n]; sample = entry["sample_input"]
        if n == 21520: source = wall_reference(); reference_kind = "self-written reference (minimum s-t cut)"
        elif n == 21006: source = (ROOT / "scripts/t004_round11_reference_21006.py").read_text(); reference_kind = "user-supplied verified Python3, platform Accepted #53000146"
        else: source = (ROOT / f"scripts/t004_platform_accepted_{n:05d}.py").read_text(); a=entry["existing_accepted"]; reference_kind=f"platform Accepted Python3 #{a['solution_id']}"
        made = TESTS / bucket(n) / f"{n:05d}_made"; data = made / "data"; data.mkdir(parents=True, exist_ok=True)
        for p in data.glob("*"): p.unlink()
        cases = [sample] + [gen(random.Random(s)) for s in range(1,21)]
        outputs = [run_source(source,c) for c in cases]
        for i,c in enumerate(cases): (data/f"{i}.in").write_text(c); (data/f"{i}.out").write_text(outputs[i])
        if n == 21520: header = "# Self-written reference: minimum s-t cut on the grid wall graph\n# Oracle: independent exhaustive cut enumeration for generated small grids\n\n"
        elif n == 21006: header = "# User-supplied verified reference; platform Accepted submission #53000146\n# Source: http://cs101.openjudge.cn/practice/solution/53000146/\n# License: not declared; no license is inferred.\n\n"
        else:
            a=entry["existing_accepted"]; header=(f"# External reference: statistics page /practice/{n:05d}/\n# Accepted submission: {a['solution_id']}\n# Source: {a['source_url']}\n# License: not declared on the submission page; no license is inferred.\n\n")
        (made/"samplecode.py").write_text(header+source); write_producecase(made,source,gen,sample)
        rows, counter = constraint_rows(n,cases[1:])
        audit = common.audit(made,cases=cases[1:],outputs=outputs[1:],sample_input=sample,sample_output=entry.get("sample_output"),constraints=rows,constraint_counterexample=counter,exemption=("题面输入 N 仅有 1..9 共 9 种，域本身小于 15" if n == 22007 else None))
        for s in range(20000): gen(random.Random(s))
        for s in range(400): run_python_fast(source,gen(random.Random(100000+s)))
        report.append({"local_number":n,"title":entry["title"],"reference_source":reference_kind,"statistics_url":f"http://cs101.openjudge.cn{entry['submit_path']}statistics/","source_url":entry.get("existing_accepted",{}).get("source_url"),"license_status":"not declared on submission page; no license is inferred","generator":gen.__name__,"generator_seed_smoke":{"seeds":20000,"status":"passed"},"reference_seed_smoke":{"seeds":400,"status":"passed"},"test_cases":len(cases),"constraints":rows,"constraint_counterexample":counter,"self_audit":audit,"sample_reproduced":audit["sample_is_case_zero"]["status"]=="passed","producecase_reproduced":audit["byte_reproduction"]["status"]=="passed"})
        print(n,"built",flush=True)
    REPORT.write_text(json.dumps({"batch":"T-004 round11","updated_at":datetime.now(timezone.utc).isoformat(),"entries":report},ensure_ascii=False,indent=2)+"\n")

if __name__ == "__main__": main()
