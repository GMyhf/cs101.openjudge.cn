# External reference: http://cs101.openjudge.cn/practice/19963/statistics/
# Accepted submission: 52668820
# Source: http://cs101.openjudge.cn/practice/solution/52668820/
# License: not declared on the submission page; no license is inferred.

from fractions import Fraction
a=int(input())
pairs = [i[1:-1] for i in input().split()]
list1=[ sum(map(int,i.split(','))) for i in pairs]
price=list(map(int,input().split()))
ratio=[Fraction(list1[i],price[i])for i in range(a)]
if a%2==0:
    sum1=0
    price1=price.copy()
    price1.sort()
    midprice=(price1[a//2]+price1[a//2-1])/2
    ratio1=ratio.copy()
    ratio1.sort()
    midratio=(ratio1[a//2]+ratio1[a//2-1])/2
    for i in range(a):
        if price[i]<midprice and ratio[i]>midratio:
            sum1+=1
        else:
            continue
    print(sum1)
else:
    sum1=0
    price1=price.copy()
    price1.sort()
    midprice=price1[a//2]
    ratio1=ratio.copy()
    ratio1.sort()
    midratio=ratio1[a//2]
    for i in range(a):
        if price[i]<midprice and ratio[i]>midratio:
            sum1+=1
        else:
            continue
    print(sum1)
