# External reference: statistics page /practice/25580/
# Accepted submission: 51529611
# Source: http://cs101.openjudge.cn/practice/solution/51529611/
# License: not declared on the submission page; no license is inferred.

# 25580: 木板掉落（修正版）
# 目标：木板落地后才能挡住到达木板处的小球
# 需要挡住 k = floor(n/2)+1 个球（严格超过一半）

import sys
import math

data = sys.stdin.read().strip().split()
H = float(data[0])
L = float(data[1])
n = int(data[2])
vs = list(map(float, data[3:3+n]))

# 计算每个球到达木板位置的时间
times = []
for v in vs:
    times.append(0.0 if L == 0 else L / v)

times.sort()

k = n // 2 + 1                  # “大于一半的最小整数”
T = times[n - k]                # t_{n-k}，保证至少 k 个球到达时间 >= T

# 要求 t_land <= T
# t_land = sqrt((H - h)/5) <= T  =>  h >= H - 5*T^2
h = H - 5.0 * T * T
if h < 0:
    h = 0.0
if h > H:
    h = H

print(f"{h:.2f}")
