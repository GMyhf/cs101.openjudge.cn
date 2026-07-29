# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1002: 方便记忆的电话号码
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/01002/
# License: not declared; no license is inferred.
import sys
# 定义字母到数字的映射关系
letter_to_digit = {
    'A': '2', 'B': '2', 'C': '2',
    'D': '3', 'E': '3', 'F': '3',
    'G': '4', 'H': '4', 'I': '4',
    'J': '5', 'K': '5', 'L': '5',
    'M': '6', 'N': '6', 'O': '6',
    'P': '7', 'R': '7', 'S': '7',
    'T': '8', 'U': '8', 'V': '8',
    'W': '9', 'X': '9', 'Y': '9'
}

# 将方便记忆的电话号码转换为标准格式
def convert_to_standard(phone):
    digits = []
    for char in phone:
        if char.isdigit():  # 如果是数字，直接加入
            digits.append(char)
        elif char.isalpha():  # 如果是字母，根据映射转换为数字
            digits.append(letter_to_digit[char.upper()])
    # 标准格式化为 xxx-xxxx
    return f"{digits[0]}{digits[1]}{digits[2]}-{digits[3]}{digits[4]}{digits[5]}{digits[6]}"

n = int(input())  # 输入电话号码的数量
phone_count = {}  # 记录每个标准电话号码出现的次数

for _ in range(n):
    phone = input().strip()  # 读取一个方便记忆的电话号码
    standard_phone = convert_to_standard(phone)  # 转换为标准格式
    phone_count[standard_phone] = phone_count.get(standard_phone, 0) + 1  # 统计次数

# 找出重复的标准电话号码
duplicates = {phone: count for phone, count in phone_count.items() if count >= 2}

if duplicates:
    # 按照标准电话号码升序排序并输出
    for phone in sorted(duplicates.keys()):
        print(f"{phone} {duplicates[phone]}")
else:
    print("No duplicates.")
