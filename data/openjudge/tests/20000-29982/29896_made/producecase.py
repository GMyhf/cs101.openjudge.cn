import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'def solve():\n    import sys\n    input = sys.stdin.read\n    data = input().split()\n    \n    X = int(data[0])\n    N = int(data[1])\n    coins = list(map(int, data[2:2+N]))\n    \n    # 去除大于 X 的硬币（无用）\n    coins = [c for c in coins if c <= X]\n    if not coins:\n        if X == 0:\n            return 0\n        else:\n            return -1\n    \n    # 排序\n    coins.sort()\n    \n    # 必须要有 1，否则无法覆盖 1\n    if coins[0] > 1:\n        return -1\n    \n    max_reach = 0  # 当前能覆盖 [1, max_reach]\n    count = 0      # 使用的硬币数量\n    \n    while max_reach < X:\n        # 选择满足 coin <= max_reach + 1 的最大面值硬币\n        candidate = -1\n        for coin in coins:\n            if coin <= max_reach + 1:\n                candidate = coin\n            else:\n                break  # 因为已排序，后面的更大\n        \n        if candidate == -1:\n            return -1  # 无法扩展\n        \n        max_reach += candidate\n        count += 1\n        \n        if max_reach >= X:\n            break\n    \n    return count\n\n# 主程序\nprint(solve())\n'
SAMPLE_IN = '20 4\n1 2 5 10\n'
def generate_case(r):
    n = r.randint(2, 10); coins = sorted(r.sample(range(1, 40), n)); x = r.randint(1, 300)
    assert len(set(coins)) == n
    return f"{x} {n}\n" + " ".join(map(str, coins)) + "\n"



def valid(text):
    """题面契约：第一行 X N；第二行恰 N 个硬币面值（「N 种不同面值」→ 互异的正整数）；
    提示 N <= 10，X <= 10000。题面没说面值有序、也没给面值上界。"""
    if not text.endswith("\n"):
        return False
    rows = text[:-1].split("\n")
    if len(rows) != 2:
        return False
    try:
        head = rows[0].split(" ")
        coins = [int(t) for t in rows[1].split(" ")]
        if len(head) != 2:
            return False
        x, n = int(head[0]), int(head[1])
    except ValueError:
        return False
    if not (1 <= x <= 10000 and 1 <= n <= 10 and len(coins) == n):
        return False
    return all(c >= 1 for c in coins) and len(set(coins)) == n


def fmt(x, coins):
    return f"{x} {len(coins)}\n" + " ".join(map(str, coins)) + "\n"


def extra_cases():
    """追加：原 40 组里 30 组答案是 -1、X <= 300、面值全部升序。
    这里补含面值 1 的可解组（X 拉到 10000）、N=1、X=1、面值乱序、面值大于 X、
    大面值远超 X 的组，以及几组无 1 的 -1 但 X 很大的。"""
    r = random.Random(298960)
    out = [fmt(1, [1]), fmt(10000, [1]), fmt(1, [3, 1]), fmt(10000, [10000, 1]),
           fmt(10000, [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]),
           fmt(10000, [512, 1, 64, 8, 256, 2, 128, 4, 32, 16]),
           fmt(9999, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]),
           fmt(10000, [5000, 3, 1, 9999, 7]),
           fmt(1, [100000, 1]), fmt(2, [2, 1]), fmt(3, [2, 1])]
    while len(out) < 40:
        n = r.randint(1, 10)
        hi = r.choice([10, 100, 1000, 10000, 20000])
        coins = r.sample(range(2, hi + 1), n - 1) + [1] if hi > n else list(range(1, n + 1))
        if len(out) % 7 == 0:
            coins = [c for c in coins if c != 1] or [2]
        r.shuffle(coins)
        x = r.choice([r.randint(1, 10000), r.randint(9000, 10000), r.randint(1, 50)])
        c = fmt(x, coins)
        if valid(c) and c not in out:
            out.append(c)
    return out


def brute(text):
    """独立 oracle（小 X）：按硬币总数 k 递增枚举可重复组合，检查子集和覆盖 1..X。"""
    from itertools import combinations_with_replacement
    rows = text.split("\n")
    x = int(rows[0].split()[0])
    coins = sorted(set(int(t) for t in rows[1].split() if int(t) <= x))
    for k in range(1, x + 1):
        for combo in combinations_with_replacement(coins, k):
            reach = 1
            for c in combo:
                reach |= reach << c
            if all(reach >> v & 1 for v in range(1, x + 1)):
                return k
    return -1


def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        cases = list(range(40)) + extra_cases()
        for index, extra in enumerate(cases):
            if index == 0: content = SAMPLE_IN
            elif index >= 40: content = extra
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(29896 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            assert valid(content) and content not in seen[1:], content
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
