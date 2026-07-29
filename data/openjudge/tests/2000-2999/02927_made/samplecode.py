# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2927: 判断数字个数
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02927/
# License: not declared; no license is inferred.
import sys
import sys
from collections import Counter

def count_digits_in_string(line):
    # 统计字符串中的数字出现次数
    digit_count = Counter(char for char in line if char.isdigit())

    # 按数字大小排序
    sorted_digit_count = sorted(digit_count.items(), key=lambda x: int(x[0]))

    # 输出结果
    for digit, count in sorted_digit_count:
        print(f"{digit}:{count}")

def main():
    # 读取所有输入行
    input_lines = sys.stdin.read().strip().split('\n')

    # 遍历每一行并处理
    for line in input_lines:
        count_digits_in_string(line)

if __name__ == "__main__":
    main()
