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
