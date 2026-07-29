# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1037: A decorative fence
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/01037/
# License: not declared in source collection; no license is inferred.
import sys
# http://cs101.openjudge.cn/practice/01037/
#
# https://blog.csdn.net/u014236804/article/details/38373729
# POJ1037 A decorative fence by Guo Wei

UP = 0
DOWN = 1
MAXN = 25

arr = lambda m,n,l : [ [ [0 for k in range(l)] for j in range(n)] for i in range(m) ]
#m = arr(2,3,4)

# C[i][k][DOWN] 是S(i)中以第k短的木棒打头的DOWN方案数,C[i][k][UP] 是S(i)中以第k短的木棒打头的UP方案数,第k短指i根中第k短
C = arr(MAXN, MAXN, 2)

def Init(n: int):
    C[1][1][UP] = C[1][1][DOWN] = 1
    for i in range(2, n+1):
        for k in range(1, i+1):         # 枚举第一根木棒的长度
            for M in range(k, i):       # 枚举第二根木棒的长度
                C[i][k][UP] += C[i-1][M][DOWN]
            for N in range(1, k):       # 枚举第二根木棒的长度
                C[i][k][DOWN] += C[i-1][N][UP]

# 总方案数是 Sum{ C[n][k][DOWN] + C[n][k][UP] } k = 1.. n;

def Print(n: int, cc: int):
    skipped = 0         #已经跳过的方案数
    seq = [0]*MAXN      #最终要输出的答案
    used = [False]*MAXN     #木棒是否用过

    for i in range(1, n+1):     # 依次确定每一个位置i的木棒序号
        oldVal = skipped
        k = 0
        No = 0      # k是剩下的木棒里的第No短的,No从1开始算
        for k in range(1, n+1):     # 枚举位置i的木棒 ，其长度为k
            oldVal = skipped
            if used[k]==False:
                No += 1      # k是剩下的木棒里的第No短的
                if i == 1:
                    skipped += C[n][No][UP] + C[n][No][DOWN]
                else:
                    if k > seq[i-1] and ( i <=2 or seq[i-2]>seq[i-1]): #合法放置
                        skipped += C[n-i+1][No][DOWN]
                    elif k < seq[i-1] and (i<=2 or seq[i-2]<seq[i-1]): #合法放置
                        skipped += C[n-i+1][No][UP]

                if skipped >= cc:
                    break


        used[k] = True
        seq[i] = k
        skipped = oldVal

    print(' '.join(map(str, seq[1:n+1])))
    '''
    for i in range(1, n+1):
        print("{}".format(seq[i]), end=' ')
    print()
    '''

Init(20);
for _ in range(int(input())):
    n, c = map(int, input().split())

    Print(n,c)
