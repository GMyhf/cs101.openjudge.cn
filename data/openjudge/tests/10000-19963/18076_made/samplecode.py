# External reference: statistics page /practice/18076/
# Accepted submission: 17302978
# Source: http://cs101.openjudge.cn/practice/solution/17302978/
# License: not declared on the submission page; no license is inferred.
# 2026-10-08 本地重写：上面引用的原始代码在题面范围内有缺陷，下面已换成按题面重写的实现，不再是原提交（原因见下方注释与 CHANGELOG）。
# 18076 链状基团大小判定 参考解（本仓库自写）。
# 原先这里存的平台 AC 提交 17302978 把「原子序数」当成「原子序号」去找下一层原子，
# 只在第 2 层就分出大小的数据上碰巧正确，所以换成按题面规则的实现：
#   比较当前原子的原子序数 -> 比较其所连原子（不含来路，键级为 k 的算 k 个）
#   按从大到小排序、补 0 后的序列 -> 各取「最大的一个支链」（按同一套规则比出的最大子基团）继续。
# 实现上对每个原子自底向上算出它的比较键：
#   key(x) = (原子序数, 子原子序列补 0 到定长 W, 最大支链的 key 去掉首项)
# 两个基团的大小就是两根原子 key 的字典序。
import sys


def read_groups():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    vals = list(map(int, data[2:2 + 4 * (n + m)]))
    groups = []
    for start, size in ((0, n), (n, m)):
        z = [0] * size
        kids = [[] for _ in range(size)]
        for i in range(size):
            idx, par, atom, bond = vals[4 * (start + i): 4 * (start + i) + 4]
            z[idx] = atom
            if par >= 0:
                kids[par].append((idx, bond))
        groups.append((z, kids))
    return groups


def root_key(group, width):
    z, kids = group
    key = [None] * len(z)
    for x in range(len(z) - 1, -1, -1):
        seq = sorted((z[c] for c, b in kids[x] for _ in range(b)), reverse=True)
        seq += [0] * (width - len(seq))
        tail = max(key[c] for c, _ in kids[x])[1:] if kids[x] else ()
        key[x] = (z[x],) + tuple(seq) + tail
    return key[0]


def main():
    groups = read_groups()
    width = max(sum(b for _, b in ks) for _, kids in groups for ks in kids)
    ka, kb = (root_key(g, width) for g in groups)
    print(1 if ka > kb else 2)


main()
