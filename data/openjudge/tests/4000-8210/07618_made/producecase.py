import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='n=int(input())\noldage=[]\nteens=[]\nfor _ in range(n):\n    name,age=input().split()\n    age=int(age)\n    if age>=60:\n        oldage.append((name,age))\n    else:\n        teens.append((name,age))\noldage.sort(reverse=True,key=lambda x:x[1])\nfor name, age in oldage:\n    print(name)\nfor name, age in teens:\n    print(name)'
SAMPLE='5\n021075 40\n004003 15\n010158 67\n021033 75\n102012 30\n'
GENERATOR_NAME='g7618'
def g7618(r):
    n=r.randint(2,30); ids=r.sample(range(10**8),n)
    return f"{n}\n"+"\n".join(f"{x:08d} {r.randint(1,99)}" for x in ids)+"\n"

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
