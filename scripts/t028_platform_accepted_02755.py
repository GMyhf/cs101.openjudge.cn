# External reference: http://cs101.openjudge.cn/practice/02755/statistics/
# Accepted submission: 52544614
# Source: http://cs101.openjudge.cn/practice/solution/52544614/
# License: not declared on the submission page; no license is inferred.

n=int(input())
vols=[]
count=0
for i in range(n):
    vols.append(int(input()))
def dfs(index, total):
    global count
    # 终止条件：所有物品都处理完了
    if index == n:
        # 如果体积刚好是40，方案数+1
        if total == 40:
            count += 1
        return

    # 第一种选择：不选当前物品，直接处理下一个
    dfs(index + 1, total)

    # 第二种选择：选当前物品（总体积不超过40才选）
    if total + vols[index] <= 40:
        dfs(index + 1, total + vols[index])
dfs(0,0)
print(count)
