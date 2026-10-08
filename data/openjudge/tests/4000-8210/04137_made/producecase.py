import random
from pathlib import Path


def solve_text(text):
    it = iter(text.split()); out = []
    for _ in range(int(next(it))):
        number, remove = next(it), int(next(it)); stack = []
        for ch in number:
            while stack and remove and stack[-1] > ch:
                stack.pop(); remove -= 1
            stack.append(ch)
        if remove: stack = stack[:-remove]
        out.append("".join(stack).lstrip("0") or "0")
    return "\n".join(out) + "\n"


def generate_case(rng):
    # 题面：第一行 t（t <= 10）；每组的 n 满足 0 < n < 10^9 且**每个数位都不为 0**。
    # 2026-09-20 之前这里固定 16 组（越过 t<=10），并且带了一个含 0 的 100000001。
    cases = [("9128456", 2), ("1444", 3), ("987654321", 4)]
    for _ in range(7):
        size = rng.randint(2, 9)
        cases.append((str(rng.randint(1, 9)) + "".join(str(rng.randint(1, 9)) for _ in range(size - 1)), rng.randint(1, size - 1)))
    return str(len(cases)) + "\n" + "\n".join(f"{n} {k}" for n, k in cases) + "\n"

def valid(text):
    """题面：首行 t（t≤10，至少 1 组）；随后恰 t 行 "n k"：0<n<1e9 且各数位非 0，m 为 n 的位数，0<k<m。"""
    if not text.endswith("\n"):
        return False
    L = text[:-1].split("\n")
    if not L[0].isdigit() or L[0][0] == "0":
        return False
    t = int(L[0])
    if not 1 <= t <= 10 or len(L) != t + 1:
        return False
    for line in L[1:]:
        q = line.split(" ")
        if len(q) != 2 or not q[0].isdigit() or not q[1].isdigit() or q[1][0] == "0":
            return False
        n, k = q
        if "0" in n or not 1 <= len(n) <= 9 or not 0 < int(k) < len(n):
            return False
    return True


EDGE = [
    [("21", 1)],
    [("12", 1), ("99", 1), ("123456789", 8), ("987654321", 8), ("111111111", 4)],
    [("123456789", 1), ("123456789", 4), ("987654321", 1), ("135797531", 3), ("999999991", 8)],
    [("19191919", 4), ("91919191", 4), ("219", 1), ("2199", 2), ("332211", 3), ("54321", 2), ("13", 1), ("31", 1), ("112", 2), ("211", 2)],
    [("989898989", k) for k in range(1, 9)] + [("123123123", 3), ("321321321", 3)],
]


def main():
    SAMPLE_IN = '2\n9128456 2\n1444 3\n'
    SAMPLE_OUT = '12456\n1\n'
    assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
    rng = random.Random(4137)
    root = Path(__file__).parent / "data"
    # 1..14 沿用原随机组；15..19 换成手工边界组（组数保持 20）
    cases = [SAMPLE_IN] + [generate_case(rng) for _ in range(14)]
    cases += [str(len(e)) + "\n" + "".join(f"{n} {k}\n" for n, k in e) for e in EDGE]
    assert all(valid(c) for c in cases) and len(set(cases)) == len(cases)
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
    print(f"generated {len(cases)} cases for 04137")


if __name__ == "__main__":
    main()
