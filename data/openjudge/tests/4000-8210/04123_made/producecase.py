"""4123 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001b
生成器与循环取自 scripts/build_001b.py（批次 001b），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4123
SAMPLE_IN = '1\n5 4 0 0\n'
SAMPLE_OUT = '32\n'
REFERENCE_SOURCE = 'maxn = 10;\nsx = [-2,-1,1,2, 2, 1,-1,-2] # 马的横向移动\nsy = [ 1, 2,2,1,-1,-2,-2,-1] # 马的纵向移动\n\nans = 0;\n \ndef Dfs(dep: int, x: int, y: int):\n    #是否已经全部走完\n    if n*m == dep:\n        global ans\n        ans += 1\n        return\n    \n    #对于每个可以走的点\n    for r in range(8):\n        s = x + sx[r]\n        t = y + sy[r]\n        if 0<=s<n and 0<=t<m and chess[s][t]==False:\n            chess[s][t]=True\n            Dfs(dep+1, s, t)\n            chess[s][t] = False; #回溯\n \n\nfor _ in range(int(input())):\n    n,m,x,y = map(int, input().split())\n    chess = [[False]*maxn for _ in range(maxn)]  #False表示没有走过\n    ans = 0\n    chess[x][y] = True\n    Dfs(1, x, y)\n    print(ans)\n'

# 题面约束：T < 10；每组 n,m,x,y 满足 0<=x<=n-1, 0<=y<=m-1, m < 10, n < 10。
def valid(text):
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if not lines:
        return False
    try:
        rows = [[int(v) for v in line.split()] for line in lines]
    except ValueError:
        return False
    if any(" ".join(map(str, r)) != line.strip() for r, line in zip(rows, lines)):
        return False
    if len(rows[0]) != 1:
        return False
    t = rows[0][0]
    if not 1 <= t < 10 or len(rows) != t + 1:
        return False
    for r in rows[1:]:
        if len(r) != 4:
            return False
        n, m, x, y = r
        if not (1 <= n < 10 and 1 <= m < 10 and 0 <= x <= n - 1 and 0 <= y <= m - 1):
            return False
    return True


# 回溯规模：n*m>27 且两边都 >=3 的棋盘无法在时限内穷举，不出。
# 下面是这些棋盘在所有起点上的最大搜索结点数（C 暴力实测），用来控制单组总耗时。
# 本题 limits.json 无记录，判题按单组 4s 兜底；参考解约 1.3us/结点，单组结点数压在 1.2M
# 以内（约 1.6s，不超过时限一半）。5x5 的角与 (0,1) 类起点要 1.7M~1.8M 结点，单组就超半限，不出。
HEAVY = {(5, 5): 1829421, (4, 6): 674019, (6, 4): 674019, (3, 9): 516359, (9, 3): 516359}
LIGHT_COST = 90000
BUDGET = 1200000
LIGHT = [(n, m) for n in range(1, 10) for m in range(1, 10)
         if (n * m <= 27 or min(n, m) <= 2) and (n, m) not in HEAVY]


def fmt(boards):
    return f"{len(boards)}\n" + "".join(f"{n} {m} {x} {y}\n" for n, m, x, y in boards)


def rand_case(r):
    t = r.randint(1, 9)
    boards, cost = [], 0
    for _ in range(t):
        n, m = r.choice(LIGHT)
        if r.random() < 0.35:
            cand = [b for b, c in HEAVY.items() if cost + c <= BUDGET]
            if cand:
                n, m = r.choice(cand)
        cost += HEAVY.get((n, m), LIGHT_COST)
        boards.append((n, m, r.randrange(n), r.randrange(m)))
    return fmt(boards)


def build_cases():
    r = random.Random(NUMBER)
    fixed = [
        fmt([(1, 1, 0, 0)]),                                   # 最小棋盘，答案 1
        fmt([(1, 9, 0, 4), (9, 1, 4, 0), (2, 9, 1, 8), (9, 2, 8, 1),
             (2, 2, 0, 0), (1, 2, 0, 1), (3, 3, 1, 1), (3, 3, 0, 0), (1, 1, 0, 0)]),  # T=9 退化棋盘
        fmt([(5, 5, 2, 2)]),                                   # 5x5 中心，64
        fmt([(5, 5, 1, 2)]),                                   # 5x5 搜满仍为 0
        fmt([(4, 5, 0, 0), (5, 4, 0, 0), (3, 6, 0, 0), (6, 3, 0, 0)]),
        fmt([(4, 6, 0, 0), (3, 8, 0, 0), (8, 3, 7, 2), (3, 4, 0, 0)]),
        fmt([(9, 3, 8, 2), (9, 3, 0, 0), (3, 7, 2, 6)]),       # n=9 走到下标 10，卡越界写法
        fmt([(3, 9, 2, 8), (3, 9, 1, 4), (7, 3, 6, 0)]),       # m=9
        fmt([(6, 4, 5, 3), (4, 5, 3, 4), (5, 4, 4, 3)]),
    ]
    return [SAMPLE_IN] + fixed + [rand_case(r) for _ in range(20 - 1 - len(fixed))]

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
