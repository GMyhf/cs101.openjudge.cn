def solve_text(text):
    it = iter(text.split()); out = []
    while True:
        try: n = int(next(it))
        except StopIteration: break
        v = [int(next(it)) for _ in range(n)]
        total, largest = sum(v), max(v)
        out.append(f"{min(total / 2, total - largest):.1f}")
    return "\n".join(out) + ("\n" if out else "")


def generate_case(rng):
    cases = [[3, 5], [3, 3, 5], [2, 2], [1, 9, 9, 9, 9]]
    cases += [[rng.randint(1, 30) for _ in range(rng.randint(2, 8))] for _ in range(8)]
    return "\n".join(str(len(v)) + "\n" + " ".join(map(str, v)) for v in cases) + "\n"

import random
import re
from pathlib import Path

SAMPLE_IN = '2\n3 5\n3\n3 3 5\n'
SAMPLE_OUT = '3.0\n5.5\n'


def valid(text):
    """题面契约：多组数据，每组两行：N（2 <= N <= 1000），下一行恰好 N 个正整数。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not lines or len(lines) % 2:
        return False
    for k in range(0, len(lines), 2):
        if not re.fullmatch(r"\d+", lines[k]):
            return False
        n = int(lines[k])
        toks = lines[k + 1].split()
        if not 2 <= n <= 1000 or len(toks) != n:
            return False
        if any(not re.fullmatch(r"\d+", t) or int(t) <= 0 for t in toks):
            return False
    return True


def fmt(groups):
    return "\n".join(str(len(v)) + "\n" + " ".join(map(str, v)) for v in groups) + "\n"


def extra_case(rng, kind):
    """边界/规模组：N=1000、大值、最大者恰等于其余之和、两个分支都要出现。题面没给值域上界，
    取到 10^6（总和 <= 10^9，不靠溢出卡人）。"""
    groups = []
    if kind == "big":
        for _ in range(5):
            groups.append([rng.randint(1, 10 ** 6) for _ in range(1000)])
        v = [rng.randint(1, 1000) for _ in range(999)]
        groups.append(v + [sum(v) + rng.randint(1, 10 ** 5)])   # 最大者压倒其余：答案 total-largest
        v = [rng.randint(1, 1000) for _ in range(999)]
        groups.append(v + [sum(v)])                             # 恰好相等：两式同值
        groups.append([10 ** 6] * 1000)
        rng.shuffle(groups)
    elif kind == "edge":
        groups = [[1, 1], [1, 2], [1, 10 ** 6], [10 ** 6, 10 ** 6], [7, 3, 4], [7, 3, 3],
                  [2, 2, 2], [1, 1, 1], [5, 1, 1, 1, 1], [1, 1, 1, 1, 5], [9, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    else:
        for _ in range(rng.randint(30, 60)):
            n = rng.randint(2, 50)
            v = [rng.randint(1, 100) for _ in range(n)]
            if rng.random() < 0.4:
                v[rng.randrange(n)] = sum(v) + rng.randint(-5, 50)
                v = [max(1, x) for x in v]
            groups.append(v)
    return fmt(groups)


def build_cases():
    rng = random.Random(3468)
    cases = [SAMPLE_IN] + [generate_case(rng) for _ in range(19)]
    rng2 = random.Random(3468 * 1000 + 1)
    cases += [extra_case(rng2, k) for k in ["edge", "mix", "mix", "big", "big"]]
    return cases


def main():
    assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
    root = Path(__file__).parent / "data"
    for index, content in enumerate(build_cases()):
        assert valid(content), index
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
    print("generated cases for 03468")


if __name__ == "__main__":
    main()
