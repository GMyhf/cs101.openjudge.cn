#!/usr/bin/env python3
"""Problem-specific generators and input contracts for T-028 phase-2 round 17."""
from __future__ import annotations

import datetime
import random
import re

NUMBERS = {18223, 19960, 19963, 23564, 25538, 25561, 25572, 27928, 19944,
           25566, 26977, 27018, 27141, 27205, 27401, 27948, 26976, 19929,
           4074, 26572}
EXEMPTIONS = {}
SAMPLE_INPUTS = {
    19963: "5\n(100,200) (50,50) (100,300) (150,50) (50,50)\n100 300 200 400 500\n",
    23564: "12\n",
    25538: "9\n",
    25561: "2 2\n1:100 2:120\n1:300 2:350\n200-30 400-70\n100-80\n",
    25572: "6\n0 0 0 0 0 9\n0 0 1 0 1 1\n0 0 0 0 0 0\n0 0 0 1 0 0\n0 0 0 1 0 0\n0 0 0 1 5 5\n",
    27928: "4\n7 10 3 6\n10\n6\n3\n",
    25566: "3\n1 2\n4 3\n3 1\n",
    26977: "12\n0 1 0 2 1 0 1 3 2 1 2 1\n",
    27018: "3\n2 1 3\n",
    27401: "5 10\n3 5 8 8 9\n",
    27948: "3\n10001011\n",
    26976: "6\n1 7 4 9 2 5\n",
}
SAMPLE_OUTPUTS = {19960: "caecaeccbffefdabbc\n", 19963: "2\n", 23564: "0\n", 25538: "Yes\n", 25561: "260\n",
                  25572: "yes\n", 27928: "3\n6\n7\n10\n", 25566: "9\n",
                  26977: "6\n", 27018: "3\n", 27401: "11\n",
                  27948: "IBFBBBFIBFIIIFF\n", 26976: "6\n"}
LABELS = {
    18223: "1<=m<=100 and each case has four integers in 1..10^100",
    19960: "three six-position rotors are permutations, the reflector is three disjoint pairs, and plaintext uses a..f",
    19963: "1<=n<=1000 with exactly n coordinate pairs and n positive prices",
    23564: "the input is one integer in 1..1000000",
    25538: "the input is one integer in 0..2^32",
    25561: "2<=n<=8, 2<=m<=5, every product has valid shop-price offers, and every coupon has q>=x>=0",
    25572: "2<=n<30 square grid over 0,1,5,9 with two adjacent 5 cells and one 9 cell",
    27928: "1<=n<500 unique positive nodes form one rooted tree and each node has one definition row",
    19944: "1<=n<=1000 followed by exactly n valid Gregorian YYYYMMDD dates on or after 1582-10-15",
    25566: "1<=n<=200 followed by n pairs of positive compute and write times",
    26977: "1<=n<=20000 followed by n heights in 0..200000",
    27018: "1<=N<=1000000 followed by a permutation of 1..N",
    27141: "1<=n<100000 followed by n integers and at least one contiguous segment averaging 520",
    27205: "1<=m,n<=1000 and the following m-by-n matrix contains only 0 and 1",
    27401: "1<=n<=100 with positive target and exactly n nonnegative prices",
    27948: "0<=N<=10 followed by a binary string of length 2^N",
    26976: "1<=n<=1000 followed by n integers in 0..1000",
    19929: "1<=m,n<=500 with m destination indices in 1..n and m weights in 1..500",
    4074: "1<=m<=100 and each dataset has 1<=n<=20000 nonnegative heights",
    26572: "each nonempty line is a syntactically valid expression over nonnegative integers, plus, multiply and parentheses",
}
INVALID = {
    18223: "1\n1 2 3\n", 19960: "1 1\n", 19963: "2\n(1,2)\n3 4\n",
    23564: "1000001\n", 25538: "4294967297\n", 25561: "1 2\n1:3\n1-2\n1-1\n",
    25572: "3\n5 0 5\n0 9 0\n0 0 0\n", 27928: "2\n1 2\n2 1\n",
    19944: "1\n15000101\n", 25566: "2\n1 2\n0 3\n", 26977: "3\n1 2\n",
    27018: "3\n1 1 2\n", 27141: "3\n1 2 3\n", 27205: "2 2\n0 1\n0 2\n",
    27401: "2 0\n1 2\n", 27948: "2\n010\n", 26976: "2\n1 1001\n",
    19929: "2 1\n1 2\n3 4\n", 4074: "1\n3\n1 -1 2\n", 26572: "1++2\n",
}


def _expression(r, depth=0):
    if depth >= 4 or r.random() < .35:
        return str(r.randint(0, 999))
    left, right = _expression(r, depth + 1), _expression(r, depth + 1)
    value = left + r.choice("+*") + right
    return "(" * r.randint(0, 2) + value + ")" * r.randint(0, 2) if False else (
        "(" + value + ")" if r.random() < .75 else value)


def generate(number, seed):
    r = random.Random(number * 1_000_003 + seed)
    if number == 18223:
        rows = [[6, 6, 6, 6], [1, 1, 1, 21], [1, 2, 3, 4]]
        for _ in range(r.randint(1, 20)):
            digits = 100 if seed == 20 else r.randint(1, 25)
            rows.append([r.randint(1, 10 ** digits) for _ in range(4)])
        return str(len(rows)) + "\n" + "\n".join(" ".join(map(str, x)) for x in rows) + "\n"
    if number == 19960:
        rows = []
        for _ in range(3):
            p = list(range(1, 7)); r.shuffle(p); rows += [(i + 1, p[i]) for i in range(6)]
        p = list(range(1, 7)); r.shuffle(p); rows += [(p[i], p[i + 1]) for i in range(0, 6, 2)]
        text = "".join(r.choice("abcdef") for _ in range(216 if seed == 20 else r.randint(1, 80)))
        return "\n".join(f"{a} {b}" for a, b in rows) + "\n" + text + "\n"
    if number == 19963:
        n = 1000 if seed == 20 else r.randint(1, 100)
        pairs = [(r.randint(0, 100000), r.randint(0, 100000)) for _ in range(n)]
        return f"{n}\n" + " ".join(f"({a},{b})" for a, b in pairs) + "\n" + " ".join(str(r.randint(1, 100000)) for _ in range(n)) + "\n"
    if number == 23564:
        choices = [1, 2, 4, 6, 30, 36, 999983, 1000000]
        return f"{choices[(seed - 1) % len(choices)] if seed <= len(choices) else r.randint(1, 1000000)}\n"
    if number == 25538:
        choices = [0, 1, 3, 5, 9, 10, 2 ** 31, 2 ** 32]
        return f"{choices[(seed - 1) % len(choices)] if seed <= len(choices) else r.randint(0, 2**32)}\n"
    if number == 25561:
        n, m = (8, 5) if seed == 20 else (r.randint(2, 7), r.randint(2, 5)); lines = []
        for _ in range(n):
            shops = r.sample(range(1, m + 1), r.randint(1, m)); lines.append(" ".join(f"{s}:{r.randint(1, 1000)}" for s in shops))
        coupons = []
        for _ in range(m):
            row = []
            for _ in range(r.randint(1, 5)):
                q = r.randint(1, 2000); row.append(f"{q}-{r.randint(0, q)}")
            coupons.append(" ".join(row))
        return f"{n} {m}\n" + "\n".join(lines + coupons) + "\n"
    if number == 25572:
        n = 29 if seed == 20 else r.randint(3, 15); grid = [[0 if r.random() < .72 else 1 for _ in range(n)] for _ in range(n)]
        horizontal = seed % 2 == 0; i, j = r.randrange(n - (not horizontal)), r.randrange(n - horizontal)
        a, b = (i, j), (i, j + 1) if horizontal else (i + 1, j); target = (r.randrange(n), r.randrange(n))
        while target in (a, b): target = (r.randrange(n), r.randrange(n))
        grid[a[0]][a[1]] = grid[b[0]][b[1]] = 5; grid[target[0]][target[1]] = 9
        return f"{n}\n" + "\n".join(" ".join(map(str, row)) for row in grid) + "\n"
    if number == 27928:
        n = 499 if seed == 20 else r.randint(1, 100); values = r.sample(range(1, 9999999), n); children = {x: [] for x in values}
        for i in range(1, n): children[values[r.randrange(i)]].append(values[i])
        order = values[:]; r.shuffle(order)
        return f"{n}\n" + "\n".join(" ".join(map(str, [x] + children[x])) for x in order) + "\n"
    if number == 19944:
        n = 1000 if seed == 20 else r.randint(1, 100); start = datetime.date(1582, 10, 15); span = (datetime.date(9999, 12, 31) - start).days
        dates = [start + datetime.timedelta(days=r.randint(0, span)) for _ in range(n)]
        if 0 <= seed <= 3: dates[0] = datetime.date(1900 + 100 * seed, 1, seed + 1)
        return f"{n}\n" + "\n".join(x.strftime("%Y%m%d") for x in dates) + "\n"
    if number == 25566:
        n = 200 if seed == 20 else r.randint(1, 100); return f"{n}\n" + "\n".join(f"{r.randint(1,100000)} {r.randint(1,100000)}" for _ in range(n)) + "\n"
    if number == 26977:
        n = 20000 if seed == 20 else r.randint(1, 500); a = [r.randint(0, 200000) for _ in range(n)]; return f"{n}\n" + " ".join(map(str, a)) + "\n"
    if number == 27018:
        n = 200000 if seed == 20 else r.randint(1, 1000); p = list(range(1, n + 1)); r.shuffle(p); return f"{n}\n" + " ".join(map(str, p)) + "\n"
    if number == 27141:
        n = 99999 if seed == 20 else r.randint(1, 500); a = [r.randint(0, 1040) for _ in range(n)]; a[r.randrange(n)] = 520; return f"{n}\n" + " ".join(map(str, a)) + "\n"
    if number == 27205:
        m, n = (300, 400) if seed == 20 else (r.randint(1, 60), r.randint(1, 60)); rows = [[r.randint(0, 1) for _ in range(n)] for _ in range(m)]
        if seed % 4 == 0: rows = [[0] * n for _ in range(m)]
        return f"{m} {n}\n" + "\n".join(" ".join(map(str, x)) for x in rows) + "\n"
    if number == 27401:
        n = 100 if seed == 20 else r.randint(1, 60); t = r.randint(1, 2000); a = [r.randint(0, 500) for _ in range(n)]; return f"{n} {t}\n" + " ".join(map(str, a)) + "\n"
    if number == 27948:
        n = (seed - 1) % 11; return f"{n}\n" + "".join(r.choice("01") for _ in range(2 ** n)) + "\n"
    if number == 26976:
        n = 1000 if seed == 20 else r.randint(1, 300); modes = ([7] * n, list(range(n)), [i % 2 * 1000 for i in range(n)])
        a = list(modes[seed % 3]) if seed <= 6 else [r.randint(0, 1000) for _ in range(n)]; return f"{n}\n" + " ".join(map(str, a)) + "\n"
    if number == 19929:
        m, n = (500, 500) if seed == 20 else (r.randint(1, 200), r.randint(1, 200)); return f"{m} {n}\n" + " ".join(str(r.randint(1, n)) for _ in range(m)) + "\n" + " ".join(str(r.randint(1, 500)) for _ in range(m)) + "\n"
    if number == 4074:
        count = r.randint(1, 10); chunks = []
        for k in range(count):
            n = 20000 if seed == 20 and k == 0 else r.randint(1, 400); a = [r.randint(0, 80) for _ in range(n)]; chunks += [str(n), " ".join(map(str, a))]
        return f"{count}\n" + "\n".join(chunks) + "\n"
    if number == 26572:
        fixed = ["(1+2)", "((1*2))", "1+(2+3)", "1*(2+3)", "(1+2)*(3+4)"]
        rows = fixed + [_expression(r) for _ in range(r.randint(1, 12))]; return "\n".join(rows) + "\n"
    raise KeyError(number)


def _valid_expr(s):
    return bool(re.fullmatch(r"\d+|\((?:[^()]|\([^()]*\))*\)|[\d+*()]+", s)) and not re.search(r"(?:^|[+*(])[+*)]|[+*](?:$|[+*)])|\d\(|\)\d", s) and _balanced(s)


def _balanced(s):
    depth = 0
    for ch in s:
        depth += (ch == "(") - (ch == ")")
        if depth < 0: return False
    return depth == 0


def valid(number, text):
    try:
        lines = text.rstrip("\n").splitlines(); tokens = text.split()
        if number == 18223:
            m = int(lines[0]); return 1 <= m <= 100 and len(lines) == m + 1 and all(len(x.split()) == 4 and all(1 <= int(v) <= 10**100 for v in x.split()) for x in lines[1:])
        if number == 19960:
            if len(lines) != 22 or not lines[-1] or set(lines[-1]) - set("abcdef"): return False
            rows = [tuple(map(int, x.split())) for x in lines[:21]]
            return all(len(x) == 2 for x in rows) and all(sorted(b for a, b in rows[k:k+6]) == list(range(1, 7)) and sorted(a for a, b in rows[k:k+6]) == list(range(1, 7)) for k in (0, 6, 12)) and sorted(v for x in rows[18:] for v in x) == list(range(1, 7))
        if number == 19963:
            n = int(lines[0]); pairs = lines[1].split(); prices = list(map(int, lines[2].split())); return 1 <= n <= 1000 and len(lines) == 3 and len(pairs) == len(prices) == n and all(re.fullmatch(r"\(\d+,\d+\)", x) for x in pairs) and all(x > 0 for x in prices)
        if number == 23564: return len(tokens) == 1 and 1 <= int(tokens[0]) <= 1000000
        if number == 25538: return len(tokens) == 1 and 0 <= int(tokens[0]) <= 2**32
        if number == 25561:
            n, m = map(int, lines[0].split())
            if not 2 <= n <= 8 or not 2 <= m <= 5 or len(lines) != 1+n+m: return False
            return all(row.split() and all(re.fullmatch(r"[1-5]:\d+", x) and 1 <= int(x.split(':')[0]) <= m and int(x.split(':')[1]) > 0 for x in row.split()) for row in lines[1:1+n]) and all(row.split() and all(re.fullmatch(r"\d+-\d+", x) and int(x.split('-')[0]) >= int(x.split('-')[1]) for x in row.split()) for row in lines[1+n:])
        if number == 25572:
            n = int(lines[0]); a = [list(map(int, x.split())) for x in lines[1:]]; fives = [(i,j) for i,row in enumerate(a) for j,x in enumerate(row) if x == 5]
            return 2 <= n < 30 and len(a) == n and all(len(x) == n and set(x) <= {0,1,5,9} for x in a) and len(fives) == 2 and abs(fives[0][0]-fives[1][0])+abs(fives[0][1]-fives[1][1]) == 1 and sum(x == 9 for row in a for x in row) == 1
        if number == 27928:
            n = int(lines[0]); rows = [list(map(int, x.split())) for x in lines[1:]]; parents = [x[0] for x in rows]; children = [v for x in rows for v in x[1:]]
            return 1 <= n < 500 and len(rows) == n and len(set(parents)) == n and all(1 <= x <= 9999999 for row in rows for x in row) and set(children) <= set(parents) and len(children) == n-1 and len(set(children)) == n-1
        if number == 19944:
            n = int(lines[0]); dates = [datetime.datetime.strptime(x, "%Y%m%d").date() for x in lines[1:]]; return 1 <= n <= 1000 and len(dates) == n and all(x >= datetime.date(1582,10,15) for x in dates)
        if number == 25566:
            n = int(lines[0]); rows = [list(map(int,x.split())) for x in lines[1:]]; return 1 <= n <= 200 and len(rows) == n and all(len(x)==2 and min(x)>0 for x in rows)
        if number in (26977, 26976):
            n = int(lines[0]); a = list(map(int, lines[1].split())); limitn, limitv = ((20000,200000) if number == 26977 else (1000,1000)); return len(lines)==2 and 1<=n<=limitn and len(a)==n and all(0<=x<=limitv for x in a)
        if number == 27018:
            n=int(lines[0]);a=list(map(int,lines[1].split()));return len(lines)==2 and 1<=n<=1000000 and len(a)==n and sorted(a)==list(range(1,n+1))
        if number == 27141:
            n=int(lines[0]);a=list(map(int,lines[1].split())); seen={0};total=0;match=False
            for x in a: total += x-520; match |= total in seen; seen.add(total)
            return len(lines)==2 and 1<=n<100000 and len(a)==n and match
        if number == 27205:
            m,n=map(int,lines[0].split());return 1<=m<=1000 and 1<=n<=1000 and len(lines)==m+1 and all(len(x.split())==n and set(x.split())<={"0","1"} for x in lines[1:])
        if number == 27401:
            n,t=map(int,lines[0].split());a=list(map(int,lines[1].split()));return len(lines)==2 and 1<=n<=100 and t>0 and len(a)==n and min(a)>=0
        if number == 27948:
            n=int(lines[0]);return len(lines)==2 and 0<=n<=10 and len(lines[1])==2**n and set(lines[1])<={"0","1"}
        if number == 19929:
            m,n=map(int,lines[0].split());a=list(map(int,lines[1].split()));w=list(map(int,lines[2].split()));return len(lines)==3 and 1<=m<=500 and 1<=n<=500 and len(a)==len(w)==m and all(1<=x<=n for x in a) and all(1<=x<=500 for x in w)
        if number == 4074:
            count=int(lines[0]);i=1
            for _ in range(count):
                n=int(lines[i]);a=list(map(int,lines[i+1].split()));i+=2
                if not 1<=n<=20000 or len(a)!=n or min(a)<0:return False
            return 1<=count<=100 and i==len(lines)
        if number == 26572: return bool(lines) and all(_valid_expr(x) for x in lines)
    except (ValueError, IndexError, TypeError):
        return False
    return False



import subprocess as _subprocess, sys as _sys, tempfile as _tempfile
from pathlib import Path as _Path
REFERENCE='# External reference: http://cs101.openjudge.cn/practice/19929/statistics/\n# Accepted submission: 51527971\n# Source: http://cs101.openjudge.cn/practice/solution/51527971/\n# License: not declared on the submission page; no license is inferred.\n\nm, n = map(int, input().split())\na = list(map(int, input().split()))\nw = list(map(int, input().split()))\ndp = [0] * (n + 1)\nfor i in range(m):\n    dp[a[i]] = max(dp[1 : a[i] + 1]) + w[i]\nprint(max(dp))\n'
LANGUAGE='Python3'
NUMBER=19929
SAMPLE='5 3\n1 2 3 2 1\n5 4 3 4 2\n'
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
