import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='from collections import deque\nM, N = map(int, input().split())\nwords = [int(x) for x in input().split()]\nq = deque()\nlength = 0\ndict = [False]*(max(words)+1)\nres = 0\nfor word in words:\n    if dict[word]:\n        continue\n    if length == M:\n        x = q.popleft()\n        dict[x] = False\n    else:\n        length += 1\n    res += 1\n    dict[word] = True\n    q.append(word)\nprint(res)'
SAMPLE='3 7 \n1 2 1 5 4 4 1\n'
GENERATOR_NAME='g9199'
def g9199(r):
    m,n=r.randint(1,20),r.randint(1,60); z=[r.randint(0,1000000) for _ in range(n)]
    return f"{m} {n}\n"+" ".join(map(str,z))+"\n"

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
