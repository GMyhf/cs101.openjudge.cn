"""Special judge for Codeforces 2208D1 Tree Orientation (Easy Version).

Written for this repository as a hand-off artifact; no external license.

Usage: python3 -I checker.py <input> <contestant_output> <reference_answer>
Exit 0 = accepted, 42 = wrong answer; first stdout line is shown to the student.

Per test case the contestant prints Yes/No (any letter case).  "No" is correct
exactly when the reference answer says No (the reference is verified against an
exhaustive oracle when the data is built).  After "Yes" there must be n-1 edges
x y (1 <= x, y <= n); they must form a tree whose reachability relation equals the
given matrix -- checked directly, so every valid edge order/listing is accepted.
All tokens must be consumed exactly; nothing is trusted from the contestant.
"""
import sys

WA = 42


def wrong(msg):
    print(msg)
    sys.exit(WA)


def main():
    inp = open(sys.argv[1], "rb").read().split()
    try:
        out = open(sys.argv[2], "rb").read().split()
    except OSError:
        out = []
    ans = open(sys.argv[3], "rb").read().split()

    t = int(inp[0]); ip = 1
    op = 0; ap = 0
    for case in range(1, t + 1):
        n = int(inp[ip]); ip += 1
        rows = [inp[ip + i].decode() for i in range(n)]; ip += n
        ref_yes = ans[ap].lower() == b"yes"; ap += 1
        if ref_yes:
            ap += 2 * (n - 1)
        if op >= len(out):
            wrong(f"第 {case} 组：输出提前结束")
        word = out[op].lower(); op += 1
        if word not in (b"yes", b"no"):
            wrong(f"第 {case} 组：应输出 Yes 或 No")
        if word == b"no":
            if ref_yes:
                wrong(f"第 {case} 组：存在满足条件的树，却输出了 No")
            continue
        need = 2 * (n - 1)
        if len(out) - op < need:
            wrong(f"第 {case} 组：边的数量不足 n-1 条")
        nums = []
        for tok in out[op:op + need]:
            if not tok.isdigit() or len(tok) > 6:
                wrong(f"第 {case} 组：边的端点不是合法整数")
            x = int(tok)
            if not 1 <= x <= n:
                wrong(f"第 {case} 组：边的端点超出 1..n")
            nums.append(x - 1)
        op += need
        parent = list(range(n))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        children = [[] for _ in range(n)]
        indeg = [0] * n
        for k in range(0, need, 2):
            u, v = nums[k], nums[k + 1]
            a, b = find(u), find(v)
            if a == b:
                wrong(f"第 {case} 组：输出的边不构成一棵树")
            parent[a] = b
            children[u].append(v)
            indeg[v] += 1
        # n-1 edges without a cycle on n vertices: a tree (hence a DAG once oriented)
        order = [v for v in range(n) if indeg[v] == 0]
        for x in order:
            for y in children[x]:
                indeg[y] -= 1
                if indeg[y] == 0:
                    order.append(y)
        reach = [0] * n
        for x in reversed(order):
            acc = 1 << x
            for y in children[x]:
                acc |= reach[y]
            reach[x] = acc
        for i in range(n):
            if reach[i] != int(rows[i][::-1], 2):
                wrong(f"第 {case} 组：按输出的边定向后，可达关系与输入不符")
        if not ref_yes:
            # a valid tree where the reference said No: the reference would be wrong
            print(f"第 {case} 组：参考答案为 No，但输出的树验证通过")
            sys.exit(3)
    if op != len(out):
        wrong("输出末尾有多余内容")
    print("答案正确")
    sys.exit(0)


main()
