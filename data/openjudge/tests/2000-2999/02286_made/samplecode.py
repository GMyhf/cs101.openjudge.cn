# External reference: http://cs101.openjudge.cn/practice/02286/statistics/
# Accepted submission: 44694931
# Source: http://cs101.openjudge.cn/practice/solution/44694931/
# License: not declared on the submission page; no license is inferred.
# 2026-10-08 本地修正：上面引用的原始代码在题面范围内有缺陷，已按题面改过，与原提交不再逐字一致（见 CHANGELOG）。
# 原写法在 IDA* 中逐格移动/回退列表、每层算三遍 h，且不剪"刚做完 A 又做 F"这类互逆走法，深解时搜索树过大。
# 新写法：仍为 IDA*（O(7^d) 量级），每步用预计算的置换生成新元组，h=8-中心最多同色数，并跳过与上一步互逆的走法。
import sys

line = {'A': [0, 2, 6, 11, 15, 20, 22],
        'B': [1, 3, 8, 12, 17, 21, 23],
        'C': [10, 9, 8, 7, 6, 5, 4],
        'D': [19, 18, 17, 16, 15, 14, 13],
        'E': [23, 21, 17, 12, 8, 3, 1],
        'F': [22, 20, 15, 11, 6, 2, 0],
        'G': [13, 14, 15, 16, 17, 18, 19],
        'H': [4, 5, 6, 7, 8, 9, 10]
        }
center = [6, 7, 8, 11, 12, 15, 16, 17]
LETTERS = 'ABCDEFGH'
reverse = {'A': 'F', 'B': 'E', 'C': 'H', 'D': 'G',
           'E': 'B', 'F': 'A', 'G': 'D', 'H': 'C'}

# perm[r][k]：做完走法 r 后第 k 格的块来自原来的哪一格
perm = {}
for r in LETTERS:
    p = list(range(24))
    for j in range(7):
        p[line[r][j - 1]] = line[r][j]
    perm[r] = p


def h(mp):
    c = [mp[i] for i in center]
    return 8 - max(c.count(1), c.count(2), c.count(3))


def dfs(mp, dep, max_d, last, ans):
    hv = h(mp)
    if hv == 0:
        return True
    if dep + hv > max_d:
        return False
    for letter in LETTERS:
        if letter == reverse.get(last):
            continue
        p = perm[letter]
        ans.append(letter)
        if dfs([mp[i] for i in p], dep + 1, max_d, letter, ans):
            return True
        ans.pop()
    return False


def main():
    out = []
    for row in sys.stdin.read().split('\n'):
        mp = list(map(int, row.split()))
        if not mp:
            continue
        if mp == [0]:
            break
        if h(mp) == 0:
            out.append('No moves needed')
            out.append(str(mp[6]))
            continue
        limit = 1
        while True:
            ans = []
            if dfs(mp, 0, limit, '', ans):
                break
            limit += 1
        out.append(''.join(ans))
        cur = mp
        for letter in ans:
            cur = [cur[i] for i in perm[letter]]
        out.append(str(cur[6]))
    print('\n'.join(out))


main()
