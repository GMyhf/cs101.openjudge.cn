# External reference: cs101.openjudge.cn practice/04142 statistics, Accepted solution 51048618.
# Source: http://cs101.openjudge.cn/practice/solution/51048618/
# Statistics: http://cs101.openjudge.cn/practice/04142/statistics/
# License: not declared on submission page; no license inferred
def fun(x):
    return x**5-15*x**4+85*x**3-225*x**2+274*x-121
left, right = 1.5, 2.4
res = 0
while right-left > 10**(-7):
    mid = (left+right)/2
    if fun(mid) == 0:
        res = mid
        break
    if fun(mid) < 0:
        right = mid
    else:
        left = mid
if res == 0:
    res = left
print(f'{res:.6f}')