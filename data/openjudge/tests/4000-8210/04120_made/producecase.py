"""4120 硬币 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 40 组数据。

第 0 组为题面样例；覆盖 n=1、没有必须硬币（输出 0 和空行）、全部硬币都必须、
存在面值大于 x 的硬币、小规模随机（可暴力核对）、以及 n=200、x 接近 10000 的满规模组。
参考解为同目录 samplecode.cpp（逐个去掉一枚硬币做 0/1 背包）。
"""
import random
import re
import subprocess
from pathlib import Path

SAMPLE_IN = '5 18\n1 2 3 5 10\n'


def reachable(coins, x):
    bits = 1
    mask = (1 << (x + 1)) - 1
    for c in coins:
        bits = (bits | (bits << c)) & mask
    return bits >> x & 1 == 1


def valid(text):
    """题面：第一行 n x（1<=n<=200，1<=x<=10000）；第二行 n 个从小到大的正整数 ai（1<=ai<=10000），
    每种面值只有一个（互不相同）；保证至少有一种组合恰好凑出 x。"""
    if not isinstance(text, str) or not text.endswith("\n") or "\r" in text:
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 2:
        return False
    head, body = lines[0].split(" "), lines[1].split(" ")
    num = re.compile(r"[1-9]\d*")
    if len(head) != 2 or not all(num.fullmatch(v) for v in head + body):
        return False
    n, x = map(int, head)
    if not (1 <= n <= 200 and 1 <= x <= 10000) or len(body) != n:
        return False
    coins = list(map(int, body))
    if not all(1 <= c <= 10000 for c in coins):
        return False
    if any(coins[i] >= coins[i + 1] for i in range(n - 1)):
        return False
    return reachable(coins, x)


def fmt(coins, x):
    coins = sorted(coins)
    return f"{len(coins)} {x}\n" + " ".join(map(str, coins)) + "\n"


def subset_case(r, n, hi, x_cap=10000):
    # 随机硬币，x 取某个随机子集之和（保证可凑）：随机顺序逐枚加入，不超过随机目标上限
    coins = r.sample(range(1, hi + 1), n)
    cap = r.randint(1, x_cap)
    order = coins[:]
    r.shuffle(order)
    x = 0
    for c in order:
        if x + c <= cap and r.random() < 0.7:
            x += c
    if x == 0:
        x = min(coins)
    return fmt(coins, x)


def special_case(r, n, base, specials, x_cap=10000):
    """大部分硬币是 base 的倍数，另有几枚「特殊」硬币不是；x = 特殊硬币之和 + base 的倍数，
    且特殊硬币的余数设计成只有全用上才能凑出 x mod base → 这些特殊硬币必须使用。"""
    while True:
        pool = list(range(base, 10001, base))
        many = r.sample(pool, min(n - specials, len(pool)))
        sp = set()
        while len(sp) < specials:
            c = r.randint(1, 2000)
            if c % base == 1 and c not in many:
                sp.add(c)
        sp = sorted(sp)
        rest = r.sample(many, r.randint(0, min(len(many), 6)))
        x = sum(sp) + sum(rest)
        if x <= x_cap and specials < base:
            return fmt(many + sp, x)


def build_cases():
    r = random.Random(4120)
    cases = [SAMPLE_IN]
    cases.append("1 5\n5\n")                                   # 1 n=1，必须用
    cases.append("3 3\n1 2 3\n")                               # 2 没有必须硬币 → 0 + 空行
    cases.append("4 15\n1 2 4 8\n")                            # 3 全部都必须
    cases.append("6 7\n3 4 7 20 9999 10000\n")                 # 4 有面值大于 x 的硬币，答案 0
    cases.append("5 10000\n1 2 3 4 10000\n")                   # 5 x 上限，只能用 10000 那枚
    cases.append("1 10000\n10000\n")                           # 6 n=1 x=10000
    cases.append("200 1\n" + " ".join(map(str, range(1, 201))) + "\n")   # 7 x=1，只能用 1
    cases.append("200 10000\n" + " ".join(map(str, range(1, 201))) + "\n")  # 8 n=200 连续面值
    for _ in range(9, 20):                                     # 9-19 小规模，可暴力
        n = r.randint(2, 15)
        cases.append(subset_case(r, n, r.choice([20, 50, 300])))
    for _ in range(20, 26):                                    # 20-25 中规模
        n = r.randint(40, 120)
        cases.append(subset_case(r, n, r.choice([500, 3000, 10000])))
    for k in range(26, 32):                                    # 26-31 满规模，含必须硬币
        cases.append(special_case(r, 200, r.choice([7, 11, 13, 50]), r.randint(1, 5)))
    for k in range(32, 40):                                    # 32-39 满规模随机
        n = 200
        hi = r.choice([400, 2000, 10000])
        coins = r.sample(range(1, hi + 1), n)
        if k % 2 == 0:
            x = r.randint(9000, 10000)
            while not reachable(coins, x):
                x = r.randint(9000, 10000)
            cases.append(fmt(coins, x))
        else:
            cases.append(subset_case(r, n, hi))
    return cases


def main():
    root = Path(__file__).parent
    binary = root / "reference"
    subprocess.run(["g++", "-std=c++17", "-O2", str(root / "samplecode.cpp"), "-o", str(binary)], check=True)
    try:
        cases = build_cases()
        assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
        assert len(set(cases)) == len(cases), "存在重复组"
        for i, c in enumerate(cases):
            assert valid(c), i
            p = subprocess.run([str(binary)], input=c, text=True, capture_output=True, check=True)
            (root / "data" / f"{i}.in").write_text(c)
            (root / "data" / f"{i}.out").write_text(p.stdout)
        assert (root / "data" / "0.out").read_text().split() == ["2", "5", "10"]
    finally:
        binary.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
