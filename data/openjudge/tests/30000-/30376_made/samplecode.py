# External reference: http://cs101.openjudge.cn/practice/30376/statistics/
# Accepted submission: 52723526
# Source: http://cs101.openjudge.cn/practice/solution/52723526/
# License: not declared on the submission page; no license is inferred.

s = input().strip()
count = 0
# 记录当前层收集到的字符
current = set()

for char in s:
    current.add(char)
    # 当前层集齐所有26个字母，层数+1，清空重新收集
    if len(current) == 26:
        count += 1
        current.clear()

# 最短非子序列长度 = 层数 + 1
print(count + 1)
