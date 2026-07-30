# External reference: http://cs101.openjudge.cn/practice/18109/statistics/
# Accepted submission: 51275581
# Source: http://cs101.openjudge.cn/practice/solution/51275581/
# License: not declared on the submission page; no license is inferred.

inp = input().strip()
d = {}
for i in inp:
    char = i.lower()
    if char not in d:
        d[char] = 0
    d[char] += 1
string, num = '', 0
for k, v in d.items():
    if v > num:
        string = k
        num = v
print(string, num)
