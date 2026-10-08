"""4129 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001b
生成器与循环取自 scripts/build_001b.py（批次 001b），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4129
SAMPLE_IN = '1\n6 6 2\n...S..\n...#..\n.#....\n...#..\n...#..\n..#E#.\n'
SAMPLE_OUT = '7\n'
REFERENCE_SOURCE = 'import sys\nfrom collections import deque\n\ndef solve():\n    input = sys.stdin.readline\n    T = int(input())\n    for _ in range(T):\n        R, C, K = map(int, input().split())\n        maze = [list(input().rstrip(\'\\n\')) for _ in range(R)]\n        \n        # Find S and E\n        for i in range(R):\n            for j in range(C):\n                if maze[i][j] == \'S\':\n                    sr, sc = i, j\n                elif maze[i][j] == \'E\':\n                    er, ec = i, j\n        \n        # dist[r][c][m] = minimum absolute time to reach (r,c) with time mod K == m\n        INF = 10**18\n        dist = [[[INF]*K for _ in range(C)] for __ in range(R)]\n        \n        dq = deque()\n        dist[sr][sc][0] = 0\n        dq.append((sr, sc, 0))  # at time 0\n        \n        ans = None\n        while dq:\n            r, c, m = dq.popleft()\n            t = dist[r][c][m]\n            # If we\'ve reached the exit, record and break (BFS ensures minimal time)\n            if (r, c) == (er, ec):\n                ans = t\n                break\n            \n            for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):\n                nr, nc = r+dr, c+dc\n                nt = t + 1\n                nm = nt % K\n                if not (0 <= nr < R and 0 <= nc < C):\n                    continue\n                cell = maze[nr][nc]\n                # If it\'s a rock, only allowed if nt % K == 0\n                if cell == \'#\' and nm != 0:\n                    continue\n                # \'.\' or \'S\' or \'E\' always ok\n                if dist[nr][nc][nm] > nt:\n                    dist[nr][nc][nm] = nt\n                    dq.append((nr, nc, nm))\n        \n        if ans is None:\n            print("Oop!")\n        else:\n            print(ans)\n\n\nif __name__ == "__main__":\n    solve()\n'

# 题面约束：首行 T（0 < T <= 20）；每组首行 R C K（0 < R, C <= 100，2 <= K <= 10），
# 接着 R 行、每行恰 C 个字符，取自 "S"、"E"、"#"、"."；S、E 各恰好一个（题面"你的位置"、"出口"）。
def valid(text):
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if not lines or lines[0] != lines[0].strip() or not lines[0].isdigit():
        return False
    t = int(lines[0])
    if not 0 < t <= 20 or lines[0] != str(t):
        return False
    i = 1
    for _ in range(t):
        if i >= len(lines):
            return False
        h = lines[i].split()
        if len(h) != 3 or " ".join(h) != lines[i] or not all(x.isdigit() and x == str(int(x)) for x in h):
            return False
        R, C, K = map(int, h)
        if not (0 < R <= 100 and 0 < C <= 100 and 2 <= K <= 10) or i + 1 + R > len(lines):
            return False
        g = lines[i + 1:i + 1 + R]
        if any(len(row) != C or set(row) - set("SE#.") for row in g):
            return False
        if sum(row.count("S") for row in g) != 1 or sum(row.count("E") for row in g) != 1:
            return False
        i += 1 + R
    return i == len(lines)


def grid_text(R, C, K, g):
    return f"{R} {C} {K}\n" + "\n".join("".join(row) for row in g)


def place(r, g, R, C, ch, avoid=()):
    while True:
        a, b = r.randrange(R), r.randrange(C)
        if g[a][b] != "S" and g[a][b] != "E" and (a, b) not in avoid:
            g[a][b] = ch
            return a, b


def rand_grid(r, R, C, K, p, far=False):
    g = [["#" if r.random() < p else "." for _ in range(C)] for _ in range(R)]
    if far:
        g[0][0] = "S"; g[R - 1][C - 1] = "E"
    else:
        place(r, g, R, C, "S"); place(r, g, R, C, "E")
    return grid_text(R, C, K, g)


def walls_grid(r, R, C, K):
    """隔行整排石头、只留个别缺口：要么绕远路，要么等到 K 的倍数时刻穿墙。"""
    g = [["." for _ in range(C)] for _ in range(R)]
    for i in range(1, R, 2):
        for j in range(C):
            g[i][j] = "#"
        if r.random() < 0.5:
            g[i][r.randrange(C)] = "."
    g[0][r.randrange(C)] = "S"
    last = R - 1 if (R - 1) % 2 == 0 else R - 2
    g[last][r.randrange(C)] = "E"
    return grid_text(R, C, K, g)


def parity_trap(r, R, C, K):
    """K 为偶数时只能在偶数时刻踩石头；E 与 S 同色且四周都是石头 → 永远进不去，Oop!，并把状态空间搜满。"""
    g = [["#" if r.random() < 0.2 else "." for _ in range(C)] for _ in range(R)]
    g[0][0] = "S"
    er, ec = R - 2, C - 2
    if (er + ec) % 2:
        ec -= 1
    g[er][ec] = "E"
    for a, b in ((er + 1, ec), (er - 1, ec), (er, ec + 1), (er, ec - 1)):
        if 0 <= a < R and 0 <= b < C:
            g[a][b] = "#"
    return grid_text(R, C, K, g)


def fmt(parts):
    return f"{len(parts)}\n" + "\n".join(parts) + "\n"


def build_cases():
    r = random.Random(NUMBER)
    cases = [SAMPLE_IN,
             fmt(["1 2 2\nSE", "2 1 10\nE\nS", "1 3 2\nS#E", "1 4 3\nS.#E", "3 3 2\n#.#\n#S#\n#E#",
                  "3 3 3\n#.#\n#S#\n#E#", "2 2 2\nS#\n#E", "2 2 3\nS#\n#E",
                  "3 3 4\nS#.\n###\n.#E"]),                                        # 小边界：等待、出不去、穿墙
             fmt([rand_grid(r, 100, 100, 10, 0.0, True)]),
             fmt([parity_trap(r, 100, 100, 10)]),
             fmt([parity_trap(r, 100, 100, k) for k in (2, 4, 6, 8, 10)]),
             fmt([rand_grid(r, 100, 100, r.randint(2, 10), p, True) for p in (0.3, 0.5, 0.7, 0.85, 0.95)]),
             fmt([walls_grid(r, 100, 100, k) for k in (2, 3, 5, 7, 10)]),
             fmt([parity_trap(r, 100, 100, r.choice([2, 4, 6, 8, 10])) if j % 2 else
                  rand_grid(r, 100, 100, r.choice([3, 5, 7, 9, 10]), 0.1, True) for j in range(20)]),  # 满规模 T=20
             ]
    while len(cases) < 20:
        parts = []
        for _ in range(r.randint(1, 20)):
            R, C = r.choice([(r.randint(1, 10), r.randint(1, 10)), (r.randint(1, 100), r.randint(1, 100))])
            if R * C < 2:
                C = 2
            K = r.randint(2, 10)
            kind = r.random()
            if kind < 0.08 and R >= 3 and C >= 3:
                parts.append(parity_trap(r, R, C, r.choice([2, 4, 6, 8, 10])))
            elif kind < 0.3 and R >= 3:
                parts.append(walls_grid(r, R, C, K))
            else:
                parts.append(rand_grid(r, R, C, K, r.choice([0.05, 0.1, 0.2, 0.3, 0.35, 0.45, 0.6, 0.8]), r.random() < 0.5))
        cases.append(fmt(parts))
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
