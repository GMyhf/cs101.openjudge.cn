# External reference: statistics page /practice/28058/
# Accepted submission: 52734701
# Source: http://cs101.openjudge.cn/practice/solution/52734701/
# License: not declared on the submission page; no license is inferred.

# 存菜品：name:[price, stock]
food = dict()
n, m = map(int, input().split())

for _ in range(n):
    name, p, s = input().split()
    price = int(p)
    stock = int(s)
    food[name] = [price, stock]

income = 0
# 处理每个学生的3个菜
for _ in range(m):
    lst = input().split()
    for dish in lst:
        pr, st = food[dish]
        if st > 0:
            income += pr
            food[dish][1] -= 1

print(income)