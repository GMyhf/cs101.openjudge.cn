import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "def dfs(mx, visited, x, y):\n    # 如果到达右下角，返回True\n    if x == n - 1 and y == n - 1:\n        return True\n\n    # 定义向右和向下的移动方向\n    directions = [(0, 1), (1, 0)]\n\n    for dx, dy in directions:\n        nx = x + dx\n        ny = y + dy\n        # 检查新坐标是否在矩阵范围内，是否已经访问过，以及是否可以通过\n        if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and mx[nx][ny] == 0:\n            visited[nx][ny] = True\n            if dfs(mx, visited, nx, ny):\n                return True\n            visited[nx][ny] = False\n\n    return False\n\n# 读取输入\nn = int(input())\nmx = [list(map(int, input().split())) for _ in range(n)]\n\n# 初始化访问标记数组\nvisited = [[False] * n for _ in range(n)]\n\n# 起始点 (0, 0) 必须是可以通过的\nif mx[0][0] == 1:\n    print('No')\nelse:\n    visited[0][0] = True\n    if dfs(mx, visited, 0, 0):\n        print('Yes')\n    else:\n        print('No')\n"
SAMPLE_IN = '5\n0 0 1 1 0\n0 0 0 0 0\n0 1 1 1 0\n0 1 1 1 0\n0 1 1 1 0\n'
SAMPLE_OUT = 'Yes\n'
def generate_case(r):
    n = r.randint(2, 14)
    grid = [[0 if r.random() < .72 else 1 for _ in range(n)] for _ in range(n)]
    grid[0][0] = grid[-1][-1] = 0
    if r.random() < .55:
        for i in range(n):
            grid[i][i] = 0
    else:
        grid[0][1] = grid[1][0] = 1
    assert grid[0][0] == grid[-1][-1] == 0
    return str(n) + "\n" + "\n".join(" ".join(map(str, row)) for row in grid) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(23937 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
