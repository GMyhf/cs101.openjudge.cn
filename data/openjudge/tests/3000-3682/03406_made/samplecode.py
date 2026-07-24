# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# 蒋子轩23工学院
def min_cows_to_reach(N, B):
	# 二分查找变形，找大于等于B的最小索引
    left, right = 1, N
    while left < right:  #注意不能取等
        mid = (left + right) // 2 #左偏
        if prefix_sum[mid]>=B:  #等于时继续向左找
            right = mid   #注意不-1，
        else:
            left = mid + 1
    return left  #return不取等的那个
N, B = map(int, input().split())
cows = [int(input()) for _ in range(N)]
#优先选择高的
cows.sort(reverse=True)
#计算前缀和
prefix_sum = [0] * (len(cows) + 1)
for i in range(1, len(cows)+1):
    prefix_sum[i] = prefix_sum[i-1] + cows[i-1]
print(min_cows_to_reach(N, B))
