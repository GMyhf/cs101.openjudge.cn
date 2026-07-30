# External reference: http://cs101.openjudge.cn/practice/31086/statistics/
# Accepted submission: 52833708
# Source: http://cs101.openjudge.cn/practice/solution/52833708/
# License: not declared on the submission page; no license is inferred.

def solve(N1, N2, N3):
    ans = [[[0 for _ in range(N3 + 1)] for _ in range(N2 + 1)] for _ in range(N1 + 1)]
    L1 = [[0 for _ in range(N2 + 1)] for _ in range(N1 + 1)]
    L2 = [[0 for _ in range(N3 + 1)] for _ in range(N1 + 1)]
    L3 = [[0 for _ in range(N3 + 1)] for _ in range(N2 + 1)]
    L1[0][0] = L2[0][0] = L3[0][0] = 1
    for i in range(N1 + 1):
        for j in range(N2 + 1):
            for k in range(N3 + 1):
                if i == j == k == 0:
                    continue

                if L1[i][j] + L2[i][k] + L3[j][k] >= 1:
                    ans[i][j][k] = 1

                else:
                    L1[i][j] += 1
                    L2[i][k] += 1
                    L3[j][k] += 1
    return ans
lst = []
N1 = N2 = N3 = 0
for _ in range(int(input())):
    a, b, c = map(int, input().split())
    N1, N2, N3 = max(a, N1), max(b, N2), max(c, N3)
    lst.append((a, b, c))
ans = solve(N1, N2, N3)
for i in lst:
    if ans[i[0]][i[1]][i[2]] == 0:
        print('KittyPig')
    else:
        print('Piggy')
