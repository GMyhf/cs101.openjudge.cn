# External reference: http://cs101.openjudge.cn/practice/27948/statistics/
# Accepted submission: 52702741
# Source: http://cs101.openjudge.cn/practice/solution/52702741/
# License: not declared on the submission page; no license is inferred.

def solve():
    n = int(input())
    s = input().strip()

    def dfs(cur):
        if len(cur) == 1:
            return 'B' if cur == '0' else 'I'
        mid = len(cur) // 2
        left = dfs(cur[:mid])
        right = dfs(cur[mid:])
        if all(ch == '0' for ch in cur):
            root = 'B'
        elif all(ch == '1' for ch in cur):
            root = 'I'
        else:
            root = 'F'
        return left + right + root

    print(dfs(s))

if __name__ == '__main__':
    solve()
