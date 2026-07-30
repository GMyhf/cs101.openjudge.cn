# External reference: http://cs101.openjudge.cn/practice/27300/statistics/
# Accepted submission: 52474297
# Source: http://cs101.openjudge.cn/practice/solution/52474297/
# License: not declared on the submission page; no license is inferred.

n=int(input())
d={}
l=[]
nam=set()
for _ in range(n):
    query=input().split("-")
    if query[0] in d:
        d[query[0]].append(" "+query[1])
    else:
        d[query[0]]=[" "+query[1]]
        l.append(query[0])

l.sort()
for name in l:
    d[name].sort(reverse=True,key=lambda x:(x[-1],-float(x[:-1])))
    print(name+":"+",".join(d[name]))
