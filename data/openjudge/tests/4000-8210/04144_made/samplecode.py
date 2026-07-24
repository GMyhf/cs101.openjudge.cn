# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# 时间调度问题
# cows元素：（start, end, index，）
import heapq
max_num = 1
n = int(input())
cows = []
number = [0]*n  # 记录每一只牛所在的畜栏
for i in range(n):
    cows.append(list(map(int, input().split())))
for i in range(n):
    cows[i].append(i)  # 为每只牛添加编号后再排序

cows.sort(key=lambda x: x[0]) # 先按开始时间排序
column = []  # 创建列表【畜栏】
heapq.heappush(column, [cows[0][1], 0]) # 初始时只有一个元素，即为第一只牛的结束时间
number[cows[0][2]] = 1  # 第一只牛默认在第一个畜栏

for i in range(1, len(cows)):  # 对之后的每只牛遍历
    k = heapq.heappop(column)
    if k[0] < cows[i][0]: # 最早结束的已经结束，新的牛可使用该畜栏
        heapq.heappush(column, [cows[i][1], k[1]])
        number[cows[i][2]] = k[1]+1
    else:
        heapq.heappush(column, k)
        heapq.heappush(column, [cows[i][1], max_num])
        max_num += 1
        number[cows[i][2]] = max_num

print(len(column))  # 【畜栏】的长度即为畜栏数量
for i in number:
    print(i)
