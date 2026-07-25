# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
#20123:7-友好数，http://cs101.openjudge.cn/practice/20123/
#
# 陈威宇：>=7位就一定YES了，因为所有后缀%7有两个相等的（抽屉原理），
# 取这两个后缀里长的那个去掉短的那个即可？
'''
通过递归地尝试不同的子串来寻找符合条件的解.
`dfs(n, i)` 函数是进行深度优先搜索的核心部分。它接受两个参数：`n`代表当前搜索到的子串，
`i`代表当前处理到的位置索引。在函数内部，通过不断拼接字符来生成不同的子串，
然后检查是否满足能够被7整除的条件。

'''
def dfs(n, i):
    global bo
    if len(n) > 0 and int(n) % 7 == 0:
        bo = True
    if bo:
        return
    if i >= l:
        return
    dfs(n, i+1)
    dfs(n+s[i], i+1)


s = input()
l = len(s)
if l >= 7:
    print('YES')
    exit()
bo = False
dfs('', 0)
if bo:
    print('YES')
else:
    print('NO')

