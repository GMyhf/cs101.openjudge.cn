# External reference: http://cs101.openjudge.cn/practice/30908/statistics/
# Accepted submission: 52635794
# Source: http://cs101.openjudge.cn/practice/solution/52635794/
# License: not declared on the submission page; no license is inferred.

import sys

def solve():
    # 一次性读入所有数据
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    N = int(input_data[0])
    Q = int(input_data[1])

    # Q = 10^5，每次操作最多增加约 2 * log2(10^9) ≈ 60 个节点。
    # 预分配 5,000,005 大小对绝大多数数据完全足够且不会爆内存
    MAX_NODES = 5000005

    # 替换为原生 list，访问速度极大提升
    lc = [0] * MAX_NODES
    rc = [0] * MAX_NODES
    val = [0] * MAX_NODES
    lazy = [0] * MAX_NODES

    node_cnt = 1  # 根节点为 1

    def update(rt, l, r, ql, qr, v):
        nonlocal node_cnt
        if ql <= l and r <= qr:
            lazy[rt] += v
            val[rt] += v
            return

        # 内联下传懒标记 (push_down)
        lazy_rt = lazy[rt]
        if lazy_rt:
            if not lc[rt]:
                node_cnt += 1
                lc[rt] = node_cnt
            if not rc[rt]:
                node_cnt += 1
                rc[rt] = node_cnt
            l_child, r_child = lc[rt], rc[rt]
            lazy[l_child] += lazy_rt
            val[l_child] += lazy_rt
            lazy[r_child] += lazy_rt
            val[r_child] += lazy_rt
            lazy[rt] = 0

        mid = (l + r) // 2
        if ql <= mid:
            if not lc[rt]:
                node_cnt += 1
                lc[rt] = node_cnt
            update(lc[rt], l, mid, ql, qr, v)
        if qr > mid:
            if not rc[rt]:
                node_cnt += 1
                rc[rt] = node_cnt
            update(rc[rt], mid + 1, r, ql, qr, v)

        # 借助 val[0] == 0 的特性，免去空节点判断；用 if-else 代替 max()
        v_l = val[lc[rt]]
        v_r = val[rc[rt]]
        val[rt] = v_l if v_l > v_r else v_r

    def query(rt, l, r, ql, qr):
        if ql <= l and r <= qr:
            return val[rt]

        # 内联下传懒标记 (push_down)
        lazy_rt = lazy[rt]
        if lazy_rt:
            nonlocal node_cnt
            if not lc[rt]:
                node_cnt += 1
                lc[rt] = node_cnt
            if not rc[rt]:
                node_cnt += 1
                rc[rt] = node_cnt
            l_child, r_child = lc[rt], rc[rt]
            lazy[l_child] += lazy_rt
            val[l_child] += lazy_rt
            lazy[r_child] += lazy_rt
            val[r_child] += lazy_rt
            lazy[rt] = 0

        mid = (l + r) // 2
        res = -2000000000000000000  # 极小值

        # 剪枝：如果子节点未创建且当前无懒标记，说明该区间全为 0，无需递归
        if ql <= mid:
            if lc[rt]:
                t = query(lc[rt], l, mid, ql, qr)
                if t > res: res = t
            else:
                if 0 > res: res = 0
        if qr > mid:
            if rc[rt]:
                t = query(rc[rt], mid + 1, r, ql, qr)
                if t > res: res = t
            else:
                if 0 > res: res = 0
        return res

    lastans = 0
    idx = 2
    out = []
    out_append = out.append  # 缓存方法，加速循环内调用

    for _ in range(Q):
        op = input_data[idx]
        l_raw = int(input_data[idx+1])
        r_raw = int(input_data[idx+2])

        # 用三元表达式代替 abs() 函数
        abs_lastans = lastans if lastans >= 0 else -lastans
        l = (l_raw ^ abs_lastans) % N + 1
        r = (r_raw ^ abs_lastans) % N + 1
        if l > r:
            l, r = r, l

        if op == 'Add':
            v = int(input_data[idx+3])
            update(1, 1, N, l, r, v)
            idx += 4
        else:
            lastans = query(1, 1, N, l, r)
            out_append(str(lastans))
            idx += 3

    sys.stdout.write('\n'.join(out) + '\n')

if __name__ == '__main__':
    solve()
