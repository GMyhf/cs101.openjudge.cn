# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# Heading: 1760: Disk Tree
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/01760/
# License: not declared in source collection; no license is inferred.
import sys
from collections import defaultdict
import sys

class TrieNode:
    """Trie 结点类"""
    def __init__(self):
        self.children = defaultdict(TrieNode)  # 存储子目录
        self.is_end = False  # 该标志在本题中可省略

class Trie:
    """Trie 前缀树"""
    def __init__(self):
        self.root = TrieNode()

    def insert(self, path: str):
        """插入目录路径"""
        node = self.root
        for folder in path.split("\\"):  # 以 "\" 分割路径
            node = node.children[folder]  # 如果不存在则自动创建

    def print_tree(self, node=None, depth=0):
        """递归打印目录树"""
        if node is None:
            node = self.root
        for folder in sorted(node.children):  # 按字典序排序
            print(" " * depth + folder)  # 根据深度打印
            self.print_tree(node.children[folder], depth + 1)  # 递归打印子目录

def main():
    # 读取输入
    n = int(sys.stdin.readline().strip())
    trie = Trie()

    for _ in range(n):
        path = sys.stdin.readline().strip()
        trie.insert(path)

    # 输出目录树
    trie.print_tree()

if __name__ == "__main__":
    main()
