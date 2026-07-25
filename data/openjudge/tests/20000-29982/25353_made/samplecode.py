# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
import sys
input = sys.stdin.readline

N, D = map(int, input().split())
height = [int(input()) for _ in range(N)]

checked = [False] * N
remaining = N
result = []

while remaining > 0:	# 只要还有未处理的位置，就继续做一轮"收集组"
    buffer = []
    i = 0
    # 每轮从左到右尝试把可归入当前 buffer 的未处理元素标记并收集
    for i in range(N):
        if checked[i]:
            continue
        val = height[i]
        if not buffer:
            # buffer 为空时，直接加入第一个未处理元素
            buffer.append(val)
            maxh = val
            minh = val
            checked[i] = True
            remaining -= 1
            continue

        # ⚠️ “先用当前元素更新 max/min，再判断”
        maxh = max(maxh, val)
        minh = min(minh, val)

        # 若假设把 val 加入后仍满足与极值的差 ≤ D，则真正加入
        if maxh - val <= D and val - minh <= D:
            buffer.append(val)
            checked[i] = True
            remaining -= 1
        
    buffer.sort()
    result.extend(buffer)

print(*result, sep="\n")
