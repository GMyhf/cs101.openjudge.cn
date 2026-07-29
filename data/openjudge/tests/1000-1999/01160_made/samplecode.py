# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1160: Post Office
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/01160/
# License: not declared in source collection; no license is inferred.
import sys
# https://blog.csdn.net/u011262722/article/details/9298011
# uses dynamic programming to efficiently solve the problem of partitioning
# an array into p subarrays with minimum cost.
#
# dp是前i个村庄建j个邮局，dis是在i和j村庄间建邮局的最小距离
'''
【题目大意】：用数轴描述一条高速公路，有V个村庄，每一个村庄坐落在数轴的某个点上，需要选择P个村庄在其中建立邮局，
要求每个村庄到最近邮局的距离和最小。
【题目分析】：经典DP
1、考虑在V个村庄中只建立【一个】邮局的情况，显然可以知道，将邮局建立在中间的那个村庄即可。
也就是在a到b间建立一个邮局，若使消耗最小，则应该将邮局建立在（a+b)/2这个村庄上。
2、下面考虑建立【多个】邮局的问题，可以这样将该问题拆分为若干子问题，在前i个村庄中建立j个邮局的最短距离，
是在前【k】个村庄中建立【j-1】个邮局的最短距离与 在【k+1】到第i个邮局建立【一个】邮局的最短距离的和。
而建立一个邮局我们在上面已经求出。

3、状态表示，由上面的讨论，可以开两个数组
dp[i][j]:在前i个村庄中建立j个邮局的最小耗费
dis[i][j]:在第i个村庄到第j个村庄中建立1个邮局的最小耗费
那么就有转移方程：dp[i][j] = min(dp[i][j],dp[k][j-1]+dis[k+1][i])
DP的边界状态即为dp[i][1] = dis[1][i]; 所要求的结果即为dp[village_num][post office_num];

4、然后就说说求sum数组的优化问题，可以假定有6个村庄，村庄的坐标已知分别为p1,p2,p3,p4,p5,p6;
那么，如果要求sum[1][4]的话邮局需要建立在2或者3处,放在2处的消耗为p4-p2+p3-p2+p2-p1=p4-p2+p3-p1
放在3处的结果为p4-p3+p3-p2+p3-p1=p4+p3-p2-p1，可见，将邮局建在2处或3处是一样的。
现在接着求sum[1][5],现在处于中点的村庄是3，那么1-4到3的距离和刚才已经求出了，即为sum[1][4],
所以只需再加上5到3的距离即可。同样，求sum[1][6]的时候也可以用sum[1][5]加上6到中点的距离。
所以有递推关系：sum[i][j] = sum[i][j-1] + p[j] -p[(i+j)/2]

'''
v, p = map(int, input().split())
x = [0] + list(map(int, input().split()))
dis = [[0] * (v + 1) for _ in range(v + 1)]
dp = [[0] * (v + 1) for _ in range(v + 1)]
for i in range(1, v + 1):
    for j in range(i + 1, v + 1):
        dis[i][j] = dis[i][j - 1] + x[j] - x[(i + j) // 2]
for i in range(1, v + 1):
    dp[i][i] = 0
    dp[i][1] = dis[1][i]
for j in range(2, p + 1):
    for i in range(j + 1, v + 1):
        dp[i][j] = float("inf")
        for k in range(j - 1, i):
            dp[i][j] = min(dp[i][j], dp[k][j - 1] + dis[k + 1][i])
print(dp[v][p])
