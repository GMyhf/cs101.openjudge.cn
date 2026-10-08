"""3406 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 25 组数据。

出处：build_001a
生成器与循环取自 scripts/build_001a.py（批次 001a），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 3406
SAMPLE_IN = '6 40\n6\n18\n11\n13\n19\n11\n'
SAMPLE_OUT = '3\n'
REFERENCE_SOURCE = '# 蒋子轩23工学院\ndef min_cows_to_reach(N, B):\n\t# 二分查找变形，找大于等于B的最小索引\n    left, right = 1, N\n    while left < right:  #注意不能取等\n        mid = (left + right) // 2 #左偏\n        if prefix_sum[mid]>=B:  #等于时继续向左找\n            right = mid   #注意不-1，\n        else:\n            left = mid + 1\n    return left  #return不取等的那个\nN, B = map(int, input().split())\ncows = [int(input()) for _ in range(N)]\n#优先选择高的\ncows.sort(reverse=True)\n#计算前缀和\nprefix_sum = [0] * (len(cows) + 1)\nfor i in range(1, len(cows)+1):\n    prefix_sum[i] = prefix_sum[i-1] + cows[i-1]\nprint(min_cows_to_reach(N, B))\n'

def valid(text):
    """题面：第 1 行 N B；第 2..N+1 行每行一个 Hi。1<=N<=20000，1<=Hi<=10000，1<=B<=S<2000000007（S 为 Hi 之和）。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    def num(x):
        return x.isdigit() and (x == '0' or x[0] != '0')
    head = lines[0].split(' ')
    if len(head) != 2 or not all(map(num, head)):
        return False
    n, b = map(int, head)
    if not 1 <= n <= 20000 or len(lines) != n + 1:
        return False
    if not all(num(x) for x in lines[1:]):
        return False
    h = list(map(int, lines[1:]))
    if not all(1 <= x <= 10000 for x in h):
        return False
    return 1 <= b <= sum(h) < 2000000007

def g3406(r, i):
    N = 20000
    if i == 1: n, hs, b = 1, [1], 1
    elif i == 2: hs = [10000]; n, b = 1, 10000
    else:
        if i <= 4: n = 2
        elif i <= 12: n = N
        elif i <= 17: n = r.randint(1000, N)
        else: n = r.randint(1, 30)
        hi = 10000 if i % 3 else r.choice((1, 3, 100))
        hs = [r.randint(1, hi) for _ in range(n)]
        if i in (5, 6): hs = [10000] * n          # 全最大，S=2e8
        if i == 7: hs = [1] * n
        S = sum(hs)
        if i in (3, 5, 7, 13): b = S              # 必须全用：答案 N
        elif i in (4, 8, 14): b = r.randint(1, max(hs))  # 答案 1
        elif i == 9: b = S - min(hs) + 1          # 答案 N（少一头就差 1）
        elif i == 10:
            t = sorted(hs, reverse=True); k = r.randint(2, n - 1); b = sum(t[:k])  # 恰好等于前 k 大之和
        elif i == 11:
            t = sorted(hs, reverse=True); k = r.randint(2, n - 1); b = sum(t[:k]) + 1
        else: b = r.randint(1, S)
    return f"{n} {b}\n" + "\n".join(map(str, hs)) + "\n"

def build_cases():
    return [SAMPLE_IN] + [g3406(random.Random(NUMBER + i), i) for i in range(1, 25)]

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
