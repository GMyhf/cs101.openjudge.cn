#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import concurrent.futures
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
MANIFEST = ROOT / "collab/t004-round12-manifest.json"
REPORT = ROOT / "collab/t004-round12-report.json"
TESTS = ROOT / "data/openjudge/tests"
sys.path.insert(0, str(ROOT / "scripts"))
from build_001a import bucket
import t004_common as common


def g22507(r):
    n = r.randint(2, 9); chars = list("ABCDEFGHIJKLMNO")[:n]
    if r.random() < .25: return "".join(chars) + " " + "".join(chars[1:] + chars[:1]) + "\n"
    def tree(items):
        if not items: return [], []
        if len(items) == 1: return items, items
        cut = r.randint(1, len(items)-1)
        a,b=tree(items[1:1+cut]),tree(items[1+cut:])
        return [items[0]]+a[0]+b[0], a[1]+b[1]+[items[0]]
    pre, post = tree(chars)
    return "".join(pre) + " " + "".join(post) + "\n"


def g22548(r):
    n=r.randint(2,40); a=[r.randint(0,10000) for _ in range(n)]
    if r.random()<.5: a.sort(reverse=True)
    return " ".join(map(str,a))+"\n"


def g22549(r):
    letters="abcdefghijklmnopqrstuvwxyz"; n=r.randint(1,60)
    return "".join(r.choice(letters) for _ in range(n))+"\n"


def g23163(r):
    n=r.randint(2,20); edges=[(i,i+1) for i in range(n-1) if r.random()<.65]
    edges += [tuple(r.sample(range(n),2)) for _ in range(r.randint(0,n))]
    if not edges: edges=[(0,1)]
    return f"{n} {len(edges)}\n"+"\n".join(f"{a} {b}" for a,b in edges)+"\n"


def g23454(r):
    words=["alpha","beta","gamma","delta"]
    return ((" "*r.randint(1,8)).join(words[:r.randint(2,4)])+"\n")


def g23556(r): return f"{r.randint(1,1000)}\n"


def g23566(r):
    n,m=r.randint(2,20),r.randint(2,8); items=[(r.randint(1,m),r.randint(1,300)) for _ in range(n)]
    coupons=[(q,r.randint(1,q)) for q in [r.randint(1,1000) for _ in range(m)]]
    return f"{n} {m}\n"+"\n".join(f"{a} {b}" for a,b in items)+"\n"+"\n".join(f"{a}-{b}" for a,b in coupons)+"\n"


def g23654(r): return f"{r.randint(1000,9000)}\n"


def g23719(r): return f"{r.uniform(.1,1000):.5f} {r.uniform(.1,1000):.5f}\n"


def g23741(r): return f"{r.randint(1,24)}\n"


def g23742(r): return f"{r.randint(10000101,50001231)}\n"


def g23744(r):
    costs=[r.uniform(.1,5) for _ in range(3)]; names=["a","b","c"]
    pts=[(r.randint(-99,99),r.randint(-99,99)) for _ in range(3)]
    return " ".join(map(str,costs))+"\n"+"\n".join(f"{s} {x} {y}" for s,(x,y) in zip(names,pts))+"\n"


def g23745(r):
    n=r.randint(1,5); return f"{n}\n"+" ".join(str(r.randint(1,100)) for _ in range(n))+"\n"+" ".join(str(r.randint(1,100)) for _ in range(n))+"\n"


def g23804(r):
    n,m=r.randint(2,15),r.randint(1,8); ans=[r.choice("ABCD") for _ in range(n)]
    rows=[" ".join(r.choice("ABCD") for _ in range(n)) for _ in range(m)]
    return f"{n} {m}\n"+" ".join(ans)+"\n"+"\n".join(rows)+"\n"


def g23805(r):
    n=r.randint(1,10); rows=[]
    for _ in range(n): rows.append(f"{r.randint(0,23)}:{r.randint(0,59)}:{r.randint(0,59)} {r.randint(1,28)}.{r.randint(1,12)}.{r.randint(2000,50000)}")
    return f"{n}\n"+"\n".join(rows)+"\n"


def g23807(r): return f"{r.randint(3,10)} {r.randint(1,12)}\n"


def g23997(r): return f"{r.randint(1,35)}\n"


def g24192(r): return f"{r.randint(1,1000000)} {r.randint(1,1000000)}\n"


def g24510(r):
    n=r.randint(2,20); rows=[]
    for i in range(n):
        a=r.randint(0,23)*3600+r.randint(0,59)*60+r.randint(0,59); b=a+r.randint(0,1000)
        rows.append(f"page{r.randint(1,5)} {a//3600:02d}:{a//60%60:02d}:{a%60:02d} {b//3600:02d}:{b//60%60:02d}:{b%60:02d}")
    return f"{n}\n"+"\n".join(rows)+"\n"


def g24607(r):
    n=r.randint(1,100); k=r.randint(1,n); return f"{n} {k}\n"+"".join(r.choice("HG") for _ in range(n))+"\n"


GENERATORS = {n: globals()[f"g{n}"] for n in (
    22507,22548,22549,23163,23454,23556,23566,23654,23719,23741,
    23742,23744,23745,23804,23805,23807,23997,24192,24510,24607)}


def run_source(source, text):
    with tempfile.TemporaryDirectory(prefix="t004-r11-run-") as d:
        path = Path(d) / "main.py"; path.write_text(source)
        x = subprocess.run([sys.executable, str(path)], input=text, text=True,
                           capture_output=True, timeout=30)
        if x.returncode: raise RuntimeError(x.stderr[-1000:] or str(x.returncode))
        return x.stdout


def run_cpp_many(source, texts):
    with tempfile.TemporaryDirectory(prefix="t004-r11-cpp-") as d:
        d = Path(d); src = d / "main.cpp"; exe = d / "main"
        src.write_text(source)
        build = subprocess.run(["g++", "-std=c++17", "-O2", str(src), "-o", str(exe)],
                               capture_output=True, text=True, timeout=60)
        if build.returncode:
            raise RuntimeError(build.stderr[-1000:])
        outputs = []
        for text in texts:
            x = subprocess.run([str(exe)], input=text, text=True, capture_output=True, timeout=30)
            if x.returncode:
                raise RuntimeError(x.stderr[-1000:] or str(x.returncode))
            outputs.append(x.stdout)
        return outputs


def run_python_fast(source, text):
    oldi, oldo = sys.stdin, sys.stdout
    try:
        sys.stdin, out = io.StringIO(text), io.StringIO()
        with contextlib.redirect_stdout(out):
            try: exec(compile(source, "<round11>", "exec"), {"__name__": "__main__"})
            except SystemExit: pass
        return out.getvalue()
    finally: sys.stdin, sys.stdout = oldi, oldo


def run_python_many(source, texts):
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(lambda text: run_source(source, text), texts))


def constraint_rows(n, cases):
    def check(label, pred, bad):
        good = bool(all(pred(x) for x in cases)); bad_value = bool(pred(bad))
        return [(label, good)], (bad, [(label, bad_value)])
    if n == 22507: return check("pre/post strings use unique symbols", lambda x: (lambda a,b: len(a)==len(b) and len(set(a))==len(a) and len(set(b))==len(b))(x.split()[0],x.split()[1]), "AA AA\n")
    if n == 22548: return check("prices are nonnegative and at most 10000", lambda x: all(0<=int(v)<=10000 for v in x.split()), "10001\n")
    if n == 22549: return check("string contains only lowercase letters", lambda x: x.strip().islower() and x.strip().isalpha(), "A\n")
    if n == 23163: return check("edge endpoints are valid distinct vertices", lambda x: all(0<=int(v)<int(x.split()[0]) for l in x.splitlines()[1:] for v in l.split()) and all(a!=b for a,b in (map(int,l.split()) for l in x.splitlines()[1:])), "2 1\n0 2\n")
    if n == 23454: return check("sentence has no leading or trailing spaces", lambda x: x==x.strip()+"\n", " leading\n")
    if n == 23556: return check("number of leaves is 1..1000", lambda x: 1<=int(x)<=1000, "0\n")
    if n == 23566: return check("coupon discount is nonnegative", lambda x: all(int(l.split('-')[0])>=int(l.split('-')[1]) for l in x.splitlines()[1+int(x.split()[0]):]), "2 2\n1 10\n2 10\n5-6\n5-1\n")
    if n == 23654: return check("year is a four digit number", lambda x: 1000<=int(x)<=9000, "999\n")
    if n == 23719: return check("land dimensions are positive", lambda x: all(float(v)>0 for v in x.split()), "0 1\n")
    if n == 23741: return check("Catalan index is 1..24", lambda x: 1<=int(x)<=24, "25\n")
    if n == 23742: return check("date bound is within stated range", lambda x: 10000101<=int(x)<=50001231, "9999999\n")
    if n == 23744: return check("part coordinates are within -100..100", lambda x: all(-100<int(v)<100 for l in x.splitlines()[1:] for v in l.split()[1:]), "1 1 1\na 100 0\nb 0 0\nc 0 0\n")
    if n == 23745: return check("food count is 1..5", lambda x: 1<=int(x.splitlines()[0])<=5, "6\n1 1 1 1 1 1\n1 1 1 1 1 1\n")
    if n == 23804: return check("answer choices are A..D", lambda x: all(v in 'ABCD' for l in x.splitlines()[1:] for v in l.split()), "1 1\nE\nE\n")
    if n == 23805: return check("years are at least 2000", lambda x: all(int(l.split()[1].split('.')[2])>=2000 for l in x.splitlines()[1:]), "1\n0:0:0 1.1.1999\n")
    if n == 23807: return check("poles and discs are within 3..100", lambda x: 3<=int(x.split()[0])<=100 and 1<=int(x.split()[1])<=100, "2 1\n")
    if n == 23997: return check("N is 1..100", lambda x: 1<=int(x)<=100, "0\n")
    if n == 24192: return check("dimensions are 1..1000000", lambda x: all(1<=int(v)<=1000000 for v in x.split()), "0 1\n")
    if n == 24510: return check("record count is positive", lambda x: int(x.splitlines()[0])>=1, "0\n")
    if n == 24607: return check("K is between 1 and N", lambda x: 1<=int(x.split()[1])<=int(x.split()[0]), "3 4\nHHH\n")
    raise AssertionError(n)


def write_producecase(made, source, generator, sample, language="python"):
    if language == "cpp":
        text = ("import random, subprocess, tempfile\nfrom pathlib import Path\n"
                f"REFERENCE={source!r}\nSAMPLE={sample!r}\nGENERATOR_NAME={generator.__name__!r}\n"
                + inspect.getsource(generator) + "\n"
                + "def run(text):\n    with tempfile.TemporaryDirectory(prefix='producecase-') as d:\n"
                + "        d=Path(d); p=d/'main.cpp'; exe=d/'main'; p.write_text(REFERENCE)\n        c=subprocess.run(['g++','-std=c++17','-O2',str(p),'-o',str(exe)],capture_output=True,text=True,timeout=60)\n        if c.returncode: raise SystemExit(c.stderr)\n        x=subprocess.run([str(exe)],input=text,text=True,capture_output=True,timeout=30)\n        if x.returncode: raise SystemExit(x.stderr)\n        return x.stdout\n"
                + "def main():\n    d=Path('data'); d.mkdir(exist_ok=True)\n    cases=[SAMPLE]+(['8\\n','9\\n'] if GENERATOR_NAME == 'g22007' else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]\n    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))\nif __name__=='__main__': main()\n")
        (made / "producecase.py").write_text(text)
        return
    text = ("import random, subprocess, sys, tempfile\nfrom pathlib import Path\n"
            f"REFERENCE={source!r}\nSAMPLE={sample!r}\nGENERATOR_NAME={generator.__name__!r}\n"
            + inspect.getsource(generator) + "\n"
            + "def run(text):\n    with tempfile.TemporaryDirectory(prefix='producecase-') as d:\n"
            + "        p=Path(d)/'main.py'; p.write_text(REFERENCE)\n        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)\n        if x.returncode: raise SystemExit(x.stderr)\n        return x.stdout\n"
            + "def main():\n    d=Path('data'); d.mkdir(exist_ok=True)\n    cases=[SAMPLE]+(['8\\n','9\\n'] if GENERATOR_NAME == 'g22007' else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]\n    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))\nif __name__=='__main__': main()\n")
    (made / "producecase.py").write_text(text)


def main():
    manifest = json.loads(MANIFEST.read_text()); report = []
    for entry in manifest["entries"]:
        n = int(entry["local_number"]); gen = GENERATORS[n]; sample = entry["sample_input"]
        source = (ROOT / f"scripts/t004_platform_accepted_{n:05d}.py").read_text()
        a=entry["existing_accepted"]; reference_kind=f"platform Accepted Python3 #{a['solution_id']}"
        made = TESTS / bucket(n) / f"{n:05d}_made"; data = made / "data"; data.mkdir(parents=True, exist_ok=True)
        for p in data.glob("*"): p.unlink()
        cases = [sample]
        cases += [gen(random.Random(s)) for s in range(1,21)]
        outputs = [run_source(source,c) for c in cases]
        for i,c in enumerate(cases): (data/f"{i}.in").write_text(c); (data/f"{i}.out").write_text(outputs[i])
        header=(f"# External reference: statistics page /practice/{n:05d}/\n# Accepted submission: {a['solution_id']}\n# Source: {a['source_url']}\n# License: not declared on the submission page; no license is inferred.\n\n")
        (made/"samplecode.py").write_text(header+source)
        write_producecase(made,source,gen,sample,"python")
        rows, counter = constraint_rows(n,cases[1:])
        audit = common.audit(made,cases=cases[1:],outputs=outputs[1:],sample_input=sample,sample_output=entry.get("sample_output"),constraints=rows,constraint_counterexample=counter)
        for s in range(20000): gen(random.Random(s))
        run_python_many(source, [gen(random.Random(100000+s)) for s in range(400)])
        report.append({"local_number":n,"title":entry["title"],"reference_source":reference_kind,"statistics_url":f"http://cs101.openjudge.cn{entry['submit_path']}statistics/","source_url":a["source_url"],"license_status":"not declared on the submission page; no license is inferred","generator":gen.__name__,"generator_seed_smoke":{"seeds":20000,"status":"passed"},"reference_seed_smoke":{"seeds":400,"status":"passed"},"test_cases":len(cases),"constraints":rows,"constraint_counterexample":counter,"self_audit":audit,"sample_reproduced":audit["sample_is_case_zero"]["status"]=="passed","producecase_reproduced":audit["byte_reproduction"]["status"]=="passed"})
        print(n,"built",flush=True)
    REPORT.write_text(json.dumps({"batch":"T-004 round12","updated_at":datetime.now(timezone.utc).isoformat(),"entries":report},ensure_ascii=False,indent=2)+"\n")

if __name__ == "__main__": main()
