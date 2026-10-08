def solve_text(text):
    values = list(map(int, text.split())); n, permutation = values[0], values[1:]
    bit = [0] * (n + 2); answer = 0
    for value in reversed(permutation):
        x = value - 1
        while x:
            answer += bit[x]; x -= x & -x
        x = value
        while x <= n:
            bit[x] += 1; x += x & -x
    return str(answer) + "\n"


def generate_case(rng, index):
    # 规模：最小、小、中、满规模（题面 n <= 100000）
    if index <= 3: n = index
    elif index <= 8: n = rng.randint(4, 100)
    elif index <= 12: n = rng.randint(1000, 30000)
    else: n = 100000 if index <= 17 else 99999          # 两轮满规模用不同 n，避免重复
    values = list(range(1, n + 1)); mode = index % 5 if index < 13 else (index - 13) % 5
    if mode == 0: rng.shuffle(values)
    elif mode == 1: values.reverse()                       # 最大逆序数 n(n-1)/2，满规模时超 int
    elif mode == 2:                                        # 近乎有序：少量交换
        for _ in range(max(1, n // 50)):
            i, j = rng.randrange(n), rng.randrange(n); values[i], values[j] = values[j], values[i]
    elif mode == 3:                                        # 近乎逆序
        values.reverse()
        for _ in range(max(1, n // 50)):
            i, j = rng.randrange(n), rng.randrange(n); values[i], values[j] = values[j], values[i]
    else:                                                  # 有序 / 随机块
        if index % 2: rng.shuffle(values)
    return f"{n}\n" + " ".join(map(str, values)) + "\n"


import re
def valid(text):
    """题面：第一行 n（n≤100000，取 n≥1）；第二行 n 个以空格隔开的不同正整数，构成 1..n 的一个排列。"""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if len(lines) != 2 or not re.fullmatch(r"[1-9][0-9]*", lines[0]):
        return False
    n = int(lines[0])
    if not 1 <= n <= 100000:
        return False
    toks = lines[1].split(" ")
    if len(toks) != n or not all(re.fullmatch(r"[1-9][0-9]*", t) for t in toks):
        return False
    return sorted(map(int, toks)) == list(range(1, n + 1))


import random
from pathlib import Path
SAMPLE_IN = '6\n2 6 3 4 5 1\n'
SAMPLE_OUT = '8\n'
COUNT = 20   # catalog.json 登记了 0..19 共 20 组


def main():
    assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
    rng = random.Random(7622)
    cases = [SAMPLE_IN] + [generate_case(rng, i) for i in range(1, COUNT)]
    assert all(valid(c) for c in cases), "有数据越出题面约束"
    assert len(set(cases)) == len(cases), "有重复数据"
    root = Path(__file__).parent / "data"
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
    print(f"generated {len(cases)} cases for 07622")


if __name__ == "__main__":
    main()
