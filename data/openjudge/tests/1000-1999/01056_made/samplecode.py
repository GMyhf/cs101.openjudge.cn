# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1056: IMMEDIATE DECODABILITY
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/01056/
# License: not declared; no license is inferred.
import sys
m=0
while True:
    try:
        a=input()
    except EOFError:
        break
    m+=1
    list1=[]
    while a!='9':
        list1.append(a)
        a=input()
    dict1={}
    flag1=True
    flag2=True
    def dfs(dict1,a,i):
        global flag1,flag2
        if not flag1:
            return
        if '-1' in dict1:
            flag1=False
            return
        if i==len(a):
            dict1['-1']=-1
            return
        if a[i] not in dict1:
            dict1[a[i]]={}
            flag2=False
        dfs(dict1[a[i]],a,i+1)
    for a in list1:
        flag2=True
        dfs(dict1,a,0)
        if not flag1:
            break
    if flag1:
        print(f'Set {m} is immediately decodable')
    else:
        print(f'Set {m} is not immediately decodable')
