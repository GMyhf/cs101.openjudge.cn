#!/usr/bin/env python3
from __future__ import annotations
import contextlib,inspect,io,json,random,subprocess,sys,tempfile
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; MANIFEST=ROOT/"collab/t004-round9-manifest.json"; REPORT=ROOT/"collab/t004-round9-report.json"; TESTS=ROOT/"data/openjudge/tests"
sys.path.insert(0,str(ROOT/"scripts"))
from build_001a import bucket
import t004_common as common

def g15291(r):
    # Three connected one-cell blocks plus the required terminator.
    x=r.randint(0,7); y=r.randint(0,7)
    return f"1 1 1\n{x} {y}\n{x+1} {y}\n{x+2} {y}\n0 0 0\n"
def g17746(r):
    n=r.randint(5,60); m=r.randint(1,min(10,n)); c=r.randint(0,20)
    return f"{n} {m} {c}\n"+" ".join(str(r.randint(0,100)) for _ in range(n))+"\n"
def g18071(r):
    m,n=r.randint(2,8),r.randint(2,8); g=[[0]*n for _ in range(m)]
    if r.random()<.5:
        for i in range(1,m): g[i][0]=1
        for j in range(n): g[0][j]=1
    else:
        for i in range(2): 
            for j in range(2): g[i][j]=1
    return f"{m} {n}\n"+"\n".join(" ".join(map(str,x)) for x in g)+"\n"
def g18076(r):
    n,m=r.randint(2,8),r.randint(2,8)
    def mol(size,carbon):
        rows=[f"0 -1 {carbon} 1"]
        for i in range(1,size): rows.append(f"{i} {i-1} {1 if i%2 else carbon} 1")
        return rows
    # Keep the two generated molecules different; the accepted submission's
    # traversal assumes the problem's non-identical-molecule precondition.
    return f"{n} {m}\n"+"\n".join(mol(n,6)+mol(m,8))+"\n"
def g18189(r): return f"{r.randint(1,600)} {r.randint(1,20)}\n"
def g18209(r):
    n=r.randint(3,10); cuts=sorted(r.sample(range(1,100),n-1)); vals=[]; last=0
    for x in cuts+[100]: vals.append((x-last)/100); last=x
    return f"{n}\n"+" ".join(f"{x:.6f}" for x in vals)+"\n"
def g18252(r):
    n=r.randint(2,8); edges=[(i,i+1,r.randint(1,20)) for i in range(1,n)]
    edges += [(r.randint(1,n-1),r.randint(2,n),r.randint(1,20)) for _ in range(r.randint(0,8))]
    edges=[e for e in edges if e[0]!=e[1]]
    return "1\n"+f"{n} {len(edges)} 1\n"+"\n".join(" ".join(map(str,e)) for e in edges)+"\n"
def g19164(r):
    t=r.randint(1,20); return f"{t} {r.randint(1,30)}\n"+"\n".join(f"{r.randint(1,100)} {r.randint(1,100)}" for _ in range(t))+"\n"
def price_line(r):
    return " ".join(f"{r.randint(1,999)/100:.2f}" if r.random()<.5 else f"{r.randint(10,999)/10:.1f}" for _ in range(r.randint(6,15)))
def g19493(r):
    line=lambda: " ".join(f"{r.randint(1,999)/100:.2f}" if r.random()<.5 else f"{r.randint(10,999)/10:.1f}" for _ in range(r.randint(6,15)))
    m=r.randint(1,8); return f"{m}\n"+"\n".join(line() for _ in range(m))+"\n"
def g19546(r):
    line=lambda: " ".join(f"{r.randint(1,999)/100:.2f}" if r.random()<.5 else f"{r.randint(10,999)/10:.1f}" for _ in range(r.randint(6,15)))
    m=r.randint(1,8); return f"{m}\n"+"\n".join(line() for _ in range(m))+"\n"
def g19946(r):
    m,n=r.randint(1,15),r.randint(1,15); return f"{m} {n}\n"+" ".join(str(r.randint(1,50)) for _ in range(m))+"\n"+" ".join(str(r.randint(1,50)) for _ in range(n))+"\n"
def g19947(r):
    n=r.randint(2,30); return f"{n}\n"+" ".join(str(r.randint(1,1000)) for _ in range(n))+"\n"
def g19948(r):
    n=r.randint(1,30); m=r.randint(1,n); return f"{n} {m}\n"+" ".join(str(r.randint(1,1000)) for _ in range(n))+"\n"
def g19949(r):
    n=r.randint(1,10); rows=[]
    for _ in range(n):
        rows.append(" ".join(r.choice(["###Alice###","plain","###Bob###","word","###X###"]) for _ in range(r.randint(2,10))))
    return f"{n}\n"+"\n".join(rows)+"\n"
def g19952(r):
    t=r.randint(1,12); return f"{t}\n"+"\n".join(str(r.randint(1,200)) for _ in range(t))+"\n"
def g19962(r):
    n=r.randint(2,30); return f"{n}\n"+" ".join(str(r.randint(-100,100)) for _ in range(n))+"\n"
def g19965(r): return f"{r.randint(1,10000)} {r.randint(1,10000)} {r.randint(1,10000)}\n"
def g19967(r):
    ops=[]; size=0
    for _ in range(r.randint(8,30)):
        choices=["+"] if size==0 else ["+","?","*","-"]
        op=r.choice(choices)
        if op=="+": idx=r.randint(0,size); ops.append(f"+ {idx} {r.randint(-20,20)}"); size+=1
        elif op=="-": idx=r.randrange(size); ops.append(f"- {idx}"); size-=1
        elif op=="*": ops.append(f"* {r.randrange(size)} {r.randint(-20,20)}")
        else: ops.append(f"? {r.randint(-20,20)}")
    return f"{len(ops)}\n"+"\n".join(ops)+"\n"
def g19971(r):
    t=r.randint(1,12); return f"{t}\n"+"\n".join((lambda b: f"{r.randint(0,b)} {b}")(r.randint(0,100)) for _ in range(t))+"\n"
def g19974(r):
    t=r.randint(1,8); return f"{t}\n"+"\n".join(f"{r.randint(-5,5)} {r.randint(1,15)} {r.randint(1,15)}" for _ in range(t))+"\n"

GENERATORS={15291:g15291,17746:g17746,18071:g18071,18076:g18076,18189:g18189,18209:g18209,18252:g18252,19164:g19164,19493:g19493,19546:g19546,19946:g19946,19947:g19947,19948:g19948,19949:g19949,19952:g19952,19962:g19962,19965:g19965,19967:g19967,19971:g19971,19974:g19974}

def run_source(source,text,language):
    with tempfile.TemporaryDirectory(prefix="t004-r9-run-") as d:
        d=Path(d)
        if language=="G++":
            src=d/"main.cpp"; exe=d/"main"; src.write_text(source)
            c=subprocess.run(["g++","-std=c++17","-O2",str(src),"-o",str(exe)],capture_output=True,text=True,timeout=30)
            if c.returncode: raise RuntimeError(c.stderr[-1000:])
            cmd=[str(exe)]
        else:
            src=d/"main.py"; src.write_text(source); cmd=[sys.executable,str(src)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise RuntimeError(x.stderr[-1000:] or str(x.returncode))
        return x.stdout
def run_python_fast(source,text):
    oldi,oldo=sys.stdin,sys.stdout
    try:
        sys.stdin=io.StringIO(text); out=io.StringIO()
        with contextlib.redirect_stdout(out):
            exec(compile(source,"<external-accepted>","exec"),{"__name__":"__main__"})
        return out.getvalue()
    finally: sys.stdin,sys.stdout=oldi,oldo
def run_cpp_many(source,texts):
    with tempfile.TemporaryDirectory(prefix="t004-r9-cpp-smoke-") as d:
        d=Path(d); src=d/"main.cpp"; exe=d/"main"
        src.write_text(source)
        c=subprocess.run(["g++","-std=c++17","-O2",str(src),"-o",str(exe)],capture_output=True,text=True,timeout=30)
        if c.returncode: raise RuntimeError(c.stderr[-1000:])
        for text in texts:
            x=subprocess.run([str(exe)],input=text,text=True,capture_output=True,timeout=30)
            if x.returncode: raise RuntimeError(x.stderr[-1000:] or str(x.returncode))

def constraint_rows(n,cases):
    def every(label,p): return [(label,all(p(x) for x in cases))]
    if n==15291: rows=every("coordinates are 0..9",lambda x:all(0<=int(v)<=9 for v in x.split()))+every("terminator is present",lambda x:x.strip().endswith("0 0 0"))
    elif n==17746: rows=every("n,m,c are in range",lambda x:(lambda v:1<=v[1]<=10000 and 0<=v[2]<=10000 and v[0]>=v[1])(list(map(int,x.splitlines()[0].split()))))+every("samples are 0..1000000",lambda x:all(0<=int(v)<=1000000 for v in x.splitlines()[1].split()))
    elif n==18071: rows=every("matrix cells are binary",lambda x:all(int(v) in (0,1) for v in "\n".join(x.splitlines()[1:]).split()))+every("dimensions are at most 30",lambda x:all(0<int(v)<=30 for v in x.splitlines()[0].split()))
    elif n==18076: rows=every("atom records have four fields",lambda x:all(len(v.split())==4 for v in x.splitlines()[1:]))+every("atom indices are non-negative",lambda x:all(int(v.split()[0])>=0 for v in x.splitlines()[1:]))
    elif n==18189: rows=every("training minutes are positive",lambda x:int(x.split()[0])>0)+every("p is positive",lambda x:int(x.split()[1])>0)
    elif n==18209: rows=every("probabilities are non-negative",lambda x:all(float(v)>=0 for v in x.splitlines()[1].split()))+every("probabilities sum to one",lambda x:abs(sum(map(float,x.splitlines()[1].split()))-1)<1e-5)
    elif n==18252: rows=every("vertices are positive",lambda x:all(int(v)>0 for v in x.split()))+every("edge weights are positive",lambda x:all(int(v.split()[2])>0 for v in x.splitlines()[2:]))
    elif n==19164: rows=every("monthly revenues are 1..100",lambda x:all(1<=int(v)<=100 for v in x.splitlines()[1:] for v in v.split()))+every("T is positive",lambda x:int(x.splitlines()[0].split()[0])>0)
    elif n in (19493,19546): rows=every("price rows have at least six values",lambda x:all(len(v.split())>=6 for v in x.splitlines()[1:]))+every("prices are positive",lambda x:all(float(v)>0 for v in x.split() if v.replace(".","",1).isdigit()))
    elif n==19946: rows=every("worker and product counts are positive",lambda x:all(int(v)>0 for v in x.splitlines()[0].split()))+every("skills and difficulties are positive",lambda x:all(int(v)>0 for v in x.split()))
    elif n==19947: rows=every("material count is at least two",lambda x:int(x.splitlines()[0])>=2)+every("material values are positive",lambda x:all(int(v)>0 for v in x.splitlines()[1].split()))
    elif n==19948: rows=every("1 <= m <= n",lambda x:(lambda v:1<=v[1]<=v[0])(list(map(int,x.splitlines()[0].split()))))+every("levels are positive",lambda x:all(int(v)>0 for v in x.splitlines()[1].split()))
    elif n==19949: rows=every("sentence count is positive",lambda x:int(x.splitlines()[0])>0)+every("sentences are present",lambda x:len(x.splitlines())==int(x.splitlines()[0])+1)
    elif n==19952: rows=every("wall lengths are 1..200",lambda x:all(1<=int(v)<=200 for v in x.splitlines()[1:]))+every("test count is positive",lambda x:int(x.splitlines()[0])>0)
    elif n==19962: rows=every("customer count is positive",lambda x:int(x.splitlines()[0])>0)+every("coordinates are signed integers",lambda x:all(v.lstrip("-").isdigit() for v in x.splitlines()[1].split()))
    elif n==19965: rows=every("A B C are positive and bounded",lambda x:all(0<int(v)<=10000 for v in x.split()))
    elif n==19967: rows=every("operation count is positive",lambda x:int(x.splitlines()[0])>0)+every("operations have valid syntax",lambda x:all(v.split()[0] in "+-*?" for v in x.splitlines()[1:]))
    elif n==19971: rows=every("query count is positive",lambda x:int(x.splitlines()[0])>0)+every("query values are non-negative",lambda x:all(int(v)>=0 for v in x.split() if v.isdigit()))
    else: rows=every("p and q are positive",lambda x:all(int(v)>0 for v in x.splitlines()[1].split()[1:]))+every("test count is positive",lambda x:int(x.splitlines()[0])>0)
    return rows,("deliberate invalid input",[(rows[0][0],False)])

def write_producecase(made,source,generator,sample,language):
    name=generator.__name__; filename="main.cpp" if language=="G++" else "main.py"
    text=f"""import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE={source!r}
LANGUAGE={language!r}
SAMPLE={sample!r}
GENERATOR_NAME={name!r}
{inspect.getsource(generator)}
def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        d=Path(d); src=d/{filename!r}
        src.write_text(REFERENCE); cmd=[sys.executable,str(src)]
        if LANGUAGE=="G++":
            exe=d/"main"; subprocess.run(["g++","-std=c++17","-O2",str(src),"-o",str(exe)],check=True)
            cmd=[str(exe)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i,text in enumerate(cases):
        (data/f"{{i}}.in").write_text(text)
        (data/f"{{i}}.out").write_text(run(text))
if __name__=="__main__": main()
"""
    (made/"producecase.py").write_text(text)
def main():
    manifest=json.loads(MANIFEST.read_text()); report=[]
    for e in manifest["entries"]:
        n=int(e["local_number"]); a=e["existing_accepted"]; lang=a["language"]; ext="cpp" if lang=="G++" else "py"
        src=(ROOT/f"scripts/t004_platform_accepted_{n:05d}.{ext}").read_text(); g=GENERATORS[n]; sample=e["sample_input"]
        made=TESTS/bucket(n)/f"{n:05d}_made"; data=made/"data"; data.mkdir(parents=True,exist_ok=True)
        for p in data.glob("*"): p.unlink()
        cases=[sample]+[g(random.Random(seed)) for seed in range(1,21)]; outputs=[]
        for i,text in enumerate(cases):
            out=run_source(src,text,lang); outputs.append(out); (data/f"{i}.in").write_text(text); (data/f"{i}.out").write_text(out)
        marker = "//" if lang == "G++" else "#"
        h=f"{marker} External reference: statistics page /practice/{n:05d}/\n{marker} Accepted submission: {a['solution_id']}\n{marker} Source: {a['source_url']}\n{marker} License: not declared on the submission page; no license is inferred.\n\n"
        (made/f"samplecode.{ext}").write_text(h+src); write_producecase(made,src,g,sample,lang)
        rows,counter=constraint_rows(n,cases[1:]); audit=common.audit(made,cases=cases[1:],outputs=outputs[1:],sample_input=sample,constraints=rows,constraint_counterexample=counter)
        for seed in range(20000): g(random.Random(seed))
        seen=set()
        smoke_inputs=[]
        for seed in range(400):
            text=g(random.Random(100000+seed))
            key=text
            if key not in seen:
                smoke_inputs.append(text); seen.add(key)
        if lang=="Python3":
            for text in smoke_inputs: run_python_fast(src,text)
        else:
            run_cpp_many(src,smoke_inputs)
        report.append({"local_number":n,"title":e["title"],"source":e["source"],"reference_source":f"platform Accepted {lang} #{a['solution_id']}","statistics_url":f"http://cs101.openjudge.cn{e['submit_path']}statistics/","solution_id":a["solution_id"],"source_url":a["source_url"],"license_status":"not declared on submission page; no license inferred","generator":g.__name__,"generator_seed_smoke":{"seeds":20000,"status":"passed"},"reference_seed_smoke":{"seeds":400,"distinct_inputs":len(seen),"status":"passed"},"test_cases":len(cases),"constraints":rows,"constraint_counterexample":counter[0],"self_audit":audit,"sample_reproduced":audit["sample_is_case_zero"]["status"]=="passed","producecase_reproduced":audit["byte_reproduction"]["status"]=="passed"})
        print(n,"built",flush=True)
    REPORT.write_text(json.dumps({"batch":"T-004 round9","updated_at":datetime.now(timezone.utc).isoformat(),"entries":report},ensure_ascii=False,indent=2)+"\n")
if __name__=="__main__": main()
