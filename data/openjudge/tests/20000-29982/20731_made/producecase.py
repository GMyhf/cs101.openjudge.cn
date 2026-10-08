import random, subprocess, sys, tempfile
from pathlib import Path
# 原内嵌的 AC 提交（52201327）在 x>y 时会跳过交换（如 x=3,y=1 / x=m,y=2），
# 原 40 组里有 8 组（4,7,11,13,16,20,21,24）答案因此是错的；改用直接交换再求和的写法。
REFERENCE = """m, n = map(int, input().split())
a = [list(map(int, input().split())) for _ in range(m)]
x, y = map(int, input().split())
a[x - 1], a[y - 1] = a[y - 1], a[x - 1]
print(sum(a[i][j] for i in range(m) for j in range(n)
          if i == 0 or i == m - 1 or j == 0 or j == n - 1))
"""
SAMPLE='3 3\n3 4 1\n3 7 1\n2 0 1\n1 2\n'
GENERATOR_NAME='g20731'
def g20731(r):
    m, n = r.randint(2, 8), r.randint(2, 8)
    rows = [[r.randint(-20, 20) for _ in range(n)] for _ in range(m)]
    x, y = r.sample(range(1, m + 1), 2)
    return f"{m} {n}\n" + "\n".join(" ".join(map(str, row)) for row in rows) + f"\n{x} {y}\n"

def valid(text):
    """题面：首行 m n（m<100, n<100，正整数，一个空格分隔）；接着 m 行、每行 n 个整数（单空格分隔）；
    最后一行两个整数 x y，表示交换第 x 行与第 y 行（必须落在 1..m）。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    def ints(line, k):
        parts = line.split(" ")
        if len(parts) != k:
            return None
        try:
            vals = [int(p) for p in parts]
        except ValueError:
            return None
        if any(p != str(v) for p, v in zip(parts, vals)):
            return None
        return vals
    head = ints(lines[0], 2)
    if head is None:
        return False
    m, n = head
    if not (1 <= m < 100 and 1 <= n < 100) or len(lines) != m + 2:
        return False
    if any(ints(lines[1 + i], n) is None for i in range(m)):
        return False
    xy = ints(lines[m + 1], 2)
    return xy is not None and all(1 <= v <= m for v in xy)


def matrix_case(m, n, x, y, r, lo=-20, hi=20):
    rows = [[r.randint(lo, hi) for _ in range(n)] for _ in range(m)]
    return f"{m} {n}\n" + "\n".join(" ".join(map(str, row)) for row in rows) + f"\n{x} {y}\n"


def extra_cases():
    """补充：满规模 99x99、首/末行与中间行交换（两种顺序）、首末行互换、x=y、m=2/n=2 等边界。"""
    r = random.Random(20731)
    out = []
    for m, n, x, y in [(99, 99, 1, 50), (99, 99, 99, 2), (99, 99, 50, 1), (99, 99, 2, 99),
                       (99, 99, 99, 1), (99, 99, 37, 61), (99, 2, 1, 98), (2, 99, 2, 1),
                       (2, 2, 1, 2), (3, 3, 3, 2), (5, 4, 4, 4), (7, 3, 1, 1), (6, 5, 6, 3)]:
        out.append(matrix_case(m, n, x, y, r, -1000, 1000))
    # 大值组：题面没给值域，元素取到 ±5e6，使 392 个边缘元素之和仍在 32 位有符号整数内（不额外要求 long long）
    out.append(matrix_case(99, 99, 98, 1, r, -5 * 10**6, 5 * 10**6))
    return out


def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+(['8\n','9\n'] if GENERATOR_NAME == 'g22007' else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1, 40)]+extra_cases()
    assert len(set(cases)) == len(cases)
    for i,c in enumerate(cases):
        assert valid(c), i
        (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
