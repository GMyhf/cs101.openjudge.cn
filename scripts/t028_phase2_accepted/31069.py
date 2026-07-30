# External reference: http://cs101.openjudge.cn/practice/31069/statistics/
# Accepted submission: 52792296
# Source: http://cs101.openjudge.cn/practice/solution/52792296/
# License: not declared on the submission page; no license is inferred.

import sys
from bisect import bisect_right

def solve():
    # 使用 sys.stdin.read 读取所有输入，以应对大量数据，提高IO效率
    input_data = sys.stdin.read().split()

    if not input_data:
        return

    iterator = iter(input_data)

    try:
        # 读取基本参数
        n1 = int(next(iterator))
        n2 = int(next(iterator))
        m = int(next(iterator))
        q = int(next(iterator))

        # 读取字符串 S1 和 S2
        s1 = next(iterator)
        s2 = next(iterator)

        # 预处理禁用组合
        # 使用 26x26 的布尔矩阵记录禁用组合，查询复杂度 O(1)
        forbidden = [[False] * 26 for _ in range(26)]
        base = ord('a')

        for _ in range(m):
            u = next(iterator)
            v = next(iterator)
            forbidden[ord(u) - base][ord(v) - base] = True

        # 读取所有查询
        qs = []
        for _ in range(q):
            qs.append(int(next(iterator)))

    except StopIteration:
        return

    # 步骤 1: 预处理 S2 的合法部分
    # 对于 'a'-'z' 每个字符作为前缀时，预先筛选出 S2 中所有合法的后缀字符
    # valid_s2_parts[i] 是一个字符列表
    valid_s2_parts = []
    for i in range(26):
        valid_list = []
        for char_s2 in s2:
            j = ord(char_s2) - base
            # 如果 (i + j) 组合没有被禁用，则加入列表
            if not forbidden[i][j]:
                valid_list.append(char_s2)
        valid_s2_parts.append(valid_list)

    # 计算每个字符类型贡献的长度（因为每个合法对产出2个字符，所以长度 * 2）
    char_block_lengths = [len(lst) * 2 for lst in valid_s2_parts]

    # 步骤 2: 构建 S1 的前缀长度数组
    # prefix[i] 表示 S1 的前 i 个字符一共生成了多长的 T
    # 数组大小为 n1 + 1，方便处理边界
    prefix = [0] * (n1 + 1)
    current_total = 0

    # 为了加速循环中的查找，预先将 s1 转换为 0-25 的索引列表
    s1_indices = [ord(c) - base for c in s1]

    for i in range(n1):
        idx = s1_indices[i]
        block_len = char_block_lengths[idx]
        current_total += block_len
        prefix[i+1] = current_total

    # 步骤 3: 回答查询
    results = []

    for k in qs:
        # 二分查找 k 所在的位置
        # 我们寻找 i 使得 prefix[i] <= k < prefix[i+1]
        # bisect_right 返回的是第一个大于 k 的位置，所以我们需要减 1
        idx_s1 = bisect_right(prefix, k) - 1

        # 计算在当前 S1[idx_s1] 生成的块内的偏移量
        rem = k - prefix[idx_s1]

        # 获取 S1 对应的字符索引（0-25）
        code = s1_indices[idx_s1]

        # 判断是取 S1 的字符还是 S2 的字符
        if rem % 2 == 0:
            # 偶数偏移量：对应组合的前半部分，即 S1[idx_s1]
            results.append(s1[idx_s1])
        else:
            # 奇数偏移量：对应组合的后半部分，即 S2 中的字符
            # rem // 2 得到它是该块中第几个合法的对
            rank = rem // 2
            # 从预处理的表中获取字符
            results.append(valid_s2_parts[code][rank])

    # 输出结果
    sys.stdout.write('\n'.join(results) + '\n')

if __name__ == '__main__':
    solve()
