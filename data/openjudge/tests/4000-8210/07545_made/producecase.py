import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = "row, col = map(int, input().split())\nmatrix = [['#']*(col+2)] + [['#']+[int(x) for x in input().split()]+['#'] for _ in range(row)] + [['#']*(col+2)]\nres = []\ndire = [[0, 1], [1, 0], [0, -1], [-1, 0]]\nidx = 0\nnum = 1\nx, y = 1, 1\nwhile num <= row*col:\n    res.append(matrix[x][y])\n    matrix[x][y] = '#'\n    dx, dy = dire[idx][0], dire[idx][1]\n    if matrix[x+dx][y+dy] == '#':\n        idx = (idx+1)%4\n        dx, dy = dire[idx][0], dire[idx][1]\n    x += dx\n    y += dy\n    num += 1\nprint(*res, sep='\\n')"
SAMPLE = '4 4\n1 2 3 4\n12 13 14 5\n11 16 15 6\n10 9 8 7\n'
GENERATOR_NAME = 'g7545'
def valid(text):
    """题面契约：首行 row col（0<row<100, 0<col<100）；随后 row 行、每行 col 个整数。
    题面未给元素取值范围，只核整数格式。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    def ints(line, cnt):
        t = line.split(' ')
        if len(t) != cnt:
            return None
        try:
            v = [int(x) for x in t]
        except ValueError:
            return None
        return v if all(str(x) == y for x, y in zip(v, t)) else None
    h = ints(lines[0], 2)
    if h is None or not all(0 < x < 100 for x in h):
        return False
    row, col = h
    return len(lines) == 1 + row and all(ints(x, col) is not None for x in lines[1:])


SHAPES = [(1, 1), (99, 99), (1, 99), (99, 1), (2, 99), (99, 2), (98, 99), (99, 98), (50, 97), (97, 50), (3, 3), (64, 65)]


def g7545(r, i=0):
    if i < 40 - len(SHAPES):
        a,b=r.randint(1,8),r.randint(1,8); z=[[r.randint(-50,50) for _ in range(b)] for _ in range(a)]
    else:
        # 边界与满规模形状：单格、单行、单列、奇偶行列、99×99；元素用互不相同的数，顺序错一位就能发现
        a,b=SHAPES[i-(40-len(SHAPES))]
        v=r.sample(range(-10**6,10**6),a*b); z=[v[x*b:(x+1)*b] for x in range(a)]
    return f"{a} {b}\n"+"\n".join(" ".join(map(str,x)) for x in z)+"\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"
        p.write_text(REFERENCE, encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed), seed) for seed in range(1, 40)]
    for i,text in enumerate(cases):
        assert valid(text), i
        (data/f"{i}.in").write_text(text, encoding="utf-8")
        (data/f"{i}.out").write_text(run(text), encoding="utf-8")
if __name__=="__main__": main()
