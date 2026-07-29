# External reference: http://cs101.openjudge.cn/practice/02800/statistics/
# Accepted submission: 50581325
# Source: http://cs101.openjudge.cn/practice/solution/50581325/
# License: not declared on the submission page; no license is inferred.

d = {'A':0, 'B':0, 'C':0, 'D':0, 'E':0, 'F':0, 'G':0, 'H':0, 'I':0, 'J':0, 'K':0, 'L':0, 'M':0, 'N':0, 'O':0, 'P':0, 'Q':0, 'R':0, 'S':0, 'T':0, 'U':0, 'V':0, 'W':0, 'X':0, 'Y':0, 'Z':0}
for _ in range(4):
    l = input()
    for i in l:
        if i in d:
            d[i] += 1
dv = d.values()
rows = max(dv)
for i in range(rows):
    L = ['*' if x >= rows-i else ' ' for x in dv]
    print(*L)
print('A B C D E F G H I J K L M N O P Q R S T U V W X Y Z')
