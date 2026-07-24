# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# 焦玮宸 24数学科学学院
dictionary = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19, 'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50, 'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90}
def convert(words):
    if words[0] == "negative":
        return -convert(words[1:])
    if "million" in words:
        ind = words.index("million")
        return convert(words[:ind]) * (10 ** 6) + (convert(words[ind + 1:]) if ind < len(words) - 1 else 0)
    if "thousand" in words:
        ind = words.index("thousand")
        return convert(words[:ind]) * (10 ** 3) + (convert(words[ind + 1:]) if ind < len(words) - 1 else 0)
    if "hundred" in words:
        ind = words.index("hundred")
        return convert(words[:ind]) * (10 ** 2) + (convert(words[ind + 1:]) if ind < len(words) - 1 else 0)
    return sum(list(map(lambda s: dictionary[s], words)))


print(convert(list(input().split())))
