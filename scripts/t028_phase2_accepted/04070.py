# External reference: http://cs101.openjudge.cn/practice/04070/statistics/
# Accepted submission: 52468009
# Source: http://cs101.openjudge.cn/practice/solution/52468009/
# License: not declared on the submission page; no license is inferred.

def dig(arr,num):
    read=[]
    for i in arr:
        if i!=num:
            read.append(i)
    return read
def gen(arr):
    global result
    if len(arr)==1:
        return [[arr[0]]]
    ans=[]
    for i in arr:
        x=gen(dig(arr,i))
        for j in x:
            ans.append([i]+j)
    return ans

while True:
    n=int(input())
    if n==0:
        break
    else:
        for x in gen([i+1 for i in range(n)]):
            print(*x)
