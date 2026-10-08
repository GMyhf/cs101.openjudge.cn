"""3441 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据（第 10 组起为边界/规模组）。

出处：build_001a
生成器与循环取自 scripts/build_001a.py（批次 001a），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import re
import subprocess
import tempfile
from pathlib import Path

NUMBER = 3441
SAMPLE_IN = '6\n-45 22 42 -16\n-41 -27 56 30\n-36 53 -37 77\n-36 30 -75 -46\n26 -38 -10 62\n-32 -54 -6 45\n'
SAMPLE_OUT = '5\n'
REFERENCE_SOURCE = "# https://docs.python.org/3/library/array.html\nimport array as arr\n\nn = int(input())\na = arr.array('i', [0]*(n+1))\nb = arr.array('i', [0]*(n+1))\nc = arr.array('i', [0]*(n+1))\nd = arr.array('i', [0]*(n+1))\n\nfor i in range(n):\n    a[i],b[i],c[i],d[i] = map(int, input().split())\n\n\ndict1 = {}\nfor i in range(n):\n    for j in range(n):\n        if not a[i]+b[j] in dict1:\n            dict1[a[i] + b[j]] = 0\n        dict1[a[i] + b[j]] += 1\n\nans = 0\nfor i in range(n):\n    for j in range(n):\n        if -(c[i]+d[j]) in dict1:\n            ans += dict1[-(c[i]+d[j])]\n\nprint(ans)\n"

LIM = 1 << 28  # 题面：absolute value as large as 2^28


def valid(text):
    """题面契约：首行 n（1 <= n <= 4000），随后恰好 n 行、每行 4 个整数，|v| <= 2^28。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    head = lines[0].split()
    if len(head) != 1 or not re.fullmatch(r"\d+", head[0]):
        return False
    n = int(head[0])
    if not 1 <= n <= 4000 or len(lines) != n + 1:
        return False
    for line in lines[1:]:
        toks = line.split()
        if len(toks) != 4:
            return False
        for t in toks:
            if not re.fullmatch(r"-?\d+", t) or abs(int(t)) > LIM:
                return False
    return True


def fmt(rows):
    return str(len(rows)) + "\n" + "\n".join(" ".join(map(str, x)) for x in rows) + "\n"


def g3441(r):
    n = r.choice([2, 4, 8, 12]); rows = [[r.randint(-20, 20) for _ in range(4)] for _ in range(n)]
    return fmt(rows)


def planted(r, n, lo, hi):
    """随机行，再把约四分之一的行改成 a+b+c+d=0（保证答案非零且覆盖跨行组合）。"""
    rows = [[r.randint(lo, hi) for _ in range(4)] for _ in range(n)]
    for i in r.sample(range(n), max(1, n // 4)):
        a, b, c = (r.randint(lo // 3, hi // 3) for _ in range(3))
        rows[i] = [a, b, c, -(a + b + c)]
    return fmt(rows)


def build_cases():
    cases = [SAMPLE_IN] + [g3441(random.Random(NUMBER + i)) for i in range(1, 10)]
    r = random.Random(NUMBER * 1000 + 7)
    cases.append(fmt([[0, 0, 0, 0]]))                          # n=1，答案 1
    cases.append(fmt([[LIM, LIM, -LIM, LIM]]))                 # n=1，答案 0，取值上界
    cases.append(fmt([[LIM, -LIM, LIM, -LIM], [-LIM, LIM, -LIM, LIM]]))  # 边界值互相抵消
    cases.append(fmt([[1, 2, 3, 4]] * 7))                      # 全正，答案 0
    cases.append(planted(r, 300, -LIM, LIM))                   # 中规模、大值域
    cases.append(fmt([[0, 0, 0, 0]] * 2000))                   # 答案 2000^4 = 1.6e13，卡 32 位计数
    cases.append(planted(r, 1000, -1000, 1000))                # 和碰撞很多
    cases.append(planted(r, 2000, -LIM, LIM))                  # 大规模、大值域，卡 O(n^4)/O(n^3)
    cases.append(planted(r, 2000, -50, 50))                    # 大规模、答案很大
    cases.append(fmt([[r.choice([-LIM, LIM, 0]) for _ in range(4)] for _ in range(1500)]))  # 只取 ±2^28 与 0
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
