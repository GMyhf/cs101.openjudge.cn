# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1061: 青蛙的约会
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/01061/
# License: not declared in source collection; no license is inferred.
x,y,m,n,L=map(int,input().split())
a,b=m-n,y-x
# 目标值t满足(t*a)%L==b
if a==0:
    print('Impossible')
    exit()
elif a<0:
    a,b=-a,-b
if b<0:
    b+=L
if L%a==0:
    if b%a==0:
        print(b//a)
        exit()
    else:
        print('Impossible')
        exit()
for i in range(1,L):
    c=(a*i)%L
    if b%c==0:
        print(i*(b//c))
        exit()
