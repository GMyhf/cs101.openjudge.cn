# External reference: statistics page /practice/06374/
# Accepted submission: 52887441
# Source: http://cs101.openjudge.cn/practice/solution/52887441/
# License: not declared on the submission page; no license is inferred.

n = int(input())
p = input()

line_char_num = 0
word_list = p.split(" ")
output = [[]]
for word in word_list:
    if len(word) + line_char_num > 80:
        output.append([])
        output[-1].append(word)
        line_char_num = len(word)+1
    else:
        output[-1].append(word)
        line_char_num += len(word)+1

for line in output:
    print(" ".join(line))

