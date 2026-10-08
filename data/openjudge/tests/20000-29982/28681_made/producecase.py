# 28681 奖学金 数据生成器（pctbook E28681 与 practice 28681 共用，两份题面相同）。
# 题面约束：n<=300（要输出前 5 名，取 n>=5）；每科成绩 0..100；输出的总分为正整数。
# 第 0 组为题面样例 1，第 1 组为题面样例 2；答案由同目录 samplecode.py 计算。
import random
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SAMPLE = '6\n90 67 80\n87 66 91\n78 89 91\n88 99 77\n67 89 64\n78 89 98\n'
SAMPLE2 = '8\n80 89 89\n88 98 78\n90 67 80\n87 66 91\n78 89 91\n88 99 77\n67 89 64\n78 89 98\n'
NMAX = 300


def valid(text):
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    try:
        if not lines[0].isdigit():
            return False
        n = int(lines[0])
        if not 5 <= n <= NMAX or len(lines) != n + 1:
            return False
        st = []
        for i, ln in enumerate(lines[1:], 1):
            p = ln.split(' ')
            if len(p) != 3 or any(not x.isdigit() or x != str(int(x)) or int(x) > 100 for x in p):
                return False
            a = list(map(int, p))
            st.append((-sum(a), -a[0], i))
        st.sort()
        return all(-t[0] > 0 for t in st[:5])
    except ValueError:
        return False


def fmt(rows):
    return f"{len(rows)}\n" + "\n".join(f"{a} {b} {c}" for a, b, c in rows) + "\n"


def tie_rows(r, n, total, k):
    # k 个总分为 total 的学生，语文成绩各不相同或部分相同
    res = []
    for _ in range(k):
        while True:
            a = r.randint(max(0, total - 200), min(100, total))
            b = r.randint(max(0, total - a - 100), min(100, total - a))
            c = total - a - b
            if 0 <= c <= 100:
                res.append((a, b, c))
                break
    return res


def gen(r, kind):
    n = r.choice([5, 6, r.randint(5, 20), r.randint(20, 300), 300])
    if kind == 0:     # 普通随机
        rows = [(r.randint(0, 100), r.randint(0, 100), r.randint(0, 100)) for _ in range(n)]
    elif kind == 1:   # 成绩集中，总分大量并列
        lo = r.randint(60, 95)
        rows = [(r.randint(lo, lo + 5), r.randint(lo, lo + 5), r.randint(lo, lo + 5)) for _ in range(n)]
    elif kind == 2:   # 前几名总分相同、语文区分；且分散插入
        rows = [(r.randint(0, 80), r.randint(0, 80), r.randint(0, 80)) for _ in range(n)]
        top = tie_rows(r, n, r.randint(250, 290), r.randint(2, 7))
        for t in top:
            rows[r.randrange(n)] = t
    else:             # 总分与语文都相同，只能靠学号
        rows = [(r.randint(0, 70), r.randint(0, 70), r.randint(0, 70)) for _ in range(n)]
        a = r.randint(80, 100)
        tot = r.randint(a + 100, a + 190)
        k = r.randint(2, 7)
        for _ in range(k):
            b = r.randint(max(0, tot - a - 100), min(100, tot - a))
            rows[r.randrange(n)] = (a, b, tot - a - b)
    return fmt(rows)


def cases():
    r = random.Random(28681)
    out = [SAMPLE, SAMPLE2]
    out.append(fmt([(100, 100, 100)] * NMAX))                                   # 全满分，按学号
    out.append(fmt([(0, 0, 0)] * (NMAX - 5) + [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1), (0, 0, 2)]))
    out.append(fmt([(r.randint(0, 100), r.randint(0, 100), r.randint(0, 100)) for _ in range(5)]))  # n=5
    out.append(fmt([(50, 50, 50)] * 6))                                          # n=6 全相同
    out.append(fmt([(r.randint(0, 60),) * 3 for _ in range(NMAX - 1)] + [(100, 100, 100)]))      # 第一名在最后
    # 总分并列：语文高者在前；同语文时学号小在前（学号大的语文更高，卡只按学号的写法）
    out.append(fmt([(60, 100, 100), (70, 90, 100), (80, 80, 100), (90, 70, 100), (100, 60, 100), (100, 100, 60)]))
    out.append(fmt([(80, 100, 100), (80, 100, 100), (80, 99, 101 - 100 + 99), (80, 100, 100), (80, 100, 100),
                    (80, 100, 100), (100, 80, 100)]))
    out.append(fmt([(r.randint(0, 100), 0, 0) for _ in range(NMAX)]))            # 只有语文有分
    out.append(fmt([(0, r.randint(0, 100), r.randint(0, 100)) for _ in range(NMAX)]))  # 语文全 0
    for s in range(30):
        out.append(gen(r, s % 4))
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
    assert len(cs) == 41 and len(set(cs)) == len(cs), len(cs)
    for i, c in enumerate(cs):
        assert valid(c), i
        (d / f'{i}.in').write_text(c)
        (d / f'{i}.out').write_text(run(c))


if __name__ == '__main__':
    main()
