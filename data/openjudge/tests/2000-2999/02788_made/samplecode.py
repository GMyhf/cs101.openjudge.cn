# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# Heading: 2788: 二叉树（2）
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md
# Upstream problem: http://cs101.openjudge.cn/2025sp_routine/02788/
# License: not declared in source collection; no license is inferred.
import sys
import sys

def count_subtree_nodes(m, n):
    count = 0
    left = m
    right = m
    # 每层的节点编号范围为 [left, right]
    while left <= n:
        count += min(n, right) - left + 1
        left *= 2
        right = right * 2 + 1
    return count

def main():
    input_stream = sys.stdin
    for line in input_stream:
        m, n = map(int, line.split())
        if m == 0 and n == 0:
            break
        print(count_subtree_nodes(m, n))

if __name__ == '__main__':
    main()
