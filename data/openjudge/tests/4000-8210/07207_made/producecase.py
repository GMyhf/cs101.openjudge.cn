import random, subprocess, tempfile
from pathlib import Path
SAMPLE_IN = '3\n'
SAMPLE_OUT = '17 24 1 8 15\n23 5 7 14 16\n4 6 13 20 22\n10 12 19 21 3\n11 18 25 2 9\n'
CASES = ['3\n', '11\n', '15\n', '19\n', '17\n', '20\n', '16\n', '12\n', '9\n', '10\n', '6\n', '8\n', '7\n', '18\n', '1\n', '14\n', '4\n', '13\n', '2\n', '5\n']
REFERENCE_SOURCE = 'def construct_magic_square(N):\n    M = 2 * N - 1\n    # 创建 M x M 的矩阵，初始为0\n    magic = [[0] * M for _ in range(M)]\n\n    # 初始位置：第一行，中间列\n    row, col = 0, M // 2\n    magic[row][col] = 1\n\n    # 填充 2 到 M*M\n    for num in range(2, M * M + 1):\n        # 计算下一个位置：上一行，右一列（边界循环）\n        next_row = (row - 1) % M\n        next_col = (col + 1) % M\n\n        # 如果目标位置已经有数字，就放在正下方\n        if magic[next_row][next_col] != 0:\n            next_row = (row + 1) % M  # 正下方，注意也可能越界，用 % M\n            next_col = col\n\n        # 放置当前数字\n        magic[next_row][next_col] = num\n        # 更新当前位置\n        row, col = next_row, next_col\n\n    return magic\n\n\ndef print_magic_square(magic):\n    M = len(magic)\n    for i in range(M):\n        # 将每行数字转为字符串，用空格连接\n        print(" ".join(str(magic[i][j]) for j in range(M)))\n\n\n# 主程序\nif __name__ == "__main__":\n    N = int(input().strip())\n    square = construct_magic_square(N)\n    print_magic_square(square)\n'
assert CASES[0] == SAMPLE_IN
random.seed(7207)
def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=5, check=True)
    return result.stdout
assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split()
root = Path(__file__).parent / "data"
for index, content in enumerate(CASES):
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")
