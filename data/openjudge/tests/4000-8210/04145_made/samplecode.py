# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# 蒋子轩23工学院
def can_achieve(target,a,b,k):
    diffs=[a[i]-target*b[i] for i in range(len(a))]
    diffs.sort()
    #放弃k场考试后可以达到target
    return sum(diffs[k:])>=0
def max_avg_score(k,a,b):
    l,r=0,100
    while r-l>1e-5:
    	#非整数二分
        m=(l+r)/2
        if can_achieve(m,a,b,k):
            l=m
        else:
            r=m
    return m*100
while True:
    n,k=map(int,input().split())
    if n==0 and k==0:
        break
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    print(f'{max_avg_score(k,a,b):.0f}')
