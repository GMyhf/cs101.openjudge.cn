# External reference: statistics page /practice/27314/
# Accepted submission: 52736038
# Source: http://cs101.openjudge.cn/practice/solution/52736038/
# License: not declared on the submission page; no license is inferred.

import re

# 读取输入
text = input().strip()
old_word, new_word = input().strip().split()

# 统一小写用于匹配
target_old = old_word.lower()
target_new = new_word.lower()

# 第一步：遍历每个字符，标记哪些字母是需要被替换的单词
result = []
n = len(text)
i = 0
capitalize_next = True  # 句子开头需要大写

while i < n:
    # 如果不是字母，直接添加
    if not text[i].isalpha():
        result.append(text[i])
        # 遇到句号，下一个字母要大写
        if text[i] == '.':
            capitalize_next = True
        i += 1
        continue

    # 提取连续字母（单词）
    word_start = i
    while i < n and text[i].isalpha():
        i += 1
    original_word = text[word_start:i]
    lower_word = original_word.lower()

    # 判断是否需要替换
    if lower_word == target_old:
        use_word = target_new
    else:
        use_word = lower_word

    # 处理大小写：仅句子首字母大写，其余小写
    if capitalize_next and use_word:
        use_word = use_word[0].upper() + use_word[1:]
        capitalize_next = False

    result.append(use_word)

# 拼接结果
print(''.join(result))