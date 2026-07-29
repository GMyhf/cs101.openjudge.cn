# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2910: 提取数字
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02910/
# License: not declared; no license is inferred.
import sys
def extract_integers(s):
    result = []
    num = ""

    for char in s:
        if char.isdigit():
            num += char
        else:
            if num:
                result.append(str(int(num)))
                num = ""

    if num:  # Add the last number if any
        result.append(str(int(num)))

    print("\n".join(result))

# Read input
s = input().strip()

# Extract and output integers
extract_integers(s)
