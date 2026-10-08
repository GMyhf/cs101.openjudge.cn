import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'from collections import defaultdict\nn,m1,m2=map(int,input().split())\nd=defaultdict(int)\nl1,l2=[],[]\nfor i in range(m1):\n    l1.append(tuple(map(int,input().split())))\nfor i in range(m2):\n    l2.append(tuple(map(int,input().split())))\nfor i in range(m1):\n    for j in range(m2):\n        if l1[i][1]==l2[j][0]:\n            d[(l1[i][0],l2[j][1])]+=l1[i][2]*l2[j][2]\nfor i in range(n):\n    for j in range(n):\n        if d[(i,j)]:\n            print(i,j,d[(i,j)])\n'
SAMPLE_IN = '3 3 2\n0 0 1\n1 0 -1\n1 2 3\n0 0 7\n2 2 1\n'
def valid(text):
    """题面契约：首行 n m1 m2；随后 m1 行、m2 行三元组 (行号, 列号, 元素值)，行列号 0..n-1，
    元素值非 0（值为 0 不存储），同一矩阵内同一位置至多一个三元组。题面未给 n、m、值域上限。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    def ints(line, k):
        t = line.split(" ")
        if len(t) != k or any(not x.lstrip("-").isdigit() or x.startswith("--") for x in t):
            return None
        return [int(x) for x in t]
    h = ints(lines[0], 3)
    if h is None:
        return False
    n, m1, m2 = h
    if n < 1 or m1 < 0 or m2 < 0 or len(lines) != 1 + m1 + m2:
        return False
    for lo, hi in ((1, 1 + m1), (1 + m1, 1 + m1 + m2)):
        seen = set()
        for line in lines[lo:hi]:
            t = ints(line, 3)
            if t is None:
                return False
            a, b, v = t
            if not (0 <= a < n and 0 <= b < n) or v == 0 or (a, b) in seen:
                return False
            seen.add((a, b))
    return True


def generate_case(r):
    n = r.randint(2, 8); cells = [(i, j) for i in range(n) for j in range(n)]
    r.shuffle(cells); m1 = r.randint(1, min(12, len(cells))); xcells = cells[:m1]
    r.shuffle(cells); m2 = r.randint(1, min(12, len(cells))); ycells = cells[:m2]
    if not any(j == k for _, j in xcells for k, _ in ycells):
        xcells[0] = (xcells[0][0], ycells[0][0])
    xv = [(i, j, r.choice([x for x in range(-9, 10) if x])) for i, j in xcells]
    yv = [(i, j, r.choice([x for x in range(-9, 10) if x])) for i, j in ycells]
    assert len({(i, j) for i, j, _ in xv}) == m1 and len({(i, j) for i, j, _ in yv}) == m2
    assert all(v != 0 and 0 <= i < n and 0 <= j < n for i, j, v in xv + yv)
    return f"{n} {m1} {m2}\n" + "\n".join(f"{i} {j} {v}" for i, j, v in xv + yv) + "\n"


def generate_extra(r, kind):
    # 2026-10 补强：原 39 组 n 只在 2..8、非零元至多 12 个，从没有 n=1，抵消成 0 的项也只有 3 组。
    # 末 6 组换成：n=1；大量「乘积求和后恰好为 0」的位置（卡输出 0 元素的写法）；中等规模（题面未给上限，
    # 取 n=100、各约 1500 个非零元，O(m1*m2) 与 O(n^3) 稠密做法都能轻松通过）。
    if kind == "n1":
        n, xv, yv = 1, [(0, 0, r.choice([-7, 3, 9]))], [(0, 0, r.choice([-5, 2, 8]))]
    elif kind == "cancel":
        n = r.randint(3, 10); xv, yv = [], []
        # X 第 i 行在列 0、1 上取 a、b；Y 第 0、1 行在列 c 取 b、-a 等，使 (i,c) 抵消为 0
        a, b = r.randint(1, 9), r.randint(1, 9)
        for i in range(n):
            xv += [(i, 0, a), (i, 1, b)]
        for c in range(n):
            if c % 2 == 0:
                yv += [(0, c, b), (1, c, -a)]          # a*b + b*(-a) = 0
            else:
                yv += [(0, c, r.randint(1, 9))]
        r.shuffle(xv); r.shuffle(yv)
    else:
        n = 100; size = r.randint(1200, 1500)
        cells = [(i, j) for i in range(n) for j in range(n)]
        xv = [(i, j, r.choice([x for x in range(-1000, 1001) if x])) for i, j in r.sample(cells, size)]
        yv = [(i, j, r.choice([x for x in range(-1000, 1001) if x])) for i, j in r.sample(cells, size)]
    return f"{n} {len(xv)} {len(yv)}\n" + "\n".join(f"{i} {j} {v}" for i, j, v in xv + yv) + "\n"


EXTRA_KINDS = ["n1", "cancel", "cancel", "cancel", "medium", "medium"]


def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        first_extra = 40 - len(EXTRA_KINDS)     # 组数保持 40（catalog 显式列出了 0..39），末 6 组换成补强组
        for index in range(40):
            if index == 0: content = SAMPLE_IN
            elif index >= first_extra:
                content = generate_extra(random.Random(23555 * 7 + index), EXTRA_KINDS[index - first_extra])
                assert content not in seen
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(23555 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            assert valid(content), index
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            assert result.stdout.strip(), index       # 乘积非全零，避免「输出空」的歧义
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
