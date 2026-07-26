import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/19164 statistics, Accepted solution 51285327.\n# Source: http://cs101.openjudge.cn/practice/solution/51285327/\n# Statistics: http://cs101.openjudge.cn/practice/19164/statistics/\n# License: not declared on submission page; no license inferred\nT, M = map(int, input().split())\np = []\nn = []\nfor _ in range(T):\n    P, N = map(int, input().split())\n    p.append(P)\n    n.append(N)\nnow_p, now_n = p[0], n[0]\nfor i in range(1, T):\n    last_p, last_n = now_p, now_n\n    now_p = max(last_p+p[i], last_n+p[i]-M)\n    now_n = max(last_n+n[i], last_p+n[i]-M)\nprint(max(now_p, now_n))\n'
LANGUAGE='Python3'
SAMPLE='4 3\n10 9\n2 8\n9 5\n8 2\n'
GENERATOR_NAME='g19164'
def g19164(r):
    t=r.randint(1,20); return f"{t} {r.randint(1,30)}\n"+"\n".join(f"{r.randint(1,100)} {r.randint(1,100)}" for _ in range(t))+"\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        d=Path(d); src=d/'main.py'
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
        (data/f"{i}.in").write_text(text)
        (data/f"{i}.out").write_text(run(text))
if __name__=="__main__": main()
