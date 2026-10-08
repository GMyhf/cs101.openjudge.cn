import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: statistics page /practice/21462/\n# Accepted submission: 52213098\n# Source: http://cs101.openjudge.cn/practice/solution/52213098/\n# License: not declared on the submission page; no license is inferred.\n\nn=int(input())\nmatrix=[]\nfor i in range(n):\n    matrix.append(list(map(int,input().split())))\ndirections=[(1,0),(0,1),(-1,0),(0,-1)]\nx,y=0,0\nans=''\nd=0\ndx,dy=1,0\nvisited=set()\nwhile matrix[x][y]!=0:\n    ans+=chr(matrix[x][y])\n    visited.add((x,y))\n    nx,ny=x+dx,y+dy\n    if (not 0<=nx<n) or (not 0<=ny<n) or (nx,ny) in visited:\n        d=(d+1)%4\n        dx,dy=directions[d]\n        x,y=x+dx,y+dy\n    else:\n        x,y=nx,ny\nprint(ans)"
SAMPLE='3\n104 101 109\n97 0 111\n110 100 115\n'
GENERATOR_NAME='g21462'


def spiral(n):
    """逆时针螺旋顺序：从 (0,0) 起先向下，再向右、向上、向左。"""
    seen = [[False] * n for _ in range(n)]
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    x = y = d = 0
    order = []
    for _ in range(n * n):
        order.append((x, y)); seen[x][y] = True
        nx, ny = x + dirs[d][0], y + dirs[d][1]
        if not (0 <= nx < n and 0 <= ny < n) or seen[nx][ny]:
            d = (d + 1) % 4
            nx, ny = x + dirs[d][0], y + dirs[d][1]
        x, y = nx, ny
    return order


def valid(text):
    """题面：第一行 n（n<=100），接下来 n 行每行 n 个整数（字符 ASCII 码，无字符处为 0）；
    字符按顺序逆时针转圈填入，故非零格恰好是螺旋顺序的一个前缀。"""
    try:
        lines = text.split('\n')
        while lines and lines[-1].strip() == '':
            lines.pop()
        if not lines or len(lines[0].split()) != 1:
            return False
        n = int(lines[0])
        if not 1 <= n <= 100 or len(lines) != n + 1:
            return False
        g = []
        for ln in lines[1:]:
            row = [int(v) for v in ln.split()]
            if len(row) != n or any(not 0 <= v <= 127 for v in row):
                return False
            g.append(row)
        vals = [g[x][y] for x, y in spiral(n)]
        k = next((i for i, v in enumerate(vals) if v == 0), len(vals))
        return all(v != 0 for v in vals[:k]) and all(v == 0 for v in vals[k:])
    except ValueError:
        return False


PRINTABLE = [chr(c) for c in range(32, 127)]
WORDS = "You are so beautiful! handsome Merry Christmas, HELLO CS101 Peking University 2020 Final Exam".split()


def build(n, msg):
    assert 1 <= len(msg) < n * n   # 至少留一个 0（见 notes：满阵时常见的 while 非零写法会越界）
    grid = [[0] * n for _ in range(n)]
    for ch, (x, y) in zip(msg, spiral(n)):
        grid[x][y] = ord(ch)
    return f"{n}\n" + "\n".join(" ".join(map(str, row)) for row in grid) + "\n"


def message(r, length):
    if r.random() < .5:
        s = ""
        while len(s) < length:
            s += r.choice(WORDS) + " "
        s = s[:length]
    else:
        s = "".join(r.choice(PRINTABLE) for _ in range(length))
    s = list(s)
    if s[0] == " ": s[0] = "Y"          # 首尾不放空格，避免与行尾空白容忍规则纠缠
    if s[-1] == " ": s[-1] = "!"
    return "".join(s)


def g21462(r):
    n = r.choice([r.randint(2, 8), r.randint(2, 30), r.randint(30, 100)])
    t = r.random()
    if t < .3:
        length = n * n - 1
    elif t < .45:
        length = r.randint(1, min(n * n - 1, 3))
    else:
        length = r.randint(1, n * n - 1)
    return build(n, message(r, length))


def specials():
    r = random.Random(21462)
    return [
        build(5, "You are so beautiful!"),            # 题面样例二
        build(2, "Hi!"),
        build(2, "A"),
        build(100, message(r, 1)),
        build(100, message(r, 9999)),
        build(99, message(r, 99 * 99 - 1)),          # 奇数阶，只空中心
        build(100, message(r, 5000)),
        build(100, message(r, 397)),                  # 恰好走完最外圈后再多 1 格
    ]

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+[g21462(random.Random(s)) for s in range(1, 40)]+specials()
    assert all(valid(c) for c in cases) and len(set(cases)) == len(cases)
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
