"""28202 好串 测试数据生成器。

题面：1 <= T <= 10000；N 为 2 的幂且 1 <= N <= 131072；所有 N 之和 <= 200000；
S 只含小写字母且长度为 N。第 0 组为样例。
"""
import random
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEED = 28202
LET = "abcdefghijklmnopqrstuvwxyz"


def valid(text):
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not re.fullmatch(r"[1-9][0-9]*", lines[0]):
        return False
    t = int(lines[0])
    if not 1 <= t <= 10000 or len(lines) != 1 + 2 * t:
        return False
    total = 0
    for i in range(t):
        ns, s = lines[1 + 2 * i], lines[2 + 2 * i]
        if not re.fullmatch(r"[1-9][0-9]*", ns):
            return False
        n = int(ns)
        if not 1 <= n <= 131072 or n & (n - 1):
            return False
        if len(s) != n or any(c not in LET for c in s):
            return False
        total += n
    return total <= 200000


def good(r, n, c=0, noise=0.0):
    """随机构造一个 c-阶好串，再按 noise 比例随机改动。"""
    def build(n, c):
        if n == 1:
            return [LET[c]]
        h = n // 2
        if r.random() < 0.5:
            return [LET[c]] * h + build(h, c + 1)
        return build(h, c + 1) + [LET[c]] * h
    s = build(n, c)
    for i in range(n):
        if r.random() < noise:
            s[i] = r.choice(LET[:20])
    return "".join(s)


def rand_str(r, n, alpha=LET):
    return "".join(r.choice(alpha) for _ in range(n))


def fmt(items):
    rows = [str(len(items))]
    for s in items:
        rows += [str(len(s)), s]
    return "\n".join(rows) + "\n"


def build_cases():
    r = random.Random(SEED)
    cases = ["6\n8\nbbdcaaaa\n8\nasdfghjk\n8\nceaaaabb\n8\nbbaaddcc\n1\nz\n2\nac\n"]
    # 满规模：单串 N=131072 + 剩余配额
    cases.append(fmt([good(r, 131072, noise=0.3), rand_str(r, 65536), good(r, 2048, noise=0.1)] + [rand_str(r, 1024) for _ in range(1)]))
    cases.append(fmt([rand_str(r, 131072, "abcdefghijklmnopqr"), good(r, 65536)]))
    cases.append(fmt([good(r, 131072)]))                      # 已是好串，答案 0
    cases.append(fmt(["z" * 131072, "a" * 65536]))            # 全同字母
    # T=10000，大量小串（ΣN 尽量接近 200000）
    items = []
    rest = 200000
    for i in range(10000):
        left = 10000 - i - 1
        n = 1
        for cand in (32, 16, 8, 4, 2):
            if rest - cand >= left and r.random() < 0.6:
                n = cand
                break
        rest -= n
        items.append(good(r, n, noise=0.3) if r.random() < 0.5 else rand_str(r, n))
    cases.append(fmt(items))
    cases.append(fmt([rand_str(r, 1) for _ in range(10000)]))  # T=10000，N 全为 1
    cases.append("1\n1\na\n")
    cases.append("1\n1\nb\n")
    cases.append("1\n2\nba\n")
    cases.append("1\n4\naacb\n")
    cases.append("1\n4\nbcaa\n")
    cases.append(fmt([good(r, 1 << 17 >> k, noise=0.05) for k in range(1, 18)][:9]))
    # 两边代价相同、需要深层比较的串
    cases.append(fmt([good(r, n, noise=0.5) for n in (2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768)]))
    # 中小随机
    for _ in range(10):
        t = r.randint(1, 1000)
        items = []
        for _ in range(t):
            n = 1 << r.randint(0, 10)
            items.append(good(r, n, noise=r.random()) if r.random() < 0.6 else rand_str(r, n, LET[:r.randint(1, 26)]))
        while sum(map(len, items)) > 200000:
            items.pop()
        cases.append(fmt(items))
    return cases


def run(text):
    x = subprocess.run([sys.executable, str(HERE / "samplecode.py")], input=text,
                       text=True, capture_output=True, timeout=120)
    if x.returncode:
        raise SystemExit(x.stderr)
    return x.stdout


def main():
    d = HERE / "data"
    d.mkdir(exist_ok=True)
    for i, c in enumerate(build_cases()):
        assert valid(c), i
        (d / f"{i}.in").write_text(c)
        (d / f"{i}.out").write_text(run(c))


if __name__ == "__main__":
    main()
