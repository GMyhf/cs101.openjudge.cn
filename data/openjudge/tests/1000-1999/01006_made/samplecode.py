# External reference: http://cs101.openjudge.cn/practice/01006/statistics/
# Accepted submission: 52528717
# Source: http://cs101.openjudge.cn/practice/solution/52528717/
# License: not declared on the submission page; no license is inferred.

cases=0
while True:
    p,q,r,d=[int(i) for i in input().split()]
    if p==-1 and q==-1 and r==-1 and d==-1:
        break
    cases+=1
    p%=23
    q%=28
    r%=33
    x=(5051145*q-5031180*p-19964*r)%21252
    while x<=d:
        x+=21252
    print(f"Case {cases}: the next triple peak occurs in {x-d} days.")
