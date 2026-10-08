# 26273 字符串的周期：输出所有周期长度（升序）。
# 输入仅一行，小写字母 a-z，1<=n<=10^6。
import random
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAXN = 1000000
SAMPLE = 'abcabca\n'
LOWER = 'abcdefghijklmnopqrstuvwxyz'


def valid(text):
    if not text.endswith('\n'):
        return False
    body = text[:-1]
    if '\n' in body:
        return False
    if not (1 <= len(body) <= MAXN):
        return False
    return all('a' <= c <= 'z' for c in body)


def rs(r, n, alpha):
    return ''.join(r.choice(alpha) for _ in range(n))


def periodic(unit, n):
    return (unit * (n // len(unit) + 1))[:n]


def fib_word(n):
    a, b = 'a', 'ab'
    while len(b) < n:
        a, b = b, b + a
    return b[:n]


def build_cases():
    r = random.Random(26273)
    cases = [SAMPLE]
    # 满规模 / 卡复杂度（输出控制在 2MB 内）
    cases.append('a' * (MAXN - 1) + 'b' + '\n')           # 只有周期 n，朴素逐个 p 比较为 O(n^2)
    cases.append(periodic('abcdefg', MAXN) + '\n')         # 约 14 万个周期
    cases.append('a' * 200000 + '\n')                       # 每个 p 都是周期
    cases.append(fib_word(MAXN) + '\n')                     # 斐波那契串，周期为斐波那契数
    # 边界
    for s in ['a', 'z', 'ab', 'aa', 'aba', 'abab', 'aab', 'abcab', 'zzzzzy', 'abacaba', 'aabaabaa']:
        cases.append(s + '\n')
    cases.append(rs(r, 20, LOWER) + '\n')
    cases.append(periodic('ab', 9999) + '\n')
    cases.append(fib_word(5000) + '\n')
    # 随机：周期串 / 周期串中改一个字符 / 嵌套周期 / 纯随机
    for i in range(24):
        n = r.randint(1, [60, 3000, 50000][i % 3])
        alpha = ['ab', 'abc', LOWER][(i // 3) % 3]
        kind = i // 6                     # 0 周期 / 1 扰动 / 2 嵌套 / 3 纯随机，各 6 组
        if kind == 0:
            s = periodic(rs(r, r.randint(1, 30), alpha), n)
        elif kind == 1:
            s = list(periodic(rs(r, r.randint(1, 30), alpha), n))
            p = r.randrange(n)
            s[p] = r.choice(LOWER)
            s = ''.join(s)
        elif kind == 2:
            u = rs(r, r.randint(1, 4), alpha)
            u = periodic(u, r.randint(len(u), 3 * len(u) + 2))
            u = periodic(u, r.randint(len(u), 4 * len(u) + 3))
            s = periodic(u, n)
        else:
            s = rs(r, n, alpha)
        cases.append(s + '\n')
    return cases


def run_ref(text):
    x = subprocess.run([sys.executable, str(HERE / 'samplecode.py')], input=text,
                       text=True, capture_output=True, timeout=120)
    if x.returncode:
        raise SystemExit(x.stderr)
    return x.stdout


def main():
    cases = build_cases()
    assert len(set(cases)) == len(cases), '存在重复组'
    d = HERE / 'data'
    d.mkdir(exist_ok=True)
    for i, c in enumerate(cases):
        assert valid(c), f'第 {i} 组不合法'
        (d / f'{i}.in').write_text(c)
        (d / f'{i}.out').write_text(run_ref(c))


if __name__ == '__main__':
    main()
