# External reference: http://cs101.openjudge.cn/routine/27150/statistics/
# Accepted submission: 43089968
# Source: http://cs101.openjudge.cn/routine/solution/43089968/
# License: not declared on the submission page; no license is inferred.

j=k=l=m=0
def p(i):print('YES\n'+i);exit()
for i in input():
    if i in'08':p(i)
    elif i in'26':
        j=i
        if'2'==i:
            if k:
                if k in'37':p(k+i)
                elif l:
                    if l in'37':p(l+i)
                    else:p(k+l+i)
        else:
            if k:
                if k in'159':p(k+i)
                elif l:
                    if l in'159':p(l+i)
                    else:p(k+l+i)
    elif'4'==i:
        if j:p(j+i)
        if m:p(k+m+i)
        if k:m=i
    else:
        if not k:k=i
        elif not l:l=i
print('NO')
