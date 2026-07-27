import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/23745/\n# Accepted submission: 52740135\n# Source: http://cs101.openjudge.cn/practice/solution/52740135/\n# License: not declared on the submission page; no license is inferred.\n\nn = int(input())\norig = list(map(int, input().split()))\ndisc = list(map(int, input().split()))\n\nsum_o = sum(orig)\nsum_d = sum(disc)\n\n# 方案1总价：满足满55-20才减20，否则原价\nif sum_o >= 55:\n    cost1 = sum_o - 20\nelse:\n    cost1 = sum_o\ncost2 = sum_d\n\n# 判断输出\nif cost1 < cost2:\n    print(1)\nelif cost2 < cost1:\n    print(2)\nelse:\n    print(3)'
SAMPLE='3\n20 5 10\n15 3 7\n'
GENERATOR_NAME='g23745'
def g23745(r):
    n=r.randint(1,5); return f"{n}\n"+" ".join(str(r.randint(1,100)) for _ in range(n))+"\n"+" ".join(str(r.randint(1,100)) for _ in range(n))+"\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+(['8\n','9\n'] if GENERATOR_NAME == 'g22007' else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
