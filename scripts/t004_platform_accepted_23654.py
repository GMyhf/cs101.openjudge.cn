# External reference: statistics page /practice/23654/
# Accepted submission: 52485897
# Source: http://cs101.openjudge.cn/practice/solution/52485897/
# License: not declared on the submission page; no license is inferred.

x=int(input())
lis=[]
while True:
    x+=1
    lis=list(str(x))
    zan=0
    for i in range(4):
        zan+=int(lis[i])
    if zan==20:
        print(x)
        break