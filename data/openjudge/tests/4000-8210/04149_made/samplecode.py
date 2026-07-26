# External reference: statistics page /practice/04149/
# Accepted submission: 45229533
# Source: http://cs101.openjudge.cn/practice/solution/45229533/
# License: not declared on the submission page; no license is inferred.

# 熊江凯
import sys

MAX = 1 << 15


class DDL:
    def __init__(self, className="", ddl=0, costTime=0):
        self.className = className
        self.ddl = ddl
        self.costTime = costTime


def main():
    input = sys.stdin.read
    data = input().split()
    idx = 0

    t = int(data[idx])
    idx += 1
    results = []

    while t > 0:
        t -= 1
        n = int(data[idx])
        idx += 1

        ddlList = []
        sum = [0] * MAX
        dp = [float('inf')] * MAX
        ans = [""] * MAX

        for i in range(n):
            className = data[idx]
            ddl = int(data[idx + 1])
            costTime = int(data[idx + 2])
            idx += 3
            ddlList.append(DDL(className, ddl, costTime))
            sum[1 << i] = ddlList[i].costTime

        for i in range(1 << n):
            for j in range(n):
                if i & (1 << j):
                    sum[i] = sum[i ^ (1 << j)] + ddlList[j].costTime

        dp[0] = 0

        for i in range(1 << n):
            for j in range(n):
                if i & (1 << j):
                    prev = i ^ (1 << j)
                    penalty = max(0, sum[i] - ddlList[j].ddl)
                    if dp[prev] + penalty < dp[i] or ans[i] == "":
                        dp[i] = dp[prev] + penalty
                        ans[i] = ans[prev] + ddlList[j].className + '\n'
                    elif dp[prev] + penalty == dp[i]:
                        ans[i] = min(ans[i], ans[prev] + ddlList[j].className + '\n')

        results.append(f"{dp[(1 << n) - 1]}\n{ans[(1 << n) - 1]}".strip())

    print("\n".join(results))


if __name__ == "__main__":
    main()
