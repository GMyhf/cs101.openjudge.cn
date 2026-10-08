import random, subprocess, sys, tempfile
from pathlib import Path
def g1061(r):
    # The collected reference divides by (a*i)%L.  A prime circumference and
    # non-zero speed difference keep that expression non-zero for i=1..L-1.
    L = r.choice([101, 211, 307, 401, 503, 601, 701, 809, 907, 1009, 2003, 3001, 4001])
    x = r.randrange(L); y = r.randrange(L)
    while y == x: y = r.randrange(L)
    m = r.randrange(1, L); n = r.randrange(1, L)
    while n == m: n = r.randrange(1, L)
    return f"{x} {y} {m} {n} {L}\n"

REFERENCE='# 参考解：原先引用的 2020fall 代码在 L 不是 a 的倍数时逐个试 i=1..L-1，L 接近 2.1e9 时必然超时，\n# 而且 i*(b//c) 不保证最小；旧生成器只用不超过 4001 的素数 L 并且永不出现 Impossible。\n# 这里改成扩展欧几里得：t*(m-n) ≡ y-x (mod L)，求最小正整数 t。\nfrom math import gcd\nx, y, m, n, L = map(int, input().split())\na = (m - n) % L\nb = (y - x) % L\ng = gcd(a, L)\nif b % g:\n    print("Impossible")\nelse:\n    M = L // g\n    print((b // g) * pow(a // g, -1, M) % M)\n'
SAMPLE='1 2 3 4 5\n'
GENERATOR='g1061'

def valid(text):
    """题面：一行 5 个整数 x y m n L，x≠y < 2000000000，0 < m、n < 2000000000，0 < L < 2100000000。"""
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    toks = text.split()
    if len(toks) != 5:
        return False
    try:
        x, y, m, n, L = map(int, toks)
    except ValueError:
        return False
    if any(str(int(t)) != t for t in toks):
        return False
    return (x != y and x < 2_000_000_000 and y < 2_000_000_000 and 0 < m < 2_000_000_000
            and 0 < n < 2_000_000_000 and 0 < L < 2_100_000_000)

def g1061_new(seed):
    """另行约定 0 ≤ x, y 且 x mod L ≠ y mod L：x ≡ y (mod L) 时「跳 0 次」与「跳 L/g 次」两种写法都常见，题面没说清，不出这类数据。"""
    r = random.Random(1061_000 + seed)
    MX, ML = 1_999_999_999, 2_099_999_999
    def make(L, a_mode, impossible):
        for _ in range(10000):
            x = r.randrange(0, MX + 1) if seed > 12 and r.random() < 0.5 else r.randrange(L)
            y = r.randrange(0, MX + 1) if seed > 12 and r.random() < 0.5 else r.randrange(L)
            if x == y or x % L == y % L:
                continue
            if a_mode == "equal":
                m = r.randint(1, min(MX, max(1, L * 3))) if seed <= 12 else r.randint(1, MX); n = m
            else:
                m = r.randint(1, MX if seed > 12 else 3 * L); n = r.randint(1, MX if seed > 12 else 3 * L)
            if m > MX or n > MX:
                continue
            from math import gcd
            g = gcd((m - n) % L, L)
            if ((y - x) % L) % g == 0 and not impossible:
                return f"{x} {y} {m} {n} {L}\n"
            if ((y - x) % L) % g != 0 and impossible:
                return f"{x} {y} {m} {n} {L}\n"
        raise RuntimeError(seed)
    if seed <= 12:      # 小 L，可暴力核对
        L = r.randint(2, 60)
        return make(L, "equal" if seed == 3 else "rand", seed % 3 == 0)
    if seed == 13:
        return f"0 1999999999 1999999999 1 2099999999\n"
    if seed == 14:
        return f"1999999999 0 1 1999999999 2099999999\n"
    if seed == 15:
        return f"0 1 1 2 2099999999\n"          # 答案 2099999998
    if seed == 16:
        return f"1 0 2 1 2\n"
    if seed == 17:
        return make(2_000_000_000, "rand", False)   # L 偶数、gcd 大
    if seed == 18:
        return make(2 ** 30, "rand", True)
    if seed == 19:
        return make(2_099_999_999, "equal", True)   # m == n
    if seed <= 26:      # L 为大素数，几乎总能碰面，答案量级接近 L
        L = r.choice([2_099_999_999, 1_999_999_973, 1_000_000_007])
        return make(L, "rand", False)
    if seed <= 32:
        L = r.randint(10 ** 9, ML)
        return make(L, "rand", seed % 2 == 0)
    L = r.randint(2, ML)
    return make(L, "rand", seed % 3 == 0)

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as folder:
        script=Path(folder)/"main.py"; script.write_text(REFERENCE)
        result=subprocess.run([sys.executable,"-I",str(script)],input=text,text=True,capture_output=True,timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    for old in data.glob("*"): old.unlink()
    cases=[SAMPLE]+[g1061_new(seed) for seed in range(1, 40)]
    for i,case in enumerate(cases):
        (data/f"{i}.in").write_text(case); (data/f"{i}.out").write_text(run(case))
if __name__=="__main__": main()
