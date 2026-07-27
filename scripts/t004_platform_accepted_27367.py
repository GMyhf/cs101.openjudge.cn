# External reference: statistics page /practice/27367/
# Accepted submission: 52735844
# Source: http://cs101.openjudge.cn/practice/solution/52735844/
# License: not declared on the submission page; no license is inferred.

n, m = map(int, input().split())
students = []

for _ in range(n):
    parts = list(map(int, input().split()))
    idx = parts[0]          # 编号
    scores = parts[1:]     # 分数列表

    # 1. 计算优秀次数（>=90）
    excellent = sum(1 for s in scores if s >= 90)

    # 2. 计算进步总和
    progress = 0
    for i in range(1, len(scores)):
        diff = scores[i] - scores[i-1]
        if diff > 0:
            progress += diff

    students.append((-excellent, -progress, idx))  # 负号=降序

# 排序：默认升序，负号就等价于降序
students.sort()

# 输出
for s in students:
    print(s[2])