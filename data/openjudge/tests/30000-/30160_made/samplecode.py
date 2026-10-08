# External reference: /practice/30160/statistics/
# Accepted submission: 50848044
# Source: http://cs101.openjudge.cn/practice/solution/50848044/
# License: not declared on the submission page; no license is inferred.
# 2026-10-08 本地修正：上面引用的原始代码在题面范围内有缺陷，已按题面改过，与原提交不再逐字一致（见 CHANGELOG）。
# 原写法只做行列推理，遇到唯一解但推不动、必须试填的盘面会死循环（满规模 6 组超时）；
# 现保留 generate_all/find_must 的行列推理，推不动时挑候选最少的一行回溯试填（R,C<=10，每组几十毫秒）。

import itertools
import sys
from functools import reduce
from operator import and_, or_


def generate_all(arr, length):
    # 长度为 length 的一行里满足提示 arr 的全部填法，第 j 位为 1 表示第 j 格涂黑
    sep = len(arr) + 1
    blank = length - sum(arr) - len(arr) + 1
    elem = [(1 << i) - 1 for i in arr]
    comb = itertools.combinations_with_replacement(range(sep), blank)
    entire = []
    for i in comb:
        this = 0
        cursor = 0
        counter = [0] * sep
        for s in i:
            counter[s] += 1
        for j in range(len(arr)):
            cursor += counter[j]
            if j > 0: cursor += 1
            this |= elem[j] << cursor
            cursor += arr[j]
        entire.append(this)
    return entire


def find_must(entire):
    must_filled = reduce(and_, entire)  # 1 if must filled
    must_empty = reduce(or_, entire)  # 0 if must empty
    return must_filled, must_empty


def cross_filter(lines, others):
    # 用 lines 里每行“必黑/必白”的格子筛掉 others（与之垂直的各行）的候选；返回是否有变化，矛盾时返回 None
    changed = False
    for i, entire in enumerate(lines):
        must_filled, must_empty = find_must(entire)
        for j, other in enumerate(others):
            if must_filled >> j & 1:
                kept = [psb for psb in other if psb >> i & 1]
            elif not must_empty >> j & 1:
                kept = [psb for psb in other if not psb >> i & 1]
            else:
                continue
            if not kept:
                return None
            if len(kept) != len(other):
                others[j] = kept
                changed = True
    return changed


def solve(rows, cols):
    # 先反复做行列推理，推不动时挑候选最少的一行逐个试填，递归求解
    rows, cols = rows[:], cols[:]
    while True:
        changed_cols = cross_filter(rows, cols)
        if changed_cols is None:
            return None
        changed_rows = cross_filter(cols, rows)
        if changed_rows is None:
            return None
        if not changed_cols and not changed_rows:
            break
    undecided = [i for i in range(len(rows)) if len(rows[i]) > 1]
    if not undecided:
        return [entire[0] for entire in rows]
    best = min(undecided, key=lambda i: len(rows[i]))
    for psb in rows[best]:
        rows[best] = [psb]
        result = solve(rows, cols)
        if result is not None:
            return result
    return None


def main():
    data = sys.stdin.read().split()
    r, c = int(data[0]), int(data[1])
    pos = 2
    conds = []
    for _ in range(r + c):
        k = int(data[pos])
        conds.append([int(x) for x in data[pos + 1:pos + 1 + k]])
        pos += 1 + k
    rows = [generate_all(i, c) for i in conds[:r]]
    cols = [generate_all(i, r) for i in conds[r:]]
    board = solve(rows, cols)
    sys.stdout.write(''.join(''.join(str(row >> j & 1) for j in range(c)) + '\n' for row in board))


if __name__ == '__main__':
    main()
