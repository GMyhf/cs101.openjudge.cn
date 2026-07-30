# External reference: http://cs101.openjudge.cn/practice/29982/statistics/
# Accepted submission: 52249020
# Source: http://cs101.openjudge.cn/practice/solution/52249020/
# License: not declared on the submission page; no license is inferred.

def digit_sum(num):
    val=0
    for k in str(num):
        val+=int(k)
    return val

m,n,k=[int(i) for i in input().split(",")]
di={}
i=0
while i*k<46:
    i+=1
    di[str(i)]=[]
for i in range(m+1,n):
    jqy=digit_sum(i)
    if jqy%k==0:
        di[str(jqy//k)].append(str(i))
for key in di:
    if di[key]:
        print(",".join(di[key]))
