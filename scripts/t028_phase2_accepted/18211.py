# External reference: http://cs101.openjudge.cn/practice/18211/statistics/
# Accepted submission: 52602683
# Source: http://cs101.openjudge.cn/practice/solution/52602683/
# License: not declared on the submission page; no license is inferred.

money=int(input())
price=list(map(int,input().split()))
price.sort()
dis=0
while price:
    if money>=price[0]:
        money-=price.pop(0)
        dis+=1
    else:
        if len(price)==1:
            break
        elif dis==0:
            break
        else:
            money+=price.pop()
            dis-=1
print(dis)
