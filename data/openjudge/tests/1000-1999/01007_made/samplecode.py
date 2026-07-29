# External reference: http://cs101.openjudge.cn/practice/01007/statistics/
# Accepted submission: 52544822
# Source: http://cs101.openjudge.cn/practice/solution/52544822/
# License: not declared on the submission page; no license is inferred.

v = {'A':0, 'C':1, 'G':2, 'T':3}
n, m = map(int, input().split())
dna = [input().strip() for _ in range(m)]

# 计算逆序对（极简暴力法）
def count(s):
    return sum(v[s[i]] > v[s[j]] for i in range(n) for j in range(i+1, n))

# 按逆序对+输入顺序排序，直接输出
for s in sorted(dna, key=lambda x: (count(x), dna.index(x))):
    print(s)
