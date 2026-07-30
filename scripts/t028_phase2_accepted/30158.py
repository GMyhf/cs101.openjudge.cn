# External reference: http://cs101.openjudge.cn/practice/30158/statistics/
# Accepted submission: 52723773
# Source: http://cs101.openjudge.cn/practice/solution/52723773/
# License: not declared on the submission page; no license is inferred.

def mat_mult(a, b, mod):
    """3x3矩阵乘法，取模"""
    res = [[0]*3 for _ in range(3)]
    for i in range(3):
        for k in range(3):
            if a[i][k] == 0:
                continue
            for j in range(3):
                # 关键：全程取模，处理负数
                res[i][j] = (res[i][j] + a[i][k] * b[k][j]) % mod
    return res

def mat_pow(mat, power, mod):
    """3x3矩阵快速幂"""
    # 单位矩阵
    res = [[1 if i == j else 0 for j in range(3)] for i in range(3)]
    while power > 0:
        if power & 1:
            res = mat_mult(res, mat, mod)
        mat = mat_mult(mat, mat, mod)
        power >>= 1
    return res

def mat_vec_mult(mat, vec, mod):
    """✅ 修复：矩阵 × 向量（正确顺序）"""
    a0 = (mat[0][0] * vec[0] + mat[0][1] * vec[1] + mat[0][2] * vec[2]) % mod
    a1 = (mat[1][0] * vec[0] + mat[1][1] * vec[1] + mat[1][2] * vec[2]) % mod
    a2 = (mat[2][0] * vec[0] + mat[2][1] * vec[1] + mat[2][2] * vec[2]) % mod
    return [a0, a1, a2]

# 读取输入
a1, a2 = map(int, input().split())
p, q, r = map(int, input().split())
n, m = map(int, input().split())

if n == 1:
    ans = a1 % m
elif n == 2:
    ans = a2 % m
else:
    # 转移矩阵（正确）
    trans = [
        [p, q, r],
        [1, 0, 0],
        [0, 0, 1]
    ]
    power = n - 2
    trans_pow = mat_pow(trans, power, m)
    # 初始向量 [a2, a1, 1]
    init_vec = [a2, a1, 1]
    # ✅ 矩阵乘向量（核心修复）
    final_vec = mat_vec_mult(trans_pow, init_vec, m)
    ans = final_vec[0]

# 强制保证结果在 [0, m) 区间
ans = (ans + m) % m
print(ans)
