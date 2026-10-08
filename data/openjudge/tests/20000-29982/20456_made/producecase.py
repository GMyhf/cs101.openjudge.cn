"""20456 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001d
生成器与循环取自 scripts/build_001d.py（批次 001d），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 20456
SAMPLE_IN = '1,0,0,0,0,0,1,0,1,0\n1,1,1,1,1,0,0,0,0,0\n1,0,0,0,1,1,1,1,0,0\n1,0,0,1,0,1,0,1,1,0\n1,0,0,0,0,1,0,1,0,0\n0,0,1,0,0,0,0,1,0,0\n1,1,1,0,0,0,0,0,0,0\n1,0,1,1,0,0,1,1,1,0\n1,0,1,0,0,1,0,0,1,0\n0,0,0,0,0,0,1,1,1,1\n'
SAMPLE_OUT = '1\n'
REFERENCE_SOURCE = "def closedIsland(grid):\n    rows, cols = len(grid), len(grid[0])\n\n    # 检查岛屿是否封闭的DFS函数\n    def dfs(r, c):\n        if grid[r][c] == 1:\n            return True\n        if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:\n            return False\n        \n        # 标记当前单元格为已访问\n        grid[r][c] = 1\n        \n        # 检查所有方向\n        up = dfs(r - 1, c)\n        down = dfs(r + 1, c)\n        left = dfs(r, c - 1)\n        right = dfs(r, c + 1)\n        \n        return up and down and left and right\n\n    closed_islands = 0\n    for r in range(1, rows - 1):  # 从1开始，忽略边界\n        for c in range(1, cols - 1):  # 从1开始，忽略边界\n            if grid[r][c] == 0 and dfs(r, c):\n                closed_islands += 1\n\n    return closed_islands\n\n# 读取输入\ngrid = []\nfor _ in range(10):\n    row = list(map(int, input().split(',')))\n    grid.append(row)\n\n# 输出结果\nprint(closedIsland(grid))\n\n"

def g20456(r): return "\n".join(",".join(r.choice("01") for _ in range(10)) for _ in range(10))+"\n"

def valid(text):
    """题面契约：恰 10 行，每行 10 个 0/1，用逗号分隔（与样例一致）。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 10:
        return False
    return all(len(t := line.split(",")) == 10 and all(x in ("0", "1") for x in t)
               for line in lines)


def _grid(rows):
    return "\n".join(",".join(row) for row in rows) + "\n"


def extra_cases():
    """补充结构化边界：全水、全陆、单个大封闭岛、棋盘形最多岛、仅对角接边、蛇形接边。"""
    out = []
    out.append(_grid(["1" * 10] * 10))                       # 0
    out.append(_grid(["0" * 10] * 10))                       # 0：整块陆地接边
    out.append(_grid(["1" * 10] + ["1" + "0" * 8 + "1"] * 8 + ["1" * 10]))  # 1
    rows = [["1"] * 10 for _ in range(10)]
    for r in range(1, 9):
        for c in range(1, 9):
            if (r + c) % 2 == 0:
                rows[r][c] = "0"
    out.append(_grid(rows))                                  # 棋盘：32 个
    rows = [["1"] * 10 for _ in range(10)]
    for r, c in ((0, 0), (1, 1), (8, 8), (9, 9), (0, 9), (2, 7), (5, 5)):
        rows[r][c] = "0"                                     # 只经对角接边的不算接边
    rows[1][8] = "0"
    out.append(_grid(rows))
    rows = [["1"] * 10 for _ in range(10)]
    for c in range(1, 9):
        rows[1][c] = "0"; rows[3][c] = "0"; rows[5][c] = "0"; rows[7][c] = "0"
    rows[2][8] = "0"; rows[4][1] = "0"; rows[6][8] = "0"
    rows[8][1] = "0"; rows[9][1] = "0"                       # 蛇形长岛在末端接边：0
    out.append(_grid(rows))
    return out


def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g20456(random.Random(NUMBER + i + attempt * 1000))
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
    for value in extra_cases():
        assert value not in cases
        cases.append(value)
    for value in cases:
        assert valid(value), "生成的数据越出题面约束"
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
