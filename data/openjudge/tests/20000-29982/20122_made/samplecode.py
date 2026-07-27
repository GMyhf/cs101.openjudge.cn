# External reference: statistics page /practice/20122/
# Accepted submission: 42258230
# Source: http://cs101.openjudge.cn/practice/solution/42258230/
# License: not declared on the submission page; no license is inferred.

# External reference: cs101.openjudge.cn practice/20122 statistics, Accepted solution 42258230.
# Source: http://cs101.openjudge.cn/practice/solution/42258230/
# Statistics: http://cs101.openjudge.cn/practice/20122/statistics/
# License: not declared on submission page; no license inferred
'''
2300015897
吴杰稀
光华管理学院
'''
cases,date = map(int,input().split())
company = []
for i in range(cases):
    dates = list(map(int,input().split()))
    dates.append(date)
    dates.sort(reverse = True)
    company.append(dates)
for _ in company:
    t = _.index(date)
    if t == 0:
        print("3")
    elif t == 1:
        print("2")
    elif t == 2:
        print("1")
    elif t == 3:
        print("-4")
    elif t == 4:
        print("-3")
