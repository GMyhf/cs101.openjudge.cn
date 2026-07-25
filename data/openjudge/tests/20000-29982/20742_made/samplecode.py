# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
def tribonacci(n):
    if n == 0:
        return 0
    elif n <= 2:
        return 1
    trib = [0, 1, 1] + [0] * (n - 2)
    for i in range(3, n + 1):
        trib[i] = trib[i - 1] + trib[i - 2] + trib[i - 3]
    return trib[n]

# 读取输入并处理
n = int(input())
print(tribonacci(n))
