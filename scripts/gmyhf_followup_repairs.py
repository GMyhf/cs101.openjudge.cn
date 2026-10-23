"""继续验收后的精确整数修正；不执行题目表达式或读取后台凭据。"""
from collections import defaultdict
from decimal import Decimal
from itertools import permutations


ROUTE_TIE_RULE = ('若有多种最优拾取顺序，将三个零件按输入先后编号为1、2、3，'
                  '输出编号序列字典序最小的顺序。比较编号序列，不比较零件名称。')


def route_answer(text):
    """枚举六种编号顺序；便宜的反向对角移动必须计入。"""
    rows = text.splitlines()
    a, b, c = map(Decimal, rows[0].split())
    a, b, c = min(a, b+c), min(b, a+c), min(c, a+b)
    parts = [row.split() for row in rows[1:]]
    def distance(p, q):
        dx, dy = abs(p[0]-q[0]), abs(p[1]-q[1])
        x, y = a, b
        if dx < dy:
            dx, dy, x, y = dy, dx, y, x
        pairs, odd = divmod(dx-dy, 2)
        return dy*c + pairs*min(2*x, 2*c) + odd*x
    candidates = []
    for order in permutations(range(3)):
        path = [(0, 0)] + [tuple(map(int, parts[i][1:])) for i in order] + [(100, 100)]
        cost = sum(distance(p, q) for p, q in zip(path, path[1:]))
        candidates.append((cost, order))
    cost, order = min(candidates)
    return ' '.join(parts[i][0] for i in order) + f'\n{cost:.2f}'


def integer_extrema(text):
    """扫描离散差分的变更点，O(n log n)；仅访问整数位置。"""
    rows = [list(map(int, row.split())) for row in text.splitlines()]
    n, bound = rows[0]
    assert len(rows) == n+1
    value = sum(c*abs(b) for a, b, c in rows[1:])
    delta = sum(c*(abs(a+b)-abs(b)) for a, b, c in rows[1:])
    events = defaultdict(int)
    for a, b, c in rows[1:]:
        if a == 0:
            continue
        if a < 0:
            a, b = -a, -b
        k, remainder = divmod(-b, a)
        if 1 <= k < bound:
            events[k] += 2*c*(a-remainder)
        if 1 <= k+1 < bound:
            events[k+1] += 2*c*remainder
    lo = hi = value
    position = 0
    for following in sorted(events):
        value += (following-position)*delta
        lo, hi = min(lo, value), max(hi, value)
        delta += events[following]
        position = following
    value += (bound-position)*delta
    return f'{max(hi, value)} {min(lo, value)}'


def integer_candidates(text):
    """独立的端点/折点邻接枚举，用于复核扫描算法，不使用浮点根。"""
    rows = [list(map(int, row.split())) for row in text.splitlines()]
    _, bound = rows[0]
    points = {0, bound}
    for a, b, c in rows[1:]:
        if a:
            floor = (-b)//a
            points.update(x for x in (floor, floor+1) if 0 <= x <= bound)
    values = [sum(c*abs(a*x+b) for a, b, c in rows[1:]) for x in points]
    return f'{max(values)} {min(values)}'


def expression_input(payload):
    rows = payload.decode('utf-8').splitlines()
    if len(rows) != 7 or 'stdout = ' not in rows[4]:
        raise ValueError('30162不符合已审核的非法输入形状')
    # 仍覆盖数学表达式的格式错误，不再混入赋值语句和输出重定向。
    rows[4] = 'abs(abs(1.00) +'
    return ('\n'.join(rows)+'\n').encode('utf-8')
