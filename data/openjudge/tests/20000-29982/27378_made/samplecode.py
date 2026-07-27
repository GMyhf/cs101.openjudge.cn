# External reference: statistics page /practice/27378/
# Accepted submission: 52739303
# Source: http://cs101.openjudge.cn/practice/solution/52739303/
# License: not declared on the submission page; no license is inferred.

key = input()
s = input()
ans = []

for char in s:
    if char != '.':
        ans.append(char)

    if char == '.':
        ans.append(key)

print(''.join(ans))