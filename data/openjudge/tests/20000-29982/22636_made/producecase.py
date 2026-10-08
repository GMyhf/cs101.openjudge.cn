import random, subprocess, sys, tempfile
from pathlib import Path
# 原内嵌参考解（递归记忆化 DFS，未设递归上限）在 100x100 蛇形长路径上会 RecursionError，
# 改用按等级排序的迭代 DP；原写法保留在 samplecode.py 用于交叉核对。
REFERENCE_SOURCE = """import sys
data = sys.stdin.buffer.read().split()
r, c = int(data[0]), int(data[1])
a = list(map(int, data[2:2 + r * c]))
order = sorted(range(r * c), key=a.__getitem__)
dp = [1] * (r * c)
for p in order:
    i, j = divmod(p, c)
    v = a[p]; best = dp[p]
    if i > 0 and a[p - c] < v and dp[p - c] + 1 > best: best = dp[p - c] + 1
    if i < r - 1 and a[p + c] < v and dp[p + c] + 1 > best: best = dp[p + c] + 1
    if j > 0 and a[p - 1] < v and dp[p - 1] + 1 > best: best = dp[p - 1] + 1
    if j < c - 1 and a[p + 1] < v and dp[p + 1] + 1 > best: best = dp[p + 1] + 1
    dp[p] = best
print(max(dp))
"""
SAMPLE_IN = '5 5\n1 2 3 4 5\n16 17 18 19 6\n15 24 25 20 7\n14 23 22 21 8\n13 12 11 10 9\n'
SAMPLE_OUT = '25\n'

def valid(text):
    # 题面：第一行 r c（1<=r,c<=100）；接下来 r 行，每行 c 个 0..100000000 的整数
    if not text.endswith("\n"):
        return False
    rows = text[:-1].split("\n")
    def nums(line):
        toks = line.split(" ")
        for t in toks:
            if not t.isdigit() or not t.isascii() or (len(t) > 1 and t[0] == "0"):
                return None
        return [int(t) for t in toks]
    head = nums(rows[0])
    if head is None or len(head) != 2:
        return False
    r, c = head
    if not (1 <= r <= 100 and 1 <= c <= 100) or len(rows) != r + 1:
        return False
    for line in rows[1:]:
        v = nums(line)
        if v is None or len(v) != c or not all(0 <= x <= 100000000 for x in v):
            return False
    return True

def generate_case(r):
    m, n = r.randint(2, 10), r.randint(2, 10); return f"{m} {n}\n" + "\n".join(" ".join(str(r.randint(0, 100000000)) for _ in range(n)) for _ in range(m)) + "\n"

def fmt(g):
    return f"{len(g)} {len(g[0])}\n" + "\n".join(" ".join(map(str, row)) for row in g) + "\n"

def special_cases():
    r = random.Random(22636)
    out = []
    out.append(fmt([[100000000]]))                                    # 1x1，答案 1
    out.append(fmt([[i * 1000000 for i in range(100)]]))               # 1x100 严格递增，答案 100
    out.append(fmt([[(i % 2) * 7 + i] for i in range(100)]))           # 100x1 锯齿
    out.append(fmt([[r.randint(0, 100000000) for _ in range(100)] for _ in range(100)]))  # 满规模随机
    snake = [[0] * 100 for _ in range(100)]
    for i in range(100):
        for j in range(100):
            snake[i][j] = 100000000 - (i * 100 + (j if i % 2 == 0 else 99 - j)) * 10000
    out.append(fmt(snake))                                            # 满规模蛇形，答案 10000
    # 带隔墙的蛇形：偶数行是路径、奇数行是最高等级的墙（只在行尾/行首留一个通道），
    # 路径上每格只有唯一更低的邻居，递归 DFS 深度约 5000，卡未调大递归上限的写法
    wall = [[100000000] * 100 for _ in range(100)]
    k = 0
    for i in range(0, 100, 2):
        cols = range(100) if (i // 2) % 2 == 0 else range(99, -1, -1)
        for j in cols:
            wall[i][j] = 90000000 - k * 10000; k += 1
        if i + 1 < 100:
            j = 99 if (i // 2) % 2 == 0 else 0
            wall[i + 1][j] = 90000000 - k * 10000; k += 1
    out.append(fmt(wall))
    out.append(fmt([[5] * 100 for _ in range(100)]))                   # 满规模全相等，答案 1
    out.append(fmt([[r.randint(0, 2) for _ in range(100)] for _ in range(100)]))  # 大量相等等级
    return out

def main():
    root = Path(__file__).parent / "data"
    assert SAMPLE_IN == '5 5\n1 2 3 4 5\n16 17 18 19 6\n15 24 25 20 7\n14 23 22 21 8\n13 12 11 10 9\n'
    specials = special_cases()
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        seen = [SAMPLE_IN]
        cases = [SAMPLE_IN]
        for index in range(1, 20 - len(specials)):
            for attempt in range(100):
                content = generate_case(random.Random(22636 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError('insufficient diversity')
            seen.append(content); cases.append(content)
        cases += specials
        assert len(set(cases)) == len(cases) == 20
        for index, content in enumerate(cases):
            assert valid(content), index
            result = subprocess.run([sys.executable, handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            if index == 0: assert result.stdout == SAMPLE_OUT
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()
