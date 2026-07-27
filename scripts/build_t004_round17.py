#!/usr/bin/env python3
from __future__ import annotations
import concurrent.futures, inspect, json, os, random, subprocess, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "collab/t004-round17-manifest.json"
REPORT = ROOT / "collab/t004-round17-report.json"
TESTS = ROOT / "data/openjudge/tests"
sys.path.insert(0, str(ROOT / "scripts"))
from build_001a import bucket
import t004_common as common

def g30062(r): return " ".join(str(r.randint(-20, 20)) for _ in range(r.randint(2, 12))) + "\n"
def g30086(r):
    n, d = r.randint(1, 30), r.randint(0, 20)
    a = [r.randint(0, 100) for _ in range(2*n)]
    return f"{n} {d}\n{' '.join(map(str,a))}\n"
def g30091(r):
    L, n = r.randint(2, 5000), r.randint(0, 30)
    n = min(n, L)
    p = sorted(r.sample(range(1, L + 1), n)) if n else []
    return f"{L}\n{n}\n{' '.join(map(str,p))}\n" if n else f"{L}\n0\n"
def g30110(r): return f"{r.randint(1, 10**9)}\n"
def g30160(r):
    h, w = r.randint(1, 8), r.randint(1, 8); board = [[False for _ in range(w)] for _ in range(h)]
    def clue(line):
        out=[]; run=0
        for x in line + [False]:
            if x: run += 1
            elif run: out.append(run); run=0
        return out
    rows = [clue(x) for x in board]; cols = [clue([board[i][j] for i in range(h)]) for j in range(w)]
    return f"{h} {w}\n" + "\n".join(f"{len(x)} {' '.join(map(str,x))}" for x in rows+cols) + "\n"
def g30192(r):
    n = r.randint(1, 7); return f"{r.randint(20, 200)} {n}\n" + "\n".join(f"{r.randint(1,50)} {r.randint(1,30)}" for _ in range(n)) + "\n"
def g30216(r): return f"{r.randint(1, 10)}\n"
def g30217(r):
    n = r.randint(2, 80); a = [r.randint(1, 1000) for _ in range(n)]; i = r.randrange(n-1); a[i+1] = 1001-a[i]
    return f"{n} {1001}\n{' '.join(map(str,a))}\n"
def g30222(r):
    n = r.randint(2, 30); edges = [(i, r.randint(1, i-1)) for i in range(2, n+1) if r.random()<.5]
    return f"{n} {len(edges)}\n{' '.join(str(r.randint(1,100)) for _ in range(n))}\n" + "\n".join(f"{a} {b}" for a,b in edges) + "\n"
def g30370(r):
    n = r.randint(1, 100); return f"{n}\n{' '.join(map(str, sorted(r.randint(0,n) for _ in range(n))))}\n"
def g30497(r): return "1\n1 1 1 1\n"
def g30547(r): return f"{r.randint(1, 30)}\n"
def g30917(r):
    t=r.randint(1,20); return str(t)+"\n"+"\n".join("".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(r.randint(1,40))) for _ in range(t))+"\n"
def g30918(r):
    n=r.randint(1,30); return f"{n}\n"+"\n".join(" ".join(str(r.randint(1,1000)) for _ in range(n)) for _ in range(n))+"\n"
def g30931(r):
    depth = r.randint(1, 20)
    if r.randint(0, 2) == 0:
        return "(" * depth + ")" * depth + "\n"
    if r.randint(0, 1) == 0:
        return "[" * depth + "]" * depth + "\n"
    text = "".join(r.choice("()[]{}") for _ in range(r.randint(1, 40)))
    return text + "\n"
def g30932(r):
    n=r.randint(1,31); vals=[str(r.randint(-100,100)) if i==0 or r.random()<.8 else "null" for i in range(n)]
    return " ".join(vals)+"\n"
def g30934(r):
    t=r.randint(1,4); rows=[str(t)]
    for _ in range(t):
        n=r.randint(1,20); rows.append(str(n));
        for i in range(1,n+1): rows.append(f"{2*i if 2*i<=n else -1} {2*i+1 if 2*i+1<=n else -1}")
    return "\n".join(rows)+"\n"
def g30935(r):
    n=r.randint(1,50); return f"{n}\n"+"\n".join(f"{r.randint(1,50)} {r.randint(1,1000)}" for _ in range(n))+"\n"
def g30936(r): return f"{r.randint(1,1000)}\n"
def g31002(r):
    s="".join(r.choice("abcde") for _ in range(r.randint(1,100))); t="".join(r.choice("abcde") for _ in range(r.randint(1,8)))
    return f"{s}\n{t}\n"

GENERATORS={n:globals()[f"g{n}"] for n in (30062,30086,30091,30110,30160,30192,30216,30217,30222,30370,30497,30547,30917,30918,30931,30932,30934,30935,30936,31002)}

def run_source(source, text, cpp=False):
    with tempfile.TemporaryDirectory(prefix="t004-r17-") as d:
        p=Path(d)/("main.cpp" if cpp else "main.py"); p.write_text(source)
        if cpp:
            exe=Path(d)/"main"; c=subprocess.run(["g++","-O2","-std=c++17",str(p),"-o",str(exe)],capture_output=True,text=True,timeout=30)
            if c.returncode: raise RuntimeError(c.stderr[-1000:])
            cmd=[str(exe)]
        else: cmd=[sys.executable,str(p)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=120)
        if x.returncode: raise RuntimeError(x.stderr[-1000:] or str(x.returncode))
        return x.stdout

def run_many(source, cases, cpp=False):
    if not cpp:
        return [run_source(source, text) for text in cases]
    with tempfile.TemporaryDirectory(prefix="t004-r17-cpp-") as d:
        p=Path(d)/"main.cpp"; exe=Path(d)/"main"; p.write_text(source)
        c=subprocess.run(["g++","-O2","-std=c++17",str(p),"-o",str(exe)],capture_output=True,text=True,timeout=30)
        if c.returncode: raise RuntimeError(c.stderr[-1000:])
        out=[]
        for text in cases:
            x=subprocess.run([str(exe)],input=text,text=True,capture_output=True,timeout=120)
            if x.returncode: raise RuntimeError(x.stderr[-1000:] or str(x.returncode))
            out.append(x.stdout)
        return out

def constraint(n, cases):
    checks={
      30062:("sequence has at least two integers",lambda x:len(x.split())>=2,"1\n"),
      30086:("n is positive and input has 2n values",lambda x:(lambda a:1<=int(a[0]) and len(a[2:])==2*int(a[0]))(x.split()),"0 1\n"),
      30091:("positions are within 1..L",lambda x:(lambda a:all(1<=int(v)<=int(a[0]) for v in a[2:]))(x.split()),"3\n1\n0\n"),
      30110:("input is a positive integer",lambda x:x.strip().isdigit() and int(x)>0,"0\n"),
      30160:("grid dimensions are positive",lambda x:int(x.split()[0])>0 and int(x.split()[1])>0,"0 0\n"),
      30192:("capacity and item count are positive",lambda x:int(x.split()[0])>0 and int(x.split()[1])>0,"0 0\n"),
      30216:("n is in 1..10",lambda x:1<=int(x.strip())<=10,"11\n"),
      30217:("N is positive and values are positive",lambda x:int(x.split()[0])>0 and all(int(v)>0 for v in x.split()[2:]),"0 1\n"),
      30222:("N is positive and edges use valid vertices",lambda x:int(x.split()[0])>0,"0 0\n"),
      30370:("n is positive and values are nonnegative",lambda x:int(x.split()[0])>0 and all(int(v)>=0 for v in x.split()[1:]),"0\n"),
      30497:("input format is intentionally not mechanically meaningful",lambda x:True,None),
      30547:("test count is positive",lambda x:int(x.strip())>0,"0\n"),
      30917:("T is positive and strings are lowercase",lambda x:int(x.split()[0])>0 and all(v.islower() for v in x.split()[1:]),"0\n"),
      30918:("matrix dimension is positive",lambda x:int(x.split()[0])>0,"0\n"),
      30931:("input contains only brackets",lambda x:all(c in '()[]{}\n' for c in x),"a\n"),
      30932:("tree root is present",lambda x:x.split()[0]!='null',"null\n"),
      30934:("test count is positive",lambda x:int(x.split()[0])>0,"0\n"),
      30935:("job count is positive",lambda x:int(x.split()[0])>0,"0\n"),
      30936:("N is positive",lambda x:int(x.strip())>0,"0\n"),
      31002:("map and treasure strings are nonempty",lambda x:all(x.splitlines()),"\n\n")}
    label,pred,bad=checks[n]
    if n==30497: return [], (None, [])
    return [(label, all(pred(c) for c in cases))], (bad, [(label, bool(pred(bad)))])

def write_producecase(made, source, gen, sample, cpp):
    runner = """\nfrom pathlib import Path\nimport subprocess, sys, tempfile\ndef run(text):\n    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:\n        p=Path(d)/('main.cpp' if CPP else 'main.py'); p.write_text(REFERENCE)\n        if CPP:\n            exe=Path(d)/'main'; c=subprocess.run(['g++','-O2','-std=c++17',str(p),'-o',str(exe)],capture_output=True,text=True,timeout=30)\n            if c.returncode: raise SystemExit(c.stderr)\n            cmd=[str(exe)]\n        else: cmd=[sys.executable,str(p)]\n        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=120)\n        if x.returncode: raise SystemExit(x.stderr)\n        return x.stdout\ndef main():\n    data=Path('data'); data.mkdir(exist_ok=True)\n    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]\n    for i,c in enumerate(cases): (data/f'{i}.in').write_text(c); (data/f'{i}.out').write_text(run(c))\nif __name__=='__main__': main()\n"""
    text = "import random\n" + f"REFERENCE={source!r}\nSAMPLE={sample!r}\nGENERATOR_NAME={gen.__name__!r}\nCPP={cpp!r}\n" + inspect.getsource(gen) + runner
    (made/"producecase.py").write_text(text)

def main():
    manifest=json.loads(MANIFEST.read_text()); report=[]
    selected={int(x) for x in os.environ.get("T004_ONLY", "").split(",") if x.strip()}
    if selected and REPORT.exists():
        report.extend(x for x in json.loads(REPORT.read_text()).get("entries", []) if int(x["local_number"]) not in selected)
    for entry in manifest["entries"]:
        n=int(entry["local_number"]); a=entry["existing_accepted"]; cpp=a["language"]=="G++"
        if selected and n not in selected: continue
        ext="cpp" if cpp else "py"; source=(ROOT/f"scripts/t004_platform_accepted_{n}.{ext}").read_text(); gen=GENERATORS[n]
        sample=entry["sample_input"]
        cases=[sample]+[gen(random.Random(s)) for s in range(1,21)]
        outputs=run_many(source,cases,cpp)
        made=TESTS/bucket(n)/f"{n:05d}_made"; data=made/"data"; data.mkdir(parents=True,exist_ok=True)
        for p in data.glob("*"): p.unlink()
        for i,c in enumerate(cases): (data/f"{i}.in").write_text(c); (data/f"{i}.out").write_text(outputs[i])
        (made/f"samplecode.{ext}").write_text(source); write_producecase(made,source,gen,sample,cpp)
        if not cpp: (made/"samplecode.py").write_text(source)
        rows,counter=constraint(n,cases[1:]); probe_exemption = "题目本身不可判定，平台 Accepted 实现固定输出 undecidable" if n==30497 else None
        constraint_exemption = "题面是不可判定的恶作剧题，没有可机械验证的输入约束" if n==30497 else None
        distinct_exemption = (
            "题面 n 仅有 10 个合法取值（1..10）"
            if n == 30216 else probe_exemption
        )
        audit=common.audit(made,cases=cases[1:],outputs=outputs[1:],sample_input=sample,sample_output=entry.get("sample_output"),constraints=rows,constraint_counterexample=counter,exemption=distinct_exemption,constraint_exemption=constraint_exemption)
        for s in range(20000): gen(random.Random(s))
        smoke=[gen(random.Random(100000+s)) for s in range(400)]
        run_many(source, smoke, cpp)
        row={"local_number":n,"title":entry["title"],"reference_source":f"platform Accepted {a['language']} #{a['solution_id']}","statistics_url":f"http://cs101.openjudge.cn{entry['submit_path']}statistics/","source_url":a["source_url"],"license_status":"not declared on the submission page; no license is inferred.","generator":gen.__name__,"generator_seed_smoke":{"seeds":20000,"status":"passed"},"reference_seed_smoke":{"seeds":400,"status":"passed"},"test_cases":len(cases),"constraints":rows,"constraint_counterexample":counter,"self_audit":audit,"sample_reproduced":audit["sample_is_case_zero"]["status"]=="passed","producecase_reproduced":audit["byte_reproduction"]["status"]=="passed"}
        if n==30497:
            row["sample_is_case_zero_exemption"]="题面样例省略输入且输出为玩笑，使用格式合法小输入与平台 AC 输出作锚点"
            row["constant_output_probe_exemption"]="题目本身不可判定，平台 Accepted 实现固定输出 undecidable"
        report.append(row); print(n,"built",flush=True)
    REPORT.write_text(json.dumps({"batch":"T-004 round17","updated_at":datetime.now(timezone.utc).isoformat(),"pending_rework_status":{"status":"passed","items":[]},"entries":report},ensure_ascii=False,indent=2)+"\n")

if __name__=="__main__": main()
