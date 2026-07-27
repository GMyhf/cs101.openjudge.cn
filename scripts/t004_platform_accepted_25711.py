# External reference: statistics page /practice/25711/
# Accepted submission: 52997591
# Source: http://cs101.openjudge.cn/practice/solution/52997591/
# License: not declared on the submission page; no license is inferred.

N, M = map(int,input().split())
result = []
for _ in range(N):
    line = input().split()
    sum1 = 0
    sum2 = 0
    for i in range(1,len(line)-1,2):
        if int(line[i])>=60:
            gpa = 4-(3*((100-int(line[i]))**2)/1600)
        else:
            gpa = 0
        sum1 += gpa * int(line[i+1])
        sum2 += int(line[i+1])
        aver = sum1/sum2

    result.append([line[0],aver])
result = sorted(result,key=lambda x:x[1],reverse=True)[:M]
name = []
for i in range(M):
    name.append(result[i][0])
print(' '.join(name))