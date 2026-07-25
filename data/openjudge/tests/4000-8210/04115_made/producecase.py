"""4115 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001b
生成器与循环取自 scripts/build_001b.py（批次 001b），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4115
SAMPLE_IN = '4 4 1\n#@##\n**##\n###+\n****\n'
SAMPLE_OUT = '6\n'
REFERENCE_SOURCE = "# 夏天明 元培学院\n\nfrom collections import deque\n\nM, N, T = map(int, input().split())\ngraph = [list(input()) for i in range(M)]\ndirec = [(0,1), (1,0), (-1,0), (0,-1)]\nstart, end = None, None\nfor i in range(M):\n    for j in range(N):\n        if graph[i][j] == '@':\n            start = (i, j)\ndef bfs():\n    q = deque([start + (T, 0)])\n    visited = [[-1]*N for i in range(M)]\n    visited[start[0]][start[1]] = T\n    while q:\n        x, y, t, time = q.popleft()\n        time += 1\n        for dx, dy in direc:\n            if 0<=x+dx<M and 0<=y+dy<N:\n                if (elem := graph[x+dx][y+dy]) == '*' and t > visited[x+dx][y+dy]:\n                    visited[x+dx][y+dy] = t\n                    q.append((x+dx, y+dy, t, time))\n                elif elem == '#' and t > 0 and t-1 > visited[x+dx][y+dy]:\n                    visited[x+dx][y+dy] = t-1\n                    q.append((x+dx, y+dy, t-1, time))\n                elif elem == '+':\n                    return time\n    return -1\nprint(bfs())\n"

def g4115(r):
    m, n, chakra = r.randint(4, 10), r.randint(4, 10), r.randint(0, 9)
    start, target = (0, 0), (m - 1, n - 1)
    path = {(i, 0) for i in range(m)} | {(m - 1, j) for j in range(n)}
    cells = []
    for i in range(m):
        row = []
        for j in range(n):
            if (i, j) == start: char = "@"
            elif (i, j) == target: char = "+"
            elif (i, j) in path: char = "*"
            else: char = "#" if r.random() < .22 else "*"
            row.append(char)
        cells.append("".join(row))
    return f"{m} {n} {chakra}\n" + "\n".join(cells) + "\n"

def build_cases():
    return [SAMPLE_IN] + [g4115(random.Random(NUMBER + i)) for i in range(1, 20)]

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
