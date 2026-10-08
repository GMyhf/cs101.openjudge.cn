import random, subprocess, sys, tempfile
from pathlib import Path
def valid(text):
    """题面：第 1 行组数 n，后跟 n 行，每行一个正整数 a（1 < a < 32768）。"""
    import re
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    if not re.fullmatch(r'[1-9]\d*', lines[0]):
        return False
    n = int(lines[0])
    if len(lines) != n + 1:
        return False
    for line in lines[1:]:
        if not re.fullmatch(r'[1-9]\d*', line) or not (1 < int(line) < 32768):
            return False
    return True

def g2749(r, seed):
    # 题面：1 < a < 32768；补上下界、最大质数、2 的幂与高合成数
    if seed == 1:
        values = [2, 3, 4, 32767, 32766, 16384, 32749, 32719]
    elif seed == 2:
        values = [27720, 30240, 32760, 20160, 25200, 15120, 30030, 13860, 10080]
    elif seed == 3:
        values = [2 ** k for k in range(1, 15)] + [3 ** k for k in range(1, 10)]
    elif seed <= 10:
        values = [r.randint(16384, 32767) for _ in range(50)]
    elif seed <= 25:
        values = [r.randint(2, 32767) for _ in range(r.randint(1, 20))]
    else:
        values = [r.randint(2, 500) for _ in range(r.randint(1, 12))]
    return str(len(values)) + "\n" + "\n".join(map(str, values)) + "\n"

REFERENCE='# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 2749: 分解因数\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/2025sp_routine/02749/\n# License: not declared in source collection; no license is inferred.\n# 蒋子轩23工学院\ndef decompositions(n,minfactor):\n    if n==1:\n        return 1\n    count=0\n    for i in range(minfactor,n+1):\n        if n%i==0:\n        #递归，只找更大的因数，避免重复\n            count+=decompositions(n//i,i)\n    return count\nn=int(input())\nfor _ in range(n):\n    x=int(input())\n    print(decompositions(x,2))\n'
SAMPLE='2\n2\n20\n'
GENERATOR='g2749'

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as folder:
        script=Path(folder)/"main.py"; script.write_text(REFERENCE)
        result=subprocess.run([sys.executable,"-I",str(script)],input=text,text=True,capture_output=True,timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    for old in data.glob("*"): old.unlink()
    cases=[SAMPLE]+[globals()[GENERATOR](random.Random(seed), seed) for seed in range(1, 40)]
    for i,case in enumerate(cases):
        (data/f"{i}.in").write_text(case); (data/f"{i}.out").write_text(run(case))
if __name__=="__main__": main()
