# External reference: http://cs101.openjudge.cn/practice/20025/statistics/
# Accepted submission: 43186595
# Source: http://cs101.openjudge.cn/practice/solution/43186595/
# License: not declared on the submission page; no license is inferred.

def f(x):
    if x==1:
        return
    for i in range(2,x+1):
        if x%i==0:
            dic[i]=dic.setdefault(i,0)+1
            f(x//i)
            break
flag=0
for u in input().split(','):
    for t in u.split():
        if t.isdigit():
            flag=1
            t=int(t)
            if t==0:
                print('no')
                continue
            dic={}
            f(t)
            ans=[]
            if t==1 or t in dic:
                print('no')
                continue
            for j in sorted(dic):
                if dic[j]==1:
                    ans.append(str(j))
                else:
                    ans.append('%d^%d'%(j,dic[j]))
            print(str(t)+'='+'*'.join(ans))
if flag==0:
    print('error')
