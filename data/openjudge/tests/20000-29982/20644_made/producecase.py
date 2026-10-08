"""20644 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001d
生成器与循环取自 scripts/build_001d.py（批次 001d），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 20644
SAMPLE_IN = '3 4\n0111\n1111\n0111\n'
SAMPLE_OUT = '15\n'
# 原参考解（同 samplecode.py）是逐个正方形逐格检查的暴力，最坏 O(m n min(m,n)^3)，
# 跑不动 300x300 全 1；改用 DP：dp[i][j] = 以 (i,j) 为右下角的最大全 1 正方形边长，答案为其和。
REFERENCE_SOURCE = """import sys
data = sys.stdin.read().split()
m, n = int(data[0]), int(data[1])
rows = data[2:2 + m]
prev = [0] * (n + 1)
total = 0
for i in range(m):
    row = rows[i]
    cur = [0] * (n + 1)
    for j in range(n):
        if row[j] == "1":
            v = min(prev[j], prev[j + 1], cur[j]) + 1
            cur[j + 1] = v
            total += v
    prev = cur
print(total)
"""

def g20644(r):
    m,n=r.randint(2,10),r.randint(2,10); return f"{m} {n}\n"+"\n".join("".join(r.choice("01") for _ in range(n)) for _ in range(m))+"\n"

def valid(text):
    """题面契约：第一行 "m n"（正整数）；随后恰 m 行，每行恰 n 个字符，每个是 0 或 1（与样例一致，不加分隔）。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    head = lines[0].split(" ")
    if len(head) != 2 or not all(t.isdigit() and t[0] != "0" for t in head):
        return False
    m, n = int(head[0]), int(head[1])
    if len(lines) != m + 1:
        return False
    return all(len(row) == n and set(row) <= set("01") for row in lines[1:])


def _mat(rows):
    return f"{len(rows)} {len(rows[0])}\n" + "\n".join(rows) + "\n"


def extra_cases():
    """补充：1x1、单行/单列、全 0、全 1（答案最大）、高密度大矩阵（卡逐个正方形暴力检查）。"""
    r = random.Random(NUMBER * 23 + 9)
    out = [_mat(["1"]), _mat(["0"]), _mat(["1101111"]), _mat(list("1110111")),
           _mat(["0" * 8] * 5), _mat(["1" * 9] * 6)]
    out.append(_mat(["1" * 300] * 300))
    out.append(_mat(["0" * 300] * 300))
    for p, (m, n) in ((0.95, (300, 300)), (0.85, (300, 250)), (0.5, (200, 300)), (0.99, (300, 300))):
        out.append(_mat(["".join("1" if r.random() < p else "0" for _ in range(n)) for _ in range(m)]))
    return out


def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g20644(random.Random(NUMBER + i + attempt * 1000))
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
    for value in extra_cases():
        if value not in cases:
            cases.append(value)
    for value in cases:
        assert valid(value), "生成的数据越出题面约束"
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
