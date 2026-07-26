# External reference: statistics page /practice/10715/
# Accepted submission: 48220499
# Source: http://cs101.openjudge.cn/practice/solution/48220499/
# License: not declared on the submission page; no license is inferred.

from itertools import permutations


def dfs(nums):
    if len(nums) == 1:
        return nums[0] == 42

    for i in range(len(nums) - 1):
        left = nums[i]
        right = nums[i + 1]
        results = [left + right, left - right, left * right]

        if right != 0 and left % right == 0:  # 确保除法结果是整数
            results.append(left // right)

        # 对每种运算结果进行递归
        for result in results:
            if dfs(nums[:i] + [result] + nums[i + 2:]):
                return True

    return False
n = int(input())
if n == 1:
    print('NO')
    exit()
t = list(map(int, input().split()))
p = list(map(list, permutations(t)))
vis = {''}
for a in p:
    if ''.join(str(i) for i in a) in vis:
        continue
    if dfs(a):
        print('YES')
        exit()
    vis.add(''.join(str(i) for i in a))
print('NO')