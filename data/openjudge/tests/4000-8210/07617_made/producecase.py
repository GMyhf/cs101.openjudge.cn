import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='n = int(input())\nl = [int(x) for x in input().split()]\nk = int(input())\nl.sort()\nfor i in range(-1, -k-1, -1):\n    print(l[i])'
SAMPLE='10\n4 5 6 9 8 7 1 2 3 0\n5\n'
GENERATOR_NAME='g7617'
def g7617(r):
    n=r.randint(3,40); k=r.randint(1,n-1)
    return f"{n}\n"+" ".join(str(r.randint(-100000000,100000000)) for _ in range(n))+f"\n{k}\n"

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
        (data/f"{i}.in").write_text(text,encoding="utf-8")
        (data/f"{i}.out").write_text(run(text),encoding="utf-8")
if __name__=="__main__": main()
