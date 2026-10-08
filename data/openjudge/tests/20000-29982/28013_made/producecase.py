import random, subprocess, sys, tempfile
from pathlib import Path

REFERENCE = '# External reference: statistics page /practice/28013/\n# Accepted submission: 52734750\n# Source: http://cs101.openjudge.cn/practice/solution/52734750/\n# License: not declared on the submission page; no license is inferred.\n\nn = int(input())\ntree = list(map(int, input().split()))\npaths = []\n\n# 1. DFS遍历：先右 后左，收集所有根到叶子的路径\ndef dfs(idx, path):\n    path.append(tree[idx])\n    # 判断是否是叶子节点\n    left = 2 * idx + 1\n    right = 2 * idx + 2\n    if left >= n and right >= n:\n        paths.append(path.copy())\n        path.pop()\n        return\n    # 关键：先右 后左\n    if right < n:\n        dfs(right, path)\n    if left < n:\n        dfs(left, path)\n    path.pop()\n\ndfs(0, [])\n\n# 2. 输出所有路径\nfor p in paths:\n    print(\' \'.join(map(str, p)))\n\n# 3. 判断大顶堆 / 小顶堆\nis_max = True\nis_min = True\n\nfor i in range(n):\n    left = 2 * i + 1\n    right = 2 * i + 2\n    if left < n:\n        if tree[i] < tree[left]:\n            is_max = False\n        if tree[i] > tree[left]:\n            is_min = False\n    if right < n:\n        if tree[i] < tree[right]:\n            is_max = False\n        if tree[i] > tree[right]:\n            is_min = False\n\nif is_max:\n    print("Max Heap")\nelif is_min:\n    print("Min Heap")\nelse:\n    print("Not Heap")'

import heapq

SAMPLE = '8\n98 72 86 60 65 12 23 50\n'
SAMPLE2 = '8\n10 28 15 12 34 9 8 56\n'
MAXV = 10 ** 9


def _int(s):
    return s.isdigit() and (s == '0' or s[0] != '0')


def valid(text):
    """题面：n≤1000（取 n≥2：n=1 时既是大顶堆又是小顶堆，输出有歧义，故避开）；
    第二行恰 n 个互不相同的整数（本数据取 1..1e9）。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    if len(lines) != 2 or not _int(lines[0]):
        return False
    n = int(lines[0])
    if not 2 <= n <= 1000:
        return False
    a = lines[1].split(' ')
    if len(a) != n or not all(_int(t) for t in a):
        return False
    a = list(map(int, a))
    return len(set(a)) == n and all(1 <= x <= MAXV for x in a)


def fmt(a):
    return f"{len(a)}\n{' '.join(map(str, a))}\n"


def vals(r, n, hi):
    return r.sample(range(1, hi + 1), n)


def min_heap(r, n, hi):
    a = vals(r, n, hi); heapq.heapify(a); return a


def max_heap(r, n, hi):
    a = [-x for x in vals(r, n, hi)]; heapq.heapify(a); return [-x for x in a]


def break_at(r, a, i, _kind):
    """把下标 i 的结点与其父结点交换，造出恰在该处的违例。"""
    a = a[:]; p = (i - 1) // 2; a[i], a[p] = a[p], a[i]; return a


def build_cases():
    r = random.Random(28013)
    N = 1000
    cases = [SAMPLE, SAMPLE2]
    cases.append(fmt(sorted(vals(r, N, MAXV), reverse=True)))   # 降序：Max
    cases.append(fmt(sorted(vals(r, N, MAXV))))                 # 升序：Min
    cases.append(fmt(max_heap(r, N, 10 ** 6)))
    cases.append(fmt(min_heap(r, N, 10 ** 6)))
    cases.append(fmt(vals(r, N, 10 ** 6)))                      # 随机：Not
    a = max_heap(r, N, 10 ** 6); cases.append(fmt(break_at(r, a, N - 1, 0)))   # 只有最后一个（唯一左孩子）违例
    a = min_heap(r, N - 1, 10 ** 6); cases.append(fmt(break_at(r, a, N - 2, 0)))  # n 奇数，最后一个是右孩子
    a = max_heap(r, 999, 10 ** 6); cases.append(fmt(break_at(r, a, 2, 0)))      # 根与右孩子违例
    # 层序并非降序但仍是大顶堆（卡“层序整体有序才算堆”的错写法）
    a = sorted(vals(r, 1000, 10 ** 6), reverse=True); a[1], a[2] = a[2], a[1]
    cases.append(fmt(a))
    # 小边界
    cases += [fmt([1, 2]), fmt([2, 1]), fmt([MAXV, 1]), fmt([2, 1, 3]), fmt([2, 3, 1]),
              fmt([3, 1, 2]), fmt([1, 3, 2]), fmt([5, 4, 3, 6]), fmt([1, 2, 3, 4, 5]),
              fmt([1, 5, 2, 6, 7, 3, 4]), fmt([7, 3, 6, 1, 2, 4, 5]), fmt([7, 3, 6, 1, 2, 8, 5])]
    while len(cases) < 41:
        n = r.choice([r.randint(2, 15), r.randint(16, 200), r.randint(201, N)])
        hi = r.choice([max(n, 100), 10 ** 6, MAXV])
        t = len(cases) % 5
        if t == 0:
            a = max_heap(r, n, hi)
        elif t == 1:
            a = min_heap(r, n, hi)
        elif t == 2:
            a = vals(r, n, hi)
        else:
            a = (max_heap if t == 3 else min_heap)(r, n, hi)
            a = break_at(r, a, r.randrange(1, n), 0)
        c = fmt(a)
        if c not in cases:
            cases.append(c)
    return cases


def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p = Path(d) / 'main.py'; p.write_text(REFERENCE)
        x = subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=90)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout


def main():
    d = Path('data'); d.mkdir(exist_ok=True)
    cases = build_cases()
    assert len(cases) == len(set(cases)), '组间有重复'
    for i, c in enumerate(cases):
        assert valid(c), f'第 {i} 组不合题面'
        (d / f'{i}.in').write_text(c); (d / f'{i}.out').write_text(run(c))


if __name__ == '__main__':
    main()
