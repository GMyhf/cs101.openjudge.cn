import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='def calculate(x):\n    s_x = str(x)\n    count = 0\n    for char in s_x:\n        count += d[int(char)]\n    return count\nd = {0:6, 1:2, 2:5, 3:5, 4:4, 5:5, 6:6, 7:3, 8:7, 9:6}\nn = int(input())\nres = 0\nfor i in range(1112):\n    if calculate(i)*2+calculate(2*i) == n-4:\n        res += 1\nfor i in range(1112):\n    for j in range(i):\n        if calculate(i)+calculate(j)+calculate(i+j) == n-4:\n            res += 2\nprint(res)'
SAMPLE='5\n'
GENERATOR_NAME='g8466'
def g8466(r):
    n=r.choice([1,5,10,15,24]); return f"{'0'*r.randint(0,20)}{n}\n"

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
