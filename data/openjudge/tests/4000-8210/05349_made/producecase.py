import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = "n=int(input())\nstrings=[]\nfor i in range(n):\n    strings.append(input())\nstan=input().upper().split('[')\nx=stan[1].split(']')\nstan[1]=x[0]\nstan.append(x[1])\nm=len(stan[0])\nn=len(stan[2])\nans=[]\ni=0\nfor s in strings:\n    S=s.upper()\n    if S[:m]==stan[0] and S[len(s)-n:]==stan[2] and S[m:len(s)-n] in stan[1] and len(s)==m+n+1:\n        ans.append((i+1,s))\n    i+=1\nfor a,s in ans:\n    print(a,s)"
SAMPLE = '4\nAab\na2B\nab\nABB\na[a2b]b\n'
GENERATOR_NAME = 'g5349'
def g5349(r):
    p,m,s=r.choice(["A","ab","Xy"]),r.choice(["a2","Q","0Z"]),r.choice(["b","T","9"])
    z=[p+r.choice([m,"bad",""])+s for _ in range(r.randint(3,8))]+["wrong",p+s]
    return f"{len(z)}\n"+"\n".join(z)+f"\n{p}[{m}]{s}\n"

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
