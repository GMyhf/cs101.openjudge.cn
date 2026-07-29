# External reference: http://cs101.openjudge.cn/pctbook/M02977/statistics/
# Accepted submission: 53000288
# Source: http://cs101.openjudge.cn/pctbook/solution/53000288/
# License: not declared on the submission page; no license is inferred.

s = input().split()
p,e,i,d = int(s[0])%23,int(s[1])%28,int(s[2])%33,int(s[3])
t = 0
while t % 23 != p:
    t += 924
while t % 28 != e:
    t += 759
while t % 33 != i:
    t += 644
t = (t-d) % 21252
if t == 0:
    t = 21252
print(t)
