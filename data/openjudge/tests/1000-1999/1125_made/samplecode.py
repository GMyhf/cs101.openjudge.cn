# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1125: Stockbroker Grapevine
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/01125/
# License: not declared in source collection; no license is inferred.
import heapq
while True:
    n=int(input())
    if n==0:
        break
    contact=[{}]
    for _ in range(n):
        list1=list(map(int,input().split()))
        dict1={}
        for i in range((len(list1)-1)//2):
            dict1[list1[2*i+1]]=list1[2*i+2]
        contact.append(dict1)
    i0=0
    s=float('inf')
    for i in range(1,n+1):
        heap=[(0,i)]
        heapq.heapify(heap)
        time=[0]+[float('inf')]*n
        time[i]=0
        condition=[True]+[False]*n
        while heap:
            t,j=heapq.heappop(heap)
            if condition[j]:
                continue
            condition[j]=True
            if sum(condition)==n+1:
                if max(time)<s:
                    s=max(time)
                    i0=i
                break
            for k in contact[j]:
                t1=t+contact[j][k]
                if not condition[k] and time[k]>t1:
                    time[k]=t1
                    heapq.heappush(heap,(t1,k))
    if i0==0:
        print('disjoint')
    else:
        print(f'{i0} {s}')
