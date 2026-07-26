import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = 'n, m, k = map(int, input().split())\nA = [[int(x) for x in input().split()] for _ in range(n)]\nB = [[int(x) for x in input().split()] for _ in range(m)]\nC = [[0]*k for _ in range(n)]\nfor i in range(n):\n    for j in range(k):\n        C[i][j] = sum(A[i][t]*B[t][j] for t in range(m))\nfor i in range(n):\n    print(*C[i])'
SAMPLE = '3 2 3\n1 1\n1 1\n1 1\n1 1 1\n1 1 1\n'
GENERATOR_NAME = 'g7544'
def g7544(r):
    n,m,k=[r.randint(1,6) for _ in range(3)]; z=[[r.randint(-20,20) for _ in range(m)] for _ in range(n)]+[[r.randint(-20,20) for _ in range(k)] for _ in range(m)]
    return f"{n} {m} {k}\n"+"\n".join(" ".join(map(str,x)) for x in z)+"\n"

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
        (data/f"{i}.in").write_text(text, encoding="utf-8")
        (data/f"{i}.out").write_text(run(text), encoding="utf-8")
if __name__=="__main__": main()
