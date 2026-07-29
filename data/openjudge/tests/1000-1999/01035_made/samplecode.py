# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1035: 拼写检查
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/01035/
# License: not declared in source collection; no license is inferred.
import sys
def is_correct(word, dictionary):
    # 检查单词是否在字典中
    return word in dictionary

def similar(word, dict_word):
    # 检查word与dict_word是否相似，依据三种规则
    len_word = len(word)
    len_dict_word = len(dict_word)

    # 1. 删除一个字母
    if len_word - 1 == len_dict_word:
        for i in range(len_word):
            if word[:i] + word[i+1:] == dict_word:
                return True

    # 2. 替换一个字母
    if len_word == len_dict_word:
        diff_count = 0
        for i in range(len_word):
            if word[i] != dict_word[i]:
                diff_count += 1
            if diff_count > 1:
                return False
        if diff_count == 1:
            return True

    # 3. 插入一个字母
    if len_word + 1 == len_dict_word:
        for i in range(len_dict_word):
            if word == dict_word[:i] + dict_word[i+1:]:
                return True

    return False

def check_words(dictionary, queries):
    results = []

    for word in queries:
        if is_correct(word, dictionary):
            results.append(f"{word} is correct")
        else:
            similar_words = []
            for dict_word in dictionary:
                if similar(word, dict_word):
                    similar_words.append(dict_word)
            if similar_words:
                results.append(f"{word}: " + " ".join(similar_words))
            else:
                results.append(f"{word}:")

    return results

def main():
    # 读入词典部分
    dictionary = []
    while True:
        word = input().strip()
        if word == '#':
            break
        dictionary.append(word)

    # 读入查询部分
    queries = []
    while True:
        word = input().strip()
        if word == '#':
            break
        queries.append(word)

    # 检查单词
    results = check_words(dictionary, queries)

    # 输出结果
    for result in results:
        print(result)

if __name__ == "__main__":
    main()
