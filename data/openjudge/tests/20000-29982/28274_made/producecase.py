"""28274 细胞计数 测试数据生成器。

题面：第一行 n m（1 <= n, m <= 400），接下来 n 行，每行恰好 m 个 '0'..'9' 字符。
第 0 组为样例；含 400x400 的多种形态（全连通、蛇形长路径卡递归、棋盘格大量细胞等）。
"""
import random
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEED = 28274


def valid(text):
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not re.fullmatch(r"[1-9][0-9]* [1-9][0-9]*", lines[0]):
        return False
    n, m = map(int, lines[0].split())
    if not (1 <= n <= 400 and 1 <= m <= 400) or len(lines) != n + 1:
        return False
    return all(re.fullmatch(r"[0-9]{%d}" % m, row) for row in lines[1:])


def fmt(g):
    return f"{len(g)} {len(g[0])}\n" + "\n".join("".join(row) for row in g) + "\n"


def rnd(r, n, m, p):
    """每格以概率 p 非零。"""
    return [[r.choice("123456789") if r.random() < p else "0" for _ in range(m)] for _ in range(n)]


def snake(r, n, m):
    g = [["0"] * m for _ in range(n)]
    for i in range(n):
        if i % 2 == 0:
            for j in range(m):
                g[i][j] = r.choice("123456789")
        else:
            g[i][m - 1 if (i // 2) % 2 == 0 else 0] = r.choice("123456789")
    return g


def maze(r, n):
    """随机迷宫（偶数坐标为房间，打通墙壁），整体一个细胞但路径曲折。"""
    g = [["0"] * n for _ in range(n)]
    g[0][0] = "3"
    st, seen = [(0, 0)], {(0, 0)}
    while st:
        x, y = st[-1]
        nb = [(x + dx, y + dy, dx, dy) for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2))
              if 0 <= x + dx < n and 0 <= y + dy < n and (x + dx, y + dy) not in seen]
        if not nb:
            st.pop()
            continue
        nx, ny, dx, dy = r.choice(nb)
        g[x + dx // 2][y + dy // 2] = r.choice("123456789")
        g[nx][ny] = r.choice("123456789")
        seen.add((nx, ny))
        st.append((nx, ny))
    return g


def build_cases():
    r = random.Random(SEED)
    cases = ["4 10\n0234500067\n1034560500\n2045600671\n0000000089\n"]
    cases.append(fmt([[r.choice("123456789") for _ in range(400)] for _ in range(400)]))  # 全非零，1 个细胞
    cases.append(fmt(snake(r, 400, 400)))                                              # 蛇形长路径
    cases.append(fmt([["5" if (i + j) % 2 == 0 else "0" for j in range(400)] for i in range(400)]))  # 棋盘格 80000 个
    cases.append(fmt([["0"] * 400 for _ in range(400)]))                               # 全零
    cases.append(fmt(rnd(r, 400, 400, 0.5)))
    cases.append(fmt(rnd(r, 400, 400, 0.6)))                                           # 接近渗流阈值
    cases.append(fmt(maze(r, 399)))
    cases += ["1 1\n0\n", "1 1\n9\n", "1 5\n10101\n", "5 1\n1\n0\n1\n1\n0\n"]
    cases.append(fmt(rnd(r, 1, 400, 0.7)))
    cases.append(fmt(rnd(r, 400, 1, 0.7)))
    cases.append("3 3\n102\n102\n333\n")
    for p in (0.1, 0.3, 0.45, 0.55, 0.7, 0.9):
        cases.append(fmt(rnd(r, r.randint(1, 40), r.randint(1, 40), p)))
    for p in (0.4, 0.6):
        cases.append(fmt(rnd(r, r.randint(100, 400), r.randint(100, 400), p)))
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
