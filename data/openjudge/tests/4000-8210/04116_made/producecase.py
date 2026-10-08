"""4116 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

覆盖：最小 1x2、单行单列、Impossible（公主被墙围死/墙太密）、卡普通队列 BFS 的守卫陷阱、
200x200 满规模蛇形长路与随机图，最后一组含 10 张满规模地图。

出处：build_001b
生成器与循环取自 scripts/build_001b.py（批次 001b），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import re
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4116
SAMPLE_IN = '2\n7 8\n#@#####@\n#@a#@@r@\n#@@#x@@@\n@@#@@#@#\n#@@@##@@\n@#@@@@@@\n@@@@@@@@ \n13 40\n@x@@##x@#x@x#xxxx##@#x@x@@#x#@#x#@@x@#@x\nxx###x@x#@@##xx@@@#@x@@#x@xxx@@#x@#x@@x@\n#@x#@x#x#@@##@@x#@xx#xxx@@x##@@@#@x@@x@x\n@##x@@@x#xx#@@#xxxx#@@x@x@#@x@@@x@#@#x@#\n@#xxxxx##@@x##x@xxx@@#x@x####@@@x#x##@#@\n#xxx#@#x##xxxx@@#xx@@@x@xxx#@#xxx@x#####\n#x@xxxx#@x@@@@##@x#xx#xxx@#xx#@#####x#@x\nxx##@#@x##x##x#@x#@a#xx@##@#@##xx@#@@x@x\nx#x#@x@#x#@##@xrx@x#xxxx@##x##xx#@#x@xx@\n#x@@#@###x##x@x#@@#@@x@x@@xx@@@@##@@x@@x\nx#xx@x###@xxx#@#x#@@###@#@##@x#@x@#@@#@@\n#@#x@x#x#x###@x@@xxx####x@x##@x####xx#@x\n#x#@x#x######@@#x@#xxxx#xx@@@#xx#x#####@\n'
SAMPLE_OUT = '13\n7\n'
REFERENCE_SOURCE = '# 用时间来扩展bfs的下一个节点\n#from collections import deque\nfrom heapq import heappush, heappop\n\ndx = [-1, 1, 0, 0]\ndy = [0, 0, -1, 1]\n\n\ndef bfs(matrix, start):\n    n, m = len(matrix), len(matrix[0])\n    visited = [[False for _ in range(m)] for _ in range(n)]\n    #q = deque([(start[0], start[1], 0)])\n    q = []\n    heappush(q, (0, start[0], start[1]))\n    visited[start[0]][start[1]] = True\n    while len(q) != 0:\n        #x, y, time = q.popleft()\n        time, x, y = heappop(q)\n        for i in range(4):\n            nx, ny = x + dx[i], y + dy[i]\n            if 0 <= nx < n and 0 <= ny < m and not visited[nx][ny]:\n                if matrix[nx][ny] == "a":\n                    #ans.append(time+1)\n                    return time + 1\n                elif matrix[nx][ny] == "@":\n                    #q.append((nx, ny, time + 1))\n                    heappush(q, (time + 1, nx, ny))\n                    visited[nx][ny] = True\n                elif matrix[nx][ny] == "x":\n                    #q.append((nx, ny, time + 2))\n                    heappush(q, (time + 2, nx, ny))\n                    visited[nx][ny] = True\n\n    return "Impossible"\n\n\nS = int(input())\nfor _ in range(S):\n    N, M = map(int, input().split())\n    matrix = [list(input()) for _ in range(N)]\n    start = None\n    ans = []\n    for i in range(N):\n        for j in range(M):\n            if matrix[i][j] == "r":\n                start = (i, j)\n                break\n    print(bfs(matrix, start))\n    # if ans == []:\n    #     print("Impossible")\n    # else:\n    #     print(min(ans))\n\n'

def valid(text):
    """题面：第一行组数 S；每组先是一行 N M（N, M <= 200），随后 N 行每行 M 个字符，
    字符取自 @ x # r a，骑士 r 与公主 a 各恰好一个。
    题面样例第 7 行行末带一个空格，因此地图行只容忍行末空格。"""
    if not isinstance(text, str) or not text.endswith("\n") or "\r" in text:
        return False
    lines = text[:-1].split("\n")
    if not re.fullmatch(r"[1-9]\d*", lines[0]):
        return False
    s = int(lines[0])
    pos = 1
    for _ in range(s):
        if pos >= len(lines):
            return False
        head = lines[pos].split(" ")
        pos += 1
        if len(head) != 2 or not all(re.fullmatch(r"[1-9]\d*", x) for x in head):
            return False
        n, m = map(int, head)
        if not (1 <= n <= 200 and 1 <= m <= 200):
            return False
        rows = [row.rstrip(" ") for row in lines[pos:pos + n]]
        pos += n
        if len(rows) != n or any(not re.fullmatch(r"[@x#ra]{%d}" % m, row) for row in rows):
            return False
        body = "".join(rows)
        if body.count("r") != 1 or body.count("a") != 1:
            return False
    return pos == len(lines)


def grid_text(grid):
    return f"{len(grid)} {len(grid[0])}\n" + "\n".join("".join(row) for row in grid)


def random_grid(r, n, m, wall, guard, far=False):
    grid = [[r.choices("#x@", weights=[wall, guard, 1 - wall - guard])[0] for _ in range(m)]
            for _ in range(n)]
    if far:
        grid[0][0] = "r"
        grid[n - 1][m - 1] = "a"
    else:
        cells = [(i, j) for i in range(n) for j in range(m)]
        a, b = r.sample(cells, 2)
        grid[a[0]][a[1]] = "r"
        grid[b[0]][b[1]] = "a"
    return grid_text(grid)


def enclosed(r, n, m):
    # 公主被一圈墙围死 → Impossible
    grid = [[r.choice("@@@x") for _ in range(m)] for _ in range(n)]
    ci, cj = n // 2, m // 2
    for i in range(ci - 1, ci + 2):
        for j in range(cj - 1, cj + 2):
            grid[i][j] = "#"
    grid[ci][cj] = "a"
    grid[0][0] = "r"
    return grid_text(grid)


def guard_trap(n, m):
    """卡「普通队列 BFS + 守卫记 2」：直线短路上有守卫，绕一格的路全是道路，
    两者一样长；普通 BFS 先把守卫格标记掉会得到偏大的答案。"""
    grid = [["#"] * m for _ in range(n)]
    for j in range(m):
        grid[0][j] = "x" if j % 2 == 1 else "@"
        grid[1][j] = "@"
    grid[0][0] = "r"
    grid[0][m - 1] = "a"
    return grid_text(grid)


def snake_grid(n, m, guards):
    grid = [["@"] * m for _ in range(n)]
    for i in range(1, n, 2):
        for j in range(m):
            grid[i][j] = "#"
        grid[i][m - 1 if (i // 2) % 2 == 0 else 0] = "x" if guards else "@"
    grid[0][0] = "r"
    last = n - 1 if (n - 1) % 2 == 0 else n - 2
    grid[last][m - 1 if (last // 2) % 2 == 1 else 0] = "a"
    return grid_text(grid)


def pack(groups):
    return str(len(groups)) + "\n" + "\n".join(groups) + "\n"


def build_cases():
    r = random.Random(NUMBER)
    cases = [SAMPLE_IN]
    cases.append(pack(["1 2\nra"]))                                  # 1 最小，相邻
    cases.append(pack(["1 3\nrxa", "2 1\na\nr", "1 3\nr#a"]))       # 2 守卫/墙/单列
    cases.append(pack([enclosed(r, 5, 5), enclosed(r, 9, 7)]))       # 3 Impossible
    cases.append(pack([guard_trap(2, 9), guard_trap(2, 30)]))        # 4 普通 BFS 陷阱
    for k in range(5, 10):                                           # 5-9 小随机，多组
        groups = [random_grid(r, r.randint(1, 10), r.randint(2, 10), r.uniform(0.1, 0.4),
                              r.uniform(0.1, 0.5)) for _ in range(r.randint(3, 8))]
        cases.append(pack(groups))
    for k in range(10, 13):                                          # 10-12 中规模
        groups = [random_grid(r, r.randint(20, 60), r.randint(20, 60), r.uniform(0.15, 0.35),
                              r.uniform(0.2, 0.5)) for _ in range(5)]
        groups.append(enclosed(r, r.randint(10, 40), r.randint(10, 40)))
        cases.append(pack(groups))
    cases.append(pack([guard_trap(2, 200), snake_grid(200, 200, True)]))      # 13
    cases.append(pack([snake_grid(200, 200, False), snake_grid(199, 200, True)]))  # 14
    cases.append(pack([random_grid(r, 200, 200, 0.0, 0.5, True),
                       random_grid(r, 200, 200, 0.0, 0.0, True)]))           # 15 无墙
    cases.append(pack([random_grid(r, 200, 200, 0.3, 0.3, True) for _ in range(3)]))  # 16
    cases.append(pack([random_grid(r, 200, 200, 0.2, 0.6) for _ in range(3)]))        # 17
    cases.append(pack([random_grid(r, 200, 200, 0.45, 0.2) for _ in range(3)]))       # 18 多 Impossible
    cases.append(pack([random_grid(r, 200, 200, r.uniform(0.1, 0.35), r.uniform(0.1, 0.6))
                       for _ in range(10)]))                                         # 19 10 组满规模
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
    assert len(set(cases)) == len(cases), "存在重复组"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        assert valid(content), index
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
