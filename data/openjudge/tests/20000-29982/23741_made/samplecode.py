# External reference: statistics page /practice/23741/
# Accepted submission: 52296431
# Source: http://cs101.openjudge.cn/practice/solution/52296431/
# License: not declared on the submission page; no license is inferred.

# External reference: statistics page /practice/23741/
# Accepted submission: 52296431
# Source: http://cs101.openjudge.cn/practice/solution/52296431/
# License: not declared on the submission page; no license is inferred.

ka=[0]*25
ka[1]=1
for i in range(2,25):
    ka[i]=ka[i-1]*(4*i-2)//(i+1)
n=int(input())
print(ka[n])