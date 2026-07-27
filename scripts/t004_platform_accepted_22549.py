# External reference: statistics page /practice/22549/
# Accepted submission: 52824884
# Source: http://cs101.openjudge.cn/practice/solution/52824884/
# License: not declared on the submission page; no license is inferred.

import sys

def main():
    # 读取所有输入并去除两端的空白字符
    try:
        s = sys.stdin.read().strip()
    except Exception:
        print(-1)
        return

    # 如果输入为空，则不存在不重复的字符，输出 -1
    if not s:
        print(-1)
        return

    # 统计每个字符出现的次数
    char_count = {}
    for char in s:
        char_count[char] = char_count.get(char, 0) + 1

    # 寻找第一个出现次数为 1 的字符
    for index, char in enumerate(s):
        if char_count[char] == 1:
            print(index)
            return
            
    # 若无符合条件的字符，输出 -1
    print(-1)

if __name__ == '__main__':
    main()