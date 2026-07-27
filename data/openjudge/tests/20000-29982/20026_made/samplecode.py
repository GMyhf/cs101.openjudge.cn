# External reference: statistics page /practice/20026/
# Accepted submission: 52332704
# Source: http://cs101.openjudge.cn/practice/solution/52332704/
# License: not declared on the submission page; no license is inferred.

# External reference: cs101.openjudge.cn practice/20026 statistics, Accepted solution 52332704.
# Source: http://cs101.openjudge.cn/practice/solution/52332704/
# Statistics: http://cs101.openjudge.cn/practice/20026/statistics/
# License: not declared on submission page; no license inferred
n=int(input())
if n%2==1:
    print(1)
if n%4==2:
    print(2)
if n%4==0:
    print(n)
