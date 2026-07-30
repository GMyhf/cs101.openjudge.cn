# External reference: http://cs101.openjudge.cn/practice/20106/statistics/
# Accepted submission: 52704034
# Source: http://cs101.openjudge.cn/practice/solution/52704034/
# License: not declared on the submission page; no license is inferred.

import heapq
m,n,p=map(int,input().split())
#m为行数，n为列数，p为测试组数
hlist=[]
for i in range(m):
    s=input().split()
    thelist=[]
    for x in s:
        if x=="#":
            thelist.append(-1)
        else:
            thelist.append(int(x))
    hlist.append(thelist)

def dijkstra(start,end):
    directions=[(0,1),(0,-1),(-1,0),(1,0)]
    cost=[(0,start)]
    heapq.heapify(cost)
    flag=0
    result=0
    visited=set()
    while cost:
        w=heapq.heappop(cost)
        currentcost=w[0]
        if w[1] not in visited:
            visited.add(w[1])
            if w[1]==end:
                flag=1
                result=currentcost
            else:
                point=w[1]
                for d in directions:
                    newpoint=(point[0]+d[0],point[1]+d[1])
                    if 0<=newpoint[0]<m and 0<=newpoint[1]<n:
                        if newpoint not in visited:
                            if hlist[newpoint[0]][newpoint[1]]!=-1:
                                newcost=currentcost+abs(hlist[newpoint[0]][newpoint[1]]-hlist[point[0]][point[1]])
                                heapq.heappush(cost,(newcost,tuple(newpoint)))
    return flag ,result
for i in range(p):
    s=input().split()
    start=tuple(map(int,s[:2:]))
    end=tuple(map(int,s[2:]))
    if hlist[start[0]][start[1]]!=-1:
        flag,result=dijkstra(start,end)
        if flag==1:
            if result==float("inf"):
                print("NO")
            else:
                print(result)
        else:
            print("NO")
    else:
        print("NO")
