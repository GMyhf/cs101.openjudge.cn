# External reference: http://cs101.openjudge.cn/practice/04030/statistics/
# Accepted submission: 50783029
# Source: http://cs101.openjudge.cn/practice/solution/50783029/
# License: not declared on the submission page; no license is inferred.

word = input().lower().strip()
article = input().lower()
first = (' '+article+' ').find(' '+word+' ')
if first == -1:
    print(-1)
else:
    print(article.split().count(word), first)
