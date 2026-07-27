# External reference: statistics page /practice/20196/
# Accepted submission: 31921452
# Source: http://cs101.openjudge.cn/practice/solution/31921452/
# License: not declared on the submission page; no license is inferred.

# External reference: statistics page /practice/20196/
# Accepted submission: 31921452
# Source: http://cs101.openjudge.cn/practice/solution/31921452/
# License: not declared on the submission page; no license is inferred.

lt1=[31,29,31,30,31,30,31,31,30,31,30,31]
lt=[31,28,31,30,31,30,31,31,30,31,30,31]
import math
y,m,d=map(int,input().split())
i_sl=365
G=y
if (y%4==0 and y%100!=0) or y%400==0:
    used=lt1
    i_sl=366
else:
    used=lt
G+=(sum(used[:m-1])+d-1)/i_sl
H=(G-621.5774) / 0.970224

y1=int(H)
d1=H-y1
lt2={2,5,7,10,13,16,18,21,24,26,29}
is_sleap=354
if y1%30 in lt2:
    is_sleap=355
d1*=is_sleap

d1=math.ceil(d1)

m1=0
mut_year=[30,29,30,29,30,29,30,29,30,29,30,29]
while m1<11 and d1>mut_year[m1]:
    d1-=mut_year[m1]
    m1+=1
print(y1,m1+1,d1)