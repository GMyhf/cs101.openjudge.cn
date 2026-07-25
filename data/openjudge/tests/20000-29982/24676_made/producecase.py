import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "from itertools import product\n\ndef right_shift(row, shift):\n    return row[-shift:] + row[:-shift]\n\ndef calculate_max_column_sum(matrix):\n    n = len(matrix)\n    column_sums = [0] * n\n    for row in matrix:\n        for i, val in enumerate(row):\n            column_sums[i] += val\n    return max(column_sums)\n\ndef find_min_max_column_sum(n, original_matrix):\n    min_max_sum = float('inf')\n\n    # 产生所有行可能的移动方式\n    all_shifts = list(product(range(n), repeat=n))\n    for shifts in all_shifts:\n        # 应用移动\n        shifted_matrix = [\n            right_shift(original_matrix[i], shifts[i]) for i in range(n)\n        ]\n        # 计算当前移动方式下的最大列和\n        max_column_sum = calculate_max_column_sum(shifted_matrix)\n        # 更新最小的最大列和\n        min_max_sum = min(min_max_sum, max_column_sum)\n    \n    return min_max_sum\n\n# 输入处理\nresults = []\nwhile True:\n    n = int(input())\n    if n == 0:\n        break\n    \n    original_matrix = [list(map(int, input().split())) for _ in range(n)]\n    result = find_min_max_column_sum(n, original_matrix)\n    results.append(result)\n\n# 输出结果\nfor result in results:\n    print(result)\n"
SAMPLE_IN = '2\n4 6\n3 7\n3\n1 2 3\n4 5 6\n7 8 9\n0\n'
SAMPLE_OUT = '11\n15\n'
def generate_case(r):
    cases = []
    for _ in range(r.randint(2, 4)):
        n = r.randint(1, 5)
        cases.append(str(n))
        cases.extend(" ".join(str(r.randint(1, 30)) for _ in range(n)) for _ in range(n))
    return "\n".join(cases + ["0"]) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(24676 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
