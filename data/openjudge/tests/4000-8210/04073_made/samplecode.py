# External reference: http://cs101.openjudge.cn/practice/04073/statistics/
# Accepted submission: 52833100
# Source: http://cs101.openjudge.cn/practice/solution/52833100/
# License: not declared on the submission page; no license is inferred.

import sys


def solve():
    # 读取标准输入中的所有 token
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)

    while True:
        try:
            n_str = next(iterator)
        except StopIteration:
            break

        n = int(n_str)
        if n == 0:
            break

        # 读取 N 个字符串
        strings = []
        for _ in range(n):
            strings.append(next(iterator))

        if not strings:
            print("")
            continue

        # 将所有字符串反转，寻找最长公共前缀
        rev_strs = [s[::-1] for s in strings]
        ref = rev_strs[0]
        common_len = 0

        # 对比字符
        for i in range(len(ref)):
            char = ref[i]
            match = True
            for s in rev_strs[1:]:
                # 如果索引超出当前字符串长度，或者字符不匹配
                if i >= len(s) or s[i] != char:
                    match = False
                    break
            if match:
                common_len += 1
            else:
                break

        # 截取公共前缀并反转还原为公共后缀
        common_prefix = ref[:common_len]
        common_suffix = common_prefix[::-1]
        print(common_suffix)


if __name__ == "__main__":
    solve()
