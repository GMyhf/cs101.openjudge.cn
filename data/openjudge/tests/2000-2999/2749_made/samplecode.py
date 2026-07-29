# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2749: 分解因数
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/2025sp_routine/02749/
# License: not declared in source collection; no license is inferred.
# 蒋子轩23工学院
def decompositions(n,minfactor):
    if n==1:
        return 1
    count=0
    for i in range(minfactor,n+1):
        if n%i==0:
        #递归，只找更大的因数，避免重复
            count+=decompositions(n//i,i)
    return count
n=int(input())
for _ in range(n):
    x=int(input())
    print(decompositions(x,2))
