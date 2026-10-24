"""审核后确定性派生合法输入；保留原件，答案由已审核的整数参考重算。"""
import ast
import json
import re


def validate_missing_deque_input(payload):
    """恢复错名输入前验证完整规格，返回原始字节。"""
    values = list(map(int, payload.split()))
    n, q = values[:2]
    assert 2 <= n <= 10**5 and 0 <= q <= 3*10**5
    assert len(values) == 2 + n + q
    assert all(0 <= x <= 10**9 for x in values[2:2+n])
    assert all(1 <= x <= 10**18 for x in values[2+n:])
    return payload


def repair_input(number, payload):
    text = payload.decode()
    if number == 29663:
        values = list(map(int, text.split()))
        k, n = values[:2]
        assert 1 <= k <= 1000 and 2 <= n <= 10001 and len(values) == n + 2
        nodes = values[2:]
        changed = nodes[0] == -1
        if changed:
            # 空根后存在实体节点；仅将根改为合法值0，其余值与输入布局保持。
            nodes[0] = 0
        slots = 1
        for value in nodes:
            assert slots > 0
            slots -= 1
            if value != -1:
                slots += 2
        if not changed:
            return payload
        tokens = list(re.finditer(rb'\S+', payload))
        root = tokens[2]
        return payload[:root.start()] + b'0' + payload[root.end():]
    if number == 31239:
        lines = text.splitlines()
        header = list(map(int, lines[0].split()))
        assert len(header) in (1, 4)
        n = header[0]
        assert 2 <= n <= 10**5 and len(lines) == n + 1
        rows = [list(map(int, line.split())) for line in lines[1:]]
        assert all(len(row) == 3 and all(0 <= v <= 10**9 for v in row) for row in rows)
        assert any(v for row in rows for v in row)
        if len(header) == 1:
            return payload
        # 已审核的旧头为N及三个多余参数；当前题面只定义N和后续数量表。
        assert header[1] >= 1 and header[2:] == [1, 2]
        first, separator, body = payload.partition(b'\n')
        assert separator
        return str(n).encode() + (b'\r' if first.endswith(b'\r') else b'') + separator + body
    if number == 31241:
        values = list(map(int, text.split()))
        n, m, k = values[:3]
        assert 2 <= n <= 8 and 2 <= m <= 10 and 1 <= k <= m*(m-1)//2
        assert len(values) == 3 + n*m + 2*k
        rows = [values[3+i*m:3+(i+1)*m] for i in range(n)]
        pairs = list(zip(values[3+n*m::2], values[4+n*m::2]))
        assert len(set(pairs)) == k and all(1 <= u < v <= m for u, v in pairs)
        assert all(sum(row) >= 1 and all(0 <= v <= 10**9 for v in row) for row in rows)
        limit = 10**9
        changed = False
        for i, row in enumerate(rows):
            total = sum(row)
            if total > limit:
                # 上取整保留每种口味的存在性；留出最多m−1的取整误差。
                budget = limit - m + 1
                factor = (total + budget - 1) // budget
                rows[i] = [(v + factor - 1) // factor for v in row]
                assert 1 <= sum(rows[i]) <= limit
                changed = True
        if not changed:
            return payload
        return (f'{n} {m} {k}\n' + '\n'.join(' '.join(map(str, row)) for row in rows) +
                '\n' + '\n'.join(f'{u} {v}' for u, v in pairs) + '\n').encode()
    if number == 28016:
        lines = text.splitlines()
        assert len(lines) == 6
        steps = int(lines[0])
        assert 1 <= steps <= 3
        columns = [list(map(int, line.split())) for line in lines[1:]]
        assert all(1 <= len(col) <= 8 and col[-1] == 0 and
                   all(1 <= v <= 10 for v in col[:-1]) for col in columns)
        board = [col[:-1] for col in columns]
        settled = stable_mayan_board(board)
        if settled == board:
            return payload
        return (str(steps) + '\n' + '\n'.join(
            ' '.join(map(str, col + [0])) for col in settled) + '\n').encode()
    if number == 21729:
        m,n,x,y = map(int,text.split())
        assert 1 < n < m < 30 and 1 <= y <= n and 1 <= x <= m-n+y
        if (x,y)==(1,1):
            return f'{m} {n}\n1 2\n'.encode()
        if (x,y)==(m,n):
            return f'{m} {n}\n{m-1} {n}\n'.encode()
        return payload
    if number == 30236:
        digits,target = text.split()
        target = int(target)
        assert 1 <= len(digits) <= 10 and all('0' <= c <= '9' for c in digits)
        legal = max(-2**31,min(2**31-1,target))
        if legal == target:
            return payload
        return f'{digits}\n{legal}\n'.encode()
    if number == 28277:
        values = list(map(int, text.split()))
        m,n = values[:2]
        assert 1 <= m <= 250 and 1 <= n <= 250 and len(values) == 2 + m*n
        assert all(1 <= x <= 4 for x in values[2:])
        if m < 250 and n < 250:
            return payload
        rows = [values[2+i*n:2+(i+1)*n] for i in range(m)]
        height,width = min(m,249),min(n,249)
        return (f'{height} {width}\n'+'\n'.join(' '.join(map(str,row[:width])) for row in rows[:height])+'\n').encode()
    if number == 28680:
        left,right,digit = map(int,text.split())
        assert 1 <= left <= right and 0 <= digit <= 9
        if digit > 0:
            return payload
        # 依原题正整数约束，0查询替换为最近合法数字1，区间不变。
        return f'{left} {right} 1\n'.encode()
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


def no_leading_zero_reference(source):
    """沿用原自写整数枚举器，按用户确认禁用多位数的前导零。"""
    old = 'return expressions_model(text, True)'
    assert source.count(old) == 1
    return source.replace(old,'return expressions_model(text, False)')


def stable_mayan_board(columns):
    """非法初始局面先同时消除并落定，级联到稳定；不消耗玩家步数。"""
    board = [list(col) for col in columns]
    while True:
        grid = [[board[x][y] if y < len(board[x]) else 0
                 for x in range(5)] for y in range(7)]
        removed = set()
        for y in range(7):
            for x in range(5):
                if not grid[y][x]:
                    continue
                for dx, dy in ((1, 0), (0, 1)):
                    if x + 2*dx < 5 and y + 2*dy < 7:
                        cells = [(x + i*dx, y + i*dy) for i in range(3)]
                        if all(grid[b][a] == grid[y][x] for a, b in cells):
                            removed.update(cells)
        if not removed:
            return board
        board = [[v for y, v in enumerate(col) if (x, y) not in removed]
                 for x, col in enumerate(board)]
