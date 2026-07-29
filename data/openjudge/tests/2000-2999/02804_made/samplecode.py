# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2804: 词典
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02804/
# License: not declared; no license is inferred.
import sys
# 初始化一个空字典用于存储词典信息
dictionary = {}

# 读取词典部分
while True:
    line = input().strip()
    if not line:
        break
    # 按空格分割每行，分别得到英文单词和外语单词
    english, foreign = line.split()
    # 将外语单词作为键，英文单词作为值存入字典
    dictionary[foreign] = english

# 读取需要翻译的文档部分
while True:
    try:
        foreign_word = input().strip()
        if not foreign_word:
            break
        # 查找该外语单词是否在词典中
        if foreign_word in dictionary:
            print(dictionary[foreign_word])
        else:
            print("eh")
    except EOFError:
        break
