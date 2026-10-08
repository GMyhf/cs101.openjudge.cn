"""04143 和为给定数 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 40 组数据。

2026-10-07 审计重写：
- 原生成器 n 只有 4..30、数值 < 500 且两两互异，m 恒取 min+max —— 40 组答案全是
  「有解」，从没出现过 No，也没有重复值，离 n<=100000、值域 10^8 很远，O(n^2) 也能过。
- 原参考解（取自一份 AC 提交）的 `while b[left]+b[right]>c: right-=1` 不检查 right>=left，
  会让同一个元素和自己配对（如 `2\\n1 3\\n2` 输出 `1 1`），全部元素都大于 m 时下标
  走成负数后越界崩溃。改用按值计数的写法：从小到大枚举较小数 x，y=m-x，
  x<y 要求 y 存在，x==y 要求 x 至少出现两次，第一个命中即为答案。
- 新数据：有解/无解、x==y 需两份相同值、多对可选（考「较小数更小」）、
  全部元素大于 m（右指针越界）、m=0、m 远超 2*10^8、n=1、满规模 n=100000 等。
"""
import random, subprocess, sys, tempfile
from collections import Counter
from pathlib import Path

SAMPLE = '4\n2 5 1 4\n6\n'
SAMPLE_OUT = '1 5\n'
MAXN = 100000
MAXV = 10 ** 8
MAXM = 2 ** 30

REFERENCE = (
    "import sys\n"
    "from collections import Counter\n"
    "d = sys.stdin.read().split()\n"
    "n = int(d[0]); a = list(map(int, d[1:1 + n])); m = int(d[1 + n])\n"
    "c = Counter(a)\n"
    "ans = 'No'\n"
    "for x in sorted(c):\n"
    "    y = m - x\n"
    "    if y < x:\n"
    "        break\n"
    "    if (y > x and y in c) or (y == x and c[x] >= 2):\n"
    "        ans = f'{x} {y}'\n"
    "        break\n"
    "print(ans)\n"
)


def valid(text):
    """题面：共三行；第一行 n (0<n<=100000)；第二行 n 个整数，范围 0..10^8；
    第三行 m (0<=m<=2^30)。整数间单个空格。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 3:
        return False

    def num(t, lo, hi):
        if not t.isdigit() or (t != "0" and t[0] == "0"):
            return None
        v = int(t)
        return v if lo <= v <= hi else None

    n = num(lines[0], 1, MAXN)
    if n is None:
        return False
    tok = lines[1].split(" ")
    if len(tok) != n or any(num(t, 0, MAXV) is None for t in tok):
        return False
    return num(lines[2], 0, MAXM) is not None


def fmt(a, m):
    return f"{len(a)}\n{' '.join(map(str, a))}\n{m}\n"


def no_pair(r, n, hi):
    """造无解组：随机取数，凡是能和已取的数凑成 m 的、或自身两倍等于 m 的都丢掉。
    相同值可以重复出现（x+x != m，安全）。"""
    m = r.randint(hi // 2, hi)
    out, used = [], set()
    while len(out) < n:
        x = r.randint(0, min(m, MAXV))
        if 2 * x == m or (m - x) in used:
            continue
        out.append(x)
        used.add(x)
    return out, m


def g_small_yes(r):
    n = r.randint(2, 30)
    a = [r.randint(0, 60) for _ in range(n)]
    i, j = r.sample(range(n), 2)
    return fmt(a, a[i] + a[j])


def g_small_no(r):
    n = r.randint(1, 30)
    a, m = no_pair(r, n, 120)
    return fmt(a, m)


def g_twin(r, n, hi):
    """答案是 x+x：x 恰好出现两次，其余数都大于 x（任两数之和都大于 m）。"""
    x = r.randint(1, hi // 2)
    m = 2 * x
    a = [x, x]
    while len(a) < n:
        v = r.randint(x + 1, min(MAXV, m + hi))   # > x，任何两数之和 > m
        a.append(v)
    r.shuffle(a)
    return fmt(a, m)


def g_single_twin(r, n, hi):
    """x 只出现一次而 m=2x：不能自己配自己，答案是另一对（或 No）。"""
    x = r.randint(hi // 4, hi // 2 - 1)
    m = 2 * x
    lo_pair = r.randint(0, x - 1)
    a = [x, lo_pair, m - lo_pair]
    while len(a) < n:
        v = r.randint(m + 1, min(MAXV, m + hi))
        a.append(v)
    r.shuffle(a)
    return fmt(a, m)


def g_many_pairs(r, n, hi):
    """很多对和为 m，答案取较小数最小的那对。"""
    m = r.randint(hi // 2, min(hi, 2 * MAXV))
    a = []
    while len(a) < n:
        x = r.randint(max(0, m - MAXV), m // 2)
        a.append(x)
        if len(a) < n and r.random() < 0.3:
            a.append(m - x)
    r.shuffle(a)
    return fmt(a[:n], m)


def g_all_big(r, n):
    """所有数都大于 m：双指针右端一路左移会越界。"""
    m = r.randint(0, 1000)
    a = [r.randint(m + 1, MAXV) for _ in range(n)]
    return fmt(a, m)


def g_random(r, n, hi, m=None):
    a = [r.randint(0, hi) for _ in range(n)]
    if m is None:
        m = r.randint(0, min(MAXM, 2 * hi))
    return fmt(a, m)


def g_big_no(r, n):
    """满规模无解：全取偶数，m 取奇数。"""
    a = [2 * r.randint(0, MAXV // 2) for _ in range(n)]
    m = 2 * r.randint(0, MAXV) + 1
    return fmt(a, m)


def g_big_yes_late(r, n):
    """满规模、唯一一对且较小数很大：逐个试的 O(n^2) 必超时。"""
    m = MAXV + 2 * r.randint(0, MAXV // 4) + 1        # m 为奇数
    x = 2 * r.randint(m // 4 - 1000, m // 4 - 1)      # x 为偶数、离 m/2 很近，m-x 为奇数
    a = [x, m - x]
    # 其余全为偶数：偶+偶≠奇；偶+(m-x)=m 只能是偶=x，仍是同一对
    while len(a) < n:
        a.append(2 * r.randint(0, MAXV // 2))
    r.shuffle(a)
    return fmt(a, m)


def build_cases():
    cases = [SAMPLE]
    R = random.Random
    # 1..12：小规模
    for s in range(1, 7):
        cases.append(g_small_yes(R(s)))
    for s in range(7, 13):
        cases.append(g_small_no(R(s)))
    # 13..20：边界小组
    cases.append("1\n5\n10\n")                 # n=1，只有一个 5，5+5 不算
    cases.append("1\n0\n0\n")                  # n=1，m=0
    cases.append("2\n0 0\n0\n")                # m=0，两个 0
    cases.append("2\n1 3\n2\n")                # 原参考解会输出 1 1
    cases.append("3\n7 8 9\n3\n")              # 全部大于 m
    cases.append("2\n100000000 100000000\n200000000\n")  # 值域上界、x==y
    cases.append(f"2\n0 100000000\n{MAXM}\n")  # m 取上界 2^30，无解
    cases.append("4\n3 3 3 3\n6\n")            # 全相同
    # 21..28：中规模
    cases.append(g_twin(R(21), 1000, 10 ** 6))
    cases.append(g_single_twin(R(22), 1000, 10 ** 6))
    cases.append(g_many_pairs(R(23), 1000, 10 ** 6))
    cases.append(g_all_big(R(24), 1000))
    cases.append(g_random(R(25), 5000, 10 ** 5))
    cases.append(fmt(*no_pair(R(26), 5000, 10 ** 7)))
    cases.append(g_random(R(27), 5000, 100, 150))   # 大量重复值
    cases.append(g_single_twin(R(28), 5000, 10 ** 7))
    # 29..39：满规模 n=100000
    cases.append(g_big_no(R(29), MAXN))
    cases.append(g_big_yes_late(R(30), MAXN))
    cases.append(g_twin(R(31), MAXN, MAXV))
    cases.append(g_single_twin(R(32), MAXN, MAXV))
    cases.append(g_many_pairs(R(33), MAXN, 2 * MAXV))
    cases.append(g_all_big(R(34), MAXN))
    cases.append(g_random(R(35), MAXN, MAXV))
    cases.append(g_random(R(36), MAXN, MAXV, MAXM))  # m=2^30 远超 2*10^8
    cases.append(fmt(*no_pair(R(37), MAXN, 2 * MAXV)))
    cases.append(g_random(R(38), MAXN, 1000, 1999))  # 大量重复值
    cases.append(fmt(list(range(MAXN, 0, -1)), 2 * MAXN - 1))  # 倒序、唯一一对是两端最大
    return cases


def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p = Path(d) / "main.py"
        p.write_text(REFERENCE, encoding="utf-8")
        x = subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=30)
        if x.returncode:
            raise SystemExit(x.stderr)
        return x.stdout


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE, "第 0 组必须是题面样例"
    assert run(SAMPLE).split() == SAMPLE_OUT.split(), "参考解法跑不出样例输出"
    assert len(set(cases)) == len(cases), "组间不得重复"
    data = Path(__file__).parent / "data"
    data.mkdir(exist_ok=True)
    for i, text in enumerate(cases):
        assert valid(text), f"第 {i} 组越出题面约束"
        (data / f"{i}.in").write_text(text, encoding="utf-8")
        (data / f"{i}.out").write_text(run(text), encoding="utf-8")


if __name__ == "__main__":
    main()
