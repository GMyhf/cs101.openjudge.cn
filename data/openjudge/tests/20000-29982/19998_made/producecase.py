import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/19998 statistics, Accepted solution 52529434.\n# Source: http://cs101.openjudge.cn/practice/solution/52529434/\n# Statistics: http://cs101.openjudge.cn/practice/19998/statistics/\n# License: not declared on submission page; no license inferred\nm,n=map(int,input().split())\nhp=list(map(int,input().split()))+list(map(int,input().split()))\ndef mani():\n    con=False\n    for i in range(14):\n        if hp[i]>=2:\n            hp[i]-=1\n        elif hp[i]==1:\n            hp[i]-=1\n            con=True\n    if con:\n        mani()\n\ndef pan():\n    for i in range(14):\n        if hp[i]>0:\n            return False\n    return True\n\nwhile m>=1 and n>=2:\n    m-=1\n    n-=2\n    mani()\n\nif pan():\n    print("YES")\nelse:\n    print("NO")\n'
SAMPLE='2 10\n3 3 5 2 2 6 4 \n1 1 4 8 8 3 7\n'
GENERATOR_NAME='g19998'
def g19998(r):
    m, n = r.randint(0, 2), r.randint(0, 10)
    if r.random() < .5:
        m, n = 2, 10
        values = [r.randint(1, 3) for _ in range(14)]
    else:
        values = [r.randint(6, 10) for _ in range(14)]
    return f"{m} {n}\n" + "\n".join(
        " ".join(map(str, values[i:i + 7])) for i in (0, 7)
    ) + "\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        src=Path(d)/'main.py'; src.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(src)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i,text in enumerate(cases):
        (data/f'{i}.in').write_text(text); (data/f'{i}.out').write_text(run(text))
if __name__=='__main__': main()
