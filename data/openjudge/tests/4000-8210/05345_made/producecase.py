"""5345 位查询 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的数据。

第 0 组是题面样例；第 1~19 组是原有的小规模随机组（初值均在 1~65535，照题面「N个正整数」）；
第 20 组起是边界组与大规模组（N=100000 满规模；M 受单组 .in ≤ 1MB 所限取到 8.2 万~14.5 万，
已足以卡掉每次 C 都整体加一遍、或每次 Q 都扫一遍 N 个数的 O(NM) 写法）。
"""
import random
from pathlib import Path

SAMPLE_IN = '3 5\n1 2 4\nQ 1\nQ 2\nC 1\nQ 1\nQ 2\n'
SAMPLE_OUT = '1\n1\n2\n1\n'
MOD = 65536


def solve_naive(text):
    """逐个模拟，只用于核小规模组。"""
    it = iter(text.split()); n, m = int(next(it)), int(next(it))
    values = [int(next(it)) for _ in range(n)]; out = []
    for _ in range(m):
        op, x = next(it), int(next(it))
        if op == "C": values = [(v + x) % MOD for v in values]
        else: out.append(str(sum((v >> x) & 1 for v in values)))
    return "\n".join(out) + ("\n" if out else "")


def solve_text(text):
    """累计偏移 D；第 i 位为 1 ⇔ (v mod 2^(i+1) + D mod 2^(i+1)) mod 2^(i+1) ≥ 2^i，按余数前缀和 O(1) 回答。"""
    data = text.split(); n, m = int(data[0]), int(data[1])
    cnt = [0] * MOD
    for token in data[2:2 + n]:
        cnt[int(token)] += 1
    prefix = [None] * 16
    level = cnt
    for i in range(15, -1, -1):
        size = 1 << (i + 1)
        if len(level) != size:
            level = [level[r] + level[r + size] for r in range(size)]
        acc = [0] * (size + 1)
        for r in range(size):
            acc[r + 1] = acc[r] + level[r]
        prefix[i] = acc
    offset = 0; out = []; pos = 2 + n
    for _ in range(m):
        op, x = data[pos], int(data[pos + 1]); pos += 2
        if op == "C":
            offset = (offset + x) % MOD
        else:
            size = 1 << (x + 1); half = 1 << x; d = offset % size; acc = prefix[x]
            lo, hi = (half - d) % size, (size - d) % size  # 余数落在循环区间 [lo, hi)
            out.append(str(acc[hi] - acc[lo] if lo < hi else acc[size] - acc[lo] + acc[hi]))
    return "\n".join(out) + ("\n" if out else "")


def valid(text):
    """题面：第一行正整数 N M（N<=100000，M<=200000）；第二行 N 个正整数，范围 [0,65535]（取交集即 1~65535）；
    之后恰 M 行操作，C d（0<=d<=65535）或 Q i（0<=i<=15）。"""
    lines = text.split("\n")
    if len(lines) < 3 or lines[-1] != "":
        return False
    lines = lines[:-1]
    head = lines[0].split(" ")
    if len(head) != 2 or not all(x.isdigit() for x in head):
        return False
    n, m = map(int, head)
    if not (1 <= n <= 100000 and 1 <= m <= 200000) or len(lines) != m + 2:
        return False
    values = lines[1].split(" ")
    if len(values) != n or not all(x.isdigit() and 1 <= int(x) <= 65535 for x in values):
        return False
    for line in lines[2:]:
        parts = line.split(" ")
        if len(parts) != 2 or parts[0] not in ("C", "Q") or not parts[1].isdigit():
            return False
        x = int(parts[1])
        if not (0 <= x <= (65535 if parts[0] == "C" else 15)):
            return False
    return True


def fmt(values, ops):
    return f"{len(values)} {len(ops)}\n" + " ".join(map(str, values)) + "\n" + "".join(f"{op} {x}\n" for op, x in ops)


def generate_case(rng):
    n, m = rng.randint(1, 20), rng.randint(20, 60)
    values = [rng.randrange(MOD) for _ in range(n)]  # 沿用原随机流；这 19 组恰好不含 0，由 valid() 断言把关
    ops = [(rng.choice(["C", "C", "Q"]), rng.randrange(16)) for _ in range(m)]
    return fmt(values, ops)


def random_op(rng, q_ratio):
    if rng.random() < q_ratio:
        return ("Q", rng.randrange(16))
    roll = rng.random()
    if roll < 0.1: return ("C", 0)
    if roll < 0.2: return ("C", 65535)
    if roll < 0.4: return ("C", rng.randint(1, 9))
    return ("C", rng.randrange(MOD))


def edge_cases(rng):
    cases = []
    # 最小规模
    cases.append(fmt([1], [("Q", 0)]))
    cases.append(fmt([65535], [("Q", 15), ("C", 1), ("Q", 15), ("Q", 0)]))
    # 回绕：65535 + 1 → 0，再逐位核
    cases.append(fmt([65535, 32768, 1, 2],
                     [("C", 1)] + [("Q", i) for i in range(16)] + [("C", 65535)] + [("Q", i) for i in range(16)]))
    # d=0 与 d=65535 交替，每一位都问
    vals = [rng.randrange(1, MOD) for _ in range(200)]
    ops = []
    for _ in range(300):
        ops.append(("C", rng.choice([0, 65535, 1, 32768])))
        ops.append(("Q", rng.randrange(16)))
    cases.append(fmt(vals, ops))
    # 中等规模随机
    for n, m in ((2000, 3000), (5000, 8000)):
        cases.append(fmt([rng.randrange(1, MOD) for _ in range(n)], [random_op(rng, 0.5) for _ in range(m)]))
    # 大规模：N=100000，M 取到单组 1MB 以内
    cases.append(fmt([rng.randrange(1, MOD) for _ in range(100000)], [random_op(rng, 0.5) for _ in range(82000)]))
    cases.append(fmt([rng.randrange(1, MOD) for _ in range(100000)], [("Q", rng.randrange(16)) for _ in range(95000)]))
    cases.append(fmt([rng.randint(1, 999) for _ in range(100000)], [random_op(rng, 0.6) for _ in range(110000)]))
    cases.append(fmt([rng.randrange(1, MOD) for _ in range(30000)], [random_op(rng, 0.5) for _ in range(145000)]))
    return cases


def build_cases():
    rng = random.Random(5345)
    cases = [SAMPLE_IN] + [generate_case(rng) for _ in range(19)]
    return cases + edge_cases(random.Random(53450))


def main():
    assert solve_text(SAMPLE_IN) == SAMPLE_OUT == solve_naive(SAMPLE_IN)
    cases = build_cases()
    assert all(valid(c) for c in cases), "有数据越出题面约束"
    assert len(set(cases)) == len(cases), "有重复组"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        assert len(content) <= 1 << 20, index
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
    print(f"generated {len(cases)} cases for 05345")


if __name__ == "__main__":
    main()
