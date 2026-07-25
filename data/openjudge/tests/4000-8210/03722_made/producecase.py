"""3722 测试数据生成器：有解 / 无解两个分支都压到，重跑可逐字节复现 data/。

出处：build_t004_round3 —— 2026-07-25 回归扫描修正。
原生成器是 `n=randint(1,1000000), m=randint(2,200)`，靠随机撞有解：
21 组里 19 组答案是 -1，仅有的 2 组有解答案还都是 5。恒定输出探针虽然抓不住
（-1 占 19/21，探针会 WA），但有解分支实际上没被覆盖。

现在一半的组构造成必有解：取 N 的两个因子 d1、d2，令 M = d1 + d2，
则 a = d1 满足「a 与 M-a 都整除 N」；另一半保留随机（多为 -1）。
题面 N <= 1000000 -> 生成器内断言；M 不设上界，但参考解法是 O(M) 循环，
封顶 500000 以免自己超时。
"""
import random
from pathlib import Path

SAMPLE_IN = '35 10\n'
SAMPLE_OUT = '5\n'
NLIMIT = 1000000
MLIMIT = 500000


def solve_text(text):
    n, m = map(int, text.split())
    answer = -1
    for a in range(1, m):
        if n % a == 0 and n % (m - a) == 0:
            answer = a
            break
    return str(answer) + "\n"


def divisors(n):
    out = []
    d = 1
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            if d != n // d:
                out.append(n // d)
        d += 1
    return sorted(out)


def solvable_case(r):
    """先选 N，再取它的两个因子凑出 M —— 这样 a=d1 必然可行。"""
    n = r.randint(2, NLIMIT)
    ds = divisors(n)
    for _ in range(200):
        d1, d2 = r.choice(ds), r.choice(ds)
        if 2 <= d1 + d2 <= MLIMIT:
            return f"{n} {d1 + d2}\n"
    return f"{n} 2\n"          # 兜底：M=2 -> a=1 必可行（1 整除任何 N）


def random_case(r):
    return f"{r.randint(1, NLIMIT)} {r.randint(2, 200)}\n"


def build_cases():
    cases = [SAMPLE_IN]
    for index in range(1, 40):
        if len(cases) >= 21:
            break
        r = random.Random(3722 + index * 7919)
        content = solvable_case(r) if index % 2 else random_case(r)
        if content not in cases:
            cases.append(content)
    # 边界：N 取上界、N=1（只有因子 1）
    for extra in (f"{NLIMIT} 4\n", "1 2\n", "1 3\n"):
        if extra not in cases:
            cases.append(extra)
    for c in cases:
        n, m = map(int, c.split())
        assert 1 <= n <= NLIMIT, "题面 N 不超过 1000000"
        assert 2 <= m <= MLIMIT
    answers = [solve_text(c).strip() for c in cases]
    assert sum(a == "-1" for a in answers) >= 5, "无解分支至少 5 组"
    assert sum(a != "-1" for a in answers) >= 8, "有解分支至少 8 组"
    assert len(set(answers)) >= 5, "答案不能塌缩成两三个值"
    assert len(set(cases)) >= 15, "去重后至少 15 组"
    return cases


def emit(cases, solve):
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for old in list(root.glob("*.in")) + list(root.glob("*.out")):
        old.unlink()
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve(content), encoding="utf-8")
    print(f"generated {len(cases)} cases")


def main():
    assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip(), "参考解法跑不出样例输出"
    cases = build_cases()
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"

    emit(cases, solve_text)


if __name__ == "__main__":
    main()
