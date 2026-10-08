"""04108 羚羊数量 测试数据生成器：固定种子，重跑逐字节可复现。

第 0 组是题面样例；其余组覆盖 n=0、n=1/2/3 边界、n=40 上界、m=1 与 m=15、
重复询问、乱序询问。f(0)=f(1)=f(2)=1，f(n)=f(n-1)+f(n-3)。
"""
import random
import re
from pathlib import Path

SAMPLE_IN = '3\n1\n3\n4\n'
SAMPLE_OUT = '1\n2\n3\n'


def valid(text):
    """题面契约：第一行 m（1<=m<=15），其后恰 m 行，每行一个整数 n（0<=n<=40）。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not all(re.fullmatch(r"0|[1-9]\d*", x) for x in lines):
        return False
    m = int(lines[0])
    if not 1 <= m <= 15 or len(lines) != m + 1:
        return False
    return all(0 <= int(x) <= 40 for x in lines[1:])


F = [1, 1, 1]
for _n in range(3, 41):
    F.append(F[-1] + F[_n - 3])


def solve(text):
    a = list(map(int, text.split()))
    return "".join(f"{F[n]}\n" for n in a[1:1 + a[0]])


def case(ns):
    return f"{len(ns)}\n" + "".join(f"{n}\n" for n in ns)


def build_cases():
    cases = [SAMPLE_IN, case([0]), case([1]), case([2]), case([3]), case([40]),
             case([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]),
             case(list(range(26, 41))),
             case([40] * 15),
             case([40, 0, 39, 1, 38, 2, 37, 3, 36, 4, 35, 5, 34, 6, 33]),
             case([20, 21, 22]),
             case(list(range(15, 26)))]
    rng = random.Random(4108)
    seen = set(cases)
    while len(cases) < 40:
        m = rng.choice([1, 2, 5, 8, 15, 15, rng.randint(1, 15)])
        c = case([rng.randint(0, 40) for _ in range(m)])
        if c not in seen:
            seen.add(c)
            cases.append(c)
    return cases


def main():
    assert F[40] < 2 ** 31
    cases = build_cases()
    assert cases[0] == SAMPLE_IN and solve(SAMPLE_IN) == SAMPLE_OUT
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for i, c in enumerate(cases):
        assert valid(c), i
        (root / f"{i}.in").write_text(c)
        (root / f"{i}.out").write_text(solve(c))


if __name__ == "__main__":
    main()
