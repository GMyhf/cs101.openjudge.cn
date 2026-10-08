# 28405 小明的刷题计划 数据生成器。
# 题面约束：1<=n<=1e5，1<=time[i]<10000，1<=m<=1000。
# 第 0 组为题面样例；答案由同目录 samplecode.py 计算。
import random
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SAMPLE = '4\n1\n2\n3\n3\n2\n'
NMAX, TMAX, MMAX = 100000, 9999, 1000


def valid(text):
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    try:
        if any(ln != ln.strip() or not ln for ln in lines):
            return False
        n = int(lines[0])
        if not 1 <= n <= NMAX or len(lines) != n + 2:
            return False
        for ln in lines[1:n + 1]:
            if not ln.isdigit() or not 1 <= int(ln) <= TMAX:
                return False
        if not lines[n + 1].isdigit():
            return False
        m = int(lines[n + 1])
        return 1 <= m <= MMAX
    except ValueError:
        return False


def fmt(a, m):
    return f"{len(a)}\n" + "\n".join(map(str, a)) + f"\n{m}\n"


def spikes(r, n, p=0.08):
    # 小值里夹着大值：大值后紧跟小值时，切天后丢掉首题耗时的写法会出错
    return [r.randint(9000, TMAX) if r.random() < p else r.randint(1, 50) for _ in range(n)]


def random_case(r, s):
    kind = s % 6
    n = r.choice([r.randint(2, 12), r.randint(2, 60), r.randint(50, 3000)])
    if kind == 0:
        a = [r.randint(1, TMAX) for _ in range(n)]
    elif kind == 1:
        a = spikes(r, n, r.choice([0.05, 0.2, 0.5]))
    elif kind == 2:
        a = sorted(r.randint(1, TMAX) for _ in range(n))
        if r.random() < 0.5:
            a.reverse()
    elif kind == 3:
        a = [TMAX if i % 2 == 0 else r.randint(1, 10) for i in range(n)]
    elif kind == 4:
        v = r.randint(1, TMAX)
        a = [v] * n
    else:
        a = [r.randint(1, 30) for _ in range(n)]
    hi = min(MMAX, n)
    m = r.choice([1, 2, r.randint(1, hi), r.randint(1, hi), max(1, n - 1), min(MMAX, n + r.randint(0, 5))])
    m = max(1, min(MMAX, m))
    return fmt(a, m)


def cases():
    r = random.Random(28405)
    out = [SAMPLE]
    out.append(fmt([r.randint(1, TMAX) for _ in range(NMAX)], MMAX))       # 满规模，m 最大
    out.append(fmt([TMAX] * NMAX, 1))                                     # 满规模，答案约 1e9
    out.append(fmt([r.randint(1, TMAX) for _ in range(NMAX)], 1))         # 满规模，m=1
    out.append(fmt(spikes(r, NMAX), MMAX))                                # 满规模，大小交错
    out.append(fmt([7], 1))                                               # n=1
    out.append(fmt([3, 9999, 1, 5, 2], 5))                                # n=m，答案 0
    out.append(fmt([r.randint(1, TMAX) for _ in range(MMAX)], MMAX))      # n=m=1000
    out.append(fmt([r.randint(1, TMAX) for _ in range(MMAX + 1)], MMAX))  # n=m+1
    out.append(fmt([9999, 1], 1))                                         # n=2,m=1
    out.append(fmt([5, 6, 7], MMAX))                                      # n<m
    out.append(fmt([1] * 10000, 7))                                       # 全 1
    out.append(fmt([7, 1, 718, 1], 2))                                    # 原参考解反例，答案 1
    out.append(fmt([1, 9999, 1, 9999, 1, 9999], 3))
    for s in range(27):
        out.append(random_case(r, s))
    return out


def run(text):
    x = subprocess.run([sys.executable, str(HERE / 'samplecode.py')], input=text,
                       text=True, capture_output=True, timeout=120)
    if x.returncode:
        raise SystemExit(x.stderr)
    return x.stdout


def main():
    d = HERE / 'data'
    d.mkdir(exist_ok=True)
    cs = cases()
    assert len(cs) == 41 and len(set(cs)) == len(cs)
    for i, c in enumerate(cs):
        assert valid(c), i
        (d / f'{i}.in').write_text(c)
        (d / f'{i}.out').write_text(run(c))


if __name__ == '__main__':
    main()
