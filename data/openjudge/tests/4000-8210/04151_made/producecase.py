import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = "while True:\n    n=int(input())\n    if n==0:\n        break\n    movie=[tuple(int(i) for i in input().split()) for _ in range(n)]\n    movie.sort(key=lambda x:(x[1],x[0]))\n    cborder=-float('inf')\n    cnt=0\n    for start,end in movie:\n        if start>=cborder:\n            cnt+=1\n            cborder=end\n    print(cnt)"
SAMPLE = '8\n3 4\n0 7 \n3 8 \n15 19\n15 20\n10 15\n8 18 \n6 12 \n0\n'
GENERATOR_NAME = 'g4151'
def g4151(r):
    n=r.randint(1,12); z=[]
    for _ in range(n):
        a=r.randint(0,80); z.append((a,a+r.randint(1,20)))
    return f"{n}\n"+"\n".join(f"{a} {b}" for a,b in z)+"\n0\n"

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
