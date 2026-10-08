# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# https://www.geeksforgeeks.org/naive-algorithm-for-pattern-searching/
# Naive Pattern Searching algorithm
# 原写法失配时 i = i+j+1 整段跳过会漏解（如 "aab ab" 应输出 1），改为贪心查找、命中后跳过 len(pat)。
# 2026-10-08 本地修正：上面引用的原始代码在题面范围内有缺陷，已按题面改过，与原提交不再逐字一致（见 CHANGELOG）。
def search(pat, txt):
    res = []
    i = txt.find(pat)
    while i != -1:
        res.append(str(i))
        i = txt.find(pat, i + len(pat))
    return res


n = int(input())
for _ in range(n):
    txt, pat = input().split()
    ans = search(pat, txt)
    if ans:
        print(' '.join(ans))
    else:
        print('no')
