# External reference: cs101.openjudge.cn practice/04151 statistics, Accepted solution 52542931.
# Source: http://cs101.openjudge.cn/practice/solution/52542931/
# Statistics: http://cs101.openjudge.cn/practice/04151/statistics/
# License: not declared on submission page; no license inferred
while True:
    n=int(input())
    if n==0:
        break
    movie=[tuple(int(i) for i in input().split()) for _ in range(n)]
    movie.sort(key=lambda x:(x[1],x[0]))
    cborder=-float('inf')
    cnt=0
    for start,end in movie:
        if start>=cborder:
            cnt+=1
            cborder=end
    print(cnt)