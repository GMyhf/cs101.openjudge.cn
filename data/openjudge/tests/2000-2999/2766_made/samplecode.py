# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2766: 最大子矩阵
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024fallroutine/02766/
# License: not declared in source collection; no license is inferred.
def kadane(s):
    curr_max = total_max = s[0]
    for x in s[1:]:
        curr_max = max(x, curr_max + x)
        total_max = max(total_max, curr_max)
    return total_max

def max_sum_matrix(mat):
    max_sum = -float('inf')
    row, col = len(mat), len(mat[0])
    for top in range(row):
        col_sum = [0] * col
        for bottom in range(top, row):
            for c in range(col):
                col_sum[c] += mat[bottom][c]
            max_sum = max(max_sum, kadane(col_sum))
    return max_sum

n = int(input())
nums = []
while len(nums) < n**2:
    nums.extend(input().split())
mat = [list(map(int, nums[i*n:(i+1)*n])) for i in range(n)]
print(max_sum_matrix(mat))
