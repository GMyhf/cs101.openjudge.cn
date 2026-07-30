# External reference: http://cs101.openjudge.cn/practice/27141/statistics/
# Accepted submission: 51841578
# Source: http://cs101.openjudge.cn/practice/solution/51841578/
# License: not declared on the submission page; no license is inferred.

n = int(input())
nums = list(map(int,input().split()))
prefix = [0]*(n)
prefix[0] = nums[0] - 520
for i in range(len(nums)):
    prefix[i] = prefix[i-1] + nums[i] - 520
dict = {0:-1}
length = []
for i , val in enumerate(prefix):
    if val in dict:
        length.append(i-dict[val])
    else:
        dict[val] = i

print(max(length)*520)
