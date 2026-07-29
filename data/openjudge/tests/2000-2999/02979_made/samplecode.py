# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2979: 陪审团的人选
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02979/
# License: not declared; no license is inferred.
import sys
# 陪审团的人选, http://cs101.openjudge.cn/practice/02979/
maxn = 400 + 10     # -20 X m <= maxn <= 20 X m, where 1<=m<=20

cnt = 0
while True:
    try:
        n, m = map(int, input().split())
    except ValueError:      #跳过空行
        continue

    if n + m == 0:
        break

    p = [0]     # 控方分数
    d = [0]     # 辩方分数
    for _ in range(n):
        tp, td = map(int, input().split())
        p.append(tp)
        d.append(td)

    cnt += 1

    if n == m:
        prosecution = sum(p)
        defence = sum(d)
        print('Jury #{}'.format(cnt))
        print("Best jury has value {} for prosecution and value {} for defence:".format(prosecution, defence))
        print(' '.join(map(str, range(1,n+1))))
        continue

    #f = []     转移方程：f[j][k]=f[j-1][x]+d[i]+p[i]; 且k=x+p[i]-d[i], f[j-1][x]是满足条件的最大值
    #path = []  记录j个人评审差为k,这种情况下的前一个人j-1是谁

    result = [None] * maxn
    f = [[-1]*5*maxn for _ in range(m+1)]
    path = [[0]*5*maxn for _ in range(m+1)]


    minP_D = 20 * m   # 避免下标为负,所以推广到零以上.题目中的辩控差为0，对应于程序中的辩控差为20*m
    f[0][minP_D] = 0  # 初始化条件. 选0个人使得辩控差为nMinP_D的方案，其辩控和就是0

    for j in range(m):  # 每次循环选出第j个人，共要选出m人
        for k in range(minP_D*2 + 1):   # 可能的辩控差为[0，nMinP_D*2]
             if f[j][k] >= 0:       # 方案 f(j,k)可行
                 for i in range(1, n+1):    # 在方案f(j,k)的基础上，挑下一个人，逐个试
                     if (f[j][k] + p[i] + d[i]) > (f[j+1][k+p[i]-d[i]]):
                        t1 = j
                        t2 = k
                        # 第i个人是否已经在方案f(j,k)中被选上了
                        while (t1 > 0) and (path[t1][t2] != i):
                            t2 = t2 - p[path[t1][t2]] + d[path[t1][t2]]
                            t1 -= 1

                        # 说明第i个人在方案f(j,k)中没有被选上，那么就选它
                        # 形成方案f(j+1,k+p[i]-d[i])
                        if t1 == 0:
                            # 记录新方案的辩控和
                            f[j+1][k+p[i]-d[i]] = f[j][k] + p[i] + d[i]
                            # 选了第i 个人，就要将其记录在path里
                            path[j+1][k+p[i]-d[i]] = i
    #i = minP_D
    j = k = 0
    # determine minimum possible |D(J)-P(J)|
    # 找选了m个人，且实际辩控差绝对值最小的方案。最终方案的程序中辩控差为k
    while (f[m][minP_D+j] < 0) and (f[m][minP_D-j] < 0):
        j += 1

    if f[m][minP_D+j] > f[m][minP_D-j]:                   # 计算k
        k = minP_D + j
    else:
        k = minP_D - j

    # sum(pi) + sum(di) = f(j,k)             (1)
    # sum(pi) - sum(di) = k - minP_D         (2)
    # sum(pi) = ((1) + (2)) // 2
    # sum(di) = ((1) - (2)) // 2
    prosecution = (k - minP_D + f[m][k]) // 2
    defence = (minP_D - k + f[m][k]) // 2

    print('Jury #{}'.format(cnt))
    print("Best jury has value {} for prosecution and value {} for defence:".format(prosecution, defence))

    # 最终方案f(m, k)的最后一个人选记录在Path[m][k]中，
    # 那么从Path[m][k]出发，顺藤摸瓜就能找出方案f(m, k)的所有人选
    for i in range(1, m+1):
        result[i] = path[m - i + 1][k]
        a = result[i]
        b = p[a] - d[a]
        k = k - b

    ans = []
    for i in range(1, m+1):
        if result[i] != None:
            ans.append(result[i])

    ans = sorted(ans)   # 按人选编号从小到大排序，以便按要求输出
    print(' '.join(map(str, ans)))
