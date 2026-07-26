#!/usr/bin/env python3
from __future__ import annotations
import contextlib,inspect,io,json,random,subprocess,sys,tempfile
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"collab/t004-round8-manifest.json"
REPORT=ROOT/"collab/t004-round8-report.json"
TESTS=ROOT/"data/openjudge/tests"
sys.path.insert(0,str(ROOT/"scripts"))
from build_001a import bucket
import t004_common as common

def g7604(r):
    n=r.randint(1,8); s="".join(r.choice("abcde") for _ in range(r.randint(n,40)))
    return f"{n}\n{s}\n"
def g7615(r):
    n=r.randint(2,15); names=[f"S{i}" for i in range(n)]
    return f"{n}\n"+"\n".join(f"{x} {r.randint(0,100)}" for x in names)+"\n"
def g7617(r):
    n=r.randint(3,40); k=r.randint(1,n-1)
    return f"{n}\n"+" ".join(str(r.randint(-100000000,100000000)) for _ in range(n))+f"\n{k}\n"
def g7618(r):
    n=r.randint(2,30); ids=r.sample(range(10**8),n)
    return f"{n}\n"+"\n".join(f"{x:08d} {r.randint(1,99)}" for x in ids)+"\n"
def g7620(r):
    n=r.randint(3,15); connected=r.random()<.7
    starts=[]; left=r.randint(1,20)
    for _ in range(n):
        if connected: a=left; b=a+r.randint(0,8); left=b
        else: a=r.randint(1,60); b=r.randint(a, min(100,a+10))
        starts.append((a,b))
    return f"{n}\n"+"\n".join(f"{a} {b}" for a,b in starts)+"\n"
def g7735(r):
    n=r.randint(3,10); k=r.randint(3,80); edges=[]
    for u in range(1,n): edges.append((u,u+1,r.randint(1,20),r.randint(0,min(10,k))))
    for _ in range(r.randint(0,12)):
        u=r.randint(1,n-1); v=r.randint(u+1,n)
        edges.append((u,v,r.randint(1,20),r.randint(0,min(10,k))))
    return f"{k}\n{n}\n{len(edges)}\n"+"\n".join(" ".join(map(str,e)) for e in edges)+"\n"
def g7832(r):
    n=r.randint(10,200); a=r.randint(1,n-2); b=r.randint(a+1,n-1)
    return f"{n} {a} {b}\n"
def g7902(r):
    m,n=r.randint(2,8),r.randint(2,8); k=r.randint(10,120)
    z=[[0]*n for _ in range(m)]
    for _ in range(r.randint(1,min(12,m*n))):
        z[r.randrange(m)][r.randrange(n)]=r.randint(1,30)
    return f"{m} {n} {k}\n"+"\n".join(" ".join(map(str,x)) for x in z)+"\n"
def g8167(r):
    n,m=r.randint(1,10),r.randint(1,10); z=[[r.randint(0,255) for _ in range(m)] for _ in range(n)]
    return f"{n} {m}\n"+"\n".join(" ".join(map(str,x)) for x in z)+"\n"
def g8183(r):
    h,w=r.randint(3,10),r.randint(5,10); return f"{h} {w} {r.choice('@#*')} {r.randint(0,1)}\n"
def g8219(r):
    value=r.choice([-10**9,-1,0,1,10**9]) if r.random()<.25 else r.randint(-10**9,10**9)
    return f"{value}\n"
def g8466(r):
    n=r.choice([1,5,10,15,24]); return f"{'0'*r.randint(0,20)}{n}\n"
def g8780(r):
    n=r.randint(1,15); return f"{n}\n"+" ".join(str(r.randint(1,30000)) for _ in range(n))+"\n"
def g9199(r):
    m,n=r.randint(1,20),r.randint(1,60); z=[r.randint(0,1000000) for _ in range(n)]
    return f"{m} {n}\n"+" ".join(map(str,z))+"\n"
def g9278(r): return f"{r.randint(1,80)}\n"
def g10715(r):
    n=r.randint(2,6); return f"{n}\n"+" ".join(str(r.randint(1,13)) for _ in range(n))+"\n"
def g13058(r):
    n=r.randint(1,50); return f"{n}\n"+"\n".join(str(r.randint(1,100000)) for _ in range(n))+"\n"
def g14685(r):
    n=r.randint(2,30); k=r.randint(-50,50); z=[r.randint(-50,50) for _ in range(n)]
    return f"{k} {n}\n"+"\n".join(map(str,z))+"\n"
def g15265(r):
    n=r.randint(2,20); z=[r.randint(0,100) for _ in range(n)]
    return f"{n}\n"+" ".join(map(str,z))+"\n"
def g15286(r):
    n=r.randint(3,10); w=r.randint(10,100); z=[r.randint(1,w) for _ in range(n)]
    return f"{n} {w}\n"+"\n".join(map(str,z))+"\n"

GENERATORS={7604:g7604,7615:g7615,7617:g7617,7618:g7618,7620:g7620,7735:g7735,7832:g7832,7902:g7902,8167:g8167,8183:g8183,8219:g8219,8466:g8466,8780:g8780,9199:g9199,9278:g9278,10715:g10715,13058:g13058,14685:g14685,15265:g15265,15286:g15286}

def run_source(source,text):
    with tempfile.TemporaryDirectory(prefix="t004-r8-run-") as d:
        p=Path(d)/"main.py"; p.write_text(source)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise RuntimeError(x.stderr[-1000:] or str(x.returncode))
        return x.stdout

def run_source_fast(source,text):
    old_stdin,old_stdout=sys.stdin,sys.stdout
    try:
        sys.stdin=io.StringIO(text); output=io.StringIO()
        with contextlib.redirect_stdout(output):
            try: exec(compile(source,"<external-accepted>","exec"),{"__name__":"__main__"})
            except SystemExit as exc:
                if exc.code not in (None,0): raise
        return output.getvalue()
    finally:
        sys.stdin,sys.stdout=old_stdin,old_stdout

def constraints(number,cases):
    def every(label,p): return [(label,all(p(x) for x in cases))]
    if number==7604: rows=every("n is positive",lambda x:int(x.splitlines()[0])>0)+every("n-gram width fits string",lambda x:int(x.splitlines()[0])<=len(x.splitlines()[1]))
    elif number==7615: rows=every("score is 0..100",lambda x:all(0<=int(v.split()[1])<=100 for v in x.splitlines()[1:]))
    elif number==7617: rows=every("k is positive and below n",lambda x:1<=int(x.splitlines()[2])<int(x.splitlines()[0]))+every("values fit int bound",lambda x:all(abs(int(v))<=10**8 for v in x.splitlines()[1].split()))
    elif number==7618: rows=every("patient IDs are unique",lambda x:len(x.splitlines()[1:])==len({v.split()[0] for v in x.splitlines()[1:]}))+every("ages are positive and below 100",lambda x:all(0<int(v.split()[1])<100 for v in x.splitlines()[1:]))
    elif number==7620: rows=every("there are at least three intervals",lambda x:int(x.splitlines()[0])>=3)+every("interval endpoints are ordered",lambda x:all(int(a)<=int(b) for a,b in (v.split() for v in x.splitlines()[1:])))
    elif number==7735: rows=every("cities are in range",lambda x:all(1<=int(v.split()[i])<=100 for v in x.splitlines()[3:] for i in (0,1)))+every("road costs are bounded",lambda x:all(int(v.split()[2])<=100 and int(v.split()[3])<=100 for v in x.splitlines()[3:]))
    elif number==7832: rows=every("1 <= A < B < N",lambda x:(lambda v:1<=v[1]<v[2]<v[0])(list(map(int,x.split()))))
    elif number==7902: rows=every("field values are non-negative",lambda x:all(int(v)>=0 for v in x.split()))+every("field dimensions are at most 20",lambda x:all(int(v)<=20 for v in x.splitlines()[0].split()[:2]))
    elif number==8167: rows=every("pixels are 0..255",lambda x:all(0<=int(v)<=255 for v in x.split()))+every("dimensions are at most 100",lambda x:all(0<int(v)<=100 for v in x.splitlines()[0].split()))
    elif number==8183: rows=every("height and width are in range",lambda x:(lambda v:3<=v[0]<=10 and 5<=v[1]<=10)(list(map(int,x.split()[:2]))))
    elif number==8219: rows=every("input is within signed 1e9",lambda x:abs(int(x))<=10**9)
    elif number==8466: rows=every("n is at most 24",lambda x:0<int(x)<=24)
    elif number==8780: rows=every("N is 1..15",lambda x:1<=int(x.splitlines()[0])<=15)+every("heights are positive and bounded",lambda x:all(0<int(v)<=30000 for v in x.splitlines()[1].split()))
    elif number==9199: rows=every("M and N are positive",lambda x:all(int(v)>0 for v in x.splitlines()[0].split()))+every("words are non-negative and bounded",lambda x:all(0<=int(v)<=1000000 for v in x.splitlines()[1].split()))
    elif number==9278: rows=every("n is positive and below 200",lambda x:0<int(x)<200)
    elif number==10715: rows=every("n is 1..6",lambda x:1<=int(x.splitlines()[0])<=6)+every("cards are 1..13",lambda x:all(1<=int(v)<=13 for v in x.splitlines()[1].split()))
    elif number==13058: rows=every("heights are positive",lambda x:all(int(v)>0 for v in x.splitlines()[1:]))
    elif number==14685: rows=every("N is 2..50000",lambda x:2<=int(x.splitlines()[0].split()[1])<=50000)+every("money is within signed 1e9",lambda x:all(abs(int(v))<=10**9 for v in x.splitlines()[1:]))
    elif number==15265: rows=every("n is 2..20",lambda x:2<=int(x.splitlines()[0])<=20)+every("values are 0..100",lambda x:all(0<=int(v)<=100 for v in x.splitlines()[1].split()))
    else: rows=every("N is positive",lambda x:int(x.splitlines()[0].split()[0])>0)+every("weights do not exceed W",lambda x:(lambda v:all(0<z<=v[1] for z in v[2:]))(list(map(int,x.split()))))
    return rows,("deliberate invalid input",[(rows[0][0],False)])

def write_producecase(made,source,generator,sample):
    text=f"""import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE={source!r}
SAMPLE={sample!r}
GENERATOR_NAME={generator.__name__!r}
{inspect.getsource(generator)}
def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"; p.write_text(REFERENCE,encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i,text in enumerate(cases):
        (data/f"{{i}}.in").write_text(text,encoding="utf-8")
        (data/f"{{i}}.out").write_text(run(text),encoding="utf-8")
if __name__=="__main__": main()
"""
    (made/"producecase.py").write_text(text,encoding="utf-8")

def main():
    manifest=json.loads(MANIFEST.read_text()); report=[]
    for e in manifest["entries"]:
        n=int(e["local_number"]); src=(ROOT/f"scripts/t004_platform_accepted_{n:05d}.py").read_text()
        g=GENERATORS[n]; sample=e["sample_input"]; made=TESTS/bucket(n)/f"{n:05d}_made"; data=made/"data"; data.mkdir(parents=True,exist_ok=True)
        for p in data.glob("*"): p.unlink()
        cases=[sample]+[g(random.Random(seed)) for seed in range(1,21)]; outputs=[]
        for i,text in enumerate(cases):
            out=run_source(src,text); outputs.append(out)
            (data/f"{i}.in").write_text(text); (data/f"{i}.out").write_text(out)
        a=e["existing_accepted"]; h=f"# External reference: statistics page /practice/{n:05d}/\n# Accepted submission: {a['solution_id']}\n# Source: {a['source_url']}\n# License: not declared on the submission page; no license is inferred.\n\n"
        (made/"samplecode.py").write_text(h+src); write_producecase(made,src,g,sample)
        rows,counter=constraints(n,cases[1:]); audit=common.audit(made,cases=cases[1:],outputs=outputs[1:],sample_input=sample,constraints=rows,constraint_counterexample=counter)
        for seed in range(20000): g(random.Random(seed))
        reference_inputs=set()
        for seed in range(400):
            text=g(random.Random(100000+seed))
            key=str(int(text.strip())) if n==8466 else text
            if key not in reference_inputs:
                run_source_fast(src,text); reference_inputs.add(key)
        report.append({"local_number":n,"title":e["title"],"source":e["source"],"reference_source":f"platform Accepted Python3 #{a['solution_id']}","statistics_url":f"http://cs101.openjudge.cn{e['submit_path']}statistics/","solution_id":a["solution_id"],"source_url":a["source_url"],"license_status":"not declared on submission page; no license inferred","generator":g.__name__,"generator_seed_smoke":{"seeds":20000,"status":"passed"},"reference_seed_smoke":{"seeds":400,"distinct_inputs":len(reference_inputs),"status":"passed"},"test_cases":len(cases),"constraints":rows,"constraint_counterexample":counter[0],"self_audit":audit,"sample_reproduced":audit["sample_is_case_zero"]["status"]=="passed","producecase_reproduced":audit["byte_reproduction"]["status"]=="passed"})
        print(n,"built",flush=True)
    REPORT.write_text(json.dumps({"batch":"T-004 round8","updated_at":datetime.now(timezone.utc).isoformat(),"entries":report},ensure_ascii=False,indent=2)+"\n")
if __name__=="__main__": main()
