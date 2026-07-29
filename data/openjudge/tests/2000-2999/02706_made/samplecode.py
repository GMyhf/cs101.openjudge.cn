# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2706: 麦森数
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/pctbook/02706/
# License: not declared in source collection; no license is inferred.
import sys
p=int(input())
print(int(0.30102999566398114*p)+1)
r=str(pow(2,p,10**500)-1)
r='0'*(500-len(r))+r
for i in range(10):
    print(r[50*i:50*(i+1)])
