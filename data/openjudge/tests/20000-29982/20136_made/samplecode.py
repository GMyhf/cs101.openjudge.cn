# External reference: statistics page /practice/20136/
# Accepted submission: 22633121
# Source: http://cs101.openjudge.cn/practice/solution/22633121/
# License: not declared on the submission page; no license is inferred.

# External reference: cs101.openjudge.cn practice/20136 statistics, Accepted solution 22633121.
# Source: http://cs101.openjudge.cn/practice/solution/22633121/
# Statistics: http://cs101.openjudge.cn/practice/20136/statistics/
# License: not declared on submission page; no license inferred
def zoutong(z,x,y):
    if x > y:
        ans = zoutong(y,x)
    ans = True
    if z>x and y>z:
        ans = False
    else:
        for i in range(x,y):
            if (i+1) not in portal[i]:
                ans = False
                break
    return ans

policerick,t = map(int,input().split())
check = []
portal = {}
for i in range(t):
    tem = list(map(int,input().split()))
    portal[i] = tem[1:]
    if len(portal[i])>2:
        check.append(i)

if policerick == 1:
    print('YES!')
else:
    flag = False
    for i in check:
        if flag == False:
            for x in range(len(portal[i])-1):
                if flag == False:
                    for y in range(len(portal[i])-x-1):
                        if flag == False:
                            if zoutong(i,portal[i][x],portal[i][x+y+1]):
                                if portal[i][x+y+1]-portal[i][x]+1 >= policerick:
                                    flag = True
        else:
            break

    if flag == True:
        print('YES!')
    else:
        print('NO!')
