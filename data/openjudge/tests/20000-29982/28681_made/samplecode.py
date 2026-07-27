# External reference: statistics page /practice/28681/
# Accepted submission: 52734455
# Source: http://cs101.openjudge.cn/practice/solution/52734455/
# License: not declared on the submission page; no license is inferred.

import sys

input = sys.stdin.read
data = input().split()

n = int(data[0])
students = []

index = 1
for i in range(1, n+1):
    chi = int(data[index])
    math = int(data[index+1])
    eng = int(data[index+2])
    total = chi + math + eng
    students.append((total, chi, -i, i))  # total desc, chi desc, id asc (use -i)
    index += 3

# Sort: total descending, chinese descending, id ascending
students.sort(reverse=True)

# Output top 5
for i in range(5):
    sid = students[i][3]
    total = students[i][0]
    print(sid, total)