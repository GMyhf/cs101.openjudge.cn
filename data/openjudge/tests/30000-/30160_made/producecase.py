import random
REFERENCE="# External reference: /practice/30160/statistics/\n# Accepted submission: 50848044\n# Source: http://cs101.openjudge.cn/practice/solution/50848044/\n# License: not declared on the submission page; no license is inferred.\n\nimport itertools\nimport sys\nfrom functools import reduce\nfrom operator import and_, or_\n\n\ndef generate_all(arr, length):\n    sep = len(arr) + 1\n    blank = length - sum(arr) - len(arr) + 1\n    elem = [(1 << i) - 1 for i in arr]\n    comb = itertools.combinations_with_replacement(range(sep), blank)\n    entire = []\n    for i in comb:\n        this = 0\n        cursor = 0\n        counter = [0] * sep\n        for s in i:\n            counter[s] += 1\n        for j in range(len(arr)):\n            cursor += counter[j]\n            if j > 0: cursor += 1\n            this |= elem[j] << cursor\n            cursor += arr[j]\n        entire.append(this)\n    return entire\n\n\ndef find_must(entire):\n    must_filled = reduce(and_, entire)  # 1 if must filled\n    must_empty = reduce(or_, entire)  # 0 if must empty\n    return must_filled, must_empty\n\ndef meet_condition(psb: int, must_filled: int, must_empty: int):\n    return not ((~psb & must_filled) | (psb & ~must_empty))\n\n\nclass Nonogram:\n    def __init__(self, rows_cond, cols_cond):\n        self.rows_cond = rows_cond\n        self.cols_cond = cols_cond\n        self.height, self.width = len(rows_cond), len(cols_cond)\n        self.size = self.height * self.width\n        self.mask = (1 << self.size) - 1\n        self.board_filled = 0\n        self.board_empty = self.mask\n\n        self.rows = [generate_all(i, self.width) for i in rows_cond]\n        self.cols = [generate_all(i, self.height) for i in cols_cond]\n\n        self.row_cache = [None] * self.height\n        self.col_cache = [None] * self.width\n\n    def get_row(self, r: int):\n        if self.row_cache[r] is None:\n            self.row_cache[r] = ((self.board_filled >> (r * self.width)) & ((1 << self.width) - 1),\n                (self.board_empty >> (r * self.width)) & ((1 << self.width) - 1))\n        return self.row_cache[r]\n\n    def get_col(self, c: int):\n        if self.col_cache[c] is None:\n            must_filled = must_empty = 0\n            for r in range(self.height):\n                must_filled |= ((self.board_filled >> (r * self.width + c)) & 1) << r\n                must_empty |= ((self.board_empty >> (r * self.width + c)) & 1) << r\n                self.col_cache[c] = (must_filled, must_empty)\n        return self.col_cache[c]\n\n    def set_row(self, r: int, filled: int, empty: int):\n        self.row_cache[r] = None\n        self.board_filled &= ~(((1 << self.width) - 1) << (r * self.width))\n        self.board_empty &= ~(((1 << self.width) - 1) << (r * self.width))\n        self.board_filled |= filled << (r * self.width)\n        self.board_empty |= empty << (r * self.width)\n\n    def set_col(self, c: int, filled: int, empty: int):\n        self.col_cache[c] = None\n        for r in range(self.height):\n            self.board_filled &= ~(1 << (r * self.width + c))\n            self.board_empty &= ~(1 << (r * self.width + c))\n            self.board_filled |= ((filled >> r) & 1) << (r * self.width + c)\n            self.board_empty |= ((empty >> r) & 1) << (r * self.width + c)\n\n    def solve(self):\n        while self.board_filled != self.board_empty:\n            for i, entire in enumerate(self.rows):\n                cond_entire = [psb for psb in entire if meet_condition(psb, *self.get_row(i))]\n                self.rows[i] = [psb for psb in entire if meet_condition(psb, *self.get_row(i))]\n                self.set_row(i, *find_must(cond_entire))\n            for i, entire in enumerate(self.cols):\n                cond_entire = [psb for psb in entire if meet_condition(psb, *self.get_col(i))]\n                self.cols[i] = cond_entire\n                self.set_col(i, *find_must(cond_entire))\n\n\ndef main():\n    r, c = map(int, input().split())\n    rows_cond = [list(map(int, input().split()))[1:] for _ in range(r)]\n    cols_cond = [list(map(int, input().split()))[1:] for _ in range(c)]\n    board = Nonogram(rows_cond, cols_cond)\n    board.solve()\n    filled = board.board_filled\n    for i in range(board.size):\n        sys.stdout.write(str(filled & 1))\n        filled >>= 1\n        if (i + 1) % board.width == 0:\n            sys.stdout.write('\\n')\n\n\nif __name__ == '__main__':\n    main()"
SAMPLE='5 5\n1 3\n1 2\n1 1\n2 2 1\n1 4\n1 2\n1 2\n2 1 1\n2 2 2\n1 3\n'
GENERATOR_NAME='g30160'
CPP=False
def g30160(r):
    h, w = r.randint(1, 8), r.randint(1, 8); board = [[False for _ in range(w)] for _ in range(h)]
    def clue(line):
        out=[]; run=0
        for x in line + [False]:
            if x: run += 1
            elif run: out.append(run); run=0
        return out
    rows = [clue(x) for x in board]; cols = [clue([board[i][j] for i in range(h)]) for j in range(w)]
    return f"{h} {w}\n" + "\n".join(f"{len(x)} {' '.join(map(str,x))}" for x in rows+cols) + "\n"

from pathlib import Path
import subprocess, sys, tempfile
def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/('main.cpp' if CPP else 'main.py'); p.write_text(REFERENCE)
        if CPP:
            exe=Path(d)/'main'; c=subprocess.run(['g++','-O2','-std=c++17',str(p),'-o',str(exe)],capture_output=True,text=True,timeout=30)
            if c.returncode: raise SystemExit(c.stderr)
            cmd=[str(exe)]
        else: cmd=[sys.executable,str(p)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=120)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (data/f'{i}.in').write_text(c); (data/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
