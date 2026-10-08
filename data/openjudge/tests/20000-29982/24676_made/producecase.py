import random, re, subprocess, sys, tempfile
from pathlib import Path
REFERENCE_SOURCE = "from itertools import product\n\ndef right_shift(row, shift):\n    return row[-shift:] + row[:-shift]\n\ndef calculate_max_column_sum(matrix):\n    n = len(matrix)\n    column_sums = [0] * n\n    for row in matrix:\n        for i, val in enumerate(row):\n            column_sums[i] += val\n    return max(column_sums)\n\ndef find_min_max_column_sum(n, original_matrix):\n    min_max_sum = float('inf')\n\n    # 产生所有行可能的移动方式\n    all_shifts = list(product(range(n), repeat=n))\n    for shifts in all_shifts:\n        # 应用移动\n        shifted_matrix = [\n            right_shift(original_matrix[i], shifts[i]) for i in range(n)\n        ]\n        # 计算当前移动方式下的最大列和\n        max_column_sum = calculate_max_column_sum(shifted_matrix)\n        # 更新最小的最大列和\n        min_max_sum = min(min_max_sum, max_column_sum)\n    \n    return min_max_sum\n\n# 输入处理\nresults = []\nwhile True:\n    n = int(input())\n    if n == 0:\n        break\n    \n    original_matrix = [list(map(int, input().split())) for _ in range(n)]\n    result = find_min_max_column_sum(n, original_matrix)\n    results.append(result)\n\n# 输出结果\nfor result in results:\n    print(result)\n"
SAMPLE_IN = '2\n4 6\n3 7\n3\n1 2 3\n4 5 6\n7 8 9\n0\n'
SAMPLE_OUT = '11\n15\n'


def valid(text):
    """题面：多组数据，每组首行正整数 n(n<=5)，接 n 行各 n 个正整数；以一个 0 结尾。"""
    lines = text.split("\n")
    if not lines or lines[-1] != "":
        return False
    lines.pop()
    pos = 0
    while True:
        if pos >= len(lines) or not re.fullmatch(r"\d+", lines[pos]):
            return False
        n = int(lines[pos]); pos += 1
        if lines[pos - 1] != str(n):
            return False
        if n == 0:
            return pos == len(lines)
        if n > 5 or pos + n > len(lines):
            return False
        for row in lines[pos:pos + n]:
            toks = row.split(" ")
            if len(toks) != n or not all(re.fullmatch(r"[1-9]\d*", t) for t in toks):
                return False
        pos += n


def old_case(r):
    cases = []
    for _ in range(r.randint(2, 4)):
        n = r.randint(1, 5)
        cases.append(str(n))
        cases.extend(" ".join(str(r.randint(1, 30)) for _ in range(n)) for _ in range(n))
    return "\n".join(cases + ["0"]) + "\n"


def pack(mats):
    out = []
    for m in mats:
        out.append(str(len(m)))
        out.extend(" ".join(map(str, row)) for row in m)
    return "\n".join(out + ["0"]) + "\n"


def rand_mat(r, n, lo, hi):
    return [[r.randint(lo, hi) for _ in range(n)] for _ in range(n)]


def build_cases():
    cases, seen = [SAMPLE_IN], {SAMPLE_IN}
    for index in range(1, 10):                       # 原随机数据保留前 9 组
        for attempt in range(100):
            content = old_case(random.Random(24676 + index + attempt * 1000))
            if content not in seen: break
        seen.add(content); cases.append(content)
    r = random.Random(246760)
    cases.append(pack([[[1]], [[1000000]]]))                                   # n=1
    cases.append(pack([[[5] * 5 for _ in range(5)], [[1, 1, 1, 1, 100]] * 5]))  # 全等；大数集中一列须错开
    cases.append(pack([[[1, 2], [1, 2]], [[3, 1, 2], [3, 1, 2], [3, 1, 2]]]))  # 原状最差，必须移动
    cases.append(pack([rand_mat(r, 5, 1, 1000000) for _ in range(8)]))          # n=5 大数值
    cases.append(pack([rand_mat(r, n, 1, 10) for n in (1, 2, 3, 4, 5) for _ in range(4)]))
    cases.append(pack([rand_mat(r, 5, 1, 1000) for _ in range(40)]))            # 多组 n=5
    cases.append(pack([rand_mat(r, 4, 1, 100000) for _ in range(30)]))
    cases.append(pack([[[r.choice([1, 1, 1, r.randint(500, 1000)]) for _ in range(5)] for _ in range(5)] for _ in range(20)]))
    cases.append(pack([rand_mat(r, r.randint(1, 5), 1, 50) for _ in range(30)]))
    cases.append(pack([rand_mat(r, 5, 1, 2) for _ in range(30)]))
    return cases


def main():
    cases = build_cases()
    assert len(cases) == 20 and len(set(cases)) == 20 and all(valid(c) for c in cases)
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        for index, content in enumerate(cases):
            result = subprocess.run([sys.executable, handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            if index == 0: assert result.stdout == SAMPLE_OUT
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
