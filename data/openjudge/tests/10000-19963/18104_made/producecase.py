#!/usr/bin/env python3
"""Problem-specific generators and input contracts for T-028 phase-2 round 20."""
from __future__ import annotations

import random
import re


NUMBERS = {4071, 4072, 4113, 4041, 4045, 4069, 4070, 4073, 4096, 4098,
           27623, 4095, 4097, 12555, 12557, 18104, 18105, 18107, 27072, 4094}
EXEMPTIONS = {}
INPUT_DOMAINS = {
    4071: "第一行是一个正整数n(1<=n<=100)，表示下面要进行查找的字符串的数量。",
    4072: "第一行是测试的组数T(1<=T<=100)，其后是T组数据",
    4113: "第一行是一个整数cases（1<=cases<=10），表示测试数据的个数。",
    4041: "所有元素都是整数，矩阵的行和列大小不超过100",
    4045: "输入为一行,正整数n,(n<300)",
    4069: "一个手机有四个信息，都是非负整数，分别为产品 id 、价格、销售量、平均得分。四个属性取值都在 10000 以内。",
    4070: "现在给你一个正整数 n ， n 小于 8",
    4073: "每个字符串的长度不超过200。",
    4096: "只有一行数据，由一串字符信号组成，长度小于500。",
    4098: "（2<=N<=50）（输入保证没有价值相同的水果）",
    27623: "每组数据一行，包含两个正整数a和b，表示初始时石子的数目。( a,b <= 10^9 )",
    4095: "第一行输入一个数字 n (n<1000),表示共有多少个需要处理的车站名。",
    4097: "第一行 n,表示该地铁线路有 n(n<100)个地铁站。",
    12555: "输入的第一行是一个整数n (1<= n <= 300000)。",
    12557: "输入为两行。 分别为两个版本号，不含空格。",
    18104: "饼干与小孩的个数不一定相等(均小于等于100)",
    18105: "一行，每个数值之间用空格隔开。",
    18107: "第一行是一个整数 T (T <= 50) ，表示一共有 T 组数据。",
    27072: "对于 100% 的数据，n≤100,000",
    4094: "第一行为两个数字 n 和 s,n(n<10000)表示共有多少辆装有重要人士的地铁",
}
SAMPLE_INPUTS = {}
SAMPLE_OUTPUTS = {}
LABELS = {
    4071: "1..100 text rows end in a non-space character and a separated positive occurrence count",
    4072: "1..100 groups each contain 1..100 distinct finite integer-coordinate points",
    4113: "1..10 cases contain 1..2 acyclic lines of 2..20 stations and 1..10 reachable queries",
    4041: "two integer matrices have positive dimensions at most 100 and exact row widths",
    4045: "the input is one positive integer less than 300",
    4069: "each phone group has 1..50 bounded nonnegative records, unique preference triples and an affordable phone",
    4070: "one or more permutation sizes in 1..7 are followed by the zero terminator",
    4073: "each group has 1..200 nonblank strings of length at most 200 and the input ends with zero",
    4096: "the single signal is a 1..499-character string over A, B, C and D",
    4098: "1..99 groups contain 2..50 nonnegative fruit records with pairwise distinct values",
    27623: "positive stone-pile pairs at most 10^9 are followed by the 0 0 terminator",
    4095: "1..999 alphabetic station names have lengths in 1..100",
    4097: "2..99 unique alphabetic stations precede 1..99 valid direction queries",
    12555: "1..300000 finite decimal sample values follow the declared sample count",
    12557: "exactly two dot-separated numeric version strings contain no spaces",
    18104: "two nonempty rows each contain at most 100 positive weights in 1..100",
    18105: "the single nonempty row contains nonnegative integer citation counts",
    18107: "1..50 ordered integer intervals follow the declared case count",
    27072: "the input is one integer n in 1..100000",
    4094: "1..9999 trains have nonnegative integer departure times and positive integer speeds with int-range arrivals",
}
INVALID = {
    4071: "1\nends with space 2 \n", 4072: "101\n", 4113: "0\n",
    4041: "2 2\n1 2\n3\n1 1\n4\n", 4045: "300\n",
    4069: "1\n5 1\n1 6 2 3\n", 4070: "8\n0\n", 4073: "1\n\n0\n",
    4096: "ABCE\n", 4098: "1\n2\n1 1 1\n2 0 2\n",
    27623: "1 2\n0 1\n", 4095: "1\nStation2\n", 4097: "2\nA\nA\n1\nA A\n",
    12555: "2\n1\n", 12557: "1.a\n2.0\n", 18104: "0\n1\n",
    18105: "1 -1 2\n", 18107: "1\n5 4\n", 27072: "100001\n",
    4094: "1 100\n0 0\n",
}


def _name(value: int) -> str:
    value += 1
    out = ""
    while value:
        value, digit = divmod(value - 1, 26)
        out = chr(65 + digit) + out
    return "Station" + out


def generate(number: int, seed: int) -> str:
    r = random.Random(number * 1_000_003 + seed)
    if number == 4071:
        n = r.randint(1, 12)
        rows = []
        alphabet = "abcXYZ  !?"
        for _ in range(n):
            text = "".join(r.choice(alphabet) for _ in range(r.randint(1, 80))).rstrip() + r.choice("abcXYZ!?")
            rows.append(f"{text} {r.randint(1, max(1, len(text)))}")
        return f"{n}\n" + "\n".join(rows) + "\n"
    if number == 4072:
        groups = []
        for group in range(r.randint(1, 8)):
            n = 100 if seed == 20 and group == 0 else r.randint(1, 20)
            x0, y0, dx, dy = r.randint(-1000, 1000), r.randint(-1000, 1000), r.randint(1, 9), r.randint(1, 9)
            points = [(x0 + i * dx, y0 + i * dy) for i in range(n)]
            if n > 2 and (seed + group) % 2:
                points[-1] = (points[-1][0], points[-1][1] + 1)
            groups.append(str(n) + "\n" + "\n".join(f"{x} {y}" for x, y in points))
        return f"{len(groups)}\n" + "\n".join(groups) + "\n"
    if number == 4113:
        blocks = []
        case_count = r.randint(1, 3)
        for case in range(case_count):
            line_count = 2 if (seed + case) % 2 else 1
            hub = _name(seed * 1000 + case * 100)
            lines, stations = [], {hub}
            for line in range(line_count):
                m = r.randint(2, 8)
                names = [hub] + [_name(seed * 1000 + case * 100 + line * 20 + i + 1) for i in range(m - 1)]
                stations.update(names)
                tokens = [str(m), names[0]]
                for name in names[1:]:
                    tokens.extend((str(r.randint(100, 20000)), name))
                lines.append(" ".join(tokens))
            queries = [f"{a} {b}" for a, b in (r.sample(sorted(stations), 2) for _ in range(r.randint(1, 10)))]
            blocks.append(f"{line_count} {len(queries)}\n" + "\n".join(lines + queries))
        return f"{case_count}\n" + "\n".join(blocks) + "\n"
    if number == 4041:
        m = r.randint(1, 8); k = r.randint(1, 7)
        compatible = seed % 2 == 0
        k1 = k if compatible else k + 1
        n = r.randint(1, 8)
        a = [[r.randint(-50, 50) for _ in range(k)] for _ in range(m)]
        b = [[r.randint(-50, 50) for _ in range(n)] for _ in range(k1)]
        return (f"{m} {k}\n" + "\n".join(" ".join(map(str, row)) for row in a) +
                f"\n{k1} {n}\n" + "\n".join(" ".join(map(str, row)) for row in b) + "\n")
    if number == 4045:
        return f"{299 if seed == 20 else (seed * 37) % 299 + 1}\n"
    if number == 4069:
        groups = []
        for group in range(r.randint(1, 8)):
            budget = r.randint(0, 9999); n = r.randint(1, 50)
            triples, rows = set(), []
            for index in range(n):
                while True:
                    price, sales, rating = (r.randint(0, 9999) for _ in range(3))
                    if (price, sales, rating) not in triples:
                        triples.add((price, sales, rating)); break
                rows.append([group * 100 + index, price, sales, rating])
            rows[0][1] = min(rows[0][1], budget)
            groups.append(f"{budget} {n}\n" + "\n".join(" ".join(map(str, row)) for row in rows))
        return f"{len(groups)}\n" + "\n".join(groups) + "\n"
    if number == 4070:
        values = list(range(1, 8)); r.shuffle(values)
        values = values[:r.randint(1, 4)]
        if seed == 20: values[-1] = 7
        return "\n".join(map(str, values + [0])) + "\n"
    if number == 4073:
        blocks = []
        for group in range(r.randint(1, 6)):
            n = r.randint(1, 30); suffix = "".join(r.choice("abcXYZ") for _ in range(r.randint(0, 20)))
            strings = ["".join(r.choice("abcXYZ") for _ in range(r.randint(1, 30))) + suffix for _ in range(n)]
            blocks.append(f"{n}\n" + "\n".join(strings))
        return "\n".join(blocks + ["0"]) + "\n"
    if number == 4096:
        length = 499 if seed == 20 else r.randint(1, 200)
        return "".join(r.choice("ABCD") for _ in range(length)) + "\n"
    if number == 4098:
        blocks = []
        for group in range(r.randint(1, 8)):
            n = r.randint(2, 50); values = r.sample(range(20000), n)
            rows = []
            for index, value in enumerate(values):
                a = r.randint(0, value); rows.append(f"{group * 100 + index} {a} {value - a}")
            blocks.append(f"{n}\n" + "\n".join(rows))
        return f"{len(blocks)}\n" + "\n".join(blocks) + "\n"
    if number == 27623:
        rows = [f"{r.randint(1, 10**9)} {r.randint(1, 10**9)}" for _ in range(r.randint(1, 12))]
        return "\n".join(rows + ["0 0"]) + "\n"
    if number == 4095:
        n = 999 if seed == 20 else r.randint(1, 100)
        names = ["".join(r.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(r.randint(1, 100))) for _ in range(n)]
        return f"{n}\n" + "\n".join(names) + "\n"
    if number == 4097:
        n = 99 if seed == 20 else r.randint(2, 40)
        names = [_name(seed * 200 + i) for i in range(n)]
        m = r.randint(1, 99)
        queries = [" ".join(r.sample(names, 2)) for _ in range(m)]
        return f"{n}\n" + "\n".join(names) + f"\n{m}\n" + "\n".join(queries) + "\n"
    if number == 12555:
        n = 30000 if seed == 20 else r.randint(1, 1000)
        values = [str(r.randint(-100000, 100000)) for _ in range(n)]
        return f"{n}\n" + " ".join(values) + "\n"
    if number == 12557:
        first = [r.randint(0, 9999) for _ in range(r.randint(1, 8))]
        second = [r.randint(0, 9999) for _ in range(r.randint(1, 8))]
        if first == second: second[-1] += 1
        return ".".join(map(str, first)) + "\n" + ".".join(map(str, second)) + "\n"
    if number == 18104:
        children = [r.randint(1, 100) for _ in range(r.randint(1, 100))]
        cookies = [r.randint(1, 100) for _ in range(r.randint(1, 100))]
        return " ".join(map(str, children)) + "\n" + " ".join(map(str, cookies)) + "\n"
    if number == 18105:
        n = r.randint(1, 300)
        values = ([0] * n if seed % 5 == 0 else [r.randint(0, 1000) for _ in range(n)])
        return " ".join(map(str, values)) + "\n"
    if number == 18107:
        rows = []
        for _ in range(r.randint(1, 50)):
            left = r.randint(-100, 5000); right = r.randint(left, 5000)
            rows.append(f"{left} {right}")
        return f"{len(rows)}\n" + "\n".join(rows) + "\n"
    if number == 27072:
        return f"{100000 if seed == 20 else (seed * 4999) % 99999 + 1}\n"
    if number == 4094:
        n = 9999 if seed == 20 else r.randint(1, 300)
        distance = r.randint(1, 10**6)
        rows = [f"{r.randint(0, 10**6)} {r.randint(1, 10000)}" for _ in range(n)]
        return f"{n} {distance}\n" + "\n".join(rows) + "\n"
    raise KeyError(number)


def valid(number: int, text: str) -> bool:
    try:
        lines = text.rstrip("\n").splitlines(); tokens = text.split()
        if number == 4071:
            n = int(lines[0]); rows = lines[1:]
            return 1 <= n <= 100 and len(rows) == n and all(
                row and not row.endswith(" ") and re.fullmatch(r".* \d+", row) and
                int(row.rsplit(" ", 1)[1]) > 0 for row in rows)
        if number == 4072:
            t = int(tokens[0]); pos = 1
            if not 1 <= t <= 100: return False
            for _ in range(t):
                n = int(tokens[pos]); pos += 1
                if not 1 <= n <= 100: return False
                points = [(int(tokens[pos + 2*i]), int(tokens[pos + 2*i + 1])) for i in range(n)]
                pos += 2*n
                if len(set(points)) != n: return False
            return pos == len(tokens)
        if number == 4113:
            cases = int(tokens[0]); pos = 1
            if not 1 <= cases <= 10: return False
            for _ in range(cases):
                line_count, query_count = map(int, tokens[pos:pos+2]); pos += 2
                if not 1 <= line_count <= 2 or not 1 <= query_count <= 10: return False
                graph = {}
                for _ in range(line_count):
                    m = int(tokens[pos]); pos += 1
                    if not 2 <= m <= 20: return False
                    previous = tokens[pos]; pos += 1; graph.setdefault(previous, set())
                    for _ in range(m-1):
                        distance, station = int(tokens[pos]), tokens[pos+1]; pos += 2
                        if distance <= 0: return False
                        graph.setdefault(station, set()); graph[previous].add(station); graph[station].add(previous); previous = station
                for _ in range(query_count):
                    if tokens[pos] not in graph or tokens[pos+1] not in graph: return False
                    pos += 2
            return pos == len(tokens)
        if number == 4041:
            m, k = map(int, lines[0].split()); split = 1 + m
            a = [row.split() for row in lines[1:split]]
            k1, n = map(int, lines[split].split()); b = [row.split() for row in lines[split+1:]]
            return (1 <= m <= 100 and 1 <= k <= 100 and 1 <= k1 <= 100 and 1 <= n <= 100 and
                    len(a) == m and all(len(row) == k and all(re.fullmatch(r"-?\d+", x) for x in row) for row in a) and
                    len(b) == k1 and all(len(row) == n and all(re.fullmatch(r"-?\d+", x) for x in row) for row in b))
        if number == 4045: return len(tokens) == 1 and 0 < int(tokens[0]) < 300
        if number == 4069:
            m = int(tokens[0]); pos = 1
            if m < 1: return False
            for _ in range(m):
                budget, n = map(int, tokens[pos:pos+2]); pos += 2
                if not 0 <= budget < 10000 or not 1 <= n <= 50: return False
                rows = [tuple(map(int, tokens[pos+4*i:pos+4*i+4])) for i in range(n)]; pos += 4*n
                if any(any(not 0 <= value < 10000 for value in row) for row in rows): return False
                if len({row[1:] for row in rows}) != n or not any(row[1] <= budget for row in rows): return False
            return pos == len(tokens)
        if number == 4070:
            values = list(map(int, tokens)); return len(values) >= 2 and values[-1] == 0 and all(1 <= n < 8 for n in values[:-1])
        if number == 4073:
            pos = 0; groups = 0
            while pos < len(tokens):
                n = int(tokens[pos]); pos += 1
                if n == 0: return groups > 0 and pos == len(tokens)
                if not 1 <= n <= 200 or pos + n > len(tokens): return False
                if any(not 1 <= len(value) <= 200 for value in tokens[pos:pos+n]): return False
                pos += n; groups += 1
            return False
        if number == 4096: return bool(re.fullmatch(r"[ABCD]{1,499}\n?", text))
        if number == 4098:
            m = int(tokens[0]); pos = 1
            if not 1 <= m < 100: return False
            for _ in range(m):
                n = int(tokens[pos]); pos += 1
                if not 2 <= n <= 50: return False
                rows = [tuple(map(int, tokens[pos+3*i:pos+3*i+3])) for i in range(n)]; pos += 3*n
                if any(any(value < 0 for value in row) for row in rows) or len({a+b for _, a, b in rows}) != n: return False
            return pos == len(tokens)
        if number == 27623:
            rows = [tuple(map(int, row.split())) for row in lines]
            return len(rows) >= 2 and rows[-1] == (0, 0) and all(len(row) == 2 and 1 <= row[0] <= 10**9 and 1 <= row[1] <= 10**9 for row in rows[:-1])
        if number == 4095:
            n = int(lines[0]); return 1 <= n < 1000 and len(lines) == n+1 and all(1 <= len(x) <= 100 and x.isascii() and x.isalpha() for x in lines[1:])
        if number == 4097:
            n = int(lines[0]); names = lines[1:n+1]; m = int(lines[n+1]); queries = lines[n+2:]
            return (2 <= n < 100 and len(set(names)) == n and all(1 <= len(x) <= 100 and x.isascii() and x.isalpha() for x in names) and
                    1 <= m < 100 and len(queries) == m and all(len(q.split()) == 2 and all(x in names for x in q.split()) for q in queries))
        if number == 12555:
            n = int(lines[0]); values = list(map(float, lines[1].split()))
            return len(lines) == 2 and 1 <= n <= 300000 and len(values) == n and all(value == value and abs(value) != float("inf") for value in values)
        if number == 12557: return len(lines) == 2 and all(re.fullmatch(r"\d+(?:\.\d+)*", line) for line in lines)
        if number == 18104:
            return len(lines) == 2 and all(1 <= len(row.split()) <= 100 and all(1 <= int(x) <= 100 for x in row.split()) for row in lines)
        if number == 18105: return len(lines) == 1 and bool(tokens) and all(re.fullmatch(r"\d+", x) for x in tokens)
        if number == 18107:
            t = int(lines[0]); rows = [list(map(int, row.split())) for row in lines[1:]]
            return 1 <= t <= 50 and len(rows) == t and all(len(row) == 2 and row[0] <= row[1] for row in rows)
        if number == 27072: return len(tokens) == 1 and 1 <= int(tokens[0]) <= 100000
        if number == 4094:
            n, distance = map(int, lines[0].split()); rows = [list(map(int, row.split())) for row in lines[1:]]
            return (1 <= n < 10000 and 0 < distance <= 2**31-1 and len(rows) == n and
                    all(len(row) == 2 and row[0] >= 0 and row[1] > 0 and row[0] + distance // row[1] <= 2**31-1 for row in rows))
    except (ValueError, IndexError, TypeError, ZeroDivisionError):
        return False
    return False



import subprocess as _subprocess, sys as _sys, tempfile as _tempfile
from pathlib import Path as _Path
REFERENCE='# External reference: http://cs101.openjudge.cn/practice/18104/statistics/\n# Accepted submission: 52523211\n# Source: http://cs101.openjudge.cn/practice/solution/52523211/\n# License: not declared on the submission page; no license is inferred.\n\ns = sorted(list(map(int,input().split())))+[float("inf")]\np = sorted(list(map(int,input().split())))\nj = 0\nfor pi in p:\n    if pi >= s[j]:\n        j += 1\nprint(j)\n'
LANGUAGE='Python3'
NUMBER=18104
SAMPLE='1 2 3\n1 1\n'
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
