# External reference: statistics page /practice/19965/
# Accepted submission: 43122751
# Source: http://cs101.openjudge.cn/practice/solution/43122751/
# License: not declared on the submission page; no license is inferred.

# External reference: cs101.openjudge.cn practice/19965 statistics, Accepted solution 43122751.
# Source: http://cs101.openjudge.cn/practice/solution/43122751/
# Statistics: http://cs101.openjudge.cn/practice/19965/statistics/
# License: not declared on submission page; no license inferred
def f(a,b):
    if a%b==0:
        return a//b
    else:
        return a//b+1
a,b,c=map(int,input().split())
while b<=a and c>=f(a,b):
    c-=f(a, b)
    b+=a//b
print(b)    
