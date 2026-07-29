# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# Heading: 2756: 二叉树（1）
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md
# Upstream problem: http://cs101.openjudge.cn/dsapre/02756/
# License: not declared in source collection; no license is inferred.
import sys
def find_common_ancestor(x, y):
    # 创建两个集合用于存储x和y的所有祖先节点
    ancestors_x = set()
    ancestors_y = set()

    # 回溯x到根节点的路径并保存
    while x > 0:
        ancestors_x.add(x)
        x //= 2

    # 回溯y到根节点的路径
    # 并在每一步检查当前节点是否也是x的祖先节点
    while y > 0:
        if y in ancestors_x:
            return y  # 找到了公共祖先
        y //= 2

    return 1  # 如果没有找到公共祖先，默认返回根节点1

# 读取输入
x, y = map(int, input().split())

# 查找并输出x和y的最近公共祖先
print(find_common_ancestor(x, y))
