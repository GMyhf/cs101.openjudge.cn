def solve_text(text):
    values = list(map(int, text.split())); n, treasure = values[0], values[1:]
    dp = [[0, 0] for _ in range(n)]
    for node in range(n - 1, -1, -1):
        left, right = 2 * node + 1, 2 * node + 2
        skip = (max(dp[left]) if left < n else 0) + (max(dp[right]) if right < n else 0)
        take = treasure[node] + (dp[left][0] if left < n else 0) + (dp[right][0] if right < n else 0)
        dp[node] = [skip, take]
    return str(max(dp[0])) + "\n"


def generate_case(rng):
    n = rng.randint(1, 100); values = [rng.randint(0, 1000) for _ in range(n)]
    return f"{n}\n" + " ".join(map(str, values)) + "\n"

import random, re
from pathlib import Path
SAMPLE_IN = '6\n3 4 5 1 3 1\n'
SAMPLE_OUT = '9\n'


def valid(text):
    """题面：两行，第一行整数 N（节点数），第二行 N 个非负整数。题面未给 N 与价值的上界。"""
    lines = text.split("\n")
    if len(lines) != 3 or lines[2] != "":
        return False
    if not re.fullmatch(r"[1-9]\d*", lines[0]):
        return False
    n = int(lines[0])
    vals = lines[1].split(" ")
    return len(vals) == n and all(re.fullmatch(r"0|[1-9]\d*", v) for v in vals)


def fmt(values):
    return f"{len(values)}\n" + " ".join(map(str, values)) + "\n"


def build_cases():
    rng = random.Random(24637)
    old = [generate_case(rng) for _ in range(19)]       # 原随机数据（n<=100，价值<=1000）
    r = random.Random(246370)
    special = [
        fmt([7]),                       # n=1
        fmt([0]),                       # n=1，价值为 0
        fmt([5, 9]),                    # n=2，取子节点
        fmt([10, 4, 5]),                # n=3，取根
        fmt([0] * 15),                  # 全 0
        fmt([1] * 31),                  # 全相等：取叶子层更优
        fmt([100] + [1] * 6 + [100] * 8),   # 隔层取：按层奇偶贪心或“取根+孙”会错
        fmt([r.randint(0, 1000) for _ in range(1000)]),
        fmt([r.choice([0, 0, 0, r.randint(1, 1000)]) for _ in range(1023)]),   # 满二叉树，稀疏非零
        fmt([r.randint(900, 1000) if (i + 1).bit_length() % 3 == 0 else r.randint(0, 50) for i in range(2047)]),  # 每 3 层一个重层
    ]
    keep = old[:9]
    cases = [SAMPLE_IN] + keep + special
    return cases


def main():
    cases = build_cases()
    assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
    assert len(cases) == 20 and len(set(cases)) == 20 and all(valid(c) for c in cases)
    root = Path(__file__).parent / "data"
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
    print(f"generated {len(cases)} cases for 24637")


if __name__ == "__main__":
    main()
