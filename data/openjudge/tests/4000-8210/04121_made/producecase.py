"""4121 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

覆盖：N=1、价格取到 ±1000000、单调递增/递减/常数、可暴力核对的小规模组、
N=100000 满规模（随机、单调、锯齿、两段大涨），以及 T=50 的多组数据。

出处：build_001b
生成器与循环取自 scripts/build_001b.py（批次 001b），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import re
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4121
SAMPLE_IN = '3\n7\n5 14 -2 4 9 3 17\n6\n6 8 7 4 1 -2\n4\n18 9 5 2\n'
SAMPLE_OUT = '28\n2\n0\n'
REFERENCE_SOURCE = 'def solve():\n    import sys\n    input = sys.stdin.readline\n\n    T = int(input().strip())\n    for _ in range(T):\n        N = int(input().strip())\n        prices = list(map(int, input().split()))\n\n        if N <= 1:\n            print(0)\n            continue\n\n        # 1. 从左到右，计算一次交易的最大利润\n        left = [0] * N\n        min_price = prices[0]\n        for i in range(1, N):\n            min_price = min(min_price, prices[i])\n            left[i] = max(left[i - 1], prices[i] - min_price)\n\n        # 2. 从右到左，计算一次交易的最大利润\n        right = [0] * N\n        max_price = prices[-1]\n        for i in range(N - 2, -1, -1):\n            max_price = max(max_price, prices[i])\n            right[i] = max(right[i + 1], max_price - prices[i])\n\n        # 3. 合并\n        res = 0\n        for i in range(N):\n            res = max(res, left[i] + right[i])\n\n        print(res)\n\nif __name__ == "__main__":\n    solve()\n'

def valid(text):
    """题面：第一行 T（T <= 50）；每组两行：N（1 <= N <= 100000），以及 N 个空格分隔的整数，
    每个价格的绝对值不超过 1000000。"""
    if not isinstance(text, str) or not text.endswith("\n") or "\r" in text:
        return False
    lines = text[:-1].split("\n")
    if not re.fullmatch(r"[1-9]\d*", lines[0]):
        return False
    t = int(lines[0])
    if not 1 <= t <= 50 or len(lines) != 1 + 2 * t:
        return False
    num = re.compile(r"-?(0|[1-9]\d*)")
    for g in range(t):
        n_line, row = lines[1 + 2 * g], lines[2 + 2 * g]
        if not re.fullmatch(r"[1-9]\d*", n_line) or not 1 <= int(n_line) <= 100000:
            return False
        vals = row.split(" ")
        if len(vals) != int(n_line) or not all(num.fullmatch(v) and v != "-0" for v in vals):
            return False
        if not all(abs(int(v)) <= 1000000 for v in vals):
            return False
    return True


LIM = 1_000_000


def pack(arrays):
    return str(len(arrays)) + "\n" + "".join(f"{len(a)}\n" + " ".join(map(str, a)) + "\n" for a in arrays)


def rand_arr(r, n, lo=-LIM, hi=LIM):
    return [r.randint(lo, hi) for _ in range(n)]


def walk(r, n, step):
    v = r.randint(-LIM // 2, LIM // 2)
    out = []
    for _ in range(n):
        v = max(-LIM, min(LIM, v + r.randint(-step, step)))
        out.append(v)
    return out


def two_peaks(r, n):
    # 两段大涨被一段大跌隔开；最优是两次交易，且单次交易/重叠交易都会算错
    a = walk(r, n, 50)
    q = n // 4
    a[0], a[q], a[2 * q], a[3 * q], a[n - 1] = -LIM, LIM, -LIM + 1, LIM - 1, -LIM
    return a


def build_cases():
    r = random.Random(NUMBER)
    cases = [SAMPLE_IN]
    cases.append(pack([[7], [1, 2], [2, 1], [-LIM, LIM], [LIM, -LIM]]))                 # 1 N=1/2 与极值
    cases.append(pack([list(range(1, 11)), list(range(10, 0, -1)), [5] * 8,
                       [3, 1, 3, 1, 3], [1, 5, 2, 8, 3, 9]]))                            # 2 单调/常数/锯齿
    for _ in range(3, 9):                                                                # 3-8 小规模，可暴力
        cases.append(pack([rand_arr(r, r.randint(1, 12), *r.choice([(-LIM, LIM), (-10, 10), (0, 5)]))
                           for _ in range(r.randint(10, 50))]))
    for _ in range(9, 12):                                                               # 9-11 中规模
        cases.append(pack([rand_arr(r, r.randint(500, 2000)) for _ in range(r.randint(20, 50))]))
    cases.append(pack([rand_arr(r, 100000)]))                                            # 12 满规模随机
    cases.append(pack([sorted(rand_arr(r, 100000), reverse=True)]))                      # 13 递减 → 0
    cases.append(pack([sorted(rand_arr(r, 100000))]))                                    # 14 递增
    cases.append(pack([[LIM - i % 7 if i % 2 else -LIM + i % 7 for i in range(100000)]]))      # 15 剧烈锯齿
    cases.append(pack([two_peaks(r, 100000)]))                                           # 16 两段大涨
    cases.append(pack([walk(r, 2000, 1000) for _ in range(50)]))                         # 17 T=50 共 1e5
    cases.append(pack([walk(r, 100000, 30)]))                                            # 18 随机游走
    cases.append(pack([rand_arr(r, 1) for _ in range(25)] +
                      [two_peaks(r, r.randint(1000, 3000)) for _ in range(25)]))         # 19 T=50 混合
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
    assert len(set(cases)) == len(cases), "存在重复组"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        assert valid(content), index
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
