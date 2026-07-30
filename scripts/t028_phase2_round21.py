#!/usr/bin/env python3
"""Problem-specific generators and input contracts for T-028 phase-2 round 21."""
from __future__ import annotations

import math
import random
import re


NUMBERS = {27862, 30193, 30912, 4043, 16527, 18109, 20025, 20127, 30162, 30204,
           30901, 18167, 19961, 27699, 30179, 30283, 30550, 31086, 31087, 29468}
EXEMPTIONS = {30193: "only disconnected no-solution instances are generated because feasible paths have multiple accepted outputs"}
MULTI_ANSWER_EXEMPTIONS = {30193: "every generated instance is disconnected and every exact output is uniquely -1"}
NO_ARCHIVE_REASONS = {
    30193: "legacy files use the current path-input format but expect token 0, which is not a valid output under the mirrored path-or--1 statement",
    18109: "legacy case 4 expects h although z and h both occur twice and z appears first, contradicting the mirrored first-on-tie rule",
}
INPUT_DOMAINS = {
    27862: "每组测试数据第一行给出节点数n，分别标为1--n，接下来n-1行给出n-1条边所连的2个节点。",
    30193: "HAL 是一个 N × M 的神经元矩阵（最多10x10）。",
    30912: "第1行：一个整数n,表示二叉搜索树有n个结点( 1 <= n <= 100)。",
    4043: "输入学生人数m（1 <= m <= 20）、课程数目n（1 <= n <= 10）",
    16527: "输入为两行，分别为字符串A和B。 输入保证A和B是可连接的。",
    18109: "一个字符串，长度大于0，且不超过1000，全部由大写或小写字母组成。",
    20025: "输入保证中间没有混有数字的单词。",
    20127: "第一行为两个整数m,n，分别表示藏宝图的行数和列数。(m<=50,n<=50)",
    30162: "第一行是样例的个数t (t <= 10)",
    30204: "1 <= n <= 10^5； - 1 <= m <= 10^{18}",
    30901: "数据保证所有测试点的 n 的总和不超过 2 * 10^5 。",
    18167: "第二行之后每行为一个长度为不超过100的字符串，不包含空格。",
    19961: "第一行：整数m与n（2 <= m, n <= 10）,最大操作次数p（1 <= p <= 6）。",
    27699: "2 <= N <= 500,000 1 <= K <= N-1 P 是1, 2, ..., N 的排列",
    30179: "数据保证每一个测试点都有 max(n^2) * t <= 10^7。",
    30283: "0 <= x1, y1, x2, y2 <= 999。",
    30550: "一行，一个整数 n (1 ≤ n ≤ 10^6)",
    31086: "1 <= N <= 10^4，0 <= a,b,c <= 100，a,b,c不全为0",
    31087: "1 <= N <= 10^4，0 <= a,b,c <= 100，a,b,c不全为0",
    29468: "第一行为用户指定散列表大小整数N 第二行为一系列数字，以空格分隔",
}
SAMPLE_INPUTS = {
    16527: "xxxxxabc\nabc********\n", 20127: "4 4\n0 0 2 0\n0 2 1 0\n0 0 0 0\n3 3 3 3\n",
    19961: "4 4 2\n2 4 512 16\n2 128 16 16\n2 8 256 0\n2 512 256 2\n",
    27699: "4 2\n4 2 3 1\n", 30550: "5\n",
    31086: "5\n0 0 1\n0 1 1\n0 2 1\n1 2 3\n2 2 1\n",
    31087: "5\n0 0 1\n0 1 1\n0 2 1\n1 2 3\n2 2 1\n",
}
SAMPLE_OUTPUTS = {
    16527: "5\n", 20127: "4\n", 19961: "1024\n", 27699: "2 1 4 3\n",
    30550: "3 4 5\n", 31086: "Piggy\nKittyPig\nPiggy\nKittyPig\nPiggy\n",
    31087: "Piggy\nKittyPig\nPiggy\nPiggy\nPiggy\n",
}
LABELS = {
    27862: "a rooted full binary game tree starts at node 1 and has payoff records for exactly its leaves",
    30193: "a 1..10 by 1..10 grid has valid distinct locks including time 1 and disjoint blocked cells",
    30912: "1..100 distinct values in 0..10000 form a valid binary-search-tree preorder",
    4043: "1..20 students and 1..10 lowercase courses have exact grades in 0..100 with each course selected",
    16527: "two nonempty whitespace-free strings have at least one suffix-prefix connection",
    18109: "the single input string has 1..1000 ASCII letters",
    20025: "the single sentence contains only standalone nonnegative integers or words without embedded digits",
    20127: "a 1..50 rectangular 0..3 map starts with zero and contains exactly one treasure",
    30162: "1..10 cases have valid constant declarations and sub-300-byte expressions over the permitted characters",
    30204: "1..100000 cores have positive x and y at most 10^9 under a positive budget at most 10^18",
    30901: "1..100 arrays contain in total at most 200000 nonnegative integers at most 10^9",
    18167: "one or more nonblank whitespace-free strings have length at most 100",
    19961: "a nonempty 2..10 by 2..10 board uses zero or powers of two through 1024 with 1..6 moves",
    27699: "2..500000 values form a permutation and 1<=K<N",
    30179: "1..100 square boards are permutations of 0..n^2-1 with 2<=n<=1000 and bounded total cells",
    30283: "1..20 knight queries use endpoints with both coordinates in 0..999",
    30550: "the input is one integer in 1..1000000",
    31086: "1..10000 nonzero Nim positions each have three pile sizes in 0..100",
    31087: "1..10000 nonzero Veto-Nim positions each have three pile sizes in 0..100",
    29468: "a positive requested table size precedes a nonempty row of nonnegative integers",
}
INVALID = {
    27862: "2\n1 2\n1\n2 1 2\n", 30193: "11 1 1 0\n1 1 1\n",
    30912: "3\n2 3 1\n", 4043: "1 1\nMath\n100\n", 16527: "abc\ndef\n",
    18109: "abc1\n", 20025: "abc123 word\n", 20127: "2 2\n1 0\n0 1\n",
    30162: "1\n4 a 1.00 b 2.00 c 3.00 d 4.00\na+b\n", 30204: "1 0\n1 1\n",
    30901: "1\n2\n0 -1\n", 18167: "1\ncontains space\n", 19961: "2 2 1\n0 0\n0 0\n",
    27699: "3 3\n1 2 3\n", 30179: "1\n2\n0 1\n1 3\n", 30283: "1\n0 0 1000 0\n",
    30550: "0\n", 31086: "1\n0 0 0\n", 31087: "1\n101 0 0\n", 29468: "0\n1 2\n",
}


def _bst_preorder(values, r):
    if not values: return []
    pivot = r.randrange(len(values))
    return [values[pivot]] + _bst_preorder(values[:pivot], r) + _bst_preorder(values[pivot+1:], r)


def generate(number, seed):
    r = random.Random(number * 1_000_003 + seed)
    if number == 27862:
        depth = r.randint(1, 5); n = 2 ** (depth + 1) - 1; first_leaf = 2 ** depth
        edges = [f"{i} {2*i}\n{i} {2*i+1}" for i in range(1, first_leaf)]
        leaves = [f"{i} {2*i + seed} {3*i + seed}" for i in range(first_leaf, n+1)]
        return f"{n}\n" + "\n".join(edges) + f"\n{len(leaves)}\n" + "\n".join(leaves) + "\n"
    if number == 30193:
        n = 2 + seed % 9; m = 3 + (seed // 9) % 8
        blocked = [f"{row} 2" for row in range(1, n+1)]
        return f"{n} {m} 1 {n}\n1 1 1\n" + "\n".join(blocked) + "\n"
    if number == 30912:
        n = 100 if seed == 20 else r.randint(1, 40); values = sorted(r.sample(range(10001), n))
        return f"{n}\n" + " ".join(map(str, _bst_preorder(values, r))) + "\n"
    if number == 4043:
        m, n = r.randint(1, 20), r.randint(1, 10); names = ["course" + chr(97+i) for i in range(n)]
        grades = [[r.randint(0, 100) for _ in range(n)] for _ in range(m)]
        for col in range(n): grades[r.randrange(m)][col] = r.randint(1, 100)
        return f"{m} {n}\n" + " ".join(names) + "\n" + "\n".join(" ".join(map(str, row)) for row in grades) + "\n"
    if number == 16527:
        prefix = "x" * (seed % 60 + 1); bridge = "a" + "c" * (seed % 20) + "b"
        return prefix + bridge + "\n" + bridge + "tail" + "x" * (seed % 13) + "\n"
    if number == 18109:
        length = 1000 if seed == 20 else r.randint(1, 300)
        return "".join(r.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(length)) + "\n"
    if number == 20025:
        words = ["number", "factor", "plain", "value"]
        parts = []
        for _ in range(r.randint(1, 15)):
            parts.append(str(r.randint(0, 10000)) if r.random() < .55 else r.choice(words))
        if seed % 7 == 0: parts = words[:]
        return " ".join(parts) + "\n"
    if number == 20127:
        m, n = r.randint(2, 4), r.randint(2, 4); grid = [[r.choice((0, 0, 0, 2, 3)) for _ in range(n)] for _ in range(m)]
        grid[0][0] = 0; tr, tc = (m-1, n-1); grid[tr][tc] = 1
        if seed % 3 == 0:
            for c in range(n): grid[1][c] = 2
            grid[tr][tc] = 1
        return f"{m} {n}\n" + "\n".join(" ".join(map(str, row)) for row in grid) + "\n"
    if number == 30162:
        cases = []
        for index in range(r.randint(1, 10)):
            count = r.randint(0, 3); names = ["v" + chr(97+i) for i in range(count)]
            defs = [str(count)] + [item for name in names for item in (name, f"{r.uniform(-99,99):.2f}")]
            if (seed + index) % 4 == 0: expr = "unknown + 1"
            elif (seed + index) % 4 == 1: expr = "1 / 0"
            elif names: expr = f"abs({names[0]}) + sin(1.00) ** 2"
            else: expr = "abs(-3.25) + cos(0.00)"
            cases.extend((" ".join(defs), expr))
        return f"{len(cases)//2}\n" + "\n".join(cases) + "\n"
    if number == 30204:
        n = 1000 if seed == 20 else r.randint(1, 300); budget = r.randint(1, 10**18)
        return f"{n} {budget}\n" + "\n".join(f"{r.randint(1,10**9)} {r.randint(1,10**9)}" for _ in range(n)) + "\n"
    if number == 30901:
        groups, total = [], 0
        for _ in range(r.randint(1, 8)):
            n = r.randint(1, min(500, 200000-total)); total += n
            groups.append(f"{n}\n" + " ".join(str(r.randint(0,10**9)) for _ in range(n)))
        return f"{len(groups)}\n" + "\n".join(groups) + "\n"
    if number == 18167:
        rows = []
        for _ in range(r.randint(1, 40)):
            unit = "".join(r.choice("abcXYZ") for _ in range(r.randint(1, 20)))
            rows.append((unit * r.randint(1, max(1, 100//len(unit))))[:100])
        return f"{len(rows)}\n" + "\n".join(rows) + "\n"
    if number == 19961:
        m, n = r.randint(2, 5), r.randint(2, 5); p = 6 if seed == 20 else r.randint(1, 4)
        board = [[r.choice((0, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024)) for _ in range(n)] for _ in range(m)]
        board[0][0] = r.choice((2,4,8))
        return f"{m} {n} {p}\n" + "\n".join(" ".join(map(str,row)) for row in board) + "\n"
    if number == 27699:
        n = 10000 if seed == 20 else r.randint(2, 500); values = list(range(1,n+1)); r.shuffle(values)
        return f"{n} {r.randint(1,n-1)}\n" + " ".join(map(str, values)) + "\n"
    if number == 30179:
        blocks = []
        for _ in range(r.randint(1, 8)):
            n = r.randint(2, 12); values = list(range(n*n)); r.shuffle(values)
            blocks.append(f"{n}\n" + "\n".join(" ".join(map(str,values[i*n:(i+1)*n])) for i in range(n)))
        return f"{len(blocks)}\n" + "\n".join(blocks) + "\n"
    if number == 30283:
        rows = []
        for index in range(r.randint(1, 3)):
            if seed == 20 and index == 0: rows.append("0 0 999 999")
            else:
                x, y = r.randint(0,999), r.randint(0,999); rows.append(f"{x} {y} {max(0,min(999,x+r.randint(-15,15)))} {max(0,min(999,y+r.randint(-15,15)))}")
        return f"{len(rows)}\n" + "\n".join(rows) + "\n"
    if number == 30550: return f"{5000 if seed == 20 else (seed*233)%4999+1}\n"
    if number in (31086, 31087):
        count = r.randint(1, 200); rows=[]
        for _ in range(count):
            row=[r.randint(0,100) for _ in range(3)]
            if not any(row): row[r.randrange(3)] = 1
            rows.append(" ".join(map(str,row)))
        return f"{count}\n" + "\n".join(rows) + "\n"
    if number == 29468:
        n = r.randint(1, 200); values = [r.randint(0,100000) for _ in range(r.randint(1, 500))]
        if seed % 3 == 0: values += [n*i for i in range(n+20)]
        return f"{n}\n" + " ".join(map(str,values)) + "\n"
    raise KeyError(number)


def valid(number, text):
    try:
        lines=text.rstrip("\n").splitlines(); tokens=text.split()
        if number==27862:
            n=int(lines[0]); edges=[tuple(map(int,x.split())) for x in lines[1:n]]; k=int(lines[n]); leaves=[list(map(int,x.split())) for x in lines[n+1:]]
            children={i:[] for i in range(1,n+1)}
            for a,b in edges:
                if not 1<=a<=n or not 1<=b<=n: return False
                children[a].append(b)
            leaf_ids={i for i in children if not children[i]}
            return len(edges)==n-1 and all(len(v) in (0,2) for v in children.values()) and k==len(leaves)==len(leaf_ids) and {x[0] for x in leaves}==leaf_ids and all(len(x)==3 for x in leaves)
        if number==30193:
            n,m,k,b=map(int,lines[0].split()); locks=[list(map(int,x.split())) for x in lines[1:1+k]]; blocks=[list(map(int,x.split())) for x in lines[1+k:]]
            total=n*m-b
            return (1<=n<=10 and 1<=m<=10 and len(locks)==k and len(blocks)==b and any(x[2]==1 for x in locks) and
                    all(len(x)==3 and 1<=x[0]<=n and 1<=x[1]<=m and 1<=x[2]<=total for x in locks) and
                    all(len(x)==2 and 1<=x[0]<=n and 1<=x[1]<=m for x in blocks) and
                    len({tuple(x[:2]) for x in locks})==k and len({tuple(x) for x in blocks})==b and not ({tuple(x[:2]) for x in locks}&{tuple(x) for x in blocks}))
        if number==30912:
            n=int(lines[0]); a=list(map(int,lines[1].split()))
            def check(seq,lo,hi):
                if not seq:return True
                root=seq[0]; split=next((i for i,x in enumerate(seq[1:],1) if x>root),len(seq))
                return lo<root<hi and all(x<root for x in seq[1:split]) and all(x>root for x in seq[split:]) and check(seq[1:split],lo,root) and check(seq[split:],root,hi)
            return len(lines)==2 and 1<=n<=100 and len(a)==len(set(a))==n and all(0<=x<=10000 for x in a) and check(a,-1,10001)
        if number==4043:
            m,n=map(int,lines[0].split()); names=lines[1].split(); rows=[list(map(int,x.split())) for x in lines[2:]]
            return 1<=m<=20 and 1<=n<=10 and len(names)==n and all(re.fullmatch(r"[a-z]{1,15}",x) for x in names) and len(rows)==m and all(len(x)==n and all(0<=v<=100 for v in x) for x in rows) and all(any(rows[i][j]>0 for i in range(m)) for j in range(n))
        if number==16527:return len(lines)==2 and all(lines) and all(not any(c.isspace() for c in x) for x in lines) and any(lines[0][i:]==lines[1][:len(lines[0])-i] for i in range(len(lines[0])))
        if number==18109:return bool(re.fullmatch(r"[A-Za-z]{1,1000}\n?",text))
        if number==20025:
            return len(lines)==1 and bool(lines[0]) and all(not (any(c.isdigit() for c in token) and not token.strip(',').isdigit()) for token in lines[0].split())
        if number==20127:
            m,n=map(int,lines[0].split()); rows=[list(map(int,x.split())) for x in lines[1:]]
            return 1<=m<=50 and 1<=n<=50 and len(rows)==m and all(len(x)==n and all(v in (0,1,2,3) for v in x) for x in rows) and rows[0][0]==0 and sum(v==1 for row in rows for v in row)==1
        if number==30162:
            t=int(lines[0]); pos=1
            if not 1<=t<=10:return False
            for _ in range(t):
                parts=lines[pos].split();pos+=1;m=int(parts[0])
                if not 0<=m<=3 or len(parts)!=1+2*m:return False
                for i in range(m):
                    if not re.fullmatch(r"[A-Za-z_]+",parts[1+2*i]) or abs(float(parts[2+2*i]))>=100:return False
                expr=lines[pos];pos+=1
                if len(expr.encode())>=300 or not re.fullmatch(r"[0-9.A-Za-z_+*/() \-]+",expr):return False
            return pos==len(lines)
        if number==30204:
            n,m=map(int,lines[0].split());rows=[list(map(int,x.split())) for x in lines[1:]]
            return 1<=n<=100000 and 1<=m<=10**18 and len(rows)==n and all(len(x)==2 and all(1<=v<=10**9 for v in x) for x in rows)
        if number==30901:
            t=int(lines[0]);pos=1;total=0
            if not 1<=t<=100:return False
            for _ in range(t):
                n=int(lines[pos]);pos+=1;a=list(map(int,lines[pos].split()));pos+=1;total+=n
                if not 1<=n<=200000 or len(a)!=n or any(not 0<=x<=10**9 for x in a):return False
            return pos==len(lines) and total<=200000
        if number==18167:
            n=int(lines[0]);return n>=1 and len(lines)==n+1 and all(1<=len(x)<=100 and not any(c.isspace() for c in x) for x in lines[1:])
        if number==19961:
            m,n,p=map(int,lines[0].split());rows=[list(map(int,x.split())) for x in lines[1:]];allowed={0}|{2**i for i in range(1,11)}
            return 2<=m<=10 and 2<=n<=10 and 1<=p<=6 and len(rows)==m and all(len(x)==n and all(v in allowed for v in x) for x in rows) and any(v for row in rows for v in row)
        if number==27699:
            n,k=map(int,lines[0].split());a=list(map(int,lines[1].split()));return len(lines)==2 and 2<=n<=500000 and 1<=k<n and len(a)==n and set(a)==set(range(1,n+1))
        if number==30179:
            t=int(lines[0]);pos=1;total=0
            if not 1<=t<=100:return False
            for _ in range(t):
                n=int(lines[pos]);pos+=1;rows=[list(map(int,x.split())) for x in lines[pos:pos+n]];pos+=n;total+=n*n
                if not 2<=n<=1000 or len(rows)!=n or any(len(x)!=n for x in rows) or {v for row in rows for v in row}!=set(range(n*n)):return False
            return pos==len(lines) and total<=10**7
        if number==30283:
            t=int(lines[0]);rows=[list(map(int,x.split())) for x in lines[1:]];return 1<=t<=20 and len(rows)==t and all(len(x)==4 and all(0<=v<=999 for v in x) for x in rows)
        if number==30550:return len(tokens)==1 and 1<=int(tokens[0])<=10**6
        if number in (31086,31087):
            n=int(lines[0]);rows=[list(map(int,x.split())) for x in lines[1:]];return 1<=n<=10**4 and len(rows)==n and all(len(x)==3 and all(0<=v<=100 for v in x) and any(x) for x in rows)
        if number==29468:
            return len(lines)==2 and int(lines[0])>0 and bool(lines[1].split()) and all(re.fullmatch(r"\d+",x) for x in lines[1].split())
    except (ValueError,IndexError,TypeError,RecursionError):return False
    return False


if __name__ == "__main__":
    import t028_phase2_common
    t028_phase2_common.build_round(21, __import__(__name__))
