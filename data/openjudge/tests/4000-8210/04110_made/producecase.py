"""04110 圣诞老人的礼物 测试数据生成器：固定种子，重跑逐字节可复现。

第 0 组是题面样例；其余组覆盖 n=1、n=100、w=1、w=9999、总重量不足以装满驯鹿、
恰好装满、单价并列、「按价值/按重量贪心」与「整数除法算单价」会出错的数据。
答案用分数精确计算；生成时拒绝精确值落在 x.x5 附近（±1e-4）的数据，避免四舍五入歧义。
"""
import random
import re
from fractions import Fraction
from pathlib import Path

SAMPLE_IN = '4 15\n100 4\n412 8\n266 7\n591 2\n'
SAMPLE_OUT = '1193.0\n'


def valid(text):
    """题面契约：首行 n w（1<=n<=100，0<w<10000）；其后恰 n 行，每行两个正整数 v w。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    pos = r"[1-9]\d*"
    head = lines[0].split(" ")
    if len(head) != 2 or not all(re.fullmatch(pos, x) for x in head):
        return False
    n, w = map(int, head)
    if not (1 <= n <= 100 and 0 < w < 10000) or len(lines) != n + 1:
        return False
    for line in lines[1:]:
        t = line.split(" ")
        if len(t) != 2 or not all(re.fullmatch(pos, x) for x in t):
            return False
    return True


def exact(text):
    a = list(map(int, text.split()))
    n, cap = a[0], a[1]
    items = sorted(((Fraction(a[2 + 2 * i], a[3 + 2 * i]), a[3 + 2 * i]) for i in range(n)), reverse=True)
    total = Fraction(0)
    for ratio, w in items:
        take = min(cap, w)
        total += ratio * take
        cap -= take
        if cap == 0:
            break
    return total


def safe(text):
    f = exact(text) * 10
    frac = f - (f.numerator // f.denominator)
    return abs(frac - Fraction(1, 2)) > Fraction(1, 10000)


def solve(text):
    t = exact(text)
    # 四舍五入到 1 位小数（safe() 已保证不在 .x5 附近）
    q = (t * 10 + Fraction(1, 2)).__floor__()
    return f"{q // 10}.{q % 10}\n"


def case(cap, items):
    return f"{len(items)} {cap}\n" + "".join(f"{v} {w}\n" for v, w in items)


def rand_case(r, n, cap, vmax, wmax):
    while True:
        items = [(r.randint(1, vmax), r.randint(1, wmax)) for _ in range(n)]
        c = case(cap, items)
        if safe(c):
            return c


def build_cases():
    r = random.Random(4110)
    fixed = [
        case(1, [(100, 1)]),                        # 最小
        case(15, [(100, 15)]),                      # 恰好装满
        case(30, [(1, 1), (200, 15)]),              # 总重量不足
        case(9999, [(100000, 10000)]),              # 只能拿一部分：99990.0
        case(1, [(7, 3)]),                          # 2.333.. -> 2.3
        case(2, [(5, 3)]),                          # 3.333.. -> 3.3
        case(3, [(2, 3), (100, 7)]),                # 单价最高者只能拿一部分
        case(10, [(100, 10), (11, 1), (11, 1)]),     # 按价值贪心得 100，正解 22+80=102
        case(10, [(1, 1), (1000, 20)]),             # 按重量（轻者优先）贪心会错
        case(3, [(3, 1), (10, 3), (7, 2)]),         # 整数除法单价 3/3/3 并列，按输入序取得 9.7，正解 10.3
        case(5, [(4, 2), (6, 3), (2, 1), (8, 4)]),  # 单价全部并列
        case(9999, [(10000, 100)] * 100),           # n=100，总重量 10000 > 9999
        case(9999, [(i, 100) for i in range(1, 101)]),
    ]
    fixed = [c for c in fixed if safe(c)]
    cases = [SAMPLE_IN] + fixed
    for _ in range(8):
        cases.append(rand_case(r, r.randint(2, 10), r.randint(1, 60), 300, 20))
    for _ in range(6):
        cases.append(rand_case(r, r.randint(10, 100), r.randint(100, 9999), 10000, 500))
    for _ in range(4):
        cases.append(rand_case(r, 100, r.randint(5000, 9999), 100000, 100))     # 总重量常不足
    for _ in range(4):
        cases.append(rand_case(r, 100, 9999, 100000, 10000))
    while len(cases) < 40:
        cases.append(rand_case(r, r.randint(1, 100), r.randint(1, 9999), r.choice([10, 1000, 100000]),
                               r.choice([5, 100, 10000])))
    return cases


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN and solve(SAMPLE_IN) == SAMPLE_OUT
    assert len(cases) == 40 and len(set(cases)) == len(cases)
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for i, c in enumerate(cases):
        assert valid(c) and safe(c), i
        (root / f"{i}.in").write_text(c)
        (root / f"{i}.out").write_text(solve(c))


if __name__ == "__main__":
    main()
