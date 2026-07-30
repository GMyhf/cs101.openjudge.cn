# External reference: http://cs101.openjudge.cn/practice/30901/statistics/
# Accepted submission: 52723259
# Source: http://cs101.openjudge.cn/practice/solution/52723259/
# License: not declared on the submission page; no license is inferred.

import sys

def solve():
    # 一次性读取所有标准输入，极大提升 I/O 速度
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    t = int(input_data[0])
    idx = 1
    out = []

    for _ in range(t):
        n = int(input_data[idx])
        idx += 1

        # 获取当前样例的数组 A
        A = [int(x) for x in input_data[idx:idx+n]]
        idx += n

        mask = 0
        max_xor = 0

        # 数字最大为 10^9，二进制最多 30 位，因此从 29 位向下遍历至 0 位
        for i in range(29, -1, -1):
            mask |= (1 << i)

            # 提取所有数字到当前位为止的前缀，放入集合中
            # 使用集合推导式在 Python 中运行速度极快
            prefixes = {num & mask for num in A}

            # 我们期望将当前位（第 i 位）变成 1
            target = max_xor | (1 << i)

            # 验证是否存在两个前缀 p1 和 p2，使得 p1 ^ p2 = target
            # 等价于对于集合中的某个 p，验证 (p ^ target) 是否也在集合中
            for p in prefixes:
                if (p ^ target) in prefixes:
                    max_xor = target
                    break

        out.append(str(max_xor))

    # 一次性输出所有样例的结果
    print('\n'.join(out))

if __name__ == '__main__':
    solve()
