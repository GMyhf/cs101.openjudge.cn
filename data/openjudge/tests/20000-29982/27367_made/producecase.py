import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/27367/\n# Accepted submission: 52735844\n# Source: http://cs101.openjudge.cn/practice/solution/52735844/\n# License: not declared on the submission page; no license is inferred.\n\nn, m = map(int, input().split())\nstudents = []\n\nfor _ in range(n):\n    parts = list(map(int, input().split()))\n    idx = parts[0]          # 编号\n    scores = parts[1:]     # 分数列表\n\n    # 1. 计算优秀次数（>=90）\n    excellent = sum(1 for s in scores if s >= 90)\n\n    # 2. 计算进步总和\n    progress = 0\n    for i in range(1, len(scores)):\n        diff = scores[i] - scores[i-1]\n        if diff > 0:\n            progress += diff\n\n    students.append((-excellent, -progress, idx))  # 负号=降序\n\n# 排序：默认升序，负号就等价于降序\nstudents.sort()\n\n# 输出\nfor s in students:\n    print(s[2])'
SAMPLE='5 4\n1001 60 80 90 90\n1002 90 80 91 92\n1003 95 94 93 92\n1004 70 90 80 85\n1005 85 88 91 96\n'
EXTRA_CASE=None
GENERATOR_NAME='g27367'
def g27367(r):
    n, m = r.randint(1, 80), r.randint(1, 12)
    rows = [f"{1000+i} {' '.join(str(r.randint(60, 100)) for _ in range(m))}" for i in range(n)]
    return f"{n} {m}\n" + "\n".join(rows) + "\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=90)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def scale_case(): return EXTRA_CASE
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    extra=scale_case(); cases=[SAMPLE]+([extra] if extra else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
