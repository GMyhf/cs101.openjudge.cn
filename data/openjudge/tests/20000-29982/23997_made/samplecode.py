# External reference: statistics page /practice/23997/
# Accepted submission: 52997582
# Source: http://cs101.openjudge.cn/practice/solution/52997582/
# License: not declared on the submission page; no license is inferred.

# External reference: statistics page /practice/23997/
# Accepted submission: 52997582
# Source: http://cs101.openjudge.cn/practice/solution/52997582/
# License: not declared on the submission page; no license is inferred.

nn=int(input())
l=[]

def dfs(n,ans):
    if n==0:
        l.append(ans[:])

    for i in range(1,n+1):
        if i%2==1 and (i not in ans) :
            if ans:
                if i > max(ans):
                    nans=ans.copy()
                    nans.append(i)
                    dfs(n-i,nans)
            else:
                nans = ans.copy()
                nans.append(i)
                dfs(n - i, nans)

dfs(nn,[])
l=sorted(l)
for i in l:
    print(" ".join(map(str,i)))
print(len(l))