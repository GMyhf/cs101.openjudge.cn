"""审核后输入修复规则；只裁剪越界部分，答案由已审核的整数参考重算。"""
import ast
import json


def repair_input(number, payload):
    text = payload.decode()
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
