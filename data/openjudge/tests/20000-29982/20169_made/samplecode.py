# External reference: statistics page /practice/20169/
# Accepted submission: 52720771
# Source: http://cs101.openjudge.cn/practice/solution/52720771/
# License: not declared on the submission page; no license is inferred.
# 2026-10-08 本地修正：上面引用的原始代码在题面范围内有缺陷，已按题面改过，与原提交不再逐字一致（见 CHANGELOG）。

# External reference: statistics page /practice/20169/
# Accepted submission: 52720771
# Source: http://cs101.openjudge.cn/practice/solution/52720771/
# License: not declared on the submission page; no license is inferred.

# 逐行读入：每次读取一整行字符串
import sys

input = sys.stdin.readline

def find(parent, x):  # 查找编号x的祖先（迭代写法：链长可达 n=30000，递归会超过默认递归深度）
    root = x
    while parent[root] != root:
        root = parent[root]
    while parent[x] != root:
        parent[x], x = root, parent[x]
    return root

def main():
    T = int(input())

    for _ in range(T):
        n, m = map(int, input().split())

        parent = list(range(n + 1))

        for _ in range(m):
            x, y = map(int, input().split())

            rx, ry = find(parent, x), find(parent, y)

            if rx != ry:
                parent[rx] = ry

        ans = [str(find(parent, i)) for i in range(1, n + 1)]
        print(" ".join(ans))

if __name__ == "__main__":
    main()
