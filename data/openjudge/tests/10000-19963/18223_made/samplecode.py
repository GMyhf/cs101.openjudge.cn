# External reference: http://cs101.openjudge.cn/practice/18223/statistics/
# Accepted submission: 52528186
# Source: http://cs101.openjudge.cn/practice/solution/52528186/
# License: not declared on the submission page; no license is inferred.

def _24points(arr):
    #print(*arr)
    if len(arr) == 1:
        if arr[0] == 24: return True
        else: return False
    l = len(arr)
    for i in range(l - 1):
        for j in range(i + 1, l):
            for k in range(6):
                newa = newarr(arr,i,j,k)
                if newa is not None:
                    if _24points(newa): return True
    return False

def calc(x,y,num):
    if num == 0: return x+y
    if num == 1: return x-y
    if num == 2: return y-x
    #if num == 3: return x*y
    #if num == 4: return x/y if y else None
    #if num == 5: return y/x if x else None

def newarr(arr,i,j,k):
    newele = calc(arr[i],arr[j],k)
    if newele is not None:
        return arr[:i]+arr[i+1:j]+arr[j+1:]+[newele]



for _ in range(int(input())):
    a = list(map(int,input().split()))
    #print(newarr(a,0,1,3))
    #print(newarr(newarr(a,0,1,3),0,1,3))
    if 1:
        if _24points(a): print("YES")
        else: print("NO")
