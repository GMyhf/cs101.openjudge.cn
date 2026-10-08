def solve_text(text):
    n = int(text.split()[0]); catalan = [0] * (n + 1); catalan[0] = 1
    for size in range(1, n + 1):
        catalan[size] = sum(catalan[left] * catalan[size - 1 - left] for left in range(size))
    return str(catalan[n]) + "\n"


def generate_case(rng): return f"{rng.randint(1, 1000)}\n"

def valid(text):
    """题面：输入只含一个整数 n（1 <= n <= 1000）。"""
    if not text.endswith("\n"):
        return False
    lines = text.split("\n")[:-1]
    if len(lines) != 1 or not lines[0].isdigit() or lines[0][0] == "0":
        return False
    return 1 <= int(lines[0]) <= 1000

import random
from pathlib import Path
SAMPLE_IN = '3\n'
SAMPLE_OUT = '5\n'
# 边界：最小 n=1、2；上限 1000、999；卡 64 位整数溢出：C(35) 仍在 int64 内、C(36) 起溢出
FIXED = [1, 2, 1000, 999, 35, 36, 19, 20]

def main():
    assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
    rng = random.Random(27217)
    cases = [SAMPLE_IN] + [f"{n}\n" for n in FIXED]
    while len(cases) < 20:
        c = generate_case(rng)
        if c not in cases:
            cases.append(c)
    root = Path(__file__).parent / "data"
    for index, content in enumerate(cases):
        assert valid(content)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
    print("generated 20 cases for 27217")

if __name__ == "__main__":
    main()
