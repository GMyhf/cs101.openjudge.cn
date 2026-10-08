"""04107 19岁生日礼物 测试数据生成器：固定种子，重跑逐字节可复现。

第 0 组是题面样例；其余组覆盖：最小值 1、int 上界 2147483647、19 的倍数但不含 "19"、
含 "19" 但不是倍数、1 和 9 不相邻（109、1091）等易错值、大量随机值、n=80000 的规模组。
"""
import random
import re
from pathlib import Path

SAMPLE_IN = '4\n95\n100\n3192\n2913\n'
SAMPLE_OUT = 'Yes\nNo\nYes\nNo\n'
INT_MAX = 2 ** 31 - 1


def valid(text):
    """题面契约：第一行正整数 n（int 范围），其后恰 n 行，每行一个正整数 p（int 范围）。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not all(re.fullmatch(r"[1-9]\d*", x) for x in lines):
        return False
    n = int(lines[0])
    if n > INT_MAX or len(lines) != n + 1:
        return False
    return all(1 <= int(x) <= INT_MAX for x in lines[1:])


def related(p):
    return p % 19 == 0 or "19" in str(p)


def solve_text(text):
    it = iter(text.split())
    out = []
    for _ in range(int(next(it))):
        out.append("Yes" if related(int(next(it))) else "No")
    return "\n".join(out) + "\n"


def case(values):
    return str(len(values)) + "\n" + "\n".join(map(str, values)) + "\n"


TRICKY = [1, 9, 18, 19, 20, 38, 91, 109, 119, 190, 191, 199, 361, 918, 1091, 1919, 9119,
          2019, 1900000000, 1999999999, 2147483647, 2147483646, 2147483629, 2147483628,
          1000000000, 1000000019, 1009, 100, 200, 95, 3192, 2913]


def generate_random(rng, n, lo=1, hi=INT_MAX):
    vals = []
    for _ in range(n):
        t = rng.random()
        if t < 0.3:
            vals.append(19 * rng.randint(max(1, lo // 19), hi // 19))
        elif t < 0.55:
            # 在随机位置嵌入 "19"
            s = str(rng.randint(lo, hi))
            k = rng.randint(0, len(s) - 1)
            s2 = (s[:k] + "19" + s[k + 2:])[: len(s)]
            if s2[0] == "0":
                s2 = "1" + s2[1:]
            v = int(s2)
            vals.append(v if 1 <= v <= INT_MAX else rng.randint(lo, hi))
        else:
            vals.append(rng.randint(lo, hi))
    return vals


def build_cases():
    rng = random.Random(7810)
    cases = [SAMPLE_IN, case([1]), case([19]), case([2147483647]), case(TRICKY),
             case([19 * k for k in (1, 2, 3, 5, 52, 53, 105, 113025455)]),   # 倍数，多数不含 "19"
             case([119, 1191, 21901, 1019, 2019, 19191, 9190, 1900]),       # 含 "19" 的非倍数为主
             case([109, 1091, 10009, 9001, 91, 9911, 1, 1009, 90001])]      # 1、9 不相邻
    for _ in range(6):
        cases.append(case(generate_random(rng, rng.randint(10, 60))))
    for _ in range(3):
        cases.append(case(generate_random(rng, rng.randint(10, 60), 1, 10000)))
    cases.append(case(generate_random(rng, 5000)))
    cases.append(case(generate_random(rng, 80000, 1000000000, INT_MAX)))
    cases.append(case(generate_random(rng, 80000)))
    assert len(cases) == 20  # catalog.json 只登记了 0..19 组
    return cases


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN and solve_text(SAMPLE_IN) == SAMPLE_OUT
    assert len(set(cases)) == len(cases)
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        assert valid(content), index
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
    print(f"generated {len(cases)} cases for 04107")


if __name__ == "__main__":
    main()
