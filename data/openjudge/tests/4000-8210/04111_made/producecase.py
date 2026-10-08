"""04111 判断游戏胜者 测试数据生成器：固定种子，重跑逐字节可复现。

第 0 组是题面样例；其余组覆盖 0x0、前导 0、跨十六进制位的连续 1 块（按位分别数块会错）、
只数 1 的个数会错的数据、三种结果都出现、超过 64 位的长数串、n=10000 的规模组。
题面只说「16 进制数串」，样例均为 0x 前缀的小写串，这里全部按此生成。
"""
import random
import re
from pathlib import Path

SAMPLE_IN = '2\n0xfa425 0xab3672\n0x52c6 0xf429\n'
SAMPLE_OUT = 'Bob\nTie\n'


def valid(text):
    """题面契约：首行正整数 n；其后恰 n 行，每行两个以 0x 开头的十六进制数串，单个空格分隔。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not re.fullmatch(r"[1-9]\d*", lines[0]):
        return False
    n = int(lines[0])
    if len(lines) != n + 1:
        return False
    return all(re.fullmatch(r"0x[0-9a-fA-F]+ 0x[0-9a-fA-F]+", x) for x in lines[1:])


def blocks(h):
    b = bin(int(h, 16))[2:]
    return len([x for x in b.split("0") if x])


def solve(text):
    a = text.split()
    out = []
    for x, y in zip(a[1::2], a[2::2]):
        p, q = blocks(x), blocks(y)
        out.append("Alice" if p > q else "Bob" if p < q else "Tie")
    return "\n".join(out) + "\n"


def case(pairs):
    return f"{len(pairs)}\n" + "".join(f"{x} {y}\n" for x, y in pairs)


def rhex(r, digits, lead_zero=False):
    s = "".join(r.choice("0123456789abcdef") for _ in range(digits))
    if not lead_zero:
        s = s.lstrip("0") or "0"
    return "0x" + s


def runs_hex(r, bits):
    """长连续段的二进制串，制造跨位的 1 块。"""
    b = []
    while len(b) < bits:
        b += [r.choice("01")] * r.randint(1, 12)
    v = int("".join(b[:bits]), 2)
    return "0x%x" % v


def build_cases():
    r = random.Random(4111)
    cases = [
        SAMPLE_IN,
        case([("0x0", "0x0")]),
        case([("0x1", "0x0")]),
        case([("0x0", "0x1")]),
        case([("0x3c", "0x5"), ("0xf0f", "0xff"), ("0x18", "0x81")]),     # 跨位块；只数 1 的个数会错
        case([("0xffffffff", "0x55555555"), ("0x8000000000000000", "0x1"),
              ("0xffffffffffffffffff", "0xaaaaaaaaaaaaaaaaaa")]),             # 超 32/64 位
        case([("0x000f", "0xf"), ("0x0001", "0x10"), ("0x00", "0x0")]),     # 前导 0
        case([("0xaaaa", "0x5555"), ("0x8000", "0x7fff"), ("0x1234", "0x1234")]),
        case([("0x" + "a" * 200, "0x" + "5" * 200), ("0x" + "f" * 300, "0x1"),
              ("0x" + "9" * 150, "0x" + "6" * 150)]),
    ]
    for _ in range(12):
        cases.append(case([(rhex(r, r.randint(1, 6)), rhex(r, r.randint(1, 6))) for _ in range(r.randint(3, 20))]))
    for _ in range(6):
        cases.append(case([(runs_hex(r, r.randint(4, 64)), runs_hex(r, r.randint(4, 64)))
                           for _ in range(r.randint(5, 30))]))
    for _ in range(5):
        cases.append(case([(rhex(r, r.randint(1, 40), True), rhex(r, r.randint(1, 40), True))
                           for _ in range(r.randint(20, 100))]))
    for _ in range(3):
        cases.append(case([(rhex(r, r.randint(100, 1000)), rhex(r, r.randint(100, 1000)))
                           for _ in range(r.randint(5, 20))]))
    cases.append(case([(rhex(r, r.randint(1, 8)), rhex(r, r.randint(1, 8))) for _ in range(10000)]))
    cases.append(case([(runs_hex(r, 64), runs_hex(r, 64)) for _ in range(10000)]))
    cases.append(case([(rhex(r, 20000), rhex(r, 20000)) for _ in range(10)]))
    while len(cases) < 40:
        cases.append(case([(rhex(r, 4), rhex(r, 4)) for _ in range(r.randint(1, 10))]))
    return cases


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN and solve(SAMPLE_IN) == SAMPLE_OUT
    assert len(cases) == 40 and len(set(cases)) == len(cases)
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for i, c in enumerate(cases):
        assert valid(c), i
        (root / f"{i}.in").write_text(c)
        (root / f"{i}.out").write_text(solve(c))


if __name__ == "__main__":
    main()
