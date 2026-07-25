"""4138 测试数据生成器：S 在题面全域 [4, 10000] 内均匀取样，重跑可逐字节复现 data/。

出处：build_001a —— 2026-07-25 回归扫描修正。
原生成器是 `p, q = choice([3..31]), choice([3..31])`，于是 S 最大只有 62，
题面却是「不大于 10000 的正整数 S」：20 组去重后只剩 13 组，全部 <=62，
上界一带完全没数据。现改为先枚举出 [4,10000] 内**全部**「能写成两个质数之和」
的 S，再等距取样，并强制带上最小的 4(=2+2)、最大的合法值和几个奇数 S(=2+p)。

题面保证 S 是两个质数之和 -> 生成器用筛法逐个验证（valid 集合本身就是这么建的），
断言每组输入都在 valid 里。"""

from pathlib import Path

SAMPLE_IN = '50\n'
SAMPLE_OUT = '589\n'
LIMIT = 10000


def sieve(n):
    flag = [True] * (n + 1)
    flag[0] = flag[1] = False
    for i in range(2, int(n ** .5) + 1):
        if flag[i]:
            for j in range(i * i, n + 1, i):
                flag[j] = False
    return flag


def solve_text(text):
    s = int(text.split()[0])
    prime = sieve(max(s, 2))
    ans = max((p * (s - p) for p in range(2, s) if prime[p] and prime[s - p]), default=0)
    return str(ans) + "\n"


def build_cases():
    prime = sieve(LIMIT)
    primes = [i for i, ok in enumerate(prime) if ok]
    valid = sorted({p + q for p in primes for q in primes if p + q <= LIMIT})
    # 奇数 S 只可能是 2+奇质数，单独挑几个，避免样本全是偶数
    odds = [s for s in valid if s % 2][:400]
    picks = [valid[0], valid[-1], odds[0], odds[len(odds) // 2], odds[-1]]
    picks += [valid[round(i * (len(valid) - 1) / 15)] for i in range(16)]
    picks = sorted(set(picks))
    cases = [SAMPLE_IN] + [f"{s}\n" for s in picks if f"{s}\n" != SAMPLE_IN]
    assert all(int(c) in set(valid) for c in cases), "题面保证 S 是两个质数之和"
    assert min(int(c) for c in cases) == 4, "最小的合法 S 是 4=2+2，要有数据"
    assert max(int(c) for c in cases) == valid[-1], "上界一带要有数据"
    assert any(int(c) % 2 for c in cases), "奇数 S(=2+p) 也要有数据"
    assert len(set(cases)) >= 15, "去重后至少 15 组"
    return cases


def main():
    assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip(), "参考解法跑不出样例输出"
    cases = build_cases()
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for old in list(root.glob("*.in")) + list(root.glob("*.out")):
        old.unlink()
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
    print(f"generated {len(cases)} cases for 04138")


if __name__ == "__main__":
    main()
