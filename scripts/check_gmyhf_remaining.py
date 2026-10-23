#!/usr/bin/env python3
"""只读复核剩余疑点；独立算法不调用题目的参考实现，不修改测试输入或答案。"""
from __future__ import annotations

import ast
from bisect import bisect_right
from collections import Counter, defaultdict, deque
from decimal import Decimal, ROUND_HALF_EVEN
from fractions import Fraction
import hashlib
import heapq
import itertools
import json
from math import comb, cos, isfinite, isqrt, lcm, sin, tan
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def need(condition, message):
    if not condition:
        raise ValueError(message)


def exam(text):
    lines = text.splitlines()
    m, n = map(int, lines[0].split())
    need(m > 0 and n > 0, "座位尺寸必须为正")
    total = m*n
    seats = [list(map(int, line.split())) for line in lines[1:m+1]]
    need(len(seats) == m and all(len(row) == n for row in seats), "座位矩阵尺寸不符")
    need(sorted(v for row in seats for v in row) == list(range(total)), "编号不是排列")
    need(len(lines) >= 1+m+total and not any(line.strip() for line in lines[1+m+total:]),
         "答题行数不符（空答题行必须保留）")
    answers = [tuple(map(int, line.split())) for line in lines[1+m:1+m+total]]
    need(all(v in (0, 1) for row in answers for v in row), "答题符号不是0/1")
    lengths = {len(row) for row in answers if row}
    need(len(lengths) <= 1, "非空答题行长度不同，需明确缺题编码")
    similar = set()
    for i in range(m):
        for j in range(n):
            for ii, jj in ((i+1, j), (i, j+1)):
                if ii < m and jj < n and answers[seats[i][j]] == answers[seats[ii][jj]]:
                    similar.update((seats[i][j], seats[ii][jj]))
    scores = sorted((sum(a) for a in answers), reverse=True)
    excellent = max((k for k in range(total+1) if 5*k <= 2*total
                     and (k == 0 or k == total or scores[k-1] != scores[k])), default=0)
    return f"{len(similar)} {excellent}"


def cookies(text):
    lines = text.splitlines()
    need(len(lines) == 2, "饼干输入应为两行")
    children, biscuits = (list(map(int, line.split())) for line in lines)
    need(len(children) <= 100 and len(biscuits) <= 100, "人数或饼干数越界")
    need(all(0 <= v <= 100 for v in children+biscuits), "阈值或重量越界")
    # 按每个阈值的 Hall 缺额求最大匹配，不复用排序双指针参考解。
    deficit = max([0] + [sum(g >= t for g in children)-sum(s >= t for s in biscuits)
                         for t in range(101)])
    return str(len(children)-deficit)


def components(text, *, maximum=True):
    lines = text.splitlines()
    t, pos, result = int(lines[0]), 1, []
    need(t > 0, "组数必须为正；题面未给组数上限")
    for _ in range(t):
        n, m = map(int, lines[pos].split()); pos += 1
        grid = lines[pos:pos+n]; pos += n
        need(n > 0 and m > 0 and len(grid) == n and
             all(len(row) == m and set(row) <= {'W', '.'} for row in grid), "棋盘格式不符")
        parent, sizes = {}, {}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for i, row in enumerate(grid):
            for j, value in enumerate(row):
                if value != 'W':
                    continue
                key = i*m+j
                parent[key], sizes[key] = key, 1
                for ii, jj in ((i-1, j-1), (i-1, j), (i-1, j+1), (i, j-1)):
                    if 0 <= ii < n and 0 <= jj < m and ii*m+jj in parent:
                        a, b = find(key), find(ii*m+jj)
                        if a != b:
                            if sizes[a] < sizes[b]: a, b = b, a
                            parent[b] = a; sizes[a] += sizes[b]
        roots = {find(k) for k in parent}
        result.append(str(max((sizes[k] for k in roots), default=0) if maximum else len(roots)))
    need(not any(line.strip() for line in lines[pos:]), "棋盘后有多余数据")
    return '\n'.join(result)


def arbitrage(text):
    lines = text.splitlines()
    n, days = map(int, lines[0].split())
    prices = [list(map(int, line.split())) for line in lines[1:]]
    need(n >= 2 and days >= 4 and len(prices) == n and
         all(len(row) == days and min(row) > 0 for row in prices), "价格矩阵格式不符")
    profits = []
    for i in range(n):
        for j in range(i+1, n):
            differences = [a-b for a, b in zip(prices[i], prices[j])]
            total, squares, profit = 0, 0, 0
            for day, value in enumerate(differences):
                if 3 <= day < days-1:
                    variance = day*squares-total*total
                    need(variance > 0, f"套利对{i+1},{j+1}第{day+1}天历史方差为0，交易规则未定义")
                    delta = day*value-total
                    units = isqrt(delta*delta//variance)
                    profit += (1 if delta >= 0 else -1)*units*(value-differences[day+1])
                total += value; squares += value*value
            profits.append((profit, i+1, j+1))
    best = max(p[0] for p in profits)
    winners = [p for p in profits if p[0] == best]
    need(len(winners) == 1, f"最优套利对不唯一：{winners[:5]}")
    profit, i, j = winners[0]
    return f"{i} {j} {profit}"


def sma(text):
    lines = text.splitlines()
    need(len(lines) == int(lines[0])+1, "价格行数不符")
    result = []
    for line in lines[1:]:
        tokens = line.split()
        need(len(tokens) >= 5 and all(re.fullmatch(r'\d+\.\d{1,2}', x) for x in tokens),
             "收盘价必须有一位或两位小数")
        values = list(map(Decimal, tokens))
        result.append(' '.join(str((sum(values[i:i+5])/5).quantize(Decimal('.01'),
                           rounding=ROUND_HALF_EVEN)) for i in range(len(values)-4)))
    return '\n'.join(result)


def houses(text):
    lines = text.splitlines()
    need(len(lines) == 3, "房屋输入应为三行")
    n = int(lines[0]); tokens = lines[1].split(); prices = list(map(int, lines[2].split()))
    need(n > 0 and len(tokens) == len(prices) == n and min(prices) > 0, "房屋数量或价格不符")
    distances = []
    for token in tokens:
        need(re.fullmatch(r'\(-?\d+,-?\d+\)', token), "坐标对格式不符")
        x, y = map(int, token[1:-1].split(',')); distances.append(x+y)
    ratios = [Fraction(d, p) for d, p in zip(distances, prices)]

    def twice_median(values):
        s = sorted(values)
        return s[(n-1)//2]+s[n//2]

    p_mid, r_mid = twice_median(prices), twice_median(ratios)
    return str(sum(2*p < p_mid and 2*r > r_mid for p, r in zip(prices, ratios)))


def circle(text):
    values = list(map(int, text.split()))
    need(0 < values[0] <= 100000 and len(values) == values[0]+1 and min(values[1:]) >= 0,
         "点数或组数格式不符")
    return '\n'.join(str(1+comb(n, 2)+comb(n, 4)) for n in values[1:])


def holiday(text):
    lines = text.splitlines(); n = int(lines[0])
    need(0 <= n < 200 and len(lines) == n+1, "计划数不符")
    by_end = defaultdict(list)
    for line in lines[1:]:
        start, end, value = line.split()

        def date(token):
            m, d = map(int, token.split('.'))
            need(m in (1, 2) and 1 <= d <= (31 if m == 1 else 28), "无效日期")
            return (m-1)*31+d-7

        a, b = date(start), date(end)
        need(0 <= a <= 44 and 1 <= b-a+1 <= 10, "开始日期或包含起止日的时长越界")
        if b <= 44: by_end[b].append((a, int(value)))
    dp = [0]*46
    for day in range(45):
        dp[day+1] = max([dp[day]]+[dp[a]+v for a, v in by_end[day]])
    return str(dp[-1])


def equations(text):
    tokens = text.split(); n = int(tokens[0]); expressions = tokens[1:]
    need(1 <= n <= 500 and len(expressions) == n and
         all(re.fullmatch(r'[a-z](==|!=)[a-z]', e) for e in expressions), "关系式格式不符")
    # 26点传递闭包，与参考解的并查集实现交叉核对。
    reach = [1 << i for i in range(26)]
    for expr in expressions:
        if expr[1:3] == '==':
            a, b = ord(expr[0])-97, ord(expr[3])-97
            reach[a] |= 1 << b; reach[b] |= 1 << a
    for k in range(26):
        for i in range(26):
            if reach[i] & (1 << k): reach[i] |= reach[k]
    return str(not any(expr[1:3] == '!=' and reach[ord(expr[0])-97] &
                       (1 << (ord(expr[3])-97)) for expr in expressions))


def hashing(text):
    lines = text.splitlines(); size = int(lines[0])
    need(len(lines) == 2 and size > 0, "散列表输入格式不符")
    while size < 2 or any(size % i == 0 for i in range(2, isqrt(size)+1)): size += 1
    table, answers = {}, []
    offsets = list(dict.fromkeys(i*i % size for i in range(size)))
    for value in map(int, lines[1].split()):
        answer = '-'
        for offset in offsets:
            position = (value+offset) % size
            if position not in table or table[position] == value:
                table[position] = value; answer = str(position); break
        answers.append(answer)
    return ' '.join(answers)


def expression_value(expression, constants):
    """解释数学AST；不调用 eval/exec，也不执行属性访问、赋值或未知函数。"""
    functions = {'abs': abs, 'sin': sin, 'cos': cos, 'tan': tan}

    def visit(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float): return node.value
        if isinstance(node, ast.Name) and node.id in constants: return constants[node.id]
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = visit(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value
        if isinstance(node, ast.BinOp):
            a, b = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Add): return a+b
            if isinstance(node.op, ast.Sub): return a-b
            if isinstance(node.op, ast.Mult): return a*b
            if isinstance(node.op, ast.Div): return a/b
            if isinstance(node.op, ast.Pow):
                if not (abs(b) <= 10000 and (not a or abs(b)*max(1, abs(a).bit_length()
                        if isinstance(a, int) else 1024) < 1000000)):
                    raise RuntimeError("幂运算超过审核资源预算，未判定答案")
                return a**b
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in functions:
            need(len(node.args) == 1 and not node.keywords, "函数参数不符")
            return functions[node.func.id](visit(node.args[0]))
        raise ValueError("不是允许的数学表达式")

    try:
        value = visit(ast.parse(expression.strip(), mode='eval').body)
        need(type(value) in (int, float) and isfinite(value), "结果不是有限实数")
        return f'{value:.2f}'
    except (ValueError, TypeError, SyntaxError, ArithmeticError):
        return 'WRONG'


def expressions(text):
    lines = text.splitlines(); t = int(lines[0]); answers = []
    need(0 < t <= 10 and len(lines) == 1+2*t, "表达式组数不符")
    for i in range(t):
        parts = lines[1+2*i].split(); m = int(parts[0]); constants = {}
        need(0 <= m <= 3 and len(parts) == 1+2*m, "常量定义数不符")
        for name, raw in zip(parts[1::2], parts[2::2]):
            need(re.fullmatch(r'[a-zA-Z_]+', name) and re.fullmatch(r'-?\d+\.\d{2}', raw)
                 and abs(Decimal(raw)) < 100, "常量名或数值格式不符")
            constants[name] = float(raw)
        expr = lines[2+2*i]
        need(len(expr.encode()) < 300, "表达式长度越界")
        need(re.fullmatch(r'[0-9.+*/()a-zA-Z_ \-]*', expr), "表达式含题面禁用字符")
        answers.append(expression_value(expr, constants))
    return '\n'.join(answers)


def project(text):
    values = list(map(int, text.split())); n, m = values[:2]
    need(1 < n <= 3000 and 1 < m <= 3000 and len(values) == 2+3*m, "项目尺寸不符")
    edges = list(zip(values[2::3], values[3::3], values[4::3]))
    adj, indegree = [[] for _ in range(n)], [0]*n
    for a, b, w in edges:
        need(1 <= a <= n and 1 <= b <= n and a != b and w >= 0, "任务端点或时长无效")
        adj[a-1].append((b-1, w)); indegree[b-1] += 1
    queue = deque(i for i in range(n) if not indegree[i]); order = []
    prefix, suffix = [0]*n, [0]*n
    while queue:
        a = queue.popleft(); order.append(a)
        for b, w in adj[a]:
            prefix[b] = max(prefix[b], prefix[a]+w)
            indegree[b] -= 1
            if not indegree[b]: queue.append(b)
    need(len(order) == n, "依赖图有环")
    for a in reversed(order):
        suffix[a] = max([0]+[w+suffix[b] for b, w in adj[a]])
    duration = max(prefix)
    critical = sorted({(a, b) for a, b, w in edges if prefix[a-1]+w+suffix[b-1] == duration})
    return '\n'.join([str(duration)]+[f'{a} {b}' for a, b in critical])


def forbidden(text):
    lines = text.splitlines(); la, lb, k, q = map(int, lines[0].split())
    need(1 <= la <= 200000 and 1 <= lb <= 200000 and 0 <= k <= 676 and 0 <= q <= 100000,
         "字符串或询问规模越界")
    need(len(lines) == 3+k+q, "禁用词输入行数不符")
    a, b = lines[1:3]
    need(len(a) == la and len(b) == lb and re.fullmatch('[a-z]+', a) and
         re.fullmatch('[a-z]+', b), "字符串长度或字母范围不符")
    banned = set()
    for line in lines[3:3+k]:
        pair = line.split()
        need(len(pair) == 2 and all(re.fullmatch('[a-z]', v) for v in pair), "禁用组合格式不符")
        banned.add(tuple(pair))
    counts = Counter(b)
    lengths = {c: 2*sum(count for d, count in counts.items() if (c, d) not in banned) for c in set(a)}
    prefix = [0]
    for c in a: prefix.append(prefix[-1]+lengths[c])
    pending, answers = defaultdict(list), ['']*q
    for i, raw in enumerate(lines[3+k:]):
        position = int(raw)
        need(0 <= position < prefix[-1], "询问下标越界")
        index = bisect_right(prefix, position)-1
        offset = position-prefix[index]
        if offset % 2 == 0: answers[i] = a[index]
        else: pending[a[index]].append((offset//2, i))
    # 按字符和询问秩离线扫描B，不构造A×B，也不建立参考解的26份过滤字符串。
    for c, queries in pending.items():
        queries.sort(); cursor, rank = 0, 0
        for d in b:
            if (c, d) in banned: continue
            while cursor < len(queries) and queries[cursor][0] == rank:
                answers[queries[cursor][1]] = d; cursor += 1
            rank += 1
        need(cursor == len(queries), "询问未被回答")
    return '\n'.join(answers)


def lattice_distance(dx, dy, costs):
    """允许反向移动：两次斜走也能代替两次轴向移动，须保留奇偶性。"""
    a, b, c = costs
    a, b, c = min(a, b+c), min(b, a+c), min(c, a+b)
    if dx < dy: dx, dy, a, b = dy, dx, b, a
    pairs, odd = divmod(dx-dy, 2)
    return dy*c + pairs*min(2*a, 2*c) + odd*a


def part_routes(text):
    lines = text.splitlines(); costs = tuple(map(Decimal, lines[0].split()))
    need(len(lines) == 4 and len(costs) == 3 and all(Decimal('.1') <= v <= 10 for v in costs),
         "移动成本越界")
    rows = [line.split() for line in lines[1:]]
    need(all(len(row) == 3 and 1 <= len(row[0]) <= 20 and
             all(-100 < int(v) < 100 for v in row[1:]) for row in rows), "零件格式不符")
    choices = []
    for order in itertools.permutations(rows):
        route = [(0, 0)]+[(int(row[1]), int(row[2])) for row in order]+[(100, 100)]
        cost = sum(lattice_distance(abs(x-xx), abs(y-yy), costs)
                   for (x, y), (xx, yy) in zip(route, route[1:]))
        choices.append((cost, tuple(row[0] for row in order)))
    return choices


def parts(text):
    cost, names = min(part_routes(text))
    return ' '.join(names)+f'\n{cost:.2f}'


def lattice_graph_check(text):
    """以实际八方向格点图复核五个关键点的十对距离，不调用参考解。"""
    lines = text.splitlines()
    costs = tuple(map(Decimal, lines[0].split()))
    scale = 10**max(-v.as_tuple().exponent for v in costs)
    a, b, c = (int(v*scale) for v in costs)
    points = [(0, 0)]+[tuple(map(int, row.split()[1:])) for row in lines[1:]]+[(100, 100)]
    xmin, xmax = min(x for x, _ in points)-1, max(x for x, _ in points)+1
    ymin, ymax = min(y for _, y in points)-1, max(y for _, y in points)+1
    checked = 0
    for index, start in enumerate(points[:-1]):
        targets = set(points[index+1:])
        distances = {start: 0}; queue = [(0, *start)]
        while queue and targets:
            cost, x, y = heapq.heappop(queue)
            if cost != distances[x, y]: continue
            targets.discard((x, y))
            for dx, dy in itertools.product((-1, 0, 1), repeat=2):
                if not (dx or dy): continue
                xx, yy = x+dx, y+dy
                if not (xmin <= xx <= xmax and ymin <= yy <= ymax): continue
                candidate = cost+(c if dx and dy else a if dx else b)
                if candidate < distances.get((xx, yy), float('inf')):
                    distances[xx, yy] = candidate
                    heapq.heappush(queue, (candidate, xx, yy))
        for x, y in points[index+1:]:
            expected = lattice_distance(abs(x-start[0]), abs(y-start[1]), costs)*scale
            need(distances.get((x, y)) == expected, "格点图与距离公式不一致")
            checked += 1
    return checked


def separator(text):
    lines = text.splitlines(); n = int(lines[0]); names = sorted(lines[1:])
    need(2 <= n <= 1000 and n % 2 == 0 and len(names) == n and
         all(re.fullmatch('[A-Z]{1,29}', s) for s in names), "姓名格式不符")
    lo, hi = names[n//2-1:n//2+1]
    need(lo < hi, "中间两名重复，无可行分隔串")
    # 每种长度取 >=lo 的最小字符串，再验证是否小于 hi。
    for width in range(1, len(lo)+1):
        candidate = lo[:width]
        if candidate < lo:
            chars = list(candidate); index = width-1
            while index >= 0 and chars[index] == 'Z': chars[index] = 'A'; index -= 1
            if index < 0: continue
            chars[index] = chr(ord(chars[index])+1); candidate = ''.join(chars)
        if candidate < hi: return candidate
    raise ValueError("不存在分隔串")


def word_search(text):
    lines = text.splitlines(); m, n = map(int, lines[0].split()); name = lines[-1]
    need(len(lines) == m+2 and len(name) >= 2 and all(len(row) == n for row in lines[1:-1]),
         "纸条矩阵格式不符")
    found = []
    for i in range(m):
        for j in range(n):
            for di, dj in itertools.product((-1, 0, 1), repeat=2):
                if not (di or dj): continue
                ii, jj = i+(len(name)-1)*di, j+(len(name)-1)*dj
                if 0 <= ii < m and 0 <= jj < n and all(
                        lines[1+i+k*di][j+k*dj] == c for k, c in enumerate(name)):
                    found.append((i+1, j+1, di, dj))
    need(len(found) == 1, f"纸条匹配数为{len(found)}，答案不唯一")
    i, j, di, dj = found[0]
    return f'{i} {j}\n{di} {dj}'


def ladder(text):
    lines = text.splitlines(); n = int(lines[0]); words = lines[1:n+1]
    need(2 <= n <= 4000 and len(words) == n and len(set(words)) == n and
         all(re.fullmatch('[a-z]{4}|[A-Z]{4}', w) for w in words), "词典格式不符")
    start, end = lines[n+1].split(); need(start in words and end in words, "词梯端点不在词典")
    buckets = defaultdict(list)
    for word in words:
        for k in range(4): buckets[word[:k]+'*'+word[k+1:]].append(word)
    distance, ways, previous = {start: 0}, {start: 1}, {}
    queue = deque([start])
    while queue:
        a = queue.popleft()
        for k in range(4):
            for b in buckets[a[:k]+'*'+a[k+1:]]:
                if b not in distance:
                    distance[b] = distance[a]+1; ways[b] = 0; previous[b] = a; queue.append(b)
                if distance[b] == distance[a]+1: ways[b] = min(2, ways[b]+ways[a])
    if end not in distance: return 'NO'
    need(ways[end] == 1, "最短词梯不唯一")
    path = [end]
    while path[-1] != start: path.append(previous[path[-1]])
    return ' '.join(reversed(path))


def linear_system(text):
    lines = text.splitlines(); n = int(lines[0])
    matrix = [list(map(Fraction, line.split())) for line in lines[1:]]
    need(n >= 2 and len(matrix) == n and all(len(row) == n+1 for row in matrix), "增广矩阵尺寸不符")
    # 逐行清除分母，Bareiss 消元避免大矩阵的 Fraction 运算膨胀。
    for i, row in enumerate(matrix):
        denominator = lcm(*(v.denominator for v in row))
        matrix[i] = [int(v*denominator) for v in row]
    previous = 1
    for col in range(n-1):
        pivot = next((i for i in range(col, n) if matrix[i][col]), None)
        need(pivot is not None, "方程组没有唯一解")
        matrix[col], matrix[pivot] = matrix[pivot], matrix[col]
        factor = matrix[col][col]
        for i in range(col+1, n):
            coefficient = matrix[i][col]
            for j in range(col+1, n+1):
                numerator = matrix[i][j]*factor-coefficient*matrix[col][j]
                quotient, remainder = divmod(numerator, previous)
                need(remainder == 0, "消元整除不变量失败")
                matrix[i][j] = quotient
            matrix[i][col] = 0
        previous = factor
    need(matrix[-1][-2] != 0, "方程组没有唯一解")
    solution = [Fraction(0)]*n
    for i in reversed(range(n)):
        solution[i] = (matrix[i][-1]-sum(matrix[i][j]*solution[j] for j in range(i+1, n)))/Fraction(matrix[i][i])
    return '\n'.join(f'x{i+1} = {float(solution[i]):.2f}' for i in range(n))


def island(text):
    lines = text.splitlines(); n, m = map(int, lines[0].split())
    grid = [list(map(int, row.split())) for row in lines[1:]]
    need(1 <= n <= 100 and 1 <= m <= 100 and len(grid) == n and
         all(len(row) == m and set(row) <= {0, 1} for row in grid), "岛屿矩阵格式不符")
    land = {(i, j) for i in range(n) for j in range(m) if grid[i][j]}
    need(land, "没有岛屿")

    def flood(start, allowed):
        seen = {start}; queue = [start]
        while queue:
            i, j = queue.pop()
            for v in ((i-1, j), (i+1, j), (i, j-1), (i, j+1)):
                if v in allowed and v not in seen: seen.add(v); queue.append(v)
        return seen

    need(len(flood(next(iter(land)), land)) == len(land), "陆地不是一个连通岛屿")
    water = {(i, j) for i in range(-1, n+1) for j in range(-1, m+1)}-land
    need(len(flood((-1, -1), water)) == len(water), "岛内有湖")
    return str(sum(v not in land for i, j in land for v in ((i-1,j),(i+1,j),(i,j-1),(i,j+1))))


SOLVERS = {16531: exam, 18104: cookies, 18160: components, 18177: arbitrage, 19493: sma,
           19963: houses, 20102: circle, 23568: holiday, 28276: equations, 29468: hashing,
           30162: expressions, 30899: project, 31069: forbidden, 30281: parts,
           16530: separator, 20135: word_search, 28046: ladder,
           18108: lambda text: components(text, maximum=False), 20138: linear_system, 12558: island}


def compare(number, actual, expected):
    if number == 19493:
        return [Decimal(x) for x in actual.split()] == [Decimal(x) for x in expected.split()]
    return actual.split() == expected.split()


def review():
    rows = json.loads((ROOT/'collab/gmyhf-download-materialize.json').read_text())['materialized']
    results = []
    for row in rows:
        number = row['global_number']
        if number not in SOLVERS and number not in (30159, 30160): continue
        directory = ROOT/'data/openjudge/tests'/row['bucket']/(row['local_id']+'_GMyhf/data')
        files = []
        for path in sorted(directory.glob('*.in'), key=lambda p: int(p.stem)):
            source, output = path.read_bytes(), path.with_suffix('.out').read_bytes()
            record = {'input': str(path.relative_to(ROOT)), 'input_sha256': hashlib.sha256(source).hexdigest(),
                      'output_sha256': hashlib.sha256(output).hexdigest()}
            try:
                text = source.decode('utf-8-sig').replace('\r\n', '\n')
                if number in (30159, 30160):
                    from check_gmyhf_supplemental_answers import nonogram
                    proved = nonogram(text, output.decode())
                    record['unique_proved'] = proved
                    if not proved:
                        record['unproved'] = '提示传播未能证明唯一解；不据此判定多解'
                        files.append(record)
                        continue
                    actual = output.decode()
                else:
                    actual = SOLVERS[number](text)
                record['matches'] = compare(number, actual, output.decode())
                if number == 30281:
                    choices = part_routes(source.decode())
                    best = min(cost for cost, _ in choices)
                    recorded = output.decode().split()
                    record['optimal_orders'] = [list(names) for cost, names in choices if cost == best]
                    record['matches'] = (len(recorded) == 4 and Decimal(recorded[-1]) == best and
                                         recorded[:3] in record['optimal_orders'])
                if not record['matches']:
                    record.update(expected=actual, recorded=output.decode())
            except RuntimeError as exc:
                record['unproved'] = str(exc)
            except AssertionError as exc:
                record['answer_issue'] = str(exc)
            except (ValueError, IndexError, StopIteration) as exc:
                record['input_issue'] = str(exc)
            files.append(record)
        results.append({'global_number': number, 'cases': len(files), 'files': files})
    return {'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'entries': results}


if __name__ == '__main__':
    if sys.argv[1:] == ['--lattice']:
        rows = json.loads((ROOT/'collab/gmyhf-download-materialize.json').read_text())['materialized']
        row = next(row for row in rows if row['global_number'] == 30281)
        directory = ROOT/'data/openjudge/tests'/row['bucket']/(row['local_id']+'_GMyhf/data')
        checks = [{'input': str(path.relative_to(ROOT)), 'input_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                   'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   'pairs': lattice_graph_check(path.read_text()),
                   'graph_dijkstra_matches': True} for path in sorted(directory.glob('*.in'))]
        print(json.dumps(checks, ensure_ascii=False, indent=2))
    elif not sys.argv[1:]:
        print(json.dumps(review(), ensure_ascii=False, indent=2))
    else:
        raise SystemExit('用法：check_gmyhf_remaining.py [--lattice]')
