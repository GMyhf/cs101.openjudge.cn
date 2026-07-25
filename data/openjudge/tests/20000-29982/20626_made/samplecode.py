# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
def precompute_xor_prefixes(values):
    xor_prefixes = [0] * (len(values) + 1)
    for i in range(len(values)):
        xor_prefixes[i+1] = xor_prefixes[i] ^ values[i]
    return xor_prefixes

# 读取输入并处理
values = list(map(int, input().split()))
xor_prefixes = precompute_xor_prefixes(values)

# 读取查询并处理
for _ in range(10000):
    L, R = map(int, input().split())
    result = xor_prefixes[R+1] ^ xor_prefixes[L]
    print(result)
