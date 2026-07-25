"""4116 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001b
生成器与循环取自 scripts/build_001b.py（批次 001b），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4116
SAMPLE_IN = '2\n7 8\n#@#####@\n#@a#@@r@\n#@@#x@@@\n@@#@@#@#\n#@@@##@@\n@#@@@@@@\n@@@@@@@@ \n13 40\n@x@@##x@#x@x#xxxx##@#x@x@@#x#@#x#@@x@#@x\nxx###x@x#@@##xx@@@#@x@@#x@xxx@@#x@#x@@x@\n#@x#@x#x#@@##@@x#@xx#xxx@@x##@@@#@x@@x@x\n@##x@@@x#xx#@@#xxxx#@@x@x@#@x@@@x@#@#x@#\n@#xxxxx##@@x##x@xxx@@#x@x####@@@x#x##@#@\n#xxx#@#x##xxxx@@#xx@@@x@xxx#@#xxx@x#####\n#x@xxxx#@x@@@@##@x#xx#xxx@#xx#@#####x#@x\nxx##@#@x##x##x#@x#@a#xx@##@#@##xx@#@@x@x\nx#x#@x@#x#@##@xrx@x#xxxx@##x##xx#@#x@xx@\n#x@@#@###x##x@x#@@#@@x@x@@xx@@@@##@@x@@x\nx#xx@x###@xxx#@#x#@@###@#@##@x#@x@#@@#@@\n#@#x@x#x#x###@x@@xxx####x@x##@x####xx#@x\n#x#@x#x######@@#x@#xxxx#xx@@@#xx#x#####@\n'
SAMPLE_OUT = '13\n7\n'
REFERENCE_SOURCE = '# 用时间来扩展bfs的下一个节点\n#from collections import deque\nfrom heapq import heappush, heappop\n\ndx = [-1, 1, 0, 0]\ndy = [0, 0, -1, 1]\n\n\ndef bfs(matrix, start):\n    n, m = len(matrix), len(matrix[0])\n    visited = [[False for _ in range(m)] for _ in range(n)]\n    #q = deque([(start[0], start[1], 0)])\n    q = []\n    heappush(q, (0, start[0], start[1]))\n    visited[start[0]][start[1]] = True\n    while len(q) != 0:\n        #x, y, time = q.popleft()\n        time, x, y = heappop(q)\n        for i in range(4):\n            nx, ny = x + dx[i], y + dy[i]\n            if 0 <= nx < n and 0 <= ny < m and not visited[nx][ny]:\n                if matrix[nx][ny] == "a":\n                    #ans.append(time+1)\n                    return time + 1\n                elif matrix[nx][ny] == "@":\n                    #q.append((nx, ny, time + 1))\n                    heappush(q, (time + 1, nx, ny))\n                    visited[nx][ny] = True\n                elif matrix[nx][ny] == "x":\n                    #q.append((nx, ny, time + 2))\n                    heappush(q, (time + 2, nx, ny))\n                    visited[nx][ny] = True\n\n    return "Impossible"\n\n\nS = int(input())\nfor _ in range(S):\n    N, M = map(int, input().split())\n    matrix = [list(input()) for _ in range(N)]\n    start = None\n    ans = []\n    for i in range(N):\n        for j in range(M):\n            if matrix[i][j] == "r":\n                start = (i, j)\n                break\n    print(bfs(matrix, start))\n    # if ans == []:\n    #     print("Impossible")\n    # else:\n    #     print(min(ans))\n\n'

def make_weighted_grid(r, rescue=False):
    m, n = r.randint(4, 9), r.randint(4, 9)
    start, target = (0, 0), (m - 1, n - 1)
    path = {(i, 0) for i in range(m)} | {(m - 1, j) for j in range(n)}
    cells = []
    for i in range(m):
        row = []
        for j in range(n):
            if (i, j) == start: char = "r" if rescue else "S"
            elif (i, j) == target: char = "a" if rescue else "E"
            elif (i, j) in path: char = "@" if rescue else "."
            elif rescue:
                char = r.choice(["@"] * 5 + ["x"] * 2 + ["#"])
            else:
                char = r.choice(["."] * 6 + ["#"] * 2)
            row.append(char)
        cells.append("".join(row))
    return m, n, cells

def g4116(r):
    cases = []
    for _ in range(r.randint(1, 3)):
        m, n, cells = make_weighted_grid(r, True)
        cases.append(f"{m} {n}\n" + "\n".join(cells))
    return str(len(cases)) + "\n" + "\n".join(cases) + "\n"

def build_cases():
    return [SAMPLE_IN] + [g4116(random.Random(NUMBER + i)) for i in range(1, 20)]

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
