# External reference: http://cs101.openjudge.cn/practice/31087/statistics/
# Accepted submission: 52833715
# Source: http://cs101.openjudge.cn/practice/solution/52833715/
# License: not declared on the submission page; no license is inferred.

def solve(N1, N2, N3):
    ans = [[[0 for _ in range(N3 + 1)] for _ in range(N2 + 1)] for _ in range(N1 + 1)] # 存每一种盘面属于W集还是L集，L集为0，W集为1
    L1 = [[0 for _ in range(N2 + 1)] for _ in range(N1 + 1)] # L1[x0][y0] = k表示：形如(x0,y0,z)的盘面有k个属于L集
    L2 = [[0 for _ in range(N3 + 1)] for _ in range(N1 + 1)] # L2[x0][z0] = k表示：形如(x0,y,z0)的盘面有k个属于L集
    L3 = [[0 for _ in range(N3 + 1)] for _ in range(N2 + 1)] # L1[y0][z0] = k表示：形如(x,y0,z0)的盘面有k个属于L集
    L1[0][0] = L2[0][0] = L3[0][0] = 1 # (0,0,0)属于L集
    for i in range(N1 + 1):
        for j in range(N2 + 1):
            for k in range(N3 + 1): # 逐一检测各种盘面，判断属于W集还是L集
                if i == j == k == 0:
                    continue
                # 下面判断这个盘面(i,j,k)能不能走到L集，如果可以，它就属于W集，特别地，如果只剩一个筹码，也属于W集
                if i + j + k == 1 or L1[i][j] + L2[i][k] + L3[j][k] >= 2:
                    ans[i][j][k] = 1
                # 否则它属于L集，把它放进L1,L2,L3
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
