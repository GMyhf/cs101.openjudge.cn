"""4118 开餐馆 测试数据生成器：固定种子 4118，重跑可逐字节复现 data/ 下的 20 组数据。

第 0 组为题面样例；覆盖 n=1、间距恰为 k（卡 >= 写法）、只能开一家/全部能开、
T=1000 且 n=99 的满规模组，以及位置接近 999999 的组。
"""
def solve_text(text):
    it = iter(text.split()); out = []
    for _ in range(int(next(it))):
        n, k = int(next(it)), int(next(it))
        pos = [int(next(it)) for _ in range(n)]
        profit = [int(next(it)) for _ in range(n)]
        dp = [0] * n
        for i in range(n):
            dp[i] = profit[i] + max(
                [dp[j] for j in range(i) if pos[i] - pos[j] > k] or [0]
            )
        out.append(str(max(dp)))
    return "\n".join(out) + "\n"


def fmt(tests):
    lines = [str(len(tests))]
    for n, k, positions, profits in tests:
        lines += [f"{n} {k}", " ".join(map(str, positions)), " ".join(map(str, profits))]
    return "\n".join(lines) + "\n"


def rand_test(rng, n, k, span, pmax=999):
    return (n, k, sorted(rng.sample(range(1, span), n)), [rng.randint(1, pmax) for _ in range(n)])


def step_test(rng, n, k, step, start=1):
    # 等间距：间距恰为 k 时卡「距离 >= k」的写法
    return (n, k, [start + i * step for i in range(n)], [rng.randint(1, 999) for _ in range(n)])


def generate_case(rng, index):
    if index == 1:
        # 原有手造组 + 最小规模
        return fmt([(3, 11, [1, 2, 10], [15, 2, 30]), (4, 2, [1, 4, 7, 10], [5, 8, 4, 10]),
                    (1, 1, [1], [1]), (1, 999, [999999], [999]), (2, 1, [1, 2], [5, 7]),
                    (2, 1, [1, 3], [5, 7])])
    if index == 2:
        # 间距恰为 k / k+1 / k-1
        tests = []
        for k in (1, 2, 7, 500, 999):
            for step in (k - 1, k, k + 1):
                if step >= 1:
                    tests.append(step_test(rng, rng.randint(5, 20), k, step))
        return fmt(tests)
    if index == 3:
        # k 很大、位置很密：只能开一家，答案是最大利润
        return fmt([rand_test(rng, rng.randint(1, 99), 999, 1000) for _ in range(30)])
    if index == 4:
        # 位置很稀：全都能开，答案是利润和
        return fmt([(n, 1, sorted(rng.sample(range(1, 999999, 3), n)), [rng.randint(1, 999) for _ in range(n)])
                    for n in (1, 50, 99)])
    if index <= 10:
        # 小规模随机，便于暴力核对
        tests = []
        for _ in range(rng.randint(5, 40)):
            n = rng.randint(1, 14)
            k = rng.randint(1, 30)
            tests.append(rand_test(rng, n, k, rng.randint(n + 1, 120), rng.choice([9, 100, 999])))
        return fmt(tests)
    if index <= 15:
        # 中等：n 接近 99，位置跨度与 k 同量级，结构复杂
        tests = []
        for _ in range(rng.randint(50, 200)):
            k = rng.randint(1, 999)
            n = rng.randint(60, 99)
            tests.append(rand_test(rng, n, k, rng.randint(n + 1, 100 * k + n + 2)))
        return fmt(tests)
    if index <= 17:
        # T=1000 满规模（位置 4 位，控制文件 < 1MB）
        tests = []
        for _ in range(1000):
            k = rng.randint(1, 999)
            tests.append(rand_test(rng, 99, k, rng.randint(100, 9999)))
        return fmt(tests)
    # 大位置值 999999 附近
    tests = []
    for _ in range(400):
        k = rng.randint(1, 999)
        n = rng.randint(90, 99)
        lo = rng.randint(1, 999999 - 100 * 999)
        tests.append((n, k, sorted(rng.sample(range(lo, min(999999, lo + 50 * k + n + 1)), n)),
                      [rng.randint(1, 999) for _ in range(n)]))
    return fmt(tests)


def valid(text):
    """题面：第一行 T（1<=T<=1000）；每组 3 行：n k（n<100，0<k<1000）；
    n 个升序（严格递增）位置 0<mi<1000000；n 个利润 0<pi<1000。"""
    if not isinstance(text, str) or not text.endswith("\n") or "\r" in text:
        return False
    lines = text[:-1].split("\n")
    if not re.fullmatch(r"[1-9]\d*", lines[0]):
        return False
    t = int(lines[0])
    if not 1 <= t <= 1000 or len(lines) != 1 + 3 * t:
        return False
    num = re.compile(r"[1-9]\d*")
    for g in range(t):
        head, pos, pro = (lines[1 + 3 * g + j].split(" ") for j in range(3))
        if len(head) != 2 or not all(num.fullmatch(x) for x in head):
            return False
        n, k = map(int, head)
        if not (1 <= n < 100 and 0 < k < 1000):
            return False
        if len(pos) != n or len(pro) != n or not all(num.fullmatch(x) for x in pos + pro):
            return False
        pos = list(map(int, pos)); pro = list(map(int, pro))
        if not all(0 < x < 1000000 for x in pos) or not all(0 < x < 1000 for x in pro):
            return False
        if any(pos[i] >= pos[i + 1] for i in range(n - 1)):
            return False
    return True

import random
import re
from pathlib import Path
SAMPLE_IN = '2\n3 11\n1 2 15\n10 2 30\n3 16\n1 2 15\n10 2 30\n'
SAMPLE_OUT = '40\n30\n'
def main():
    assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
    rng = random.Random(4118)
    root = Path(__file__).parent / "data"
    cases = [SAMPLE_IN] + [generate_case(rng, index) for index in range(1, 20)]
    assert len(set(cases)) == len(cases), "存在重复组"
    for index, content in enumerate(cases):
        assert valid(content), index
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
    print("generated 20 cases for 04118")


if __name__ == "__main__":
    main()
