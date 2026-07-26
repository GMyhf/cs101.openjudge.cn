import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = 'a=int(input())\nb=list(map(int, input().split()))\nb.sort()\nc=int(input())\nleft=0\nright=a-1\nwhile left<right:\n    while b[left]+b[right]>c:\n        right-=1\n    if b[left]+b[right]==c:\n        print(b[left],b[right],end=" ")\n        quit()\n    else:\n        left+=1\nprint("No")'
SAMPLE = '4\n2 5 1 4\n6\n'
GENERATOR_NAME = 'g4143'
def g4143(r):
    n=r.randint(4,30); a=r.sample(range(500),n)
    target=min(a)+max(a)
    return f"{n}\n{' '.join(map(str,a))}\n{target}\n"

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
