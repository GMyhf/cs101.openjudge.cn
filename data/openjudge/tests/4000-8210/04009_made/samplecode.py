# T-004-r4
# 2026-10-08 本地重写：原写法在满规模数据上超时，已换成更快的算法（见 CHANGELOG）。
# 原写法对每个 n 逐个枚举 2^n 种首行、每种 O(n) 次运算，n=24 在纯 Python 里要几分钟；
# 现把首行前 18 个符号按位切片成大整数并行计算（逐条对角线异或 + 位切片计数器），一次跑最大 n 顺带得出所有更小 n，共 O(n^2·log n) 次大整数运算。
import sys

LOW = 18  # 首行前 LOW 个符号按位切片并行处理，其余符号逐一枚举


def plane(j, width):
    # 长 2**width 位的大整数：第 m 位 = 首行编号 m 的第 j 个符号（1 表示 "-"）
    if j < 3:
        byte = (0xAA, 0xCC, 0xF0)[j]
        return int.from_bytes(bytes([byte]) * (1 << width >> 3), 'little')
    half = 1 << j >> 3
    return int.from_bytes((b'\x00' * half + b'\xff' * half) * (1 << width >> (j + 1)), 'little')


def count_all(N):
    # 返回 ans[m]（m=1..N）：首行长 m 时 "+"、"-" 个数相同的符号三角形个数
    low = min(N, LOW)
    width = max(low, 3)
    full = (1 << (1 << width)) - 1
    planes = [plane(j, width) for j in range(low)]
    hits = [0] * (N + 1)
    for high in range(1 << (N - low)):
        row0 = planes + [full if high >> (j - low) & 1 else 0 for j in range(low, N)]
        cnt = []  # 每个首行已出现的 "-" 个数，按二进制位切片存放
        diag = []  # 上一条对角线 a[i][d-i]
        for d in range(N):
            # 第 d 条对角线：a[0][d] 是首行第 d 个符号，a[i][d-i] = a[i-1][d-i] ^ a[i-1][d-i+1]
            new = [row0[d]]
            for i in range(1, d + 1):
                new.append(diag[i - 1] ^ new[i - 1])
            diag = new
            for x in new:  # 把这一位加到计数器上（逐位进位）
                for k in range(len(cnt)):
                    if not x:
                        break
                    cnt[k], x = cnt[k] ^ x, cnt[k] & x
                if x:
                    cnt.append(x)
            m = d + 1  # 此时计数器正好是首行前 m 个符号构成的三角形里 "-" 的个数
            total = m * (m + 1)
            if total % 4 or high >> max(m - low, 0):
                continue  # 总数为奇数必为 0；首行第 m 位之后不全为 "+" 的已在别处数过
            half = total // 4
            eq = full
            for k in range(len(cnt)):
                eq &= cnt[k] if half >> k & 1 else full ^ cnt[k]
            if half >> len(cnt):
                eq = 0
            if m < low:
                eq &= (1 << (1 << m)) - 1  # 只数前 m 位不同的首行，避免重复
            hits[m] += bin(eq).count('1')
    return hits


def main():
    ns = []
    for x in sys.stdin.read().split():
        n = int(x)
        if n == 0:
            break
        ns.append(n)
    if not ns:
        return
    ans = count_all(max(ns))
    sys.stdout.write(''.join(f'{n} {ans[n]}\n' for n in ns))


main()
