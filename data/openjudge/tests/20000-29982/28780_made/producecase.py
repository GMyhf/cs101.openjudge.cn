import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'from math import inf\nn, m = map(int, input().split())\ncoins = list(map(int, input().split()))\ndp = [0] + [inf for _ in range(m)]\nfor i in range(n):\n    for j in range(coins[i], m + 1):\n        dp[j] = min(dp[j], dp[j - coins[i]] + 1)\nprint(dp[m] if dp[m] != inf else -1)\n'
SAMPLE_IN = '3 11\n1 2 4\n'
SAMPLE_OUT = '4\n'
def generate_case(r):
    # 题面：所有硬币面值均小于 m（原写法会生成大于 m 的面值）
    amount = r.randint(2, 100)
    coins = sorted(set(r.randint(1, min(30, amount - 1)) for _ in range(r.randint(2, 6))))
    return f"{len(coins)} {amount}\n" + " ".join(map(str, coins)) + "\n"


def valid(text):
    """题面契约：两行；首行 n m（1≤n≤100，0≤m≤10^6）；第二行恰 n 个互异正整数面值，且均小于 m。"""
    if not text.endswith("\n") or "\r" in text:
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 2:
        return False
    def ints(line):
        parts = line.split(" ")
        if any(not p.isdigit() or (len(p) > 1 and p[0] == "0") for p in parts):
            return None
        return [int(p) for p in parts]
    first, coins = ints(lines[0]), ints(lines[1])
    if first is None or coins is None or len(first) != 2:
        return False
    n, m = first
    if not (1 <= n <= 100 and 0 <= m <= 10 ** 6) or len(coins) != n or len(set(coins)) != n:
        return False
    return all(1 <= c < m for c in coins)


def fmt(m, coins):
    return f"{len(coins)} {m}\n" + " ".join(map(str, coins)) + "\n"


def extra_cases():
    """追加的规模/边界组。参考解是 O(n·m) 的 Python DP，单组 n·m 控制在约 1e7 以内。"""
    r = random.Random(287800)
    out = ["1 3\n2\n"]                                             # 题面样例 2
    out.append(fmt(2, [1]))                                        # 最小 m
    out.append(fmt(10 ** 6, [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]))   # m 上限
    out.append(fmt(10 ** 6, [7, 13, 999983]))
    out.append(fmt(10 ** 6, [500000]))                             # 单币整除
    out.append(fmt(10 ** 6, [3]))                                  # 单币不整除 → -1
    out.append(fmt(999999, [2, 4, 8, 16, 1000, 99998]))            # 全偶数凑奇数 → -1
    out.append(fmt(10 ** 6, [1, 4999, 7001, 10007]))              # 贪心取最大面值会错
    out.append(fmt(6, [1, 3, 4]))                                  # 小规模贪心反例，答案 2
    out.append(fmt(100000, list(range(1000, 1100))))               # n 上限
    out.append(fmt(100000, sorted(r.sample(range(1, 100000), 100))))
    out.append(fmt(99991, sorted(r.sample(range(2, 100000, 2), 100))))   # n 上限且无解
    out.append(fmt(10 ** 6, sorted(r.sample(range(10000, 999999), 8))))
    out.append(fmt(999997, sorted(r.sample(range(100, 5000), 10))))
    out.append(fmt(50000, sorted(r.sample(range(1, 50000), 100), reverse=True)))  # 面值降序给出
    return out


def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        for index in range(20):
            if index == 0: content = SAMPLE_IN
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(28780 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
        for index, content in enumerate(extra_cases(), start=20):
            assert content not in seen, index
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=60, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
        assert (root / "0.out").read_text(encoding="utf-8") == SAMPLE_OUT
        for index in range(len(seen) - 1):
            assert valid((root / f"{index}.in").read_text(encoding="utf-8")), index


if __name__ == "__main__":
    main()
