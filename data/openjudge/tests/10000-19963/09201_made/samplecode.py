# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
#蒋子轩
from bisect import *
n=int(input())
a=list(map(int,input().split()))
sorted_list=[]
cnt=0
for num in a:
    pos=bisect_left(sorted_list,num)
    cnt+=pos
    insort_left(sorted_list,num)
print(cnt)
