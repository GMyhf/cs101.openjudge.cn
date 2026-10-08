"""9201 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001c
生成器与循环取自 scripts/build_001c.py（批次 001c），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 9201
SAMPLE_IN = '5\n1 3 10 8 5\n'
SAMPLE_OUT = '7\n'
REFERENCE_SOURCE = '#蒋子轩\nfrom bisect import *\nn=int(input())\na=list(map(int,input().split()))\nsorted_list=[]\ncnt=0\nfor num in a:\n    pos=bisect_left(sorted_list,num)\n    cnt+=pos\n    insort_left(sorted_list,num)\nprint(cnt)\n'

def valid(text):
    """题面：第一行 N（2<=N<=100000）；第二行 N 个非负整数，「速度各不相同」。"""
    lines = text.split("\n")
    if len(lines) != 3 or lines[2] != "":
        return False
    head = lines[0].split()
    if len(head) != 1 or not head[0].isdigit():
        return False
    n = int(head[0])
    vals = lines[1].split()
    if not 2 <= n <= 100000 or len(vals) != n or not all(v.isdigit() for v in vals):
        return False
    return len(set(map(int, vals))) == n


def fmt(values):
    return f"{len(values)}\n" + " ".join(map(str, values)) + "\n"


def g9201(r):
    # 2026-10 审计：原写法 randint 独立抽取，20 组里 19 组有重复速度，违反「速度各不相同」
    n = r.randint(5, 1000); values = r.sample(range(0, 10001), n)
    return fmt(values)


def extra_cases():
    """2026-10 审计补充：原数据 N<=1000，O(N^2) 暴力能过；也没有 N=2、单调、
    答案超过 2^31 的情形。"""
    r = random.Random(92010)
    out = [[0, 1], [1, 0], [0, 1000000000], list(range(10)), list(range(9, -1, -1))]
    out.append(r.sample(range(1000000), 100000))
    out.append(list(range(100000)))                      # 全部赶超：N(N-1)/2 ≈ 5e9
    out.append(list(range(99999, -1, -1)))               # 无赶超：0
    out.append(r.sample(range(1000000000), 80000))       # 大值域
    near = list(range(100000))                           # 近乎有序，少量扰动
    for _ in range(2000):
        i, j = r.randrange(100000), r.randrange(100000)
        near[i], near[j] = near[j], near[i]
    out.append(near)
    return [fmt(v) for v in out]

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g9201(random.Random(NUMBER + i + attempt * 1000))
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
    cases += [c for c in extra_cases() if c not in cases]
    assert all(valid(c) for c in cases), "题面：2<=N<=100000，速度各不相同"
    return cases

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
