import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='N = int(input())\nheights = []\nfor _ in range(N):\n    heights.append(int(input()))\nstack = []\nans = 0\nfor i in range(N):\n    h = heights[i]\n    while stack and stack[-1][0] <= h:\n        stack.pop()\n    ans += len(stack)\n    stack.append((h, i))\nprint(ans)'
SAMPLE='6\n10\n3\n7\n4\n12\n2\n'
GENERATOR_NAME='g13058'
def g13058(r):
    n=r.randint(1,50); return f"{n}\n"+"\n".join(str(r.randint(1,100000)) for _ in range(n))+"\n"

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
