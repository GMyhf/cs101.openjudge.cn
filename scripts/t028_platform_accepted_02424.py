# External reference: http://cs101.openjudge.cn/practice/02424/statistics/
# Accepted submission: 44298654
# Source: http://cs101.openjudge.cn/practice/solution/44298654/
# License: not declared on the submission page; no license is inferred.

while 1:
    a,b,c=map(int,input().split())
    pa=[a,b,c]
    l=[a,b,c]
    now=[[],[],[]]
    flag=[0,0,0]
    ans=0
    if a==0 and b==0 and c==0:
        break
    while 1:
        x=input()
        if x=='#':
            break
        t,p=x.split()
        p=int(p)
        h,m=map(int,t.split(':'))
        t=60*h+m-480
        i=(p-1)//2
        for u in range(flag[i],len(now[i])):
                if now[i][u]+30<=t:
                    l[i]+=1
                else:
                    flag[i]=u
                    break
        if l[i]>0:
                now[i].append(t)
                l[i]-=1
                ans+=p
        elif abs(l[i])<pa[i]:

            now[i].append(now[i][flag[i]+abs(l[i])]+30)
            l[i]-=1
            ans+=p
    print(ans)
