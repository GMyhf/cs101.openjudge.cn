# External reference: statistics page /practice/29334/
# Accepted submission: 52829500
# Source: http://cs101.openjudge.cn/practice/solution/52829500/
# License: not declared on the submission page; no license is inferred.

import sys

def titleToNumber(columnTitle: str) -> int:
    ans = 0
    for char in columnTitle:
        # 计算字符对应的数值 (A -> 1, B -> 2, ..., Z -> 26)
        value = ord(char) - ord('A') + 1
        ans = ans * 26 + value
    return ans

if __name__ == "__main__":
    # 读取标准输入
    input_data = sys.stdin.read().split()
    if input_data:
        columnTitle = input_data[0]
        print(titleToNumber(columnTitle))