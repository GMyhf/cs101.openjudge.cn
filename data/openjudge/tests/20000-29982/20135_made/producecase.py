import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/20135 statistics, Accepted solution 52789538.\n# Source: http://cs101.openjudge.cn/practice/solution/52789538/\n# Statistics: http://cs101.openjudge.cn/practice/20135/statistics/\n# License: not declared on submission page; no license inferred\nmove = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]\n\nm, n = map(int, input().split())\ns = [input() for i in range(m)]\nname = input()\n\ndef find(x, y, d, i):\n    if i == len(name):\n        print(x + 1, y + 1)\n        print(move[d][0], move[d][1])\n        return True\n    return name[i] == s[x + i*move[d][0]][y + i*move[d][1]] and find(x, y, d, i + 1)\n\n\nfor x in range(m):\n    for y in range(n):\n        if s[x][y] == name[0]:\n            for d in range(8):\n                if 0 <= x + move[d][0]*(len(name) - 1) < m and 0 <= y + move[d][1]*(len(name) - 1) < n:\n                    if find(x, y, d, 0):\n                        exit()\n'
SAMPLE='4 5\nsdadd\nerahh\nwDave\nqqqqe\ndave\n'
GENERATOR_NAME='g20135'
SAMPLE2='5 5\nddsfh\necilA\nalice\nshGfu\npOgvd\nAlice\n'
DIRS = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def matches(grid, name):
    m, n, L = len(grid), len(grid[0]), len(name)
    out = []
    for x in range(m):
        for y in range(n):
            if grid[x][y] != name[0]:
                continue
            for dx, dy in DIRS:
                ex, ey = x + dx * (L - 1), y + dy * (L - 1)
                if 0 <= ex < m and 0 <= ey < n and all(grid[x + i * dx][y + i * dy] == name[i] for i in range(L)):
                    out.append((x, y, dx, dy))
    return out


def valid(text):
    """题面：第一行 m n；接下来 m 行每行 n 个英文字母（区分大小写）；第 m+2 行为长度 >= 2 的姓名；
    纸条只能横向、纵向或斜 45° 摆放，且「题目保证对于每个数据点，答案是唯一的」。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    head = lines[0].split()
    if len(head) != 2 or not all(t.isdigit() for t in head):
        return False
    m, n = map(int, head)
    if m < 1 or n < 1 or len(lines) != m + 2:
        return False
    grid, name = lines[1:m + 1], lines[m + 1]
    if any(len(row) != n or any(ch not in LETTERS for ch in row) for row in grid):
        return False
    if len(name) < 2 or any(ch not in LETTERS for ch in name):
        return False
    return len(matches(grid, name)) == 1


def _swapcase_one(r, name):
    i = r.randrange(len(name))
    return name[:i] + name[i].swapcase() + name[i + 1:]


def g20135(r):
    kind = r.randrange(4)
    if kind == 0:
        m, n = r.randint(5, 12), r.randint(5, 12)
    elif kind == 1:
        m, n = r.randint(60, 100), r.randint(60, 100)
    elif kind == 2:                                  # 单行 / 单列 / 细长
        m, n = r.choice([(1, r.randint(2, 30)), (r.randint(2, 30), 1), (2, r.randint(5, 40)), (r.randint(5, 40), 2)])
    else:
        m, n = r.randint(2, 30), r.randint(2, 30)
    alpha = r.choice(['ab', 'abc', 'aAbB', 'eilacAE', LETTERS])
    while True:
        L = r.randint(2, max(2, min(max(m, n), 12)))
        name = ''.join(r.choice(alpha) for _ in range(L))
        if name == name[::-1]:
            continue
        cand = [(x, y, dx, dy) for x in range(m) for y in range(n) for dx, dy in DIRS
                if 0 <= x + dx * (L - 1) < m and 0 <= y + dy * (L - 1) < n]
        if cand:
            break
    grid = [[r.choice(alpha) for _ in range(n)] for _ in range(m)]
    # 诱饵：大小写差一位、只差最后一个字母的近似串
    for _ in range(r.randint(0, 6)):
        x, y, dx, dy = r.choice(cand)
        fake = _swapcase_one(r, name) if r.random() < .5 else name[:-1] + r.choice(LETTERS.replace(name[-1], ''))
        for i, ch in enumerate(fake):
            grid[x + i * dx][y + i * dy] = ch
    x, y, dx, dy = r.choice(cand)
    keep = {(x + i * dx, y + i * dy) for i in range(L)}
    for i, ch in enumerate(name):
        grid[x + i * dx][y + i * dy] = ch
    while True:
        extra = [mt for mt in matches(grid, name) if mt != (x, y, dx, dy)]
        if not extra:
            break
        ex, ey, edx, edy = r.choice(extra)
        cells = [(ex + i * edx, ey + i * edy) for i in range(L) if (ex + i * edx, ey + i * edy) not in keep]
        cx, cy = r.choice(cells)
        grid[cx][cy] = r.choice(LETTERS)
    return f"{m} {n}\n" + "\n".join("".join(row) for row in grid) + f"\n{name}\n"


def build_cases():
    cases = [SAMPLE, SAMPLE2]
    seed = 1
    while len(cases) < 40:
        text = g20135(random.Random(seed)); seed += 1
        if text not in cases:
            cases.append(text)
    return cases

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        src=Path(d)/'main.py'; src.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(src)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=build_cases()
    assert all(valid(c) for c in cases)
    for i,text in enumerate(cases):
        (data/f'{i}.in').write_text(text); (data/f'{i}.out').write_text(run(text))
if __name__=='__main__': main()
