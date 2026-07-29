# External reference: http://cs101.openjudge.cn/practice/02141/statistics/
# Accepted submission: 51717315
# Source: http://cs101.openjudge.cn/practice/solution/51717315/
# License: not declared on the submission page; no license is inferred.

key = input()
d = {}
for i in range(26):
    d[chr(i+97)] = key[i]
    d[chr(i+65)] = key[i].upper()
res = ''
message = input()
for char in message:
    if char == ' ':
        res += ' '
    else:
        res += d[char]
print(res)
