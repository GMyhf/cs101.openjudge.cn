# External reference: cs101.openjudge.cn practice/19546 statistics, Accepted solution 30264505.
# Source: http://cs101.openjudge.cn/practice/solution/30264505/
# Statistics: http://cs101.openjudge.cn/practice/19546/statistics/
# License: not declared on submission page; no license inferred
m = int(input())
for i in range(m):
    a = list(map(float,input().split()))
    for i in range(5, len(a)):
        mom = a[i] - a[i-5]
        if abs(mom - round(mom,1))<1e-6:
            mom = round(mom,1)
        else:
            mom = round(mom,2)
        print(mom, end = ' ')
    print()
