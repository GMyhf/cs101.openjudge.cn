#!/usr/bin/env python3
"""Problem-specific generators and input contracts for T-028 phase-2 round 15."""
from __future__ import annotations

import random
import re

NUMBERS = {18164, 20106, 4067, 27638, 20140, 8210, 4015, 23421, 4133, 28046,
           23558, 23568, 27637, 20052, 18161, 19930, 21458, 21554, 27256, 27300}
EXEMPTIONS = {}
SAMPLE_INPUTS = {
    23558: "7 7 2\n0 1\n1 2\n2 3\n2 4\n0 4\n0 5\n5 6\n0\n",
    23568: "3\n1.18 1.27 100\n1.23 1.27 20\n2.4 2.8 81\n",
    20052: "4 4 2\n2 4 512 16\n2 128 16 16\n2 8 256 0\n2 512 256 2\n",
    18161: "3 1\n0\n1\n0\n1 2\n1 1\n3 2\n3 1\n3 1\n3 1\n",
    19930: "3 4\n0 0 2 0\n0 2 1 0\n0 0 0 0\n",
    21458: "6 4\n2 1\n4 7\n3 5\n3 5\n",
    21554: "10\n81 365 72 99 22 7 444 203 1024 203\n",
    27256: "5\nadd 1\nadd 2\nquery\ndel\nquery\n",
}
SAMPLE_OUTPUTS = {
    20106: "2\n3\nNO\n",
    23558: "0 1 2 4 5 6\n", 23568: "181\n", 20052: "1024\n",
    18161: "3 1\n4 2\n3 1\n", 19930: "5\n", 21458: "10\n",
    21554: "6 5 3 1 4 8 10 2 7 9\n431.90\n", 27256: "1.5\n2\n",
}
LABELS = {
    18164: "N is 1..20000 and the second line contains exactly N lengths in 0..50000",
    20106: "the m-by-n terrain and p in-range endpoint queries match their declared dimensions",
    4067: "every nonempty input line is a decimal integer in 0..99999999",
    27638: "the child table describes one rooted binary tree on exactly nodes 0..n-1",
    20140: "repeat counts are 1..100 and brackets form a valid nested lowercase expression",
    8210: "0<N<=50000 distinct rock positions are strictly increasing inside 0..L and 0<=M<=N",
    4015: "every tested email candidate is a nonempty line shorter than 100 characters",
    23421: "the value and weight rows each contain exactly N positive integers and capacity is nonnegative",
    4133: "1<=d<=50 and 1<=n<=20 unique intersections lie inside the 1025-by-1025 grid",
    28046: "2..4000 distinct same-case four-letter words are followed by two dictionary endpoints",
    23558: "the graph has nodes 0..n-1, unique undirected edges, nonnegative depth and an in-range start",
    23568: "plans start during Jan 7..Feb 20 and each inclusive/exclusive date span is 1..10 days",
    27637: "the first line matches valid single-character bracket-nested binary-tree expressions",
    20052: "the 2..10 board is nonempty, uses zero or powers of two through 1024, and 1<=p<=6",
    18161: "all three positive matrix dimensions match the exact row widths that follow",
    19930: "the <=50-by-50 map contains only 0/1/2 and exactly one treasure",
    21458: "1<=T<=1000, item count matches, and every training time is in 1..T with 0<=gain<20",
    21554: "1<=n<=1000 and the duration row contains exactly n positive durations",
    27256: "at most 100000 add/del/query operations never delete or query an empty queue",
    27300: "1..1000 model records use alphanumeric names and canonical 1..999 M/B parameter values",
}
INVALID = {
    18164: "3\n1 2\n", 20106: "2 2 1\n1 2\n3 #\n0 0 2 0\n",
    4067: "100000000\n", 27638: "2\n1 -1\n1 -1\n", 20140: "[0abc]\n",
    8210: "10 2 1\n3\n3\n", 4015: "a" * 100 + "\n",
    23421: "3 4\n1 2\n1 2 3\n", 4133: "51\n1\n0 0 1\n",
    28046: "2\ncat\ndogs\ncat dogs\n", 23558: "3 2 1\n0 1\n1 0\n0\n",
    23568: "1\n1-07 1-20 5\n", 27637: "1\nA(B)\n",
    20052: "2 2 1\n0 0\n0 0\n", 18161: "1 2\n1\n2 1\n1\n1\n1 1\n0\n",
    19930: "2 2\n1 0\n0 1\n", 21458: "10 1\n11 5\n",
    21554: "3\n1 2\n", 27256: "1\nquery\n", 27300: "1\nGPT-1000M\n",
}


def _binary_tree(r: random.Random, n: int):
    children = [[-1, -1] for _ in range(n)]
    available = [(0, 0), (0, 1)]
    for node in range(1, n):
        index = r.randrange(len(available)); parent, side = available.pop(index)
        children[parent][side] = node
        available.extend([(node, 0), (node, 1)])
    return children


def _tree_expression(r: random.Random, labels: list[str]) -> str:
    if not labels:
        return "*"
    root = labels[0]
    if len(labels) == 1:
        return root
    split = r.randrange(len(labels))
    left = _tree_expression(r, labels[1:1 + split])
    right = _tree_expression(r, labels[1 + split:])
    return f"{root}({left},{right})"


def _date(day: int) -> str:
    absolute = 7 + day
    return f"1.{absolute}" if absolute <= 31 else f"2.{absolute - 31}"


def generate(number: int, seed: int) -> str:
    r = random.Random(number * 1_000_003 + seed)
    if number == 18164:
        n = 20000 if seed == 20 else r.randint(1, 80)
        values = [r.randint(0, 50000) for _ in range(n)]
        return f"{n}\n" + " ".join(map(str, values)) + "\n"
    if number == 20106:
        m, n, p = (100, 100, 12) if seed == 20 else (r.randint(2, 14), r.randint(2, 14), r.randint(2, 15))
        grid = [["#" if r.random() < .18 else str(r.randint(0, 1000)) for _ in range(n)] for _ in range(m)]
        queries = [(r.randrange(m), r.randrange(n), r.randrange(m), r.randrange(n)) for _ in range(p)]
        return f"{m} {n} {p}\n" + "\n".join(" ".join(row) for row in grid) + "\n" + \
            "\n".join(" ".join(map(str, row)) for row in queries) + "\n"
    if number == 4067:
        values = ["0", "1", "11", "101", "1001", "10", "12340", "99999999", str(r.randint(0, 99999999))]
        r.shuffle(values); return "\n".join(values) + "\n"
    if number == 27638:
        n = 100 if seed == 20 else r.randint(1, 45); tree = _binary_tree(r, n)
        return f"{n}\n" + "\n".join(f"{a} {b}" for a, b in tree) + "\n"
    if number == 20140:
        atoms = ["".join(r.choice("abcdef") for _ in range(r.randint(1, 5))) for _ in range(3)]
        inner = f"[{r.randint(1,9)}{atoms[1]}]"
        return atoms[0] + f"[{r.randint(1,8)}{inner}{atoms[2]}]" + atoms[1] + "\n"
    if number == 8210:
        n = 50000 if seed == 20 else r.randint(1, 120)
        length = 1_000_000_000 if seed == 20 else r.randint(n + 1, 2_000_000)
        stones = sorted(r.sample(range(1, length), n)); removed = r.randint(0, n)
        return f"{length} {n} {removed}\n" + "\n".join(map(str, stones)) + "\n"
    if number == 4015:
        serial = str(seed)
        rows = [f"user{serial}@host.com", f"a{serial}@b.co.uk", f"plain{serial}",
                f"x{serial}@@a.com", f"x{serial}@.com", f".x{serial}@a.com",
                f"x{serial}@a", f"x{serial}@a.", f"x{serial}.y@a.b"]
        r.shuffle(rows)
        return "\n".join(rows[:5 + seed % 5]) + "\n"
    if number == 23421:
        n = 80 if seed == 20 else r.randint(1, 35); capacity = 500 if seed == 20 else r.randint(0, 150)
        values = [r.randint(1, 5000) for _ in range(n)]; weights = [r.randint(1, 100) for _ in range(n)]
        return f"{n} {capacity}\n" + " ".join(map(str, values)) + "\n" + " ".join(map(str, weights)) + "\n"
    if number == 4133:
        d = 50 if seed == 20 else r.randint(1, 50); n = 20 if seed == 20 else r.randint(1, 20)
        points = r.sample([(x, y) for x in range(1025) for y in range(1025)], n)
        return f"{d}\n{n}\n" + "\n".join(f"{x} {y} {r.randint(0,10000)}" for x, y in points) + "\n"
    if number == 28046:
        alphabet = "abcdefghijklmnopqrstuvwxyz"; start = list(r.sample(alphabet, 4)); words = ["".join(start)]
        current = start[:]
        for index in range(4):
            choices = [c for c in alphabet if c != current[index]]; current[index] = r.choice(choices); words.append("".join(current))
        isolated = []
        while len(isolated) < 3 + seed % 8:
            word = "".join(r.choice("mnopqr") for _ in range(4))
            if word not in words + isolated and all(sum(a != b for a, b in zip(word, other)) >= 2 for other in words + isolated): isolated.append(word)
        all_words = words + isolated; r.shuffle(all_words)
        target = words[-1] if seed % 3 else isolated[0]
        return f"{len(all_words)}\n" + "\n".join(all_words) + f"\n{words[0]} {target}\n"
    if number == 23558:
        n = 100 if seed == 20 else r.randint(2, 35); limit = r.randint(0, n)
        edges = {(i, i + 1) for i in range(n - 1)}
        for _ in range(r.randint(0, n * 2)):
            a, b = r.sample(range(n), 2); edges.add(tuple(sorted((a, b))))
        rows = list(edges); r.shuffle(rows)
        return f"{n} {len(rows)} {limit}\n" + "\n".join(f"{a} {b}" for a, b in rows) + f"\n{r.randrange(n)}\n"
    if number == 23568:
        n = 199 if seed == 20 else r.randint(1, 60); rows = []
        for _ in range(n):
            start = r.randint(0, 44); duration = r.randint(1, 10); end = start + duration
            rows.append(f"{_date(start)} {_date(end)} {r.randint(0,1000)}")
        return f"{n}\n" + "\n".join(rows) + "\n"
    if number == 27637:
        count = r.randint(1, 8); rows = []
        labels = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
        for _ in range(count):
            n = r.randint(1, 20); chosen = r.sample(labels, n); rows.append(_tree_expression(r, chosen))
        return f"{count}\n" + "\n".join(rows) + "\n"
    if number == 20052:
        m, n, p = (10, 10, 6) if seed == 20 else (r.randint(2, 6), r.randint(2, 6), r.randint(1, 6))
        values = [0, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
        board = [[r.choice(values) for _ in range(n)] for _ in range(m)]
        if not any(map(any, board)): board[0][0] = 2
        return f"{m} {n} {p}\n" + "\n".join(" ".join(map(str, row)) for row in board) + "\n"
    if number == 18161:
        a, shared, b = r.randint(1, 10), r.randint(1, 10), r.randint(1, 10)
        valid_shape = seed % 4 != 0; br = shared if valid_shape else shared + 1
        cr, cc = (a, b) if seed % 5 else (a + 1, b)
        matrices = [(a, shared), (br, b), (cr, cc)]; chunks = []
        for rows, cols in matrices:
            chunks.append(f"{rows} {cols}\n" + "\n".join(" ".join(str(r.randint(-50,50)) for _ in range(cols)) for _ in range(rows)))
        return "\n".join(chunks) + "\n"
    if number == 19930:
        m, n = (50, 50) if seed == 20 else (r.randint(2, 18), r.randint(2, 18)); grid = [[0] * n for _ in range(m)]
        ty, tx = r.randrange(m), r.randrange(n); grid[ty][tx] = 1
        for y in range(m):
            for x in range(n):
                if (y, x) not in {(0, 0), (ty, tx)} and r.random() < .28: grid[y][x] = 2
        if seed % 3 == 0:
            for y, x in ((ty-1,tx),(ty+1,tx),(ty,tx-1),(ty,tx+1)):
                if 0 <= y < m and 0 <= x < n and (y,x)!=(0,0): grid[y][x]=2
        return f"{m} {n}\n" + "\n".join(" ".join(map(str, row)) for row in grid) + "\n"
    if number == 21458:
        target = 1000 if seed == 20 else r.randint(1, 250); n = r.randint(1, 80)
        rows = [(r.randint(1, target), r.randint(0, 19)) for _ in range(n)]
        return f"{target} {n}\n" + "\n".join(f"{t} {w}" for t, w in rows) + "\n"
    if number == 21554:
        n = 1000 if seed == 20 else r.randint(1, 120); values = [r.randint(1, 10000) for _ in range(n)]
        return f"{n}\n" + " ".join(map(str, values)) + "\n"
    if number == 27256:
        count = 100000 if seed == 20 else r.randint(30, 300); size = 0; rows = []
        for index in range(count):
            if size == 0 or r.random() < .5:
                rows.append(f"add {r.randint(-10**9,10**9)}"); size += 1
            elif r.random() < .45:
                rows.append("del"); size -= 1
            else: rows.append("query")
        if not any(row == "query" for row in rows): rows[-1] = "query"
        return f"{count}\n" + "\n".join(rows) + "\n"
    if number == 27300:
        n = 1000 if seed == 20 else r.randint(3, 100); names = ["ModelA", "GPT3", "Bert2", f"Net{seed}"]
        rows = []
        for _ in range(n):
            unit = r.choice("MB"); value = r.randint(1, 999)
            rows.append(f"{r.choice(names)}-{value}{unit}")
        return f"{n}\n" + "\n".join(rows) + "\n"
    raise KeyError(number)


def _valid_tree(children):
    n = len(children); parents = [-1] * n
    for parent, row in enumerate(children):
        for child in row:
            if child == -1: continue
            if not 0 <= child < n or parents[child] != -1: return False
            parents[child] = parent
    roots = [i for i, parent in enumerate(parents) if parent == -1]
    if len(roots) != 1: return False
    seen, stack = set(), roots[:]
    while stack:
        node = stack.pop()
        if node in seen: return False
        seen.add(node); stack.extend(child for child in children[node] if child != -1)
    return len(seen) == n


def _valid_expression(text: str) -> bool:
    index = 0
    def parse():
        nonlocal index
        if index >= len(text): return False
        if text[index] == "*": index += 1; return True
        if not text[index].isalpha(): return False
        index += 1
        if index < len(text) and text[index] == "(":
            index += 1
            if not parse() or index >= len(text) or text[index] != ",": return False
            index += 1
            if not parse() or index >= len(text) or text[index] != ")": return False
            index += 1
        return True
    return parse() and index == len(text)


def valid(number: int, text: str) -> bool:
    try:
        lines = text.rstrip("\n").splitlines(); tokens = text.split()
        if number == 18164:
            n = int(tokens[0]); return 1 <= n <= 20000 and len(tokens) == n + 1 and all(0 <= int(x) <= 50000 for x in tokens[1:])
        if number == 20106:
            m,n,p=map(int,lines[0].split()); grid=lines[1:1+m]; queries=lines[1+m:]
            return 1<=m<=100 and 1<=n<=100 and 0<=p<=100 and len(grid)==m and len(queries)==p and all(len(row.split())==n and all(x=="#" or x.lstrip("-").isdigit() for x in row.split()) for row in grid) and all(len(q.split())==4 and 0<=int(q.split()[0])<m and 0<=int(q.split()[2])<m and 0<=int(q.split()[1])<n and 0<=int(q.split()[3])<n for q in queries)
        if number == 4067:
            return bool(lines) and all(line.isdigit() and 0 <= int(line) <= 99999999 for line in lines)
        if number == 27638:
            n=int(lines[0]); rows=[list(map(int,line.split())) for line in lines[1:]]; return 1<=n<=100 and len(rows)==n and all(len(row)==2 for row in rows) and _valid_tree(rows)
        if number == 20140:
            if len(lines)!=1 or not re.fullmatch(r"[a-z0-9\[\]]+",lines[0]): return False
            stack=[]; i=0; s=lines[0]
            while i<len(s):
                if s[i]=="[":
                    j=i+1
                    while j<len(s) and s[j].isdigit(): j+=1
                    if j==i+1 or not 1<=int(s[i+1:j])<=100: return False
                    stack.append("["); i=j; continue
                if s[i]=="]":
                    if not stack:return False
                    stack.pop()
                elif not s[i].islower(): return False
                i+=1
            return not stack
        if number == 8210:
            L,n,m=map(int,lines[0].split()); stones=list(map(int,lines[1:])); return 1<=L<=10**9 and 0<n<=50000 and 0<=m<=n and len(stones)==n and stones==sorted(set(stones)) and all(0<x<L for x in stones)
        if number == 4015: return bool(lines) and all(0<len(line)<100 for line in lines)
        if number == 23421:
            n,b=map(int,lines[0].split()); return n>=1 and b>=0 and len(lines)==3 and len(lines[1].split())==len(lines[2].split())==n and all(int(x)>0 for x in lines[1].split()+lines[2].split())
        if number == 4133:
            d=int(lines[0]);n=int(lines[1]);rows=[tuple(map(int,x.split())) for x in lines[2:]];return 1<=d<=50 and 1<=n<=20 and len(rows)==n and len({(x,y) for x,y,_ in rows})==n and all(0<=x<=1024 and 0<=y<=1024 and value>=0 for x,y,value in rows)
        if number == 28046:
            n=int(lines[0]); words=lines[1:1+n]; ends=lines[1+n].split() if len(lines)==n+2 else []
            return 2<=n<=4000 and len(words)==len(set(words))==n and all(len(x)==4 and x.isalpha() for x in words) and (all(x.islower() for x in words) or all(x.isupper() for x in words)) and len(ends)==2 and all(x in words for x in ends)
        if number == 23558:
            n,m,L=map(int,lines[0].split());edges=[tuple(map(int,x.split())) for x in lines[1:1+m]];start=int(lines[-1]);canon=[tuple(sorted(e)) for e in edges]
            return 1<=n<=100 and m>=0 and L>=0 and len(lines)==m+2 and all(len(e)==2 and 0<=e[0]<n and 0<=e[1]<n and e[0]!=e[1] for e in edges) and len(set(canon))==m and 0<=start<n
        if number == 23568:
            n=int(lines[0]); rows=lines[1:];
            if not n<200 or len(rows)!=n:return False
            def day(value):
                month,date=map(int,re.split(r"[.-]",value));return date-7 if month==1 else 31+date-7
            return all(len(row.split())==3 and 0<=day(row.split()[0])<=44 and 1<=day(row.split()[1])-day(row.split()[0])<=10 for row in rows)
        if number == 27637:
            n=int(lines[0]);return 1<=n<100 and len(lines)==n+1 and all(_valid_expression(x) for x in lines[1:])
        if number == 20052:
            m,n,p=map(int,lines[0].split());vals=[int(x) for x in tokens[3:]];allowed={0,2,4,8,16,32,64,128,256,512,1024}
            return 2<=m<=10 and 2<=n<=10 and 1<=p<=6 and len(lines)==m+1 and all(len(x.split())==n for x in lines[1:]) and set(vals)<=allowed and any(vals)
        if number == 18161:
            index=0
            for _ in range(3):
                if index>=len(lines):return False
                r,c=map(int,lines[index].split());index+=1
                if r<1 or c<1 or index+r>len(lines) or any(len(row.split())!=c for row in lines[index:index+r]):return False
                index+=r
            return index==len(lines)
        if number == 19930:
            m,n=map(int,lines[0].split());vals=[int(x) for x in tokens[2:]];return 1<=m<=50 and 1<=n<=50 and len(lines)==m+1 and all(len(x.split())==n for x in lines[1:]) and set(vals)<={0,1,2} and vals.count(1)==1
        if number == 21458:
            T,n=map(int,lines[0].split());rows=[list(map(int,x.split())) for x in lines[1:]];return 1<=T<=1000 and n>=1 and len(rows)==n and all(len(x)==2 and 1<=x[0]<=T and 0<=x[1]<20 for x in rows)
        if number == 21554:
            n=int(tokens[0]);return 1<=n<=1000 and len(tokens)==n+1 and all(int(x)>0 for x in tokens[1:])
        if number == 27256:
            n=int(lines[0]);size=0
            if not 1<=n<=100000 or len(lines)!=n+1:return False
            for op in lines[1:]:
                if re.fullmatch(r"add -?\d+",op):size+=1
                elif op=="del" and size:size-=1
                elif op=="query" and size:pass
                else:return False
            return True
        if number == 27300:
            n=int(lines[0]);
            if not 1<=n<=1000 or len(lines)!=n+1:return False
            for row in lines[1:]:
                match=re.fullmatch(r"([A-Za-z0-9]+)-(\d+(?:\.\d+)?)([MB])",row)
                if not match or not 1<=float(match.group(2))<1000:return False
            return True
    except (ValueError, IndexError, TypeError): return False
    return False



import subprocess as _subprocess, sys as _sys, tempfile as _tempfile
from pathlib import Path as _Path
REFERENCE="# External reference: http://cs101.openjudge.cn/practice/18161/statistics/\n# Accepted submission: 51773075\n# Source: http://cs101.openjudge.cn/practice/solution/51773075/\n# License: not declared on the submission page; no license is inferred.\n\ndef matrix_mult(m1,m2):\n    r,c=len(m1),len(m2[0])\n    rt,ct=len(m2),len(m1[0])\n    if rt != ct:\n        return 0\n    ans=[[0]*c for _ in range(r)]\n    for i in range(r):\n        for j in range(c):\n            for m in range(len(m1[0])):\n                ans[i][j]+=m1[i][m]*m2[m][j]\n    return ans\ndef matrix_add(m1,m2):\n    r,c=len(m1),len(m1[0])\n    rt,ct=len(m2),len(m2[0])\n    if r!=rt or c !=ct:\n        return 0\n    ans=[[0]*c for _ in range(r)]\n    for i in range(r):\n        for j in range(c):\n            ans[i][j]=m1[i][j]+m2[i][j]\n    return ans\ndef main():\n    rA,cA=map(int,input().split())\n    matrixA=[list(map(int,input().split())) for _ in range(rA)]\n    rB,cB=map(int,input().split())\n    matrixB=[list(map(int,input().split())) for _ in range(rB)]\n    rC,cC=map(int,input().split())\n    matrixC=[list(map(int,input().split())) for _ in range(rC)]\n    mul=matrix_mult(matrixA,matrixB)\n    if not mul:\n        print('Error!')\n        return\n    ans=matrix_add(mul,matrixC)\n    if not ans:\n        print('Error!')\n        return\n    for line in ans:\n        print(*line)\n    return\nif __name__ == '__main__':\n    main()\n"
LANGUAGE='Python3'
NUMBER=18161
SAMPLE='3 1\n0\n1\n0\n1 2\n1 1\n3 2\n3 1\n3 1\n3 1\n'
def _build():
 with _tempfile.TemporaryDirectory() as folder:
  folder=_Path(folder);src=folder/('s.py' if LANGUAGE=='Python3' else 's.cpp');src.write_text(REFERENCE)
  cmd=[_sys.executable,'-I',str(src)]
  if LANGUAGE!='Python3':
   exe=folder/'s';_subprocess.run(['g++','-std=c++20','-O2','-pipe',str(src),'-o',str(exe)],check=True);cmd=[str(exe)]
  out=_Path('data');out.mkdir(exist_ok=True)
  for path in out.glob('*'):path.unlink()
  cases=([SAMPLE] if SAMPLE else [])+[generate(NUMBER,seed) for seed in range(1,21)]
  for index,case in enumerate(cases):
   result=_subprocess.run(cmd,input=case,text=True,capture_output=True,timeout=120,check=True)
   answer='\n'.join(line.rstrip() for line in result.stdout.rstrip().splitlines())+'\n'
   (out/f'{index}.in').write_text(case);(out/f'{index}.out').write_text(answer)
if __name__=='__main__':_build()
