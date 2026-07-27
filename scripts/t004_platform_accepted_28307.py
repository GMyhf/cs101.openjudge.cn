# External reference: statistics page /practice/28307/
# Accepted submission: 52726248
# Source: http://cs101.openjudge.cn/practice/solution/52726248/
# License: not declared on the submission page; no license is inferred.

n = int(input().strip())
data = []
data.append(list(map(int, input().strip().split())))
data.append(list(map(int, input().strip().split())))
k = int(input().strip())

reward1 = []
reward2 = []
for i in range(n):
    if data[0][i] >= data[1][i]:
        reward1.append((data[0][i], data[1][i],abs(data[0][i]-data[1][i])))
    else:
        reward2.append((data[0][i], data[1][i],abs(data[0][i]-data[1][i])))
reward1.sort(key = lambda x:x[2],reverse = True)
reward2.sort(key = lambda x:x[2])

result = 0
if k <= len(reward1):
    for i in range(k):
        result += reward1[i][0]
    for i in range(k,len(reward1)):
        result += reward1[i][1]
    for i in range(len(reward2)):
        result += reward2[i][1]
else:
    for i in range(len(reward1)):
        result += reward1[i][0]
    for i in range(k-len(reward1)):
        result += reward2[i][0]
    for i in range(k-len(reward1),len(reward2)):
        result += reward2[i][1]
print(result)