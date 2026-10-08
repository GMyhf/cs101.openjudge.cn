# 27311 牛栏空调：差分 d=p-t，答案为正/负部分各自的上升量之和。
# 约束：1<=N<=100000，温度为 0..10000 的非负整数；输入三行。
import random
import subprocess
import sys
from collections import deque
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAXN = 100000
MAXV = 10000
SAMPLE = '5\n1 5 3 3 4\n1 2 2 2 1\n'


def valid(text):
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    if len(lines) != 3 or not lines[0].isdigit():
        return False
    n = int(lines[0])
    if not (1 <= n <= MAXN) or str(n) != lines[0]:
        return False
    for ln in lines[1:]:
        a = ln.split(' ')
        if len(a) != n:
            return False
        for x in a:
            if not x.isdigit() or str(int(x)) != x or int(x) > MAXV:
                return False
    return True


def mk(p, t):
    return f'{len(p)}\n{" ".join(map(str, p))}\n{" ".join(map(str, t))}\n'


def alt_answer(text):
    """另一种写法：按符号段处理，同号取增量，异号重新计入 |d|。"""
    lines = text.split('\n')
    p = list(map(int, lines[1].split()))
    t = list(map(int, lines[2].split()))
    ans, prev = 0, 0
    for a, b in zip(p, t):
        d = a - b
        if d == 0:
            pass
        elif prev == 0 or (d > 0) != (prev > 0):
            ans += abs(d)
        elif abs(d) > abs(prev):
            ans += abs(d) - abs(prev)
        prev = d
    return ans


def bfs_answer(d):
    """极小规模暴力：对 d 做区间 ±1，BFS 到全 0 的最少步数。"""
    n = len(d)
    lim = max(abs(x) for x in d) + 1
    start = tuple(d)
    goal = (0,) * n
    dist = {start: 0}
    q = deque([start])
    while q:
        u = q.popleft()
        if u == goal:
            return dist[u]
        for i in range(n):
            for j in range(i, n):
                for s in (1, -1):
                    v = list(u)
                    for k in range(i, j + 1):
                        v[k] += s
                    if max(abs(x) for x in v) > lim:
                        continue
                    v = tuple(v)
                    if v not in dist:
                        dist[v] = dist[u] + 1
                        q.append(v)
    raise AssertionError


def build_cases():
    r = random.Random(27311)
    cases = [SAMPLE]
    # 满规模（.in 控制在 1MB 内）
    n = MAXN
    cases.append(mk([0 if i % 2 else MAXV for i in range(n)], [MAXV if i % 2 else 0 for i in range(n)]))  # 答案最大
    cases.append(mk([r.randint(0, MAXV) for _ in range(75000)], [r.randint(0, MAXV) for _ in range(75000)]))
    same = [r.randint(0, 999) for _ in range(n)]
    cases.append(mk(same, same[:]))                                                                     # 答案 0
    cases.append(mk([MAXV] * n, [0] * n))                                                               # 一条命令区间但需 10000 次
    cases.append(mk([0] * n, [MAXV] * n))                                                               # 全为负方向
    # 边界
    cases.append(mk([0], [0]))
    cases.append(mk([MAXV], [0]))
    cases.append(mk([0], [MAXV]))
    cases.append(mk([7], [3]))
    cases.append(mk([1, 2, 3, 4, 5], [0, 0, 0, 0, 0]))
    cases.append(mk([5, 4, 3, 2, 1], [0, 0, 0, 0, 0]))
    cases.append(mk([0, 0, 0, 0, 0], [1, 3, 1, 3, 1]))
    cases.append(mk([3, 0, 3, 0, 3], [0, 3, 0, 3, 0]))                                                  # 正负交替
    cases.append(mk([5, 5, 5, 0, 5], [0, 0, 0, 5, 0]))
    cases.append(mk([MAXV] * 10, [MAXV] * 10))
    cases.append(mk([2, 2, 1, 1, 2, 2], [0, 0, 0, 0, 0, 0]))                                            # 中间凹下去
    # 小随机组（可 BFS 验证）
    while len(cases) < 27:
        n = r.randint(1, 4)
        p = [r.randint(0, 3) for _ in range(n)]
        t = [r.randint(0, 3) for _ in range(n)]
        if mk(p, t) not in cases:
            cases.append(mk(p, t))
    # 中等随机：不同值域、不同长度
    for i in range(14):
        n = r.randint(1, [20, 2000, 30000][i % 3])
        hi = [5, 100, MAXV][(i // 3) % 3] if i < 9 else MAXV
        if i >= 9:
            # 平滑起伏：相邻差小，常见分段写法易错
            p, t = [r.randint(0, hi)], [r.randint(0, hi)]
            for _ in range(n - 1):
                p.append(min(hi, max(0, p[-1] + r.randint(-50, 50))))
                t.append(min(hi, max(0, t[-1] + r.randint(-50, 50))))
        else:
            p = [r.randint(0, hi) for _ in range(n)]
            t = [r.randint(0, hi) for _ in range(n)]
        cases.append(mk(p, t))
    return cases


def run_ref(text):
    x = subprocess.run([sys.executable, str(HERE / 'samplecode.py')], input=text,
                       text=True, capture_output=True, timeout=120)
    if x.returncode:
        raise SystemExit(x.stderr)
    return x.stdout


def main():
    cases = build_cases()
    assert len(set(cases)) == len(cases), '存在重复组'
    d = HERE / 'data'
    d.mkdir(exist_ok=True)
    for i, c in enumerate(cases):
        assert valid(c), f'第 {i} 组不合法'
        out = run_ref(c)
        assert out == f'{alt_answer(c)}\n', f'第 {i} 组与另一写法不一致'
        lines = c.split('\n')
        n = int(lines[0])
        if n <= 4:
            dd = [a - b for a, b in zip(map(int, lines[1].split()), map(int, lines[2].split()))]
            if max(map(abs, dd)) <= 4:
                assert out == f'{bfs_answer(dd)}\n', f'第 {i} 组与 BFS 暴力不一致'
        (d / f'{i}.in').write_text(c)
        (d / f'{i}.out').write_text(out)


if __name__ == '__main__':
    main()
