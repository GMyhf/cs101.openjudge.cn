import random, subprocess, sys, tempfile
from pathlib import Path

REFERENCE = '# External reference: statistics page /practice/27932/\n# Accepted submission: 52723138\n# Source: http://cs101.openjudge.cn/practice/solution/52723138/\n# License: not declared on the submission page; no license is inferred.\n\nn, k = map(int, input().split())\na = list(map(int, input().split()))\na.sort()\nif k == 0:\n    print(1 if a[0] != 1 else -1)\nelif k == n:\n    print(a[-1])\nelse:\n    if a[k-1] == a[k]:\n        print(-1)\n    else:\n        print(a[k-1])'

SAMPLE = '7 4\n3 7 5 1 10 3 20\n'
SAMPLE2 = '7 2\n3 7 5 1 10 3 20\n'
MAXV = 10 ** 9


def _int(s):
    return s.isdigit() and (s == '0' or s[0] != '0')


def valid(text):
    """题面：1≤n≤2e5，0≤k≤n；第二行恰 n 个整数，1≤a_i≤1e9。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    if len(lines) != 2:
        return False
    h = lines[0].split(' ')
    if len(h) != 2 or not all(_int(t) for t in h):
        return False
    n, k = map(int, h)
    if not (1 <= n <= 2 * 10 ** 5 and 0 <= k <= n):
        return False
    a = lines[1].split(' ')
    if len(a) != n or not all(_int(t) for t in a):
        return False
    return all(1 <= int(t) <= MAXV for t in a)


def fmt(k, a):
    return f"{len(a)} {k}\n{' '.join(map(str, a))}\n"


def gap_case(r, n, k, lo, hi):
    """排序后第 k-1 与第 k 个不同，答案为 a[k-1]。"""
    mid = r.randint(lo + 1, hi - 1)
    a = [r.randint(lo, mid) for _ in range(k)] + [r.randint(mid + 1, hi) for _ in range(n - k)]
    r.shuffle(a)
    return fmt(k, a)


def tie_case(r, n, k, lo, hi):
    """排序后第 k-1 与第 k 个相同，答案 -1。"""
    v = r.randint(lo + 1, hi - 1)
    left = r.randint(1, k); right = r.randint(1, n - k)
    a = [v] * (left + right) + [r.randint(lo, v - 1) for _ in range(k - left)] + [r.randint(v + 1, hi) for _ in range(n - k - right)]
    r.shuffle(a)
    return fmt(k, a)


def rand_case(r, n, hi):
    k = r.randint(0, n)
    return fmt(k, [r.randint(1, hi) for _ in range(n)])


def build_cases():
    r = random.Random(27932)
    N = 2 * 10 ** 5
    cases = [SAMPLE, SAMPLE2]
    # 满规模（数值压小以保证单组 .in ≤ 1MB），卡 O(n^2)
    cases.append(gap_case(r, N, N // 2, 1, 3000))
    cases.append(tie_case(r, N, N // 2 + 7, 1, 3000))
    a = [r.randint(1, 999) for _ in range(N - 1)] + [MAXV]; r.shuffle(a)
    cases.append(fmt(N, a))                                   # k=n，答案 1e9
    cases.append(fmt(0, [r.randint(2, 999) for _ in range(N)]))  # k=0，答案 1
    a = [r.randint(1, 999) for _ in range(N - 1)] + [1]; r.shuffle(a)
    cases.append(fmt(0, a))                                   # k=0 且含 1，答案 -1
    # 大数值、接近 1MB
    cases.append(gap_case(r, 80000, 33333, 1, MAXV))
    cases.append(rand_case(r, 80000, MAXV))
    # 边界
    cases += [fmt(0, [1]), fmt(0, [5]), fmt(1, [MAXV]), fmt(1, [1]), fmt(0, [MAXV]),
              fmt(0, [1, 1, 1]), fmt(3, [4, 4, 4]), fmt(2, [4, 4, 4]), fmt(1, [2, 1]),
              fmt(1, [1, 2]), fmt(2, [MAXV, MAXV - 1]), fmt(1, [MAXV, MAXV]),
              fmt(3, [9, 1, 10, 9, 2]),          # a[k-1]+1==a[k] 之外的普通情形
              fmt(2, [6, 5, 7, 8]),              # a[k-1]+1==a[k]
              fmt(0, [2, 3, 4]),                 # k=0，最小值 2，答案 1（a[0]-1 恰也等于 1）
              fmt(0, [100, 200])]                # k=0，答案 1（不是 a[0]-1）
    # 随机：中小规模，混合重复多/重复少
    while len(cases) < 41:
        t = len(cases) % 4
        n = r.randint(2, 10000)
        if t == 0:
            cases.append(rand_case(r, n, 50))
        elif t == 1:
            cases.append(rand_case(r, n, MAXV))
        elif t == 2:
            cases.append(gap_case(r, n, r.randint(1, n - 1), 1, r.choice([100, 10 ** 5, MAXV])))
        else:
            cases.append(tie_case(r, n, r.randint(1, n - 1), 1, r.choice([100, 10 ** 5, MAXV])))
    return cases


def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p = Path(d) / 'main.py'; p.write_text(REFERENCE)
        x = subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=90)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout


def main():
    d = Path('data'); d.mkdir(exist_ok=True)
    cases = build_cases()
    assert len(cases) == len(set(cases)), '组间有重复'
    for i, c in enumerate(cases):
        assert valid(c), f'第 {i} 组不合题面'
        (d / f'{i}.in').write_text(c); (d / f'{i}.out').write_text(run(c))


if __name__ == '__main__':
    main()
