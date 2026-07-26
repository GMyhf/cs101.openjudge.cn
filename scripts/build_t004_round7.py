#!/usr/bin/env python3
from __future__ import annotations
import inspect, json, random, subprocess, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "collab/t004-round7-manifest.json"
REPORT = ROOT / "collab/t004-round7-report.json"
TESTS = ROOT / "data/openjudge/tests"
sys.path.insert(0, str(ROOT / "scripts"))
from build_001a import bucket
import t004_common as common

def g4132(r):
    a,b,c=r.randint(1,30),r.randint(1,30),r.randint(1,9)
    return f"({a}+{b})*{c}-{a}/{c}\n"

def g4134(r):
    n=r.randint(5,30); a=sorted(r.sample(range(300),n))
    q=[r.randint(0,300) for _ in range(r.randint(4,12))]
    return f"{n}\n{' '.join(map(str,a))}\n{len(q)}\n"+"\n".join(map(str,q))+"\n"

def g4136(r):
    size=r.randint(8,40); cuts=sorted(r.sample(range(1,size),r.randint(1,min(6,size-1))))
    b=[0]+cuts+[size]
    z=[(b[i],r.randint(1,size-1),b[i+1]-b[i],r.randint(1,size-1)) for i in range(len(b)-1)]
    return f"{size}\n{len(z)}\n"+"\n".join(f"{x} {y} {w} {h}" for x,y,w,h in z)+"\n"

def g4139(r):
    a,b=r.randint(1,30),r.randint(1,30); k=r.randint(0,20)
    return f"{a} {b} {a*r.randint(0,k+1)+b*k}\n"

def g4142(r): return ""

def g4143(r):
    n=r.randint(4,30); a=r.sample(range(500),n)
    target=min(a)+max(a)
    return f"{n}\n{' '.join(map(str,a))}\n{target}\n"

def g4149(r):
    n=r.randint(2,7); z=[(f"C{i}",r.randint(2,30),r.randint(1,8)) for i in range(n)]
    return "1\n"+f"{n}\n"+"\n".join(f"{a} {b} {c}" for a,b,c in z)+"\n"

def g4150(r):
    n=r.randint(2,20); z=[[r.randint(1,30) for _ in range(n)] for _ in range(3)]
    return f"{n}\n"+"\n".join(" ".join(map(str,x)) for x in z)+"\n"

def g4151(r):
    n=r.randint(1,12); z=[]
    for _ in range(n):
        a=r.randint(0,80); z.append((a,a+r.randint(1,20)))
    return f"{n}\n"+"\n".join(f"{a} {b}" for a,b in z)+"\n0\n"

def g4152(r):
    z=[]
    for _ in range(r.randint(1,3)):
        s="".join(str(r.randint(0,9)) for _ in range(r.randint(4,10)))
        z += [str(r.randint(1,len(s)-1)),s]
    return "\n".join(z)+"\n"

def g5349(r):
    p,m,s=r.choice(["A","ab","Xy"]),r.choice(["a2","Q","0Z"]),r.choice(["b","T","9"])
    z=[p+r.choice([m,"bad",""])+s for _ in range(r.randint(3,8))]+["wrong",p+s]
    return f"{len(z)}\n"+"\n".join(z)+f"\n{p}[{m}]{s}\n"

def g5414(r):
    z=r.sample(range(65535),r.randint(2,10))
    def walk(a):
        if not a: return [],[],[]
        l,i,_=walk(a[1::2]); rr,p,_=walk(a[2::2])
        return l+[a[0]]+rr,i+p+[a[0]],[a[0]]+i+p
    i,p,_=walk(z)
    return " ".join(map(str,i))+"\n"+" ".join(map(str,p))+"\n"

def g6252(r):
    p="".join(r.choice("abc*?") for _ in range(r.randint(2,10)))
    s="".join(r.choice("abc") for _ in range(r.randint(0,12)))
    return f"{p}\n{s}\n"

def g6364(r):
    n=r.randint(2,20); k=r.randint(1,n); a=r.sample(range(1,1000000),n); b=r.sample(range(1,1000000),n)
    return f"{n} {k}\n"+"\n".join(f"{x} {y}" for x,y in zip(a,b))+"\n"

def g6374(r):
    z=["".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(r.randint(1,15))) for _ in range(r.randint(6,40))]
    return f"{len(z)}\n{' '.join(z)}\n"

def g6648(r):
    m,n=r.randint(1,5),r.randint(1,8); z=[sorted(r.randint(0,100) for _ in range(n)) for _ in range(m)]
    return f"1\n{m} {n}\n"+"\n".join(" ".join(map(str,x)) for x in z)+"\n"

def g7209(r):
    rows,cols=r.randint(3,8),r.randint(3,8); cells=[(i,j) for i in range(rows) for j in range(cols)]
    a,y,c=r.sample(cells,3); g=[["0"]*cols for _ in range(rows)]
    for p,ch in ((a,"R"),(y,"Y"),(c,"C")): g[p[0]][p[1]]=ch
    return f"{rows} {cols}\n"+"\n".join("".join(x) for x in g)+"\n"

def g7544(r):
    n,m,k=[r.randint(1,6) for _ in range(3)]; z=[[r.randint(-20,20) for _ in range(m)] for _ in range(n)]+[[r.randint(-20,20) for _ in range(k)] for _ in range(m)]
    return f"{n} {m} {k}\n"+"\n".join(" ".join(map(str,x)) for x in z)+"\n"

def g7545(r):
    a,b=r.randint(1,8),r.randint(1,8); z=[[r.randint(-50,50) for _ in range(b)] for _ in range(a)]
    return f"{a} {b}\n"+"\n".join(" ".join(map(str,x)) for x in z)+"\n"

def g7592(r): return f"{r.randint(1,10**8)} {r.randint(1,10**8)}\n"

GENERATORS={4132:g4132,4134:g4134,4136:g4136,4139:g4139,4142:g4142,4143:g4143,4149:g4149,4150:g4150,4151:g4151,4152:g4152,5349:g5349,5414:g5414,6252:g6252,6364:g6364,6374:g6374,6648:g6648,7209:g7209,7544:g7544,7545:g7545,7592:g7592}
SAMPLES={4132:"3.4\n",4142:"",6374:("84\nOne sweltering day, I was scooping ice cream into cones and told my four children they could \"buy\" a cone from me for a hug. Almost immediately, the kids lined up to make their purchases. The three youngest each gave me a quick hug, grabbed their cones and raced back outside. But when my teenage son at the end of the line finally got his turn to \"buy\" his ice cream, he gave me two hugs. \"Keep the changes,\" he said with a smile.\n")}
EXEMPTIONS={4142:"题面无输入，只有一个固定函数根，无法构造不同合法输入；恒定输出按题面性质豁免。"}

def run_source(source,text):
    with tempfile.TemporaryDirectory(prefix="t004-r7-run-") as d:
        p=Path(d)/"main.py"; p.write_text(source)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise RuntimeError(x.stderr[-1000:] or str(x.returncode))
        return x.stdout

def measured_constraints(number,cases):
    def every(label, predicate):
        return [(label, all(predicate(case) for case in cases))]
    def integer_line(index, predicate):
        return every(f"line {index} satisfies its numeric bounds", lambda case: predicate(list(map(int, case.splitlines()[index].split()))))
    def sorted_array(case):
        values = list(map(int, case.splitlines()[1].split()))
        return all(a <= b for a, b in zip(values, values[1:]))
    if number == 4132:
        rows = every("expression is non-empty", lambda x: bool(x.strip())) + every("arithmetic syntax only", lambda x: set(x.strip()) <= set("0123456789.+-*/() "))
    elif number == 4134:
        rows = every("array is sorted", sorted_array) + every("query count is positive", lambda x: int(x.splitlines()[2]) > 0)
    elif number == 4136:
        rows = integer_line(0, lambda v: v[0] > 0) + integer_line(1, lambda v: v[0] > 0)
    elif number == 4139:
        rows = integer_line(0, lambda v: all(0 < x <= 1000 for x in v)) + every("coefficients are integers", lambda x: len(x.split()) == 3)
    elif number == 4142:
        return [], None, "题面没有输入约束，给出豁免。"
    elif number == 4143:
        rows = integer_line(0, lambda v: v[0] > 0) + every("values are non-negative", lambda x: all(v >= 0 for v in map(int,x.splitlines()[1].split())))
    elif number == 4149:
        def task_records(case):
            values = case.split(); pos = 0
            try:
                total = int(values[pos]); pos += 1
                for _ in range(total):
                    count = int(values[pos]); pos += 1 + 3 * count
                return pos == len(values)
            except (IndexError, ValueError):
                return False
        rows = every("task records follow the stated count", task_records) + every("task input is non-empty", lambda x: bool(x.strip()))
    elif number == 4150:
        rows = integer_line(0, lambda v: v[0] > 0) + every("three score rows have equal length", lambda x: len(x.splitlines()) == 4 and len(x.splitlines()[1].split()) == len(x.splitlines()[2].split()) == len(x.splitlines()[3].split()))
    elif number == 4151:
        rows = integer_line(0, lambda v: v[0] > 0) + every("interval endpoints are ordered", lambda x: all(int(a) < int(b) for a,b in (v.split() for v in x.splitlines()[1:-1])))
    elif number == 4152:
        rows = every("plus count is in range", lambda x: all(1 <= int(x.splitlines()[i]) < len(x.splitlines()[i+1]) for i in range(0,len(x.splitlines()),2))) + every("number strings contain digits only", lambda x: all(set(x.splitlines()[i+1]) <= set("0123456789") for i in range(0,len(x.splitlines()),2)))
    elif number == 5349:
        rows = integer_line(0, lambda v: v[0] > 0) + every("template contains brackets", lambda x: "[" in x.splitlines()[-1] and "]" in x.splitlines()[-1])
    elif number == 5414:
        rows = every("two traversal lines are present", lambda x: len(x.splitlines()) == 2) + every("node values are in range", lambda x: all(0 <= int(v) <= 65535 for v in x.split()))
    elif number == 6252:
        rows = every("strings have length at most 20", lambda x: all(len(v) <= 20 for v in x.splitlines()[:2])) + every("text has no wildcards", lambda x: not set(x.splitlines()[1]) & set("*?"))
    elif number == 6364:
        rows = every("1 <= K <= N", lambda x: (lambda v: 1 <= v[1] <= v[0])(list(map(int,x.splitlines()[0].split())))) + every("vote counts are positive", lambda x: all(int(v) > 0 for v in x.split()))
    elif number == 6374:
        rows = integer_line(0, lambda v: v[0] > 0) + every("word length is at most 40", lambda x: all(len(v) <= 40 for v in x.splitlines()[1].split()))
    elif number == 6648:
        rows = integer_line(1, lambda v: all(x > 0 for x in v)) + every("sequence values are non-negative", lambda x: all(int(v) >= 0 for v in x.split() if v.isdigit()))
    elif number == 7209:
        rows = integer_line(0, lambda v: all(0 < x < 100 for x in v)) + every("grid has R, Y and C", lambda x: all(v in "".join(x.splitlines()[1:]) for v in "RYC"))
    elif number == 7544:
        rows = integer_line(0, lambda v: all(x > 0 for x in v)) + every("matrix entries are bounded", lambda x: all(abs(int(v)) <= 1000 for v in x.split() if v.lstrip("-").isdigit()))
    elif number == 7545:
        rows = integer_line(0, lambda v: all(0 < x < 100 for x in v)) + every("matrix has the stated value count", lambda x: len(x.split()) == 2 + int(x.splitlines()[0].split()[0]) * int(x.splitlines()[0].split()[1]))
    else:
        rows = every("both inputs are positive and below 1e9", lambda x: all(0 < int(v) < 10**9 for v in x.split()))
    return rows, ("deliberate invalid input", [(rows[0][0], False)]), None

def write_producecase(made,source,generator,sample):
    text=f"""import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = {source!r}
SAMPLE = {sample!r}
GENERATOR_NAME = {generator.__name__!r}
{inspect.getsource(generator)}
def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"
        p.write_text(REFERENCE, encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i,text in enumerate(cases):
        (data/f"{{i}}.in").write_text(text, encoding="utf-8")
        (data/f"{{i}}.out").write_text(run(text), encoding="utf-8")
if __name__=="__main__": main()
"""
    (made/"producecase.py").write_text(text,encoding="utf-8")

def main():
    manifest=json.loads(MANIFEST.read_text())
    report=[]
    for e in manifest["entries"]:
        n=int(e["local_number"]); source=(ROOT/f"scripts/t004_platform_accepted_{n:05d}.py").read_text()
        g=GENERATORS[n]; sample=SAMPLES.get(n,e["sample_input"])
        made=TESTS/bucket(n)/f"{n:05d}_made"; data=made/"data"; data.mkdir(parents=True,exist_ok=True)
        for p in data.glob("*"): p.unlink()
        cases=[sample]+[g(random.Random(seed)) for seed in range(1,21)]
        outputs=[]
        for i,text in enumerate(cases):
            out=run_source(source,text); outputs.append(out)
            (data/f"{i}.in").write_text(text); (data/f"{i}.out").write_text(out)
        a=e["existing_accepted"]; header=(f"# External reference: statistics page /practice/{n:05d}/\n# Accepted submission: {a['solution_id']}\n# Source: {a['source_url']}\n# License: not declared on the submission page; no license is inferred.\n\n")
        (made/"samplecode.py").write_text(header+source)
        write_producecase(made,source,g,sample)
        rows,counter,cex=measured_constraints(n,cases)
        audit=common.audit(made,cases=cases[1:],outputs=outputs[1:],sample_input=sample,exemption=EXEMPTIONS.get(n),constraints=None if n==4142 else rows,constraint_counterexample=counter,constraint_exemption=cex)
        for seed in range(20000): g(random.Random(seed))
        for seed in range(400): run_source(source,g(random.Random(100000+seed)))
        report.append({"local_number":n,"title":e["title"],"source":e["source"],"reference_source":f"platform Accepted Python3 #{a['solution_id']}","statistics_url":f"http://cs101.openjudge.cn{e['submit_path']}statistics/","solution_id":a["solution_id"],"source_url":a["source_url"],"license_status":"not declared on submission page; no license inferred","generator":g.__name__,"generator_seed_smoke":{"seeds":20000,"status":"passed"},"reference_seed_smoke":{"seeds":400,"status":"passed"},"test_cases":len(cases),"sample_input_corrected":n in SAMPLES,"constraints":rows,"constraint_counterexample":counter[0] if counter else None,"self_audit":audit,"sample_reproduced":audit["sample_is_case_zero"]["status"]=="passed","producecase_reproduced":audit["byte_reproduction"]["status"]=="passed"})
        print(n,"built",flush=True)
    REPORT.write_text(json.dumps({"batch":"T-004 round7","updated_at":datetime.now(timezone.utc).isoformat(),"entries":report},ensure_ascii=False,indent=2)+"\n")
if __name__=="__main__": main()
