# External reference: http://cs101.openjudge.cn/practice/30204/statistics/
# Accepted submission: 52203120
# Source: http://cs101.openjudge.cn/practice/solution/52203120/
# License: not declared on the submission page; no license is inferred.

n,m=[int(i) for i in input().split()]
x=[]
y=[]
z=[]
for i in range(n):
    query=input().split()
    x.append(int(query[0]))
    y.append(int(query[1]))
    z.append(int(query[0])+int(query[1]))

count=0
result=min(z)
x.sort()
sum1=0
for i in x:
    if i<result/2:
        if sum1+i>m:
            break
        sum1+=i
        count+=1
    else:
        break
count+=((m-sum1)//result)*2
rest=(m-sum1)%result
if rest>=result/2:
    count+=1
print(count)
