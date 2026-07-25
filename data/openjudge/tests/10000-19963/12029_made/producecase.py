"""12029 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001c
生成器与循环取自 scripts/build_001c.py（批次 001c），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 12029
SAMPLE_IN = '1\n5 5\n1 1 1 1 1\n1 0 0 0 1\n1 0 1 0 1\n1 0 0 0 1\n1 1 1 1 1\n3 3\n2\n1 1\n2 2\n'
SAMPLE_OUT = 'No\n'
REFERENCE_SOURCE = 'from collections import deque\nimport sys\ninput = sys.stdin.read\n\n# 判断坐标是否有效\ndef is_valid(x, y, m, n):\n    return 0 <= x < m and 0 <= y < n\n\n# 广度优先搜索模拟水流\ndef bfs(start_x, start_y, start_height, m, n, h, water_height):\n    dx = [-1, 1, 0, 0]\n    dy = [0, 0, -1, 1]\n    q = deque([(start_x, start_y, start_height)])\n    water_height[start_x][start_y] = start_height\n\n    while q:\n        x, y, height = q.popleft()\n        for i in range(4):\n            nx, ny = x + dx[i], y + dy[i]\n            if is_valid(nx, ny, m, n) and h[nx][ny] < height:\n                if water_height[nx][ny] < height:\n                    water_height[nx][ny] = height\n                    q.append((nx, ny, height))\n\n# 主函数\ndef main():\n    data = input().split()  # 快速读取所有输入数据\n    idx = 0\n    k = int(data[idx])\n    idx += 1\n    results = []\n\n    for _ in range(k):\n        m, n = map(int, data[idx:idx + 2])\n        idx += 2\n        h = []\n        for i in range(m):\n            h.append(list(map(int, data[idx:idx + n])))\n            idx += n\n        water_height = [[0] * n for _ in range(m)]\n\n        i, j = map(int, data[idx:idx + 2])\n        idx += 2\n        i, j = i - 1, j - 1\n\n        p = int(data[idx])\n        idx += 1\n\n        for _ in range(p):\n            x, y = map(int, data[idx:idx + 2])\n            idx += 2\n            x, y = x - 1, y - 1\n\n            bfs(x, y, h[x][y], m, n, h, water_height)\n\n        results.append("Yes" if water_height[i][j] > 0 else "No")\n\n    sys.stdout.write("\\n".join(results) + "\\n")\n\nif __name__ == "__main__":\n    main()\n'

def g12029(r):
    cases = []
    for _ in range(r.randint(1, 3)):
        m, n = r.randint(3, 8), r.randint(3, 8); grid = [[r.randint(0, 100) for _ in range(n)] for _ in range(m)]
        i, j = r.randint(1, m), r.randint(1, n); points = [(r.randint(1, m), r.randint(1, n)) for _ in range(r.randint(1, min(5, m*n)))]
        cases.append(f"{m} {n}\n" + "\n".join(" ".join(map(str, row)) for row in grid) + f"\n{i} {j}\n{len(points)}\n" + "\n".join(f"{x} {y}" for x, y in points))
    return str(len(cases)) + "\n" + "\n".join(cases) + "\n"

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g12029(random.Random(NUMBER + i + attempt * 1000))
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
