# External reference: statistics page /practice/19998/
# Accepted submission: 52529434
# Source: http://cs101.openjudge.cn/practice/solution/52529434/
# License: not declared on the submission page; no license is inferred.

# External reference: cs101.openjudge.cn practice/19998 statistics, Accepted solution 52529434.
# Source: http://cs101.openjudge.cn/practice/solution/52529434/
# Statistics: http://cs101.openjudge.cn/practice/19998/statistics/
# License: not declared on submission page; no license inferred
m,n=map(int,input().split())
hp=list(map(int,input().split()))+list(map(int,input().split()))
def mani():
    con=False
    for i in range(14):
        if hp[i]>=2:
            hp[i]-=1
        elif hp[i]==1:
            hp[i]-=1
            con=True
    if con:
        mani()

def pan():
    for i in range(14):
        if hp[i]>0:
            return False
    return True

while m>=1 and n>=2:
    m-=1
    n-=2
    mani()

if pan():
    print("YES")
else:
    print("NO")
