# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2812: 恼人的青蛙
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02812/
# License: not declared in source collection; no license is inferred.
import sys
import array
def is_valid(x, y):
    return 0 < x <= R and 0 < y <= C
R, C = map(int, input().split())
N = int(input())
#紧凑数组，省内存
flag = [array.array("B", [0] * (C + 1)) for _ in range(R + 1)]
points = [tuple(map(int, input().split())) for _ in range(N)]
for x, y in points:
    flag[x][y] = 1
#排序，先按行升序，再按列升序
points.sort()
max_count = 2
for i in range(N):
    x1, y1 = points[i]
    for j in range(i + 1, N):
        x2, y2 = points[j]
        dx, dy = x2 - x1, y2 - y1
        # x1,y1只是途径点而非起始点，跳过本次循环
        if is_valid(x1-dx, y1-dy):
            continue
        # 行越界，跳出整个循环
        if not (0 < x1 + dx * (max_count - 1) <= R):
            break
        # 列越界，跳出本次循环
        if not (0< y1 + dy * (max_count - 1) <= C):
            continue
        cnt = 2
        while is_valid(x2 + dx, y2 + dy):
            x2 += dx
            y2 += dy
            if not flag[x2][y2]:
                break
            cnt += 1
        else:
            max_count = max(max_count, cnt)
print(max_count if max_count > 2 else 0)
