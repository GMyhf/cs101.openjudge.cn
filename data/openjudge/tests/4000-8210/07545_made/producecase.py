import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = "row, col = map(int, input().split())\nmatrix = [['#']*(col+2)] + [['#']+[int(x) for x in input().split()]+['#'] for _ in range(row)] + [['#']*(col+2)]\nres = []\ndire = [[0, 1], [1, 0], [0, -1], [-1, 0]]\nidx = 0\nnum = 1\nx, y = 1, 1\nwhile num <= row*col:\n    res.append(matrix[x][y])\n    matrix[x][y] = '#'\n    dx, dy = dire[idx][0], dire[idx][1]\n    if matrix[x+dx][y+dy] == '#':\n        idx = (idx+1)%4\n        dx, dy = dire[idx][0], dire[idx][1]\n    x += dx\n    y += dy\n    num += 1\nprint(*res, sep='\\n')"
SAMPLE = '4 4\n1 2 3 4\n12 13 14 5\n11 16 15 6\n10 9 8 7\n'
GENERATOR_NAME = 'g7545'
def g7545(r):
    a,b=r.randint(1,8),r.randint(1,8); z=[[r.randint(-50,50) for _ in range(b)] for _ in range(a)]
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
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text, encoding="utf-8")
        (data/f"{i}.out").write_text(run(text), encoding="utf-8")
if __name__=="__main__": main()
