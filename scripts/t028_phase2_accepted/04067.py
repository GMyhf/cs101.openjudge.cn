# External reference: http://cs101.openjudge.cn/practice/04067/statistics/
# Accepted submission: 52833053
# Source: http://cs101.openjudge.cn/practice/solution/52833053/
# License: not declared on the submission page; no license is inferred.

import sys


def main():
    # 读取所有标准输入
    input_data = sys.stdin.read().splitlines()

    for line in input_data:
        # 去除行首尾的空白字符
        s = line.strip()
        if not s:
            continue

        # 判断字符串是否与反转后的字符串相同
        if s == s[::-1]:
            print("YES")
        else:
            print("NO")


if __name__ == "__main__":
    main()
