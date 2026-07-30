#!/usr/bin/env python3
"""Problem-specific generators and input contracts for T-028 phase-2 round 23."""
from __future__ import annotations

import random
import re

NUMBERS = {27598, 28052, 28186, 28203, 30158, 30201, 30274, 30281, 30313,
           30363, 30376, 30381, 30382, 30399, 27371, 30276, 27372, 27631,
           28190, 30159}
EXEMPTIONS = {}
EXCLUDE_ARCHIVE_DIRS = {
    27631: {"tests/20000-29982/27631/data":
            "each legacy batch output repeats one answer for every dataset; seven independent platform Accepted sources disagree, while the five top-level sample oracles remain usable"}
}
INPUT_DOMAINS = {
    27598: "有一根长度为n的木材（n为不大于100的正整数），要将其切割为m（0 < m < n) 段出售，每段均为正整数长度。",
    28052: "The first line is a positive integer n (2 <= n <= 1000), indicating that the size of the chessboard is n*n.",
    28186: "第一行包含两个整数n, m(1 ≤ n ≤100; 1 ≤ m ≤ 100)。第二行包含n个整数a1, a2，…， an (1 ≤ ai ≤ 100)。",
    28203: "对于 100% 的数据，1 <= n <= 3 * 10^6，1 <= ai <= 10^9。",
    30158: "第三行两个整数 n, m, 由空格分隔 (3<=n<=10e18, 10<=m<=10e9)",
    30201: "输入的第 1 行是一个正整数 n （3 <= n <= 18）",
    30274: "第一行两个整数 n 和 m（1 <= n <= 50, 1 <= m <= 20）；",
    30281: "第一行是a b c，以空格分隔，均为非负实数，0.1 <= a,b,c <= 10.0。",
    30313: "第一行两个整数 n,m，表示点数和指定权值的边数。(1≤n≤100,000, 0≤m≤min(200,000,n(n−1)/2))",
    30363: "第一行两个正整数 N, Q，N <= 2 * 10^5, Q <= 2 * 10^5。",
    30376: "一行一个只包含小写字符的字符串 S，(1 ≤ |S| ≤ 10^5）。",
    30381: "数据满足：2<=N<=50, 0<=M, ci<=500,000,000。",
    30382: "第一行输入一个只包含小写字母的字符串 S(1≤|S|≤10^5)；",
    30399: "第一行输入两个整数 m, n 表示滑雪场的大小，1 ≤ m, n ≤ 10。",
    27371: "第二行包含一个数字n，表示待加密明文数量。1 <= n <= 100。",
    30276: "所有k满足3<=k<=100",
    27372: "满足 1 <= n <= 100，字符串长度 <= 50，没有两个字符串是完全相同的。",
    27631: "第一行输入一个整数 T(1 <= T <= 500)表示数据组数。每组数据第一行输入一个整数 n(1 <= n <= 100)表示套餐的数量。",
    28190: "第一行一个正整数 N，表示奶牛的头数。(2<=N<=10^6)",
    30159: "第一行是R和C，用空格分割。（R, C <= 30）",
}
LABELS = {
    27598: "n is 2..100, m is 1..n-1, and n prices are in 1..99",
    28052: "a 2..1000 square board uses 0,1,2 and red count equals blue or exceeds it by one",
    28186: "n,m and exactly n candy demands are all in 1..100",
    28203: "exactly n values in 1..10^9 follow n in 1..3,000,000",
    30158: "initials are 0..20, coefficients -20..20, n is 3..10e18 and modulus 10..10e9",
    30201: "a symmetric 3..18 city matrix has zero diagonal and positive off-diagonal costs at most 10^4",
    30274: "n is 1..50, threshold is 1..20, and exactly n masses are in 0..m-1",
    30281: "three costs are 0.1..10 and three uniquely named parts have coordinates strictly inside (-100,100)",
    30313: "1..100000 vertices and distinct ordered positive edges obey the complete-graph bounds",
    30363: "1..200000 vertices and operations use in-range endpoints with an exact Q row count",
    30376: "the sole input is a 1..100000 character lowercase string",
    30381: "2..50 card counts and wildcard count are each in 0..500000000",
    30382: "two nonempty lowercase strings each have length at most 100000",
    30399: "a 1..10 rectangular grid has heights in 0..10000",
    27371: "a nonempty lowercase key of at most 25 letters precedes 1..100 nonempty lowercase plaintexts of at most 100 letters",
    30276: "3..100 pegs and 1..100 disks have an optimal move count at most 2^31-1",
    27372: "1..100 distinct lowercase words each have length 1..50",
    27631: "1..500 datasets each contain 1..100 prices in 1..10^9",
    28190: "2..1000000 positive heights are each below 2^31",
    30159: "a 1..30 puzzle supplies syntactically valid row and column clues for a uniquely fixed board",
}
INVALID = {
    27598: "2\n2\n1 2\n", 28052: "2\n1 1\n0 0\n", 28186: "2 1\n1\n",
    28203: "2\n1 0\n", 30158: "1 2\n0 0 0\n2 10\n",
    30201: "3\n0 1 2\n2 0 3\n2 3 0\n", 30274: "2 4\n1 4\n",
    30281: "0 1 1\na 0 0\nb 1 1\nc 2 2\n", 30313: "3 2\n1 2 1\n1 2 2\n",
    30363: "2 2\n1 2\n", 30376: "abcD\n", 30381: "1 0\n0\n",
    30382: "abc\nA\n", 30399: "1 2\n0 10001\n", 27371: "key\n0\n",
    30276: "2 3\n", 27372: "2\na\na\n", 27631: "1\n0\n\n",
    28190: "1\n5\n", 30159: "2 2\n1 2\n1 2\n0\n0\n",
}
SAMPLE_INPUTS = {
    28186: "5 2\n1 3 1 4 2\n", 30363: "3 2\n1 2\n2 3\n",
    30313: "6 11\n1 3 10\n1 4 10\n1 5 10\n1 6 10\n2 3 10\n2 4 10\n2 5 10\n2 6 10\n3 4 5\n3 5 6\n3 6 7\n",
    27371: "keyword\n1\nballoon\n", 30276: "3 3\n", 27372: "3\nhello\nhell\nhi\n",
    27631: "1\n5\n10 20 30 40 50\n", 28190: "5\n1\n2\n3\n4\n1\n",
}
SAMPLE_OUTPUTS = {28186: "4\n", 30363: "1\n3\n", 30313: "15\n",
                  27371: "cbizsces\n", 30276: "7\n", 27372: "6\n",
                  27631: "3\n", 28190: "4\n", 30381: "3\n"}


def _hanoi(k, n):
    dp = [[10**40] * (n + 1) for _ in range(k + 1)]
    for pegs in range(3, k + 1):
        dp[pegs][0] = 0
        if n: dp[pegs][1] = 1
    for disks in range(2, n + 1): dp[3][disks] = 2**disks - 1
    for pegs in range(4, k + 1):
        for disks in range(2, n + 1):
            dp[pegs][disks] = min(2 * dp[pegs][cut] + dp[pegs - 1][disks - cut]
                                   for cut in range(1, disks))
    return dp[k][n]


def _runs(bits):
    out = []
    for bit in bits:
        if bit:
            if out and out[-1][0]: out[-1][1] += 1
            else: out.append([1, 1])
        elif out and out[-1][0]: out.append([0, 0])
    return [length for marker, length in out if marker]


def _route_cost(costs, points, order):
    def leg(p, q):
        dx, dy = abs(p[0] - q[0]), abs(p[1] - q[1])
        a, b, c = costs
        return min(dx, dy) * c + max(dx - dy, 0) * a + max(dy - dx, 0) * b
    route = [(0, 0)] + [points[i] for i in order] + [(100, 100)]
    return sum(leg(route[i], route[i + 1]) for i in range(4))


def generate(number, seed):
    r = random.Random(number * 1_000_003 + seed)
    if number == 27598:
        n = 100 if seed == 20 else r.randint(2, 35); m = r.randint(1, n - 1)
        return f"{n}\n{m}\n" + " ".join(str(r.randint(1, 99)) for _ in range(n)) + "\n"
    if number == 28052:
        n = r.randint(2, 18); cells = [0] * (n * n); count = r.randint(0, n * n // 2)
        for offset, i in enumerate(r.sample(range(n * n), 2 * count)):
            cells[i] = 1 if offset < count else 2
        if r.choice((False, True)) and 2 * count < n * n:
            cells[next(i for i, value in enumerate(cells) if value == 0)] = 1
        return f"{n}\n" + "\n".join(" ".join(map(str, cells[i*n:(i+1)*n])) for i in range(n)) + "\n"
    if number == 28186:
        n, m = r.randint(1, 100), r.randint(1, 100)
        return f"{n} {m}\n" + " ".join(str(r.randint(1, 100)) for _ in range(n)) + "\n"
    if number == 28203:
        n = 50000 if seed == 20 else r.randint(1, 5000)
        return f"{n}\n" + " ".join(str(r.randint(1, 10**9)) for _ in range(n)) + "\n"
    if number == 30158:
        return (f"{r.randint(0,20)} {r.randint(0,20)}\n"
                f"{r.randint(-20,20)} {r.randint(-20,20)} {r.randint(-20,20)}\n"
                f"{r.randint(3,10**18)} {r.randint(10,10**9)}\n")
    if number == 30201:
        n = r.randint(3, 11); matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n): matrix[i][j] = matrix[j][i] = r.randint(1, 10**4)
        return f"{n}\n" + "\n".join(" ".join(map(str, row)) for row in matrix) + "\n"
    if number == 30274:
        n, m = r.randint(1, 10), r.randint(1, 20)
        return f"{n} {m}\n" + " ".join(str(r.randrange(m)) for _ in range(n)) + "\n"
    if number == 30281:
        while True:
            costs = tuple(r.randint(1, 100) / 10 for _ in range(3))
            points = [tuple(r.randint(-99, 99) for _ in range(2)) for _ in range(3)]
            reduced = (min(costs[0], costs[1] + costs[2]), min(costs[1], costs[0] + costs[2]),
                       min(costs[2], costs[0] + costs[1]))
            values = [_route_cost(reduced, points, order) for order in
                      ((0,1,2),(0,2,1),(1,0,2),(1,2,0),(2,0,1),(2,1,0))]
            if values.count(min(values)) == 1: break
        return (" ".join(f"{x:.1f}" for x in costs) + "\n" +
                "\n".join(f"part{i+1} {x} {y}" for i, (x, y) in enumerate(points)) + "\n")
    if number == 30313:
        n = r.randint(1, 250); max_edges = n * (n - 1) // 2; m = r.randint(0, min(1000, max_edges))
        pairs = r.sample([(u, v) for u in range(1, n + 1) for v in range(u + 1, n + 1)], m)
        return f"{n} {m}\n" + "".join(f"{u} {v} {r.randint(1,10**9)}\n" for u, v in pairs)
    if number == 30363:
        n, q = r.randint(1, 1000), r.randint(1, 2000)
        return f"{n} {q}\n" + "".join(f"{r.randint(1,n)} {r.randint(1,n)}\n" for _ in range(q))
    if number == 30376:
        n = 100000 if seed == 20 else r.randint(1, 5000)
        return "".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(n)) + "\n"
    if number == 30381:
        n, m = r.randint(2, 50), r.randint(0, 500_000_000)
        return f"{n} {m}\n" + " ".join(str(r.randint(0, 500_000_000)) for _ in range(n)) + "\n"
    if number == 30382:
        alphabet = "abcde"; s = "".join(r.choice(alphabet) for _ in range(r.randint(1, 5000)))
        t_alpha = alphabet if seed % 4 else "abcd"
        t = "".join(r.choice(t_alpha) for _ in range(r.randint(1, 1000)))
        return f"{s}\n{t}\n"
    if number == 30399:
        m, n = r.randint(1, 10), r.randint(1, 10)
        return f"{m} {n}\n" + "\n".join(" ".join(str(r.randint(0,10000)) for _ in range(n)) for _ in range(m)) + "\n"
    if number == 27371:
        key = "".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(r.randint(1,25)))
        rows = ["".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(r.randint(1,100))) for _ in range(r.randint(1,20))]
        return f"{key}\n{len(rows)}\n" + "\n".join(rows) + "\n"
    if number == 30276:
        while True:
            k, n = r.randint(3, 12), r.randint(1, 35)
            if _hanoi(k, n) <= 2**31 - 1: return f"{k} {n}\n"
    if number == 27372:
        words = set()
        while len(words) < r.randint(1, 60):
            words.add("".join(r.choice("abcde") for _ in range(r.randint(1, 20))))
        return f"{len(words)}\n" + "\n".join(sorted(words)) + "\n"
    if number == 27631:
        groups = []
        for _ in range(r.randint(1, 20)):
            values = [r.randint(1, 10**9) for _ in range(r.randint(1, 100))]
            groups.append(f"{len(values)}\n" + " ".join(map(str, values)))
        return f"{len(groups)}\n" + "\n".join(groups) + "\n"
    if number == 28190:
        n = 100000 if seed == 20 else r.randint(2, 5000)
        return f"{n}\n" + "\n".join(str(r.randint(1, 2**31 - 1)) for _ in range(n)) + "\n"
    if number == 30159:
        rows, cols = r.randint(1, 20), r.randint(1, 20)
        bits = [r.randint(0, 1) for _ in range(rows)]
        if rows > 1: bits[0], bits[1] = 0, 1
        row_clues = [f"1 {cols}" if bit else "0" for bit in bits]
        runs = _runs(bits); clue = str(len(runs)) + (" " + " ".join(map(str, runs)) if runs else "")
        return f"{rows} {cols}\n" + "\n".join(row_clues + [clue] * cols) + "\n"
    raise KeyError(number)


def valid(number, text):
    try:
        lines = text.rstrip("\n").splitlines(); tokens = text.split()
        if number == 27598:
            n, m, prices = int(lines[0]), int(lines[1]), list(map(int, lines[2].split()))
            return len(lines)==3 and 2<=n<=100 and 0<m<n and len(prices)==n and all(0<p<100 for p in prices)
        if number == 28052:
            n=int(lines[0]); rows=[list(map(int,row.split())) for row in lines[1:]]; flat=sum(rows,[])
            return 2<=n<=1000 and len(rows)==n and all(len(row)==n for row in rows) and set(flat)<={0,1,2} and flat.count(1)-flat.count(2) in (0,1)
        if number == 28186:
            n,m=map(int,lines[0].split()); values=list(map(int,lines[1].split()))
            return len(lines)==2 and 1<=n<=100 and 1<=m<=100 and len(values)==n and all(1<=x<=100 for x in values)
        if number == 28203:
            n=int(lines[0]); values=list(map(int,lines[1].split()))
            return len(lines)==2 and 1<=n<=3_000_000 and len(values)==n and all(1<=x<=10**9 for x in values)
        if number == 30158:
            a=list(map(int,lines[0].split())); p=list(map(int,lines[1].split())); n,m=map(int,lines[2].split())
            return len(lines)==3 and len(a)==2 and all(0<=x<=20 for x in a) and len(p)==3 and all(-20<=x<=20 for x in p) and 3<=n<=10*10**18 and 10<=m<=10*10**9
        if number == 30201:
            n=int(lines[0]); matrix=[list(map(int,row.split())) for row in lines[1:]]
            return 3<=n<=18 and len(matrix)==n and all(len(row)==n for row in matrix) and all(matrix[i][i]==0 for i in range(n)) and all(1<=matrix[i][j]<=10**4 and matrix[i][j]==matrix[j][i] for i in range(n) for j in range(i+1,n))
        if number == 30274:
            n,m=map(int,lines[0].split()); values=list(map(int,lines[1].split()))
            return len(lines)==2 and 1<=n<=50 and 1<=m<=20 and len(values)==n and all(0<=x<m for x in values)
        if number == 30281:
            costs=list(map(float,lines[0].split())); rows=[row.split() for row in lines[1:]]
            if not (len(lines)==4 and len(costs)==3 and all(.1<=x<=10 for x in costs) and len(rows)==3 and len({row[0] for row in rows})==3 and all(len(row)==3 and 1<=len(row[0])<=20 and -100<int(row[1])<100 and -100<int(row[2])<100 for row in rows)): return False
            points=[(int(row[1]),int(row[2])) for row in rows]
            reduced=(min(costs[0],costs[1]+costs[2]),min(costs[1],costs[0]+costs[2]),min(costs[2],costs[0]+costs[1]))
            values=[_route_cost(reduced,points,order) for order in ((0,1,2),(0,2,1),(1,0,2),(1,2,0),(2,0,1),(2,1,0))]
            return values.count(min(values))==1
        if number == 30313:
            n,m=map(int,lines[0].split()); edges=[tuple(map(int,row.split())) for row in lines[1:]]
            return 1<=n<=100000 and 0<=m<=min(200000,n*(n-1)//2) and len(edges)==m and len({(u,v) for u,v,w in edges})==m and all(1<=u<v<=n and 1<=w<=10**9 for u,v,w in edges)
        if number == 30363:
            n,q=map(int,lines[0].split()); edges=[tuple(map(int,row.split())) for row in lines[1:]]
            return 1<=n<=200000 and 1<=q<=200000 and len(edges)==q and all(len(edge)==2 and 1<=edge[0]<=n and 1<=edge[1]<=n for edge in edges)
        if number == 30376: return bool(re.fullmatch(r"[a-z]{1,100000}\n?", text))
        if number == 30381:
            n,m=map(int,lines[0].split()); values=list(map(int,lines[1].split()))
            return len(lines)==2 and 2<=n<=50 and 0<=m<=500_000_000 and len(values)==n and all(0<=x<=500_000_000 for x in values)
        if number == 30382: return len(lines)==2 and all(re.fullmatch(r"[a-z]{1,100000}", row) for row in lines)
        if number == 30399:
            m,n=map(int,lines[0].split()); rows=[list(map(int,row.split())) for row in lines[1:]]
            return 1<=m<=10 and 1<=n<=10 and len(rows)==m and all(len(row)==n and all(0<=x<=10000 for x in row) for row in rows)
        if number == 27371:
            count=int(lines[1]); rows=lines[2:]
            return 1<=len(lines[0])<=25 and bool(re.fullmatch(r"[a-z]+",lines[0])) and 1<=count<=100 and len(rows)==count and all(re.fullmatch(r"[a-z]{1,100}",row) for row in rows)
        if number == 30276:
            k,n=map(int,tokens); return len(tokens)==2 and 3<=k<=100 and 1<=n<=100 and _hanoi(k,n)<=2**31-1
        if number == 27372:
            n=int(lines[0]); words=lines[1:]
            return 1<=n<=100 and len(words)==n==len(set(words)) and all(re.fullmatch(r"[a-z]{1,50}",word) for word in words)
        if number == 27631:
            total=int(lines[0]); pos=1
            if not 1<=total<=500: return False
            for _ in range(total):
                n=int(lines[pos]); values=list(map(int,lines[pos+1].split())); pos+=2
                if not 1<=n<=100 or len(values)!=n or any(not 1<=x<=10**9 for x in values): return False
            return pos==len(lines)
        if number == 28190:
            n=int(lines[0]); values=list(map(int,lines[1:])); return 2<=n<=10**6 and len(values)==n and all(1<=x<2**31 for x in values)
        if number == 30159:
            rows,cols=map(int,lines[0].split()); clues=[list(map(int,row.split())) for row in lines[1:]]
            if not 1<=rows<=30 or not 1<=cols<=30 or len(clues)!=rows+cols: return False
            if any(not clue or clue[0]!=len(clue)-1 or any(x<=0 for x in clue[1:]) for clue in clues): return False
            if any(sum(clue[1:])+max(0,clue[0]-1)>length for clue,length in [(c,cols) for c in clues[:rows]]+[(c,rows) for c in clues[rows:]]): return False
            fixed=[clue==[1,cols] for clue in clues[:rows]]
            if any(clue not in ([0],[1,cols]) for clue in clues[:rows]): return False
            return all(clue[1:]==_runs(fixed) for clue in clues[rows:])
    except (ValueError, IndexError, TypeError):
        return False
    return False



import subprocess as _subprocess, sys as _sys, tempfile as _tempfile
from pathlib import Path as _Path
REFERENCE='# External reference: http://cs101.openjudge.cn/practice/30382/statistics/\n# Accepted submission: 52740194\n# Source: http://cs101.openjudge.cn/practice/solution/52740194/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\nfrom bisect import bisect_left\n\ndef solve():\n    # 使用 sys.stdin.read 一次性读取，防止多次 I/O 带来的开销\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n\n    s = input_data[0]\n    t = input_data[1]\n\n    n = len(s)\n    m = len(t)\n\n    # 1. 预处理 T 中每个字符出现的所有索引位置\n    char_indices = [[] for _ in range(26)]\n    ord_a = ord(\'a\')\n    for i, char in enumerate(t):\n        char_indices[ord(char) - ord_a].append(i)\n\n    # 2. 贪心计算最少需要的副本数 k\n    k = 1\n    curr_pos = 0 # 当前在 T 副本中的匹配位置\n\n    for char in s:\n        indices = char_indices[ord(char) - ord_a]\n        if not indices:\n            # S 中存在 T 中没有的字符，无法匹配\n            print("-1")\n            return\n\n        # 使用二分查找寻找当前副本中第一个大于等于 curr_pos 的字符索引\n        it = bisect_left(indices, curr_pos)\n\n        if it < len(indices):\n            # 在当前副本的剩余部分找到了\n            curr_pos = indices[it] + 1\n        else:\n            # 当前副本匹配完了，需要开启一个新副本\n            k += 1\n            curr_pos = indices[0] + 1\n\n    # 如果 1 个副本就够了，不需要任何操作\n    if k == 1:\n        print(0)\n        return\n\n    # 3. DP 计算最少操作次数\n    # 这是一个经典的“复制与粘贴”问题，目标是得到至少 k 个副本。\n    # 达到 x 个副本的最少次数等于其所有质因数之和。\n    # 由于可以超过 k，我们需要在一个范围内寻找最小值。\n\n    # 设置上限。考虑到 2^17 > 10^5，在这个范围内一定能找到最优解。\n    limit = max(k + 500, 131072)\n    if limit > 200005:\n        limit = 200005\n\n    # dp[i] 表示得到恰好 i 个副本的最少操作次数\n    # 初始值设为 i，表示 1 次复制后进行 i-1 次粘贴\n    dp = list(range(limit + 1))\n    dp[0] = 0\n    dp[1] = 0\n\n    # 状态转移：从 i 个副本出发，复制一次，粘贴 (j-1) 次，得到 i*j 个副本\n    # 总代价 = dp[i] + j\n    for i in range(2, limit // 2 + 1):\n        base_cost = dp[i]\n        # v = i * j, 则 j = v // i\n        # 这个循环类似于素数筛法，复杂度为 O(N log N)\n        for v in range(i * 2, limit + 1, i):\n            cost = base_cost + (v // i)\n            if cost < dp[v]:\n                dp[v] = cost\n\n    # 在所有大于等于 k 的副本数中找最小值\n    print(min(dp[k:]))\n\nif __name__ == "__main__":\n    solve()\n'
LANGUAGE='Python3'
NUMBER=30382
SAMPLE='abbbbbbbbb\ncbaca\n'
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
