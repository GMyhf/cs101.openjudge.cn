# 27312 拍照：只能反转偶数长前缀，求使偶数位置更赛牛(G)最多的最少反转次数。
# 约束：2<=N<=200000，N 为偶数；第二行为长 N 的 G/H 串。
import random
import subprocess
import sys
from collections import deque
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAXN = 200000
SAMPLE = '14\nGGGHGHHGHHHGHG\n'


def valid(text):
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    if len(lines) != 2 or not lines[0].isdigit() or str(int(lines[0])) != lines[0]:
        return False
    n = int(lines[0])
    if not (2 <= n <= MAXN) or n % 2:
        return False
    s = lines[1]
    return len(s) == n and all(c in 'GH' for c in s)


def mk(s):
    return f'{len(s)}\n{s}\n'


def bfs_answer(s):
    """暴力：BFS 所有偶数前缀反转，取偶数位置 G 最多的状态中的最短距离。"""
    n = len(s)
    score = lambda x: sum(1 for i in range(1, n, 2) if x[i] == 'G')
    dist = {s: 0}
    q = deque([s])
    while q:
        u = q.popleft()
        for j in range(2, n + 1, 2):
            v = u[:j][::-1] + u[j:]
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    best = max(score(x) for x in dist)
    return min(d for x, d in dist.items() if score(x) == best)


def build_cases():
    r = random.Random(27312)
    cases = [SAMPLE]
    # 满规模
    cases.append(mk(''.join(r.choice(['GH', 'HG']) for _ in range(MAXN // 2))))      # 答案接近 N/2 量级
    cases.append(mk('GHHG' * (MAXN // 4)))                                            # 交替，答案最大
    cases.append(mk(''.join(r.choice('GH') for _ in range(MAXN))))
    cases.append(mk('G' * MAXN))                                                      # 答案 0
    cases.append(mk('GH' * (MAXN // 2)))                                              # 全是 GH
    # 边界：N=2 全部四种，N=4 若干
    for s in ['GG', 'GH', 'HG', 'HH', 'GHHG', 'HGGH', 'HGHG', 'GHGH', 'GGHH', 'HHGG', 'GHGG', 'HGHH']:
        cases.append(mk(s))
    # 全部 N=6 中挑若干、N<=12 随机（BFS 验证）
    seen = set(cases)
    while len(cases) < 34:
        n = r.choice([6, 8, 10, 12])
        c = mk(''.join(r.choice('GH') for _ in range(n)))
        if c not in seen:
            seen.add(c)
            cases.append(c)
    # 中等随机：成对出现的块结构 + 纯随机
    for i in range(10):
        n = 2 * r.randint(1, [50, 3000, 40000][i % 3])
        if i % 2:
            s = ''.join(r.choice('GH') for _ in range(n))
        else:
            blocks = []
            while sum(map(len, blocks)) < n:
                blocks.append(r.choice(['GH', 'HG', 'GG', 'HH']) * r.randint(1, 20))
            s = ''.join(blocks)[:n]
        cases.append(mk(s))
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
        s = c.split('\n')[1]
        if len(s) <= 12:
            assert out == f'{bfs_answer(s)}\n', f'第 {i} 组与 BFS 暴力不一致'
        (d / f'{i}.in').write_text(c)
        (d / f'{i}.out').write_text(out)


if __name__ == '__main__':
    main()
