import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = 's=input()\nprint(f"{eval(s):.2f}")'
SAMPLE = '3.4\n'
GENERATOR_NAME = 'g4132'
def g4132(r):
    a,b,c=r.randint(1,30),r.randint(1,30),r.randint(1,9)
    return f"({a}+{b})*{c}-{a}/{c}\n"

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
