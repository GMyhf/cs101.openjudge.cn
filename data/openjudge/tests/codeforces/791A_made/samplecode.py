# Written for this repository from the public problem statement; no external submission used.
# 791A Bear and Big Brother —— 逐年模拟，直到 Limak **严格**重于 Bob。
a, b = map(int, input().split())
years = 0
while a <= b:
    a *= 3
    b *= 2
    years += 1
print(years)
