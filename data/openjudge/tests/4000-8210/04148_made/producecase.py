import random
from pathlib import Path


def valid(text):
    """题面契约：多组数据，每组一行四个整数 p e i d，均为 0..365；以 -1 -1 -1 -1 一行结束。"""
    lines = text.split("\n")
    while lines and lines[-1].strip() == "":
        lines.pop()
    if len(lines) < 2:
        return False
    if lines[-1].split() != ["-1", "-1", "-1", "-1"]:
        return False
    for line in lines[:-1]:
        tok = line.split()
        if len(tok) != 4:
            return False
        try:
            vals = [int(t) for t in tok]
        except ValueError:
            return False
        if not all(0 <= v <= 365 for v in vals):
            return False
    return True


def solve_text(text):
    out = []; case = 1
    for line in text.splitlines():
        p, e, i, d = map(int, line.split())
        if (p, e, i, d) == (-1, -1, -1, -1): break
        day = d + 1
        while (day - p) % 23 or (day - e) % 28 or (day - i) % 33:
            day += 1
        out.append(f"Case {case}: the next triple peak occurs in {day - d} days.")
        case += 1
    return "\n".join(out) + ("\n" if out else "")


def _peak(rng, x, period):
    # 取一个 0..365 内、与 x 同余于 period 的高峰日
    r = x % period
    return r + period * rng.randint(0, (365 - r) // period)


def _line(rng, d, gap):
    x = d + gap  # 下一次三峰重合的绝对日
    return f"{_peak(rng, x, 23)} {_peak(rng, x, 28)} {_peak(rng, x, 33)} {d}"


def generate_case(rng, kind, count):
    lines = []
    for _ in range(count):
        d = rng.randint(0, 365)
        if kind == "full":            # 恰在 d 当天重合，答案 21252
            gap = 21252
        elif kind == "one":           # 答案 1
            gap = 1
        elif kind == "edge":          # 混合边界
            d = rng.choice([0, 365, rng.randint(0, 365)])
            gap = rng.choice([1, 2, 21251, 21252, rng.randint(1, 21252)])
        elif kind == "smallpeak":     # d 小于 p/e/i：高峰日取得大
            d = rng.randint(0, 40)
            gap = rng.randint(1, 21252)
            x = d + gap
            lines.append(f"{x % 23 + 23 * ((365 - x % 23) // 23)} {x % 28 + 28 * ((365 - x % 28) // 28)} "
                         f"{x % 33 + 33 * ((365 - x % 33) // 33)} {d}")
            continue
        else:                         # 一般随机
            gap = rng.randint(1, 21252)
        lines.append(_line(rng, d, gap))
    return "\n".join(lines) + "\n-1 -1 -1 -1\n"


SAMPLE_IN = '0 0 0 0\n0 0 0 100\n5 20 34 325\n4 5 6 7\n283 102 23 320\n203 301 203 40\n-1 -1 -1 -1\n'
SAMPLE_OUT = 'Case 1: the next triple peak occurs in 21252 days.\nCase 2: the next triple peak occurs in 21152 days.\nCase 3: the next triple peak occurs in 19575 days.\nCase 4: the next triple peak occurs in 16994 days.\nCase 5: the next triple peak occurs in 8910 days.\nCase 6: the next triple peak occurs in 10789 days.\n'

PLAN = [("rand", 1), ("full", 1), ("one", 1), ("rand", 10), ("rand", 10), ("full", 5),
        ("one", 5), ("edge", 20), ("edge", 20), ("smallpeak", 15), ("smallpeak", 15),
        ("rand", 30), ("rand", 50), ("edge", 60), ("full", 100), ("rand", 150),
        ("edge", 200), ("full", 250), ("rand", 300)]


def main():
    assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
    rng = random.Random(4148)
    cases = [SAMPLE_IN] + [generate_case(rng, kind, cnt) for kind, cnt in PLAN]
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        assert valid(content), index
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
    print(f"generated {len(cases)} cases for 04148")


if __name__ == "__main__":
    main()
