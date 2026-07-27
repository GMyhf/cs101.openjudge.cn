# External reference: statistics page /practice/26588/
# Accepted submission: 51479172
# Source: http://cs101.openjudge.cn/practice/solution/51479172/
# License: not declared on the submission page; no license is inferred.

for _ in range(int(input())):
    s = input()
    l, m, ma = s[0], 1, 1
    for c in s[1:]:
        m, l = m + 1 if c >= l else 1, c
        ma = max(ma, m)
    print(ma)