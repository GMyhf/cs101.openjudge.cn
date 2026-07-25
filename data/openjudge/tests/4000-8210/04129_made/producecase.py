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

def g4129(r):
    t = r.randint(1, 3)
    cases = []
    for _ in range(t):
        m, n, k = r.randint(4, 9), r.randint(4, 9), r.randint(2, 10)
        start, target = (0, 0), (m - 1, n - 1)
        path = {(i, 0) for i in range(m)} | {(m - 1, j) for j in range(n)}
        rows = []
        for i in range(m):
            row = []
            for j in range(n):
                if (i, j) == start: ch = "S"
                elif (i, j) == target: ch = "E"
                elif (i, j) in path: ch = "."
                else: ch = "#" if r.random() < .25 else "."
                row.append(ch)
            rows.append("".join(row))
        cases.append(f"{m} {n} {k}\n" + "\n".join(rows))
    return str(t) + "\n" + "\n".join(cases) + "\n"

def build_cases():
    return [SAMPLE_IN] + [g4129(random.Random(NUMBER + i)) for i in range(1, 20)]

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
