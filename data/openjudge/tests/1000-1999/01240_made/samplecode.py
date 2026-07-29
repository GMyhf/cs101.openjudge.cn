# External reference: http://cs101.openjudge.cn/practice/01240/statistics/
# Accepted submission: 49174560
# Source: http://cs101.openjudge.cn/practice/solution/49174560/
# License: not declared on the submission page; no license is inferred.

from math import comb
def count(m,sPre,sPost):
    if not sPre or not sPost:
        return 1
    i=1
    j=0
    res=1
    k=0
    while i<len(sPre):
        k+=1
        root=sPre[i]
        ind=sPost.index(root)
        sub_tree=ind-j+1
        newPre=sPre[i:i+sub_tree]
        newPost=sPost[j:ind+1]
        res*=count(m,newPre,newPost)
        i=i+sub_tree
        j=ind+1
    res*=comb(m,k)
    return res
while True:
    line=input().split()
    if line[0]=='0':
        break
    m=int(line[0])
    sPre=line[1]
    sPost=line[2]
    print(count(m,sPre,sPost))
