# External reference: statistics page /practice/24510/
# Accepted submission: 52740116
# Source: http://cs101.openjudge.cn/practice/solution/52740116/
# License: not declared on the submission page; no license is inferred.

# External reference: statistics page /practice/24510/
# Accepted submission: 52740116
# Source: http://cs101.openjudge.cn/practice/solution/52740116/
# License: not declared on the submission page; no license is inferred.

def time2sec(t):
    h, m, s = map(int, t.split(':'))
    return h * 3600 + m * 60 + s

from collections import defaultdict
dic = defaultdict(int)

n = int(input())
for _ in range(n):
    name, st, ed = input().split()
    sec1 = time2sec(st)
    sec2 = time2sec(ed)
    dic[name] += sec2 - sec1

# 找总时长最大的文件名
max_name = max(dic, key=lambda k: dic[k])
print(max_name)