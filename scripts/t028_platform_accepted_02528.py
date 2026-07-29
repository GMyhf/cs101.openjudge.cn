# External reference: http://cs101.openjudge.cn/practice/02528/statistics/
# Accepted submission: 45986421
# Source: http://cs101.openjudge.cn/practice/solution/45986421/
# License: not declared on the submission page; no license is inferred.

for _ in range(int(input())):
    c=int(input());a=[list(map(int,input().split()))for i in range(c)];b=[[-1,-1],[1<<30,1<<30]]
    while a:
        a[-1][1]+=1
        for i in range(len(b)):
            if b[i][1]>=a[-1][0]:
                if b[i][0]<=a[-1][0]and b[i][1]>=a[-1][1]:c-=1;a.pop();break
                if b[i][0]>a[-1][1]:b.insert(i,a.pop());break
                b[i][0]=min(b[i][0],a[-1][0])
                while b[i+1][1]<a[-1][1]:b.pop(i+1)
                b[i][1]=max(a[-1][1],b[i][1])if a[-1][1]<b[i+1][0]else b.pop(i+1)[1];a.pop();break
    print(c)
