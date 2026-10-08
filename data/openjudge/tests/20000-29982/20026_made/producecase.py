import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/20026 statistics, Accepted solution 52332704.\n# Source: http://cs101.openjudge.cn/practice/solution/52332704/\n# Statistics: http://cs101.openjudge.cn/practice/20026/statistics/\n# License: not declared on submission page; no license inferred\nn=int(input())\nif n%2==1:\n    print(1)\nif n%4==2:\n    print(2)\nif n%4==0:\n    print(n)\n'
SAMPLE='1\n'
GENERATOR_NAME='g20026'
def g20026(r):
    a, b = r.randint(0, 8), r.randint(0, 6)
    return f"{2 ** a * 3 ** b}\n"

def valid(text):
    """题面契约：一个正整数 n，且 n 只含质因子 2 和 3（n=1 视为满足）。题面无上界。"""
    import re
    if not re.fullmatch(r"[1-9]\d*\n", text):
        return False
    n = int(text)
    for q in (2, 3):
        while n % q == 0:
            n //= q
    return n == 1

def distinct_cases():
    """原生成器 39 个种子只落在 63 个 2^a·3^b 上，有 7 组重复、2 和 3 都没出现。
    这里改成：题面 4 个样例值 + 不重复地抽取其余 2^a·3^b（a<=8，b<=6，与原值域相同），
    并排除 4·3^6=2916（a=2 时 4·3^b 型 Hadamard 矩阵的存在性在 b=6 上不靠已知构造兜底）。"""
    pool = [2 ** a * 3 ** b for a in range(9) for b in range(7) if (a, b) != (2, 6)]
    head = [1, 2, 3, 4]
    rest = [x for x in pool if x not in head]
    random.Random(20026).shuffle(rest)
    picked = head + sorted(rest[:36], key=lambda x: (x % 4 != 0, x % 2 == 1, x))
    return [f"{x}\n" for x in picked]

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        src=Path(d)/'main.py'; src.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(src)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=distinct_cases()
    assert cases[0] == SAMPLE and len(cases) == 40 and len(set(cases)) == 40 and all(valid(c) for c in cases)
    for i,text in enumerate(cases):
        (data/f'{i}.in').write_text(text); (data/f'{i}.out').write_text(run(text))
if __name__=='__main__': main()
