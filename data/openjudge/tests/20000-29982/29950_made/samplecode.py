# External reference: http://cs101.openjudge.cn/practice/29950/statistics/
# Accepted submission: 52793309
# Source: http://cs101.openjudge.cn/practice/solution/52793309/
# License: not declared on the submission page; no license is inferred.

s = input().strip()

max_count = 0

for i in range(len(s)):
    number = set()
    count = 0

    for j in range(i, len(s)):
        if s[j] not in number:
            number.add(s[j])
            count += 1
            max_count = max(max_count, count)
        else:
            break

print(max_count)
