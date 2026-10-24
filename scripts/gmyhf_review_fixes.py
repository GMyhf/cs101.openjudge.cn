"""审核后确定性派生合法输入；保留原件，答案由已审核的整数参考重算。"""
import ast
import json


def repair_input(number, payload):
    text = payload.decode()
    if number == 25685:
        values = list(map(int, text.split()))
        m, wealth = values[0], values[1:]
        assert m >= 0 and 2 <= len(wealth) <= 1000 and min(wealth) >= m
        if len(set(wealth)) == len(wealth):
            return payload
        # 按原财富及输入位置稳定排序，仅在相邻值冲突时递增至最近合法整数。
        fixed = wealth[:]
        previous = m - 1
        for i in sorted(range(len(wealth)), key=lambda i: (wealth[i], i)):
            fixed[i] = max(wealth[i], previous + 1)
            previous = fixed[i]
        assert len(set(fixed)) == len(fixed) and min(fixed) >= m
        return (str(m) + '\n' + ' '.join(map(str, fixed)) + '\n').encode()
    if number == 25579:
        values = list(map(int, text.split()))
        n = values[0]
        assert 3 <= n <= 100 and len(values) == 1 + 2 * n
        rows = [values[1:1+n], values[1+n:]]
        assert all(x >= 0 for row in rows for x in row)
        if all(min(row) > 0 for row in rows):
            return payload
        # 每支含零股价的股票整体加一，保留该股票所有买卖价差及最优收益。
        rows = [[x + (min(row) == 0) for x in row] for row in rows]
        return (str(n) + '\n' + '\n'.join(' '.join(map(str, row)) for row in rows) + '\n').encode()
    if number == 19964:
        values = list(map(int, text.split()))
        n = values[0]
        assert n >= 3 and len(values) == 1 + 2 * n
        if n <= 10:
            return payload
        # 两组各取前十人，不能把前一组被裁掉的成员混进后一组。
        return ('10\n' + ' '.join(map(str, values[1:11])) + '\n' +
                ' '.join(map(str, values[n + 1:n + 11])) + '\n').encode()
    if number == 19968:
        a, b = text.split()
        assert len(a) == len(b) and a and set(a + b) <= {'0', '1'}
        if len(a) < 30:
            return payload
        return (a[:29] + '\n' + b[:29] + '\n').encode()
    if number == 30825:
        values = list(map(int, text.split()))
        n, w, k = values[:3]
        assert 1 <= n <= 200000 and len(values) == n + 3
        assert all(1 <= x <= 10**9 for x in values[3:])
        assert 1 <= w <= n and k >= 1
        if k <= w:
            return payload
        return (f'{n} {w} {w}\n' + ' '.join(map(str, values[3:])) + '\n').encode()
    if number == 30920:
        n, m = map(int, text.split())
        assert 2 <= n <= 10**12 and 1 <= m <= 10**12
        if m >= 2:
            return payload
        return f'{n} 2\n'.encode()
    if number == 27945:
        lines = text.splitlines()
        rows = [list(map(int, line.split())) for line in lines[1:]]
        assert 1 <= len(rows) <= 3500 and all(rows)
        assert all(row == sorted(row) for row in rows)
        if int(lines[0]) == len(rows):
            return payload
        return (str(len(rows)) + '\n' + '\n'.join(lines[1:]) + '\n').encode()
    if number == 28014:
        lines = text.splitlines()
        operations = lines[1:]
        assert 1 <= len(operations) <= 1000
        for line in operations:
            tokens = line.split()
            assert tokens == ['popSmallest'] or (len(tokens) == 2 and tokens[0] == 'addBack' and 1 <= int(tokens[1]) <= 1000)
        if int(lines[0]) == len(operations):
            return payload
        return (str(len(operations)) + '\n' + '\n'.join(operations) + '\n').encode()
    if number == 28191:
        values = list(map(int, text.split()))
        n = values[0]
        heights, energies = values[1::2], values[2::2]
        assert 1 <= n <= 10**6 and len(values) == 2 * n + 1
        assert len(set(heights)) == n and all(1 <= x <= 10**9 for x in heights)
        assert all(x >= 1 for x in energies)
        factor = (max(energies) + 9999) // 10000
        if factor == 1:
            return payload
        # 整组同比例缩放，保留能量差异，避免大量截断为相同的上界。
        energies = [(x + factor - 1) // factor for x in energies]
        assert sum(energies) < 2**31
        return (str(n) + '\n' + '\n'.join(f'{h} {v}' for h, v in zip(heights, energies)) + '\n').encode()
    if number == 28339:
        values = list(map(int, text.split()))
        assert len(values) >= 2 and all(1 <= x <= 10**9 for x in values)
        if len(values) <= 50000:
            return payload
        return (' '.join(map(str, values[:50000])) + '\n').encode()
    if number == 29905:
        values = list(map(int, text.split()))
        n, m = values[:2]
        distances = values[2:]
        assert 1 <= m <= n < 200 and all(1 <= x <= 100 for x in distances)
        assert len(distances) in (n - 1, n)
        if len(distances) == n - 1:
            return payload
        return (f'{n} {m}\n' + ' '.join(map(str, distances[:n-1])) + '\n').encode()
    if number == 21471:
        values = list(map(int, text.split()))
        n = values[0]
        assert n >= 1 and len(values) == 1 + n * n
        if n <= 20:
            return payload
        rows = [values[1+i*n:1+i*n+20] for i in range(20)]
        return ('20\n' + '\n'.join(' '.join(map(str,row)) for row in rows) + '\n').encode()
    if number == 25563:
        values = list(map(int, text.split()))
        n, m = values[:2]
        scores = values[2:]
        assert 1 < n < 50000 and 1 <= m <= n and len(scores) == n
        assert all(1 <= x < 1000 for x in scores)
        if min(scores) > 1:
            return payload
        return (f'{n} {m}\n' + ' '.join(str(max(x,2)) for x in scores) + '\n').encode()
    if number == 25577:
        tokens = text.split()
        if len(tokens) == 1:
            assert int(tokens[0]) >= 0
            return payload
        # 混入了其他题输入，替换为自产的高精度锚点，不猜测原文件含义。
        return b'10000\n'
    if number == 27946:
        lines = text.splitlines()
        values = list(map(int,lines[0].split()))
        index, distance = map(int,' '.join(lines[1:]).split())
        assert 2 <= len(values) <= 100000 and 1 <= index <= len(values) and 0 <= distance <= 1000
        if all(-1000 <= x <= 1000 for x in values):
            return payload
        # 范围出自hint的Constraints，同属当前题面；参数保持。
        values = [min(1000,max(-1000,x)) for x in values]
        return (' '.join(map(str,values)) + f'\n{index}\n{distance}\n').encode()
    if number == 30177:
        values = list(map(int,text.split()))
        m,k = values[:2]
        coins = values[2:2+m]
        assert 1 <= m <= 10 and 1 <= k <= 10 and len(set(coins)) == m
        assert len(coins) == m and coins[0] == 1 and all(1 <= x <= 100 for x in coins)
        if len(values) == 2+m:
            return payload
        # 单组输入只保留声明的m个面值，移除串接在末尾的额外内容。
        return (f'{m} {k}\n' + ' '.join(map(str,coins)) + '\n').encode()
    if number == 28187:
        values = list(map(int,text.split()))
        n = values[0]
        assert 2 <= n <= 100000 and len(values)%2 == 1
        parent = list(range(n+1))
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        edges = []
        for u,v in zip(values[1::2],values[2::2]):
            if 1 <= u <= n and 1 <= v <= n:
                ru,rv = find(u),find(v)
                if ru != rv:
                    edges.append((u,v))
                    parent[rv] = ru
        if len(edges) == n-1 and len(values) == 2*n-1:
            return payload
        for v in range(2,n+1):
            ru,rv = find(1),find(v)
            if ru != rv:
                edges.append((1,v))
                parent[rv] = ru
        assert len(edges) == n-1 and all(find(v)==find(1) for v in range(1,n+1))
        return (str(n)+'\n'+'\n'.join(f'{u} {v}' for u,v in edges)+'\n').encode()
    if number == 28188:
        values = list(map(int,text.split()))
        n = values[0]
        kinds,parents = values[1:n+1],values[n+1:]
        assert 1 <= n <= 100000 and len(values) == 2*n+1
        assert all(t in (0,1) for t in kinds) and 1 in kinds and all(0 <= p <= n for p in parents)
        fixed = [p if not p or not kinds[p-1] else 0 for p in parents]
        if fixed == parents:
            return payload
        return (str(n)+'\n'+' '.join(map(str,kinds))+'\n'+' '.join(map(str,fixed))+'\n').encode()
    if number == 28189:
        values = list(map(int,text.split()))
        t = values[0]
        assert 1 <= t <= 1000
        at,cases,total = 1,[],0
        for _ in range(t):
            n = values[at]
            a,b = values[at+1:at+1+n],values[at+1+n:at+1+2*n]
            assert 1 <= n <= 1000 and len(a) == len(b) == n and all(1 <= x <= 1000 for x in a+b)
            cases.append((n,a,b));total += n;at += 1+2*n
        assert at == len(values)
        if total <= 1000:
            return payload
        kept,total = [],0
        for case in cases:
            if total+case[0] > 1000:
                break
            kept.append(case);total += case[0]
        assert kept and total <= 1000
        rows = [str(len(kept))]
        for n,a,b in kept:
            rows += [str(n),' '.join(map(str,a)),' '.join(map(str,b))]
        return ('\n'.join(rows)+'\n').encode()
    if number == 28682:
        tokens = text.split()
        n,m = map(int,tokens[:2])
        assert 2 <= n <= 100000 and 1 <= m <= 100000 and len(tokens) == 2+2*(n+m)
        people = [(int(tokens[2+2*i]),tokens[3+2*i]) for i in range(n)]
        operations = [tuple(map(int,tokens[2+2*n+2*i:4+2*n+2*i])) for i in range(m)]
        assert all(d in (0,1) and 1 <= len(name) <= 10 and name.isascii() and name.isalpha() for d,name in people)
        assert all(d in (0,1) and 1 <= steps <= n for d,steps in operations)
        fixed_operations = [(d,min(steps,n-1)) for d,steps in operations]
        reserved = {name for d,name in people}
        if len(reserved) == n and fixed_operations == operations:
            return payload
        seen,fixed,counter = set(),[],0
        for direction,name in people:
            if name in seen:
                while True:
                    x,letters = counter,[]
                    while True:
                        letters.append(chr(ord('a')+x%26));x //= 26
                        if not x:break
                    candidate = 'fix'+''.join(reversed(letters));counter += 1
                    if candidate not in reserved:break
                name = candidate;reserved.add(name)
            seen.add(name);fixed.append((direction,name))
        assert len(seen) == n and all(len(name) <= 10 for d,name in fixed)
        rows = [f'{n} {m}']+[f'{d} {name}' for d,name in fixed]+[f'{d} {steps}' for d,steps in fixed_operations]
        return ('\n'.join(rows)+'\n').encode()
    if number == 28696:
        values = list(map(int,text.split()))
        n,health = values[0],values[1:]
        assert 2 <= n <= 1000 and len(health) == n
        if len(set(health)) == n:
            return payload
        ranks = [0]*n
        for rank,index in enumerate(sorted(range(n),key=lambda i:(health[i],i)),1):
            ranks[index] = rank
        assert len(set(ranks)) == n
        return (str(n)+'\n'+' '.join(map(str,ranks))+'\n').encode()
    return payload


def canonical_ranges(text):
    """与题面样例一致：双引号、外层方括号、逗号间无空格。"""
    s = text.strip()
    if s.startswith('['):
        a = ast.literal_eval(s)
    else:
        a = list(map(int, s.split()))
    assert isinstance(a, list) and all(type(x) is int for x in a)
    assert all(x < y for x, y in zip(a, a[1:]))
    out = []
    start = end = None
    for value in a:
        if start is None:
            start = end = value
        elif value == end + 1:
            end = value
        else:
            out.append(str(start) if start == end else f'{start}->{end}')
            start = end = value
    if start is not None:
        out.append(str(start) if start == end else f'{start}->{end}')
    return json.dumps(out, separators=(',', ':'))
