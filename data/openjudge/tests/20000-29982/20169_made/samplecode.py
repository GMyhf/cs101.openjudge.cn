# External reference: statistics page /practice/20169/
# Accepted submission: 52720771
# Source: http://cs101.openjudge.cn/practice/solution/52720771/
# License: not declared on the submission page; no license is inferred.

# External reference: statistics page /practice/20169/
# Accepted submission: 52720771
# Source: http://cs101.openjudge.cn/practice/solution/52720771/
# License: not declared on the submission page; no license is inferred.

# 逐行读入：每次读取一整行字符串
import sys

input = sys.stdin.readline

def find(parent, x):  # 查找编号x的祖先
    if parent[x] != x:
        parent[x] = find(parent, parent[x])
    return parent[x]

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
