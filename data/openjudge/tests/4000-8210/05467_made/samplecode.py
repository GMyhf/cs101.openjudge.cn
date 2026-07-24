# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
#23n2300011072(X)
from collections import defaultdict
def add(a):
    i=0
    while 1:
        m,n=a[i],a[i+1]
        if n<0:
            break
        res[n]+=m
        i+=2
for _ in range(int(input())):
    res=defaultdict(int)
    add(list(map(int,input().split())))
    add(list(map(int,input().split())))
    for i in sorted(res,reverse=True):
        if res[i]!=0:
            print(f'[ {res[i]} {i} ] ',end='')
    print()
