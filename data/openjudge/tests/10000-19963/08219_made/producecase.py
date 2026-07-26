import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='n = int(input())\nif n > 0:\n    print(\'positive\')\nelif n < 0:\n    print(\'negative\')\nelse:\n    print("zero")'
SAMPLE='1\n'
GENERATOR_NAME='g8219'
def g8219(r):
    value=r.choice([-10**9,-1,0,1,10**9]) if r.random()<.25 else r.randint(-10**9,10**9)
    return f"{value}\n"

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
