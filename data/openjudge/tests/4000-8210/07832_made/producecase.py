import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='import math\nN, A, B = map(int, input().split())\nres = 0\nans = (0, 0)\nfor i in range(1, N+1):\n    j = math.ceil(i*A/B-1)\n    if j/i > res:\n        res = j/i\n        ans = (j, i)\nprint(*ans)'
SAMPLE='100 7 13\n'
GENERATOR_NAME='g7832'
def g7832(r):
    n=r.randint(10,200); a=r.randint(1,n-2); b=r.randint(a+1,n-1)
    return f"{n} {a} {b}\n"

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
