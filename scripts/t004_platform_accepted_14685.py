k, n = map(int, input().split())
money = []
for _ in range(n):
    money.append(int(input()))

# 使用集合加快查找速度
money_set = set(money)
# 使用集合去重
found = set()
result = []

for a in money:
    b = k - a
    if b in money_set:
        # 确保不是同一个元素（当a=b时，需要有两个相同的数）
        if a != b or money.count(a) > 1:
            # 标准化组合：较小的在前
            pair = (min(a, b), max(a, b))
            if pair not in found:
                found.add(pair)
                result.append(pair)

# 排序输出
result.sort(key=lambda x: x[0])
if result:
    for a, b in result:
        print(f'{a} {b}')
else:
    print('No Solution')