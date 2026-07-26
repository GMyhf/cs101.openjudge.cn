import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = 'n, k = map(int, input().split())\n\nround1 = []\nfor i in range(n):\n    a, b = map(int, input().split())\n    round1.append((a, b, i+1))\n\nround1.sort(key = lambda x : -x[0])\n\nround2 = round1[:k]\n\nround2.sort(key = lambda x : -x[1])\n\nprint(round2[0][2])'
SAMPLE = '5 3\n3 10\n9 2\n5 6\n8 4\n6 5\n'
GENERATOR_NAME = 'g6364'
def g6364(r):
    n=r.randint(2,20); k=r.randint(1,n); a=r.sample(range(1,1000000),n); b=r.sample(range(1,1000000),n)
    return f"{n} {k}\n"+"\n".join(f"{x} {y}" for x,y in zip(a,b))+"\n"

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
