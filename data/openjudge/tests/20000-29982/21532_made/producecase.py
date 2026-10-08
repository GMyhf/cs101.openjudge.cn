import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# 原外部参考（提交 52201278）从 6 逐个试到最小因子，N 为接近 1e9 的质数时要循环约 1e9 次，\n# 生成满规模数据会超时，改为 O(sqrt N) 枚举因子：答案 = N / (N 的不小于 6 的最小因子)。\nn = int(input())\nbest = n\ni = 1\nwhile i * i <= n:\n    if n % i == 0:\n        for d in (i, n // i):\n            if d >= 6 and d < best:\n                best = d\n    i += 1\nprint(n // best)\n'
SAMPLE='231\n'
GENERATOR_NAME='g21532'
def valid(text):
    """题面：输入一个正整数 N，6 <= N <= 10^9。"""
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    t = text[:-1]
    if not t.isdigit() or (len(t) > 1 and t[0] == "0"):
        return False
    return 6 <= int(t) <= 10 ** 9

def _is_prime(x):
    if x < 2:
        return False
    i = 2
    while i * i <= x:
        if x % i == 0:
            return False
        i += 1
    return True

def _prime_below(x):
    while not _is_prime(x):
        x -= 1
    return x

# 手工构造的边界与易错点：
#   6,7,8,9,10,11 -> 1；12 -> 2；最小 N、质数、2p/3p/4p/5p（答案 2..5）、
#   两个大质数之积、10^9 本身、接近 10^9 的大质数（卡 O(N) 逐个试除）。
_P1 = _prime_below(10 ** 9)            # 999999937
_P2 = _prime_below(10 ** 9 // 2)
_P3 = _prime_below(10 ** 9 // 3)
_P4 = _prime_below(10 ** 9 // 4)
_P5 = _prime_below(10 ** 9 // 5)
_Q = _prime_below(31622)               # 两个约 3e4 的质数之积，接近 1e9
_Q2 = _prime_below(_Q - 1)
FIXED = [6, 7, 8, 9, 10, 11, 12, 18, 25, 49, 10 ** 9, _P1, 2 * _P2, 3 * _P3, 4 * _P4, 5 * _P5,
         _Q * _Q2, _Q * _Q, _prime_below(_P1 - 1), 2 ** 29, 3 ** 18, 7 * 11 * 13 * 17 * 19 * 23 * 29,
         _prime_below(10 ** 6) * 997]

def g21532(r, s):
    k = s - 1
    if k < len(FIXED):
        return f"{FIXED[k]}\n"
    # 其余：随机三个互不相同正整数之和，规模覆盖到 10^9
    kind = s % 3
    if kind == 0:
        g = r.randint(1, 10 ** 9 // 6)
        a, b, c = r.sample(range(1, 10 ** 9 // g // 3 + 2), 3) if g < 10 ** 9 // 6 else (1, 2, 3)
        n = g * (a + b + c)
        if n > 10 ** 9:
            n = g * 6
    elif kind == 1:
        n = r.randint(10 ** 8, 10 ** 9)
    else:
        n = r.randint(6, 10 ** 9)
    return f"{n}\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+(['8\n','9\n'] if GENERATOR_NAME == 'g22007' else [])+[g21532(random.Random(s), s) for s in range(1, 40)]
    for i,c in enumerate(cases):
        assert valid(c), i
        (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
