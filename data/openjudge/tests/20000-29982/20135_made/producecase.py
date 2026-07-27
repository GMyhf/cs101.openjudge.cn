import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/20135 statistics, Accepted solution 52789538.\n# Source: http://cs101.openjudge.cn/practice/solution/52789538/\n# Statistics: http://cs101.openjudge.cn/practice/20135/statistics/\n# License: not declared on submission page; no license inferred\nmove = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]\n\nm, n = map(int, input().split())\ns = [input() for i in range(m)]\nname = input()\n\ndef find(x, y, d, i):\n    if i == len(name):\n        print(x + 1, y + 1)\n        print(move[d][0], move[d][1])\n        return True\n    return name[i] == s[x + i*move[d][0]][y + i*move[d][1]] and find(x, y, d, i + 1)\n\n\nfor x in range(m):\n    for y in range(n):\n        if s[x][y] == name[0]:\n            for d in range(8):\n                if 0 <= x + move[d][0]*(len(name) - 1) < m and 0 <= y + move[d][1]*(len(name) - 1) < n:\n                    if find(x, y, d, 0):\n                        exit()\n'
SAMPLE='4 5\nsdadd\nerahh\nwDave\nqqqqe\ndave\n'
GENERATOR_NAME='g20135'
def g20135(r):
    m, n = r.randint(5, 10), r.randint(5, 10)
    word = "abc"
    grid = [["z"] * n for _ in range(m)]
    x, y, d = r.randint(0, m - 1), r.randint(0, n - 3), r.choice([0, 4])
    dx, dy = (0, 1) if d == 0 else (0, -1)
    if d == 4:
        y += 2
    for i, ch in enumerate(word):
        grid[x + i * dx][y + i * dy] = ch
    return f"{m} {n}\n" + "\n".join("".join(row) for row in grid) + f"\n{word}\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        src=Path(d)/'main.py'; src.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(src)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i,text in enumerate(cases):
        (data/f'{i}.in').write_text(text); (data/f'{i}.out').write_text(run(text))
if __name__=='__main__': main()
