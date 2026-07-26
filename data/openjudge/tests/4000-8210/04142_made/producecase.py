import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = "def fun(x):\n    return x**5-15*x**4+85*x**3-225*x**2+274*x-121\nleft, right = 1.5, 2.4\nres = 0\nwhile right-left > 10**(-7):\n    mid = (left+right)/2\n    if fun(mid) == 0:\n        res = mid\n        break\n    if fun(mid) < 0:\n        right = mid\n    else:\n        left = mid\nif res == 0:\n    res = left\nprint(f'{res:.6f}')"
SAMPLE = ''
GENERATOR_NAME = 'g4142'
def g4142(r): return ""

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
