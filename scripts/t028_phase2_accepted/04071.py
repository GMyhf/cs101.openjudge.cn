# External reference: http://cs101.openjudge.cn/practice/04071/statistics/
# Accepted submission: 52833085
# Source: http://cs101.openjudge.cn/practice/solution/52833085/
# License: not declared on the submission page; no license is inferred.

import sys
from collections import Counter


def solve():
    # 读取所有输入行
    input_lines = sys.stdin.read().splitlines()
    if not input_lines:
        return

    try:
        n = int(input_lines[0].strip())
    except ValueError:
        return

    for i in range(1, n + 1):
        if i >= len(input_lines):
            break
        line = input_lines[i]
        if not line:
            continue

        # 从右侧切分，确保将末尾的数字 k 分离出来
        parts = line.rsplit(" ", 1)
        if len(parts) < 2:
            continue

        text, k_str = parts[0], parts[1]
        try:
            k = int(k_str)
        except ValueError:
            continue

        # 统计字符出现次数
        counter = Counter(text)

        # 寻找出现次数恰好为 k 的字符
        result_chars = [char for char, count in counter.items() if count == k]

        # 按照 ASCII 码升序排序
        result_chars.sort()

        # 格式化并输出，例如 'a','d','i'
        output_str = ",".join(f"'{char}'" for char in result_chars)
        print(output_str)


if __name__ == "__main__":
    solve()
