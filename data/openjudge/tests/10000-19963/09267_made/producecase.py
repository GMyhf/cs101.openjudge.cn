def solve_text(text):
    n, m = map(int, text.split()); states = [0] * m; states[0] = 1
    for _ in range(n):
        next_states = [0] * m
        for run, count in enumerate(states):
            next_states[0] += count
            if run + 1 < m: next_states[run + 1] += count
        states = next_states
    return str(sum(states)) + "\n"


def generate_case(rng): return f"{rng.randint(2, 49)} {rng.randint(2, 5)}\n"

import random
from pathlib import Path
SAMPLE_IN = '4 3\n'
SAMPLE_OUT = '13\n'
# 2026-10 审计补充：原数据最大只到 N=46，缺 N=49 各个 M、N=2 的最小规模、N=M 等边界
EXTRA = ["49 5\n", "49 2\n", "49 3\n", "49 4\n", "2 2\n", "2 5\n", "5 5\n", "3 2\n", "48 5\n"]


def valid(text):
    """题面：只有一行，两个正整数 N，M（1 < N < 50, 2 <= M <= 5）。"""
    lines = text.split("\n")
    if len(lines) != 2 or lines[1] != "":
        return False
    tok = lines[0].split()
    if len(tok) != 2 or not all(t.isdigit() for t in tok):
        return False
    n, m = map(int, tok)
    return 1 < n < 50 and 2 <= m <= 5


def main():
    assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
    rng = random.Random(9267)
    cases = [SAMPLE_IN] + [generate_case(rng) for _ in range(19)]
    cases += [c for c in EXTRA if c not in cases]
    assert all(valid(c) for c in cases), "题面：1 < N < 50, 2 <= M <= 5"
    root = Path(__file__).parent / "data"
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
    print(f"generated {len(cases)} cases for 09267")


if __name__ == "__main__":
    main()
