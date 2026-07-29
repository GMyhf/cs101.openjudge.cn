# External reference: http://cs101.openjudge.cn/practice/03225/statistics/
# Accepted submission: 50843945
# Source: http://cs101.openjudge.cn/practice/solution/50843945/
# License: not declared on the submission page; no license is inferred.

for i in range(2,101):
    for j in range(i + 1,101):
        for k in range(j + 1,101):
            if i**2 + j**2 == k**2:
                print(str(i)+'*'+str(i)+' + '+str(j)+'*'+str(j)+' = '+str(k)+'*'+str(k))
