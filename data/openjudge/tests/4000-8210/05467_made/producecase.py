"""5467 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001b
生成器与循环取自 scripts/build_001b.py（批次 001b），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 5467
SAMPLE_IN = '2\n-1 17 2 20 5 9 -7 7 10 4 22 2 -15 0 16 5 0 -1\n2 19 7 7 3 17 4 4 15 10 -10 5 13 2 -7 0 8 -8\n-1 17 2 23 22 2 6 8 -4 7 -18 0 1 5 21 4 0 -1\n12 7 -7 5 3 17 23 4 15 10 -10 5 13 5 2 19 9 -7\n'
SAMPLE_OUT = '[ 2 20 ] [ 2 19 ] [ 2 17 ] [ 15 10 ] [ 5 9 ] [ 6 5 ] [ 14 4 ] [ 35 2 ] [ -22 0 ]\n[ 2 23 ] [ 2 19 ] [ 2 17 ] [ 15 10 ] [ 6 8 ] [ 8 7 ] [ -3 5 ] [ 44 4 ] [ 22 2 ] [ -18 0 ]\n'
REFERENCE_SOURCE = "#23n2300011072(X)\nfrom collections import defaultdict\ndef add(a):\n    i=0\n    while 1:\n        m,n=a[i],a[i+1]\n        if n<0:\n            break\n        res[n]+=m\n        i+=2\nfor _ in range(int(input())):\n    res=defaultdict(int)\n    add(list(map(int,input().split())))\n    add(list(map(int,input().split())))\n    for i in sorted(res,reverse=True):\n        if res[i]!=0:\n            print(f'[ {res[i]} {i} ] ',end='')\n    print()\n"

def g5467(r):
    groups = r.randint(2, 5)
    lines = [str(groups)]
    for _ in range(groups * 2):
        exponents = r.sample(range(0, 50), r.randint(2, 10))
        pairs = []
        for exponent in exponents:
            pairs.append((str(r.randint(-30, 30) or 1), str(exponent)))
        r.shuffle(pairs)
        pairs.append((str(r.randint(1, 30)), str(-r.randint(1, 9))))
        lines.append(" ".join(value for pair in pairs for value in pair))
    return "\n".join(lines) + "\n"

def build_cases():
    return [SAMPLE_IN] + [g5467(random.Random(NUMBER + i)) for i in range(1, 20)]

def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=120, check=True)
    return result.stdout


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
    assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split(), "参考解法跑不出样例输出"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
