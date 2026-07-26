import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='n = int(input())\ntable = []\nfor _ in range(n):\n    a, b = input().split()\n    table.append((a, int(b)))\ntable.sort(key = lambda x: (-x[1], x[0]))\nfor i in table:\n    print(*i)'
SAMPLE='4\nKitty 80\nHanmeimei 90\nJoey 92\nTim 28\n'
GENERATOR_NAME='g7615'
def g7615(r):
    n=r.randint(2,15); names=[f"S{i}" for i in range(n)]
    return f"{n}\n"+"\n".join(f"{x} {r.randint(0,100)}" for x in names)+"\n"

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
