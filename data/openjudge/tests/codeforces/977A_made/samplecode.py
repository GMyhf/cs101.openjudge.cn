# Written for this repository from the public problem statement; no external submission used.
# 977A Wrong Subtraction —— 按 Tanya 的规则模拟 k 次：末位非 0 减一，末位是 0 去掉末位。
n, k = map(int, input().split())
for _ in range(k):
    if n % 10:
        n -= 1
    else:
        n //= 10
print(n)
