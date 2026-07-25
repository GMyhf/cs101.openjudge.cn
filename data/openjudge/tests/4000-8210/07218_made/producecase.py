"""7218 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001c
生成器与循环取自 scripts/build_001c.py（批次 001c），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 7218
SAMPLE_IN = '3\n3 4\n.S..\n###.\n..E.\n3 4\n.S..\n.E..\n....\n3 4\n.S..\n####\n..E.\n'
SAMPLE_OUT = '5\n1\noop!\n'
REFERENCE_SOURCE = 'from collections import deque\n\ndef solve_maze():\n    T = int(input())\n    for _ in range(T):\n        R, C = map(int, input().split())\n        maze = [list(input().strip()) for _ in range(R)]\n\n        # 找起点 S\n        for i in range(R):\n            for j in range(C):\n                if maze[i][j] == \'S\':\n                    start = (i, j)\n                if maze[i][j] == \'E\':\n                    end = (i, j)\n\n        # BFS\n        queue = deque()\n        visited = [[False] * C for _ in range(R)]\n        queue.append((start[0], start[1], 0))  # (row, col, distance)\n        visited[start[0]][start[1]] = True\n\n        found = False\n\n        while queue:\n            x, y, dist = queue.popleft()\n            if (x, y) == end:\n                print(dist)\n                found = True\n                break\n\n            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:\n                nx, ny = x + dx, y + dy\n                if 0 <= nx < R and 0 <= ny < C:\n                    if not visited[nx][ny] and maze[nx][ny] != \'#\':\n                        visited[nx][ny] = True\n                        queue.append((nx, ny, dist + 1))\n\n        if not found:\n            print("oop!")\n\n# 调用主函数\nsolve_maze()\n'

def g7218(r):
    cases = []
    for _ in range(r.randint(1, 3)):
        m, n = r.randint(3, 9), r.randint(3, 9); path = {(0, j) for j in range(n)} | {(i, n - 1) for i in range(m)}
        rows = []
        for i in range(m):
            row = []
            for j in range(n):
                if (i, j) == (0, 0): ch = "S"
                elif (i, j) == (m - 1, n - 1): ch = "E"
                elif (i, j) in path: ch = "."
                else: ch = "#" if r.random() < .25 else "."
                row.append(ch)
            rows.append("".join(row))
        cases.append(f"{m} {n}\n" + "\n".join(rows))
    return str(len(cases)) + "\n" + "\n".join(cases) + "\n"

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g7218(random.Random(NUMBER + i + attempt * 1000))
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
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
