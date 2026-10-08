import random
REFERENCE='# External reference: /practice/30497/statistics/\n# Accepted submission: 52740197\n# Source: http://cs101.openjudge.cn/practice/solution/52740197/\n# License: not declared on the submission page; no license is inferred.\n\n# 只需要输出：\nprint("undecidable")'
SAMPLE='2\n1 1 1 1\n2 2 2 2\n'
GENERATOR_NAME='g30497'
CPP=False
def g30497(r):
    # 本题按题面提示任何输入都输出 undecidable；这里只让各组输入互不相同、覆盖 N 与颜色的取值范围
    n = r.choice([1, 2, r.randint(1, 100), r.randint(50, 100), 100])
    hi = r.choice([1, 3, 10, 1000])
    return f"{n}\n" + "".join(" ".join(str(r.randint(0, hi)) for _ in range(4)) + "\n" for _ in range(n))


def valid(text):
    """题面契约：第一行 N（1<=N<=100）；接下来 N 行每行 4 个整数 T R B L，0<=颜色<=1000。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not lines[0].isdigit() or str(int(lines[0])) != lines[0]:
        return False
    n = int(lines[0])
    if not 1 <= n <= 100 or len(lines) != n + 1:
        return False
    for line in lines[1:]:
        toks = line.split(" ")
        if len(toks) != 4 or any(not t.isdigit() or str(int(t)) != t or int(t) > 1000 for t in toks):
            return False
    return True


def fixed_cases():
    return ["1\n1 1 1 1\n",
            "100\n" + "1000 1000 1000 1000\n" * 100,
            "1\n0 0 0 0\n",
            "2\n0 1000 0 1000\n1000 0 1000 0\n"]

from pathlib import Path
import subprocess, sys, tempfile
def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/('main.cpp' if CPP else 'main.py'); p.write_text(REFERENCE)
        if CPP:
            exe=Path(d)/'main'; c=subprocess.run(['g++','-O2','-std=c++17',str(p),'-o',str(exe)],capture_output=True,text=True,timeout=30)
            if c.returncode: raise SystemExit(c.stderr)
            cmd=[str(exe)]
        else: cmd=[sys.executable,str(p)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=120)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+fixed_cases()
    s=1
    while len(cases)<40:
        c=globals()[GENERATOR_NAME](random.Random(s)); s+=1
        if c not in cases: cases.append(c)
    assert all(valid(c) for c in cases)
    for i,c in enumerate(cases): (data/f'{i}.in').write_text(c); (data/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
